import numpy as np
import sounddevice as sd
from scipy.io import wavfile
from utils.modulation import QFSK
from utils.convencode import ConvEncode
from utils.speechtexttool import SpeechTextTool

qfsk_modulation = QFSK()
conven = ConvEncode()
sttool = SpeechTextTool()

# load wav file and compress it to 8 bits
sr, message = wavfile.read('wav/hello.wav')
message = (message / 256).astype(np.int8)

# convert the wave to bit(list[str]), encode and modulate
char = sttool.speech2text(message, sr)
bit = qfsk_modulation.chinese2bit(char)
bit = conven.convolutional_encode(bit)
wave = qfsk_modulation.modulation(bit, tb=0.05, sr=sr)

de_bit = qfsk_modulation.demodulation(wave, tb=0.05, sr=sr)
de_bit = conven.convolutional_decode(de_bit)
de_message = qfsk_modulation.bit2chinese(de_bit)

wave = sttool.text2speech(de_message)

sd.play(wave, 24000)
sd.wait()