import tkinter as tk
import threading
import asyncio


class VoiceAssistantGUI:
    def __init__(self, recorder, chat_model, speech_generator, audio_player):
        self.window = tk.Tk()
        self.window.title("Athene")
        self.window.geometry("300x200")
        
        # Components
        self.recorder = recorder
        self.chat_model = chat_model
        self.speech_generator = speech_generator
        self.audio_player = audio_player
        
        # Create event loop
        self.loop = asyncio.new_event_loop()
        
        self.setup_gui()
        self.setup_async_loop()
    
    def setup_gui(self):
        self.record_button = tk.Button(self.window, text="Hold to Record")
        self.record_button.pack(pady=20)
        
        self.status_label = tk.Label(self.window, text="Ready")
        self.status_label.pack(pady=10)
        
        self.record_button.bind('<ButtonPress-1>', self.start_recording)
        self.record_button.bind('<ButtonRelease-1>', self.stop_recording)
    
    def setup_async_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def start_recording(self, event):
        self.recorder.start()
        self.status_label.config(text="Recording...")
        
        self.record_thread = threading.Thread(target=self.recorder.record)
        self.record_thread.start()

    def stop_recording(self, event):
        self.recorder.stop()
        self.status_label.config(text="Processing...")
        
        # Run the async processing in the event loop
        asyncio.run_coroutine_threadsafe(self.process_recording(), self.loop)

    def update_status(self, text):
        self.status_label.config(text=text)

    async def process_recording(self):
        try:
            # Get audio data directly
            audio_data = self.recorder.get_audio_data()
            print("[Recording] Got audio data")
            
            try:
                # Convert speech to text
                text = self.recorder.transcribe(audio_data)
                print(f"[Speech Recognition] Detected text: {text}")
                self.window.after(0, self.update_status, "Converting to text...")
                
                # Get AI response
                print("[LangChain] Sending to LLM...")
                response_text = await self.chat_model.get_response(text)
                print(f"[LangChain] Received response: {response_text}")
                
                # Convert to speech
                print("[Kokoro] Generating speech...")
                samples, sample_rate = self.speech_generator.generate(response_text)
                print("[Kokoro] Speech generated, playing audio...")
                
                # Play the response
                self.audio_player.play(samples, sample_rate)
                print("[Audio] Finished playing")
                
                self.window.after(0, self.update_status, "Ready")
                
            except Exception as e:
                print(f"[Error] An error occurred: {str(e)}")
                self.window.after(0, self.update_status, f"Error: {str(e)}")
        except Exception as e:
            print(f"[Error] Process recording failed: {str(e)}")
            self.window.after(0, self.update_status, f"Error: {str(e)}")

        print("[App] Completed process")
        print()

    def run(self):
        # Start the async event loop in a separate thread
        threading.Thread(target=self._run_event_loop, daemon=True).start()
        self.window.mainloop()
    
    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()