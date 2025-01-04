import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from utils.modulation import QFSK
from utils.convencode import ConvEncode

qfsk_modulation = QFSK()
conven = ConvEncode()

# load wav file and compress it to 8 bits
sr, message = wavfile.read('wav/hello.wav')
message = (message / 256).astype(np.int8)

# convert the wave to bit(list[str]), encode and modulate
bit = qfsk_modulation.wave2bit(message, bit_rate=8)
bit = conven.convolutional_encode(bit)
wave = qfsk_modulation.modulation(bit, tb=0.05, sr=sr)

# play the modulated wave (be cautious when selecting, it is too long to play)
# sd.play(wave, sr)
# sd.wait()

de_bit = qfsk_modulation.demodulation(wave, tb=0.05, sr=sr)
de_bit = conven.convolutional_decode(de_bit) # it will take more than 3min, be patience
de_message = qfsk_modulation.bit2wave(de_bit, bit_rate=8)

sd.play(de_message, sr)
sd.wait()