# Athene

Athene is a voice-controlled AI assistant that can manage your tasks, read to you your clipboard content, and engage in natural conversations using LLMs.

## Features

- Voice recognition and processing 
- Natural language task management with persistent storage
- Text-to-speech responses using [Kokoro](https://github.com/thewh1teagle/kokoro-onnx)
- Read text from clipboard
- General conversation
- Modular plugin system for easy extension

## Prerequisites

- Python 3.12 or higher
- NVIDIA GPU with CUDA support (recommended)
- Groq API key for LLM access


## Installation

1. Clone the repository

2. Install dependencies using uv (recommended) or pip:

```bash
uv sync
```

3. Set up environment variables:
   - Create a `.env` file
   - Add your Groq API key: `GROQ_API_KEY=your_key_here`

4. Download Kokoro models:
   - Create a `models/kokoro` directory
   - Add required model files:
     - `kokoro-v1.0.onnx`
     - `voices-v1.0.bin`

5. Run the application:

```bash
uv run src/main.py
```

## Supported Commands

- Task Management: Add, remove, and list tasks
- Clipboard: Read your clipboard text
- General Conversation: Natural dialogue on various topics

## Planned Features

- [ ] Add support alternative LLMs backends (e.g. OpenAI, local)
- [ ] Voice activation by name (e.g. "Athene")
- [ ] Recurring tasks
- [ ] Additional plugins:
  - [ ] Reminders
  - [ ] Day planning
  - [ ] Habit tracking
  - [ ] Internet search
  - [ ] File reading


## Technical Stack

- **Speech Recognition**: SpeechRecognition
- **NLP**: LangChain (currently only Groq is supported)
- **TTS**: Kokoro ONNX