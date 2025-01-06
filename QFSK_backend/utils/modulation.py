import numpy as np
from math import sqrt
import sounddevice as sd
import soundfile as sf
from scipy.io import wavfile
import matplotlib.pyplot as plt
from utils.convencode import ConvEncode
from scipy.fft import fft, fftfreq
from scipy.signal import correlate
from utils.speechtexttool import SpeechTextTool

class QPSK:
	def wave2bit(self, message) -> list[str]:
		bitstream = []
		for mess in message:
			bit = format(mess & 0xFFFF, '016b')
			bitstream.append(bit)
		return bitstream
	
	def bit2wave(self, bitstream) -> list[int]:
		wave = [int(bin_str, 2) for bin_str in bitstream]
		wave = np.array(wave).astype(np.int16)
		return wave

	def modulation(self, message: list[str], sr: int):
		self.tb = 0.01
		self.fc = 500

		t = np.linspace(0, self.tb, int(sr * self.tb)) # per signal duration

		c1 = np.cos(2 * np.pi * self.fc * t)  # carrier frequency cosine wave
		c2 = np.sin(2 * np.pi * self.fc * t)  # carrier frequency sine wave

		qpsk = np.zeros((len(message), 8, len(t)))

		for i, mess in enumerate(message):
			for j in range(0, 16, 2):
				if mess[j] == '1':
					m_s = 1
				else:
					m_s = -1

				odd_sig = c1 * m_s

				if mess[j + 1] == '1':
					m_s = 1
				else:
					m_s = -1

				even_sig = c2 * m_s

				qpsk[i, j // 2, :] = odd_sig + even_sig

		return qpsk
	
	def demodulation(self, qpsk_wave, tb, fc, sr):
		t = np.linspace(0, tb, int(sr * tb)) # per signal duration
		c1 = sqrt(2 / tb) * np.cos(2 * np.pi * fc * t)  # carrier frequency cosine wave
		c2 = sqrt(2 / tb) * np.sin(2 * np.pi * fc * t)  # carrier frequency sine wave
		
		demod = np.zeros((len(qpsk_wave), 16))

		for i, qpsk in enumerate(qpsk_wave):
			for j, per_wave in enumerate(qpsk):
				x1 = sum(c1 * per_wave)
				x2 = sum(c2 * per_wave)

				if x1>0 and x2>0:
					demod[i][2 * j] = '1'
					demod[i][2 * j + 1] = '1'
				elif x1>0 and x2<0:
					demod[i][2 * j] = '1'
					demod[i][2 * j + 1] = '0'
				elif x1<0 and x2<0:
					demod[i][2 * j] = '0'
					demod[i][2 * j + 1] = '0'
				elif x1<0 and x2>0:
					demod[i][2 * j] = '0'
					demod[i][2 * j + 1] = '1'
		
		result = [''.join(map(str, row.astype(int))) for row in demod]
		return result
		
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
						freq = 500
					else:
						freq = 1000
				else:
					if mess[j + 1] == '1':
						freq = 1500
					else:
						freq = 2000

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

				distances = [abs(peak - 500), abs(peak - 1000), abs(peak - 1500), abs(peak - 2000)]
				min_index = distances.index(min(distances))
				freqs = [500, 1000, 1500, 2000][min_index]

				if freqs == 500:
					demod[i][2 * j] = '1'
					demod[i][2 * j + 1] = '1'
				elif freqs == 1000:
					demod[i][2 * j] = '1'
					demod[i][2 * j + 1] = '0'
				elif freqs == 1500:
					demod[i][2 * j] = '0'
					demod[i][2 * j + 1] = '1'
				else:
					demod[i][2 * j] = '0'
					demod[i][2 * j + 1] = '0'
		
		result = [''.join(map(str, row.astype(int))) for row in demod]
		return result
	
	def chinese2bit(self, chinese_char: str):
		bit = []
		for char in chinese_char:
			utf16_bytes = char.encode('utf-16')
			utf16_bytes = utf16_bytes[2:]
			binary_list = [bin(byte)[2:].zfill(8) for byte in utf16_bytes]
			bit.append(''.join(binary_list))
		return bit
	
	def bit2chinese(self, bit):
		word = []
		for b in bit:
			bytes_list = [b[i:i+8] for i in range(0, len(b), 8)]
			byte_values = [int(byte, 2) for byte in bytes_list]
			try:
				char = bytes(byte_values).decode('utf-16')
				word.append(char)
			except Exception as e:
				print("missing 1 char")
		return ''.join(word)


if __name__ == '__main__':
	# QFSK local test
	'''
	# modulation
	sr, message = wavfile.read('wav/hello.wav')
	message = (message / 256).astype(np.int8)

	qfsk_module = QFSK()
	conven = ConvEncode()

	temp_bit = qfsk_module.wave2bit(message)
	temp_bit, original_length = conven.convolutional_encode(temp_bit)

	qfsk_wave = qfsk_module.modulation(temp_bit, sr=sr, tb=0.05, bit=8)
	qfsk_wave_o = qfsk_wave

	qfsk_wave = qfsk_wave.reshape((-1, ))
	qfsk_len = len(qfsk_wave)

	t = np.linspace(0, 1, sr)
	start_wave = np.sin(2 * np.pi * (250 * t**2))

	qfsk_wave = np.concatenate((start_wave, qfsk_wave))
	
	# de module on local device
	temp_de_message = qfsk_module.demodulation(qfsk_wave_o, 0.05, sr, bit=8)
	temp_de_message = conven.convolutional_decode(temp_de_message, original_length)
	temp_de_message = qfsk_module.bit2wave(temp_de_message)

	sd.play(temp_de_message, sr)
	sd.wait()
	'''

	# QFSK char test
	'''
	sttool = SpeechTextTool()
	qfsk_module = QFSK()
	conven = ConvEncode()

	sr, message = wavfile.read('wav/output.wav')
	text = sttool.speech2text(message, sr)
	bit = qfsk_module.chinese2bit(text)
	bit, original_length = conven.convolutional_encode(bit)

	qfsk_wave = qfsk_module.modulation(bit, sr, tb=0.1)
	qfsk_wave = qfsk_wave.reshape((-1, ))

	t = np.linspace(0, 1, sr)
	start_wave = np.sin(2 * np.pi * (250 * t**2))

	qfsk_wave = np.concatenate((start_wave, qfsk_wave))

	sd.play(qfsk_wave, sr)
	sd.wait()
	'''