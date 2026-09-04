# 🎙️ Edge TTS Studio

A powerful Text-to-Speech tool built with Microsoft Edge TTS engine. Convert any text to natural-sounding speech with 400+ voices across 100+ languages.

## ✨ Features

- 🗣️ **400+ Neural Voices** - Access Microsoft Edge's complete voice library
- 🌍 **100+ Languages** - English, Urdu, Hindi, Arabic, and many more
- ⚡ **Speed Control** - Adjust speech rate from -100% to +200%
- 🎵 **Pitch Control** - Fine-tune voice pitch
- 🔊 **Volume Control** - Adjust output volume
- 📝 **Long Text Support** - Automatic text chunking for YouTube scripts
- 📦 **MP3 & WAV Export** - Download in your preferred format
- 📜 **Audio History** - Access previously generated files
- 🌙 **Dark/Light Mode** - Easy on the eyes
- ⌨️ **Keyboard Shortcuts** - Ctrl+Enter to generate

## 🚀 Quick Start

### Windows
```bash
run.bat
```

### Manual Setup
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Run the server
python app.py
```

Then open **http://localhost:8000** in your browser.

## 📁 Project Structure

```
edge-tts-tool/
├── backend/
│   ├── app.py              # FastAPI server
│   ├── config.py           # Configuration
│   ├── services/           # Business logic
│   │   ├── tts_service.py  # Edge TTS integration
│   │   └── voice_service.py# Voice management
│   ├── api/                # API routes
│   │   ├── tts_routes.py   # TTS endpoints
│   │   └── voice_routes.py # Voice endpoints
│   ├── utils/              # Utilities
│   │   ├── text_chunker.py # Smart text splitting
│   │   └── audio_utils.py  # Audio processing
│   └── output/             # Generated audio files
├── frontend/
│   ├── index.html          # Main UI
│   ├── css/                # Styles
│   └── js/                 # Frontend logic
├── tests/                  # Unit tests
├── .env                    # Environment config
└── run.bat                 # Windows launcher
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/tts/generate` | Generate speech from text |
| POST | `/api/tts/stream` | Stream audio |
| GET | `/api/tts/download/{filename}` | Download audio file |
| GET | `/api/tts/history` | Get generated files list |
| DELETE | `/api/tts/history/{filename}` | Delete a file |
| GET | `/api/voices/` | Get available voices |
| GET | `/api/voices/languages` | Get available languages |
| GET | `/api/voices/{voice_name}` | Get voice details |
| POST | `/api/voices/refresh` | Refresh voice cache |
| GET | `/api/health` | Health check |

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, edge-tts
- **Frontend**: HTML5, CSS3, JavaScript
- **TTS Engine**: Microsoft Edge Neural TTS

## 📄 License

MIT License
