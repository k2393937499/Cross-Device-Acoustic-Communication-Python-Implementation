import torch
import ChatTTS
import warnings
import numpy as np
import soundfile as sf
import sounddevice as sd
from datasets import load_dataset
from scipy.io import wavfile
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline

warnings.filterwarnings('ignore')

class SpeechTextTool:
    def __init__(self):
        device = "cuda:0" if torch.cuda.is_available() else "cpu"
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        model_id = "openai/whisper-small"
        model = AutoModelForSpeechSeq2Seq.from_pretrained(
            model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True
        ).to(device)

        processor = AutoProcessor.from_pretrained(model_id)

        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            chunk_length_s=30,
            batch_size=1,
            torch_dtype=torch_dtype,
            device=device,
            generate_kwargs={"language": 'zh'},
        )

        self.ctts = ChatTTS.Chat()
        self.ctts.load()

        self.params = ChatTTS.Chat.InferCodeParams(
            prompt='[speed_1]'
        )

    def speech2text(self, message: np.ndarray, sr: int) -> str:
        message = message / max(message)
        message = {'array': message, 'sampling_rate': sr}
        result = self.pipe(message)
        return result['text']
    
    def text2speech(self, text: str) -> np.ndarray:
        text += '[uv_break]'
        wave = self.ctts.infer(text, params_infer_code=self.params)[0]
        return wave
    
if __name__ == '__main__':
    whisper = SpeechTextTool()
    sr, message = wavfile.read('wav/output1.wav')

    # sd.play(message, sr)
    # sd.wait()

    dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
    sample = dataset[0]["audio"]

    text = whisper.speech2text(message, sr)

    print(text)

    wave = whisper.text2speech(text)

    sd.play(wave, 24000)
    sd.wait()
