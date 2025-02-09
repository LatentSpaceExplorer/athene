import sounddevice as sd
import soundfile as sf
import numpy as np
import speech_recognition as sr

class AudioRecorder:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.is_recording = False
        self.recorded_data = []
        self.recognizer = sr.Recognizer()
    
    def start(self):
        self.is_recording = True
        self.recorded_data = []
    
    def stop(self):
        self.is_recording = False
    
    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.recorded_data.append(indata.copy())
    
    def record(self):
        with sd.InputStream(channels=1, samplerate=self.sample_rate, 
                          callback=self.audio_callback):
            while self.is_recording:
                sd.sleep(100)
    
    def save_recording(self, filename="temp_recording.wav"):
        recording = np.concatenate(self.recorded_data, axis=0)
        sf.write(filename, recording, self.sample_rate)
        return filename
    
    def transcribe(self, audio_file):
        with sr.AudioFile(audio_file) as source:
            audio = self.recognizer.record(source)
            return self.recognizer.recognize_google(audio)