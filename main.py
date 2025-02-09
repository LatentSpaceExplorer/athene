from src.gui.app import VoiceAssistantGUI
from src.audio.recorder import AudioRecorder
from src.audio.player import AudioPlayer
from src.audio.speech import SpeechGenerator
from src.models.chat import ChatModel
from src.models.todo_manager import TodoManager


def main():
    todo_manager = TodoManager()
    chat_model = ChatModel(todo_manager)
    recorder = AudioRecorder()
    speech_generator = SpeechGenerator(
        "./models/kokoro/kokoro-v1.0.onnx",
        "./models/kokoro/voices-v1.0.bin"
    )
    audio_player = AudioPlayer()
    
    app = VoiceAssistantGUI(recorder, chat_model, speech_generator, audio_player)

    app.run()

if __name__ == "__main__":
    main()