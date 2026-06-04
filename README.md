# 🤖 Siri-like AI Voice Assistant

A modular, Python-based voice assistant that listens to your voice commands and responds with spoken output — just like Siri, Alexa, or Google Assistant!

## ✨ Features

| Command | Example | What It Does |
|---|---|---|
| 🗣️ Greetings | "Hello" / "Hey" | Friendly greeting |
| 🕐 Time | "What time is it?" | Tells the current time |
| 📅 Date | "What's the date?" | Tells today's date |
| 🔍 Web Search | "Search for Python tutorials" | Opens a Google search |
| 🌐 Open Website | "Open YouTube" | Opens a website in your browser |
| 🌤️ Weather | "What's the weather in London?" | Fetches live weather data |
| 😂 Jokes | "Tell me a joke" | Tells a random joke |
| 📚 Wikipedia | "Who is Elon Musk?" | Fetches a Wikipedia summary |
| 🔋 Battery | "Battery status" | Shows battery percentage |
| 💻 CPU | "CPU usage" | Shows CPU usage percentage |
| 📝 Notes | "Remember that my meeting is at 3" | Saves and recalls notes |
| 👋 Exit | "Goodbye" / "Exit" | Shuts down gracefully |

## 📁 Project Structure

```
sirilike/
├── main.py              # Entry point & main loop
├── assistant/
│   ├── __init__.py      # Package init
│   ├── listener.py      # 🎤 Speech recognition
│   ├── speaker.py       # 🔊 Text-to-speech
│   ├── commands.py      # 🧠 Intent matching & command routing
│   └── utils.py         # 🛠️ Weather, Wikipedia, jokes, notes, system info
├── requirements.txt     # Python dependencies
└── README.md            # You're here!
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A working microphone (for voice mode)

### 1. Clone the repo
```bash
git clone https://github.com/Shouryadot23/sirilike.git
cd sirilike
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Note (Linux users):** You may need to install PortAudio for PyAudio:
> ```bash
> sudo apt-get install portaudio19-dev python3-pyaudio
> ```

> **Note (macOS users):**
> ```bash
> brew install portaudio
> ```

## 🎮 Usage

### Voice Mode (default)
```bash
python main.py
```
Speak into your microphone. Say **"Hey Assistant"** to wake it up, or just start talking!

### Text Mode (no microphone needed)
```bash
python main.py --text
```
Type your commands — great for testing or environments without a mic.

## 🔧 Adding Custom Commands

It's easy to extend! Edit `assistant/commands.py` and add a new `elif` block:

```python
# --- My Custom Command ---
elif "my command" in text:
    speak("This is my custom response!")
```

For commands that need helper functions, add them in `assistant/utils.py` and import them in `commands.py`.

## 🛠️ Tech Stack

- **SpeechRecognition** — Google Speech-to-Text
- **pyttsx3** — Offline text-to-speech
- **PyAudio** — Microphone input
- **psutil** — System information
- **wttr.in** — Free weather API
- **Wikipedia REST API** — Knowledge lookups

## 📜 License

MIT License — feel free to use, modify, and share!

---

*Built with ❤️ by [Shouryadot23](https://github.com/Shouryadot23)*
