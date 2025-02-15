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
    
    def get_audio_data(self):
        recording = np.concatenate(self.recorded_data, axis=0)
        # Convert to int16 format which is what speech_recognition expects
        recording = (recording * 32767).astype(np.int16)
        return sr.AudioData(recording.tobytes(), self.sample_rate, 2)
    
    def transcribe(self, audio_data):
        return self.recognizer.recognize_google(audio_data)