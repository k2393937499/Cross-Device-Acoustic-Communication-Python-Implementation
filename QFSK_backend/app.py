import re
import numpy as np
import sounddevice as sd
from flask_cors import CORS
from scipy.io import wavfile
from utils.record import record
from utils.modulation import QFSK
from scipy.signal import correlate
from utils.convencode import ConvEncode
from utils.speechtexttool import SpeechTextTool
from flask import Flask, request, jsonify, current_app

app = Flask(__name__)
CORS(app)

qfsk_module = QFSK()
conven = ConvEncode()
sttool = SpeechTextTool()

@app.route('/record', methods=['POST'])
def record_():
    data = request.get_json()
    response = record(data['time'])
    return response

@app.route('/modulation_option', methods=['POST'])
def modulation_option():
    data = request.get_json()
    current_app.config['option'] = data['option']
    response = {
        "status": "success",
        "status_code": 200,
        "data": current_app.config['option']
    }

    return jsonify(response)

@app.route('/send', methods=['POST'])
def send():
    sr, message = wavfile.read('wav/output.wav')
    if current_app.config['option'] == '8bit' or current_app.config['option'] == '16bit':
        if current_app.config['option'] == '8bit':
            message = (message / 256).astype(np.int8)
            bit = qfsk_module.wave2bit(message, bit_rate=8)
            qfsk_wave = qfsk_module.modulation(bit, sr, tb=0.05)
        else:
            bit = qfsk_module.wave2bit(message, bit_rate=16)
            qfsk_wave = qfsk_module.modulation(bit, sr, tb=0.05)
        
        qfsk_wave = qfsk_wave.reshape((-1, ))

        t = np.linspace(0, 1, sr)
        start_wave = np.sin(2 * np.pi * (250 * t**2))

        qfsk_wave = np.concatenate((start_wave, qfsk_wave))

        sd.play(qfsk_wave, sr)
        sd.wait()

    else:
        sr, message = wavfile.read('wav/output.wav')
        text = sttool.speech2text(message, sr)
        bit = qfsk_module.chinese2bit(text)
        bit = conven.convolutional_encode(bit)

        qfsk_wave = qfsk_module.modulation(bit, sr, tb=0.1)
        qfsk_wave = qfsk_wave.reshape((-1, ))

        t = np.linspace(0, 1, sr)
        start_wave = np.sin(2 * np.pi * (250 * t**2))

        qfsk_wave = np.concatenate((start_wave, qfsk_wave))

        sd.play(qfsk_wave, sr)
        sd.wait()

    response = {"status": "success", "status_code": 200, "data": text}
    return jsonify(response)

@app.route('/output', methods=['POST'])
def output():
    sr, transmit = wavfile.read('wav/output.wav')

    t = np.linspace(0, 1, sr)
    start_wave = np.sin(2 * np.pi * (250 * t**2))

    corr = correlate(transmit, start_wave)
    start = np.argmax(corr)

    if current_app.config['option'] == '8bit' or current_app.config['option'] == '16bit':
        length = int(0.05 * sr) - 1
        end = ((len(transmit)-start) // (8 * length)) * (8 * length)
        transmit = transmit[start:start + end]

        if current_app.config['option'] == '8bit':
            transmit = transmit.reshape((-1, 4, length))
            de_message = qfsk_module.demodulation(transmit, 0.05, sr)
            de_message = qfsk_module.bit2wave(de_message, bit_rate=8)
        else:
            transmit = transmit.reshape((-1, 8, length))
            de_message = qfsk_module.demodulation(transmit, 0.05, sr)
            de_message = conven.convolutional_decode(de_message)
            de_message = qfsk_module.bit2wave(de_message, bit_rate=16)

        sd.play(de_message, sr)
        sd.wait()

        response = {"status": "success", "status_code": 200, "data": "finished to output sound"}
        return jsonify(response)

    else:
        length = int(0.1 * sr) - 1
        end = ((len(transmit)-start) // (23 * length)) * (23 * length)
        transmit = transmit[start:start + end]

        transmit = transmit.reshape((-1, 23, length))
        de_message = qfsk_module.demodulation(transmit, 0.1, sr)
        de_message = conven.convolutional_decode(de_message)
        de_message_char = qfsk_module.bit2chinese(de_message)
        de_message_char = re.sub(r'㓇+$', '', de_message_char)

        de_message = sttool.text2speech(de_message_char)

        sd.play(de_message, 24000)
        sd.wait()

        response = {"status": "success", "status_code": 200, "data": de_message_char}
        return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
