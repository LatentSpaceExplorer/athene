from src.gui.app import VoiceAssistantGUI
from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer
from src.audio.speech import SpeechGenerator
from src.models.chat import ChatModel
from src.plugins.todo_plugin import TodoPlugin
from src.plugins.clipboard_plugin import ClipboardPlugin

def main():
    
    # Initialize chat model with plugins
    chat_model = ChatModel([
        ClipboardPlugin,
        TodoPlugin, 
    ])
    
    # Initialize other components
    recorder = AudioRecorder()
    speech_generator = SpeechGenerator(
        "./models/kokoro/kokoro-v1.0.onnx",
        "./models/kokoro/voices-v1.0.bin"
    )
    audio_player = AudioPlayer()
    
    # run the app
    app = VoiceAssistantGUI(recorder, chat_model, speech_generator, audio_player)
    app.run()

if __name__ == "__main__":
    main()