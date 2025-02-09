import sounddevice as sd

class AudioPlayer:
    @staticmethod
    def play(samples, sample_rate):
        sd.play(samples, sample_rate)
        sd.wait()