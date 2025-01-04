import os
import wave
import numpy as np
import sounddevice as sd

from flask import jsonify

# parameters set
root = 'wav'
channels = 1  # sound channel
sample_rate = 5000
output_filename = "output.wav"
dtype = np.int16

path = os.path.join(root, output_filename)

def record(duration):
    print("start record...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype=dtype)
    sd.wait()
    print("record done.")

    # save
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(np.dtype(dtype).itemsize)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"录音保存为 {path}")

    return jsonify({"status": "success", "status_code": 200, "data":{"record_status": "done"}})

if __name__ == '__main__':
    record(1)