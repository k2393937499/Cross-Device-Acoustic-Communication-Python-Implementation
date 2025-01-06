import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import correlate
from utils.speechtexttool import SpeechTextTool
		
class QFSK:
	def wave2bit(self, message, bit_rate=8) -> list[str]:
		bitstream = []
		for mess in message:
			if bit_rate==8:
				bit = format(mess & 0xFF, '08b')
			else:
				bit = format(mess & 0xFFFF, '016b')
			bitstream.append(bit)
		return bitstream
	
	def bit2wave(self, bitstream, bit_rate=8) -> list[int]:
		wave = [int(bin_str, 2) for bin_str in bitstream]
		if bit_rate == 8:
			wave = np.array(wave).astype(np.int8)	
		else:
			wave = np.array(wave).astype(np.int16)
		return wave

	def modulation(self, message: list[str], sr: int, tb: float):
		t = np.linspace(0, tb, int(sr * tb))

		bit_len = len(message[0])

		qpsk = np.zeros((len(message), bit_len // 2, len(t)-1))

		for i, mess in enumerate(message):
			for j in range(0, bit_len, 2):
				if mess[j] == '1':
					if mess[j + 1] == '1':
						freq = 8000
					else:
						freq = 8500
				else:
					if mess[j + 1] == '1':
						freq = 9000
					else:
						freq = 9500

				sig = np.sin(2 * np.pi * freq * t)

				qpsk[i, j // 2, :] = sig[:-1]

		return qpsk
	
	def demodulation(self, qfsk_wave, tb, sr):
		t = np.linspace(0, tb, int(sr * tb))

		bit_len = qfsk_wave.shape[1] * 2

		demod = np.zeros((len(qfsk_wave), bit_len))

		for i, qpsk in enumerate(qfsk_wave):
			for j, per_wave in enumerate(qpsk):
				fft_qfsk = np.abs(fft(per_wave))
				freqs = fftfreq(len(per_wave), 1/sr)
				pos_mask = freqs > 0
				peak = freqs[pos_mask][np.argmax(fft_qfsk[pos_mask])]

				distances = [abs(peak - 8000), abs(peak - 8500), abs(peak - 9000), abs(peak - 9500)]
				min_index = distances.index(min(distances))
				freqs = [8000, 8500, 9000, 9500][min_index]

				if freqs == 8000:
					demod[i][2 * j] = '0'
					demod[i][2 * j + 1] = '0'
				elif freqs == 8500:
					demod[i][2 * j] = '0'
					demod[i][2 * j + 1] = '1'
				elif freqs == 9000:
					demod[i][2 * j] = '1'
					demod[i][2 * j + 1] = '0'
				else:
					demod[i][2 * j] = '1'
					demod[i][2 * j + 1] = '1'
		
		result = [''.join(map(str, row.astype(int))) for row in demod]
		return result
	
	def chinese2bit(self, chinese_char: str):
		bit = []
		for char in chinese_char:
			utf8_bytes = char.encode('utf-8')
			binary_list = [bin(byte)[2:].zfill(8) for byte in utf8_bytes]
			bit.append(''.join(binary_list))
		return bit
	
	def bit2chinese(self, bit):
		word = []
		for b in bit:
			bytes_list = [b[i:i+8] for i in range(0, len(b), 8)]
			byte_values = [int(byte, 2) for byte in bytes_list]
			try:
				char = bytes(byte_values).decode('utf-8')
				word.append(char)
			except Exception as e:
				print("missing 1 char")
		return ''.join(word)


if __name__ == '__main__':
	qfsk_module = QFSK()
	sttool = SpeechTextTool()
	
	# load the binary file from sonar
	def read_arb_file(arb_filename, dtype, count):
		data = np.fromfile(arb_filename, dtype=dtype, count=count)
		return data

	arb_filename = 'unit_test/sonar_transmit.txt'
	dtype = np.float32  
	count = 150000  # the valid data is about to 70k

	transmit = read_arb_file(arb_filename, dtype, count)

	plt.plot(transmit)
	plt.show()

	sr = 96000

	# synchronization
	duration = 8192 / 96000
	t = np.linspace(0, duration, 8192)
	k = (14000 - 10000) / duration
	start_wave = np.cos(np.pi * k * t**2 + 2 * np.pi * 10000 * t)

	corr = correlate(transmit, start_wave)
	start = np.argmax(corr)

	print('start idx', start)

	length = int(0.01 * sr)
	end = ((len(transmit)-start) // (12 * length)) * (12 * length)
	transmit = transmit[start:start + end]

	transmit = transmit.reshape((-1, 12, int(0.01 * sr)))
	de_message = qfsk_module.demodulation(transmit, 0.01, sr)
	print(de_message)
	de_message = qfsk_module.bit2chinese(de_message)

	print('text', de_message)

	de_message = sttool.text2speech(de_message)

	sd.play(de_message, 24000)
	sd.wait()
