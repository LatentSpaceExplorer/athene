from kokoro_onnx import Kokoro

class SpeechGenerator:
    def __init__(self, model_path, voices_path):
        self.kokoro = Kokoro(model_path, voices_path)
    
    def generate(self, text, voice="af_heart", speed=1.0, lang="en-us"): # af_bella
        return self.kokoro.create(text, voice=voice, speed=speed, lang=lang)