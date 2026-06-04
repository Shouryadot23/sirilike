#!/usr/bin/env python3
"""
🤖 Siri-like AI Voice Assistant
================================
A Python-based voice assistant that listens to your commands
and responds with spoken output.

Usage:
    python main.py           # Voice mode (default)
    python main.py --text    # Text mode (type commands instead)
"""

import sys
from assistant.speaker import speak
from assistant.listener import listen
from assistant.commands import handle_command

# Wake word to activate the assistant
WAKE_WORD = "hey assistant"


def main_voice():
    """Run the assistant in voice mode with wake word detection."""
    speak("Hello! I'm your AI assistant. Say 'Hey Assistant' to wake me up, or just start talking!")

    while True:
        text = listen(timeout=10, phrase_time_limit=15)
        if text is None:
            continue

        # Check for wake word — if used, strip it from the command
        if WAKE_WORD in text:
            text = text.replace(WAKE_WORD, "").strip()
            if not text:
                speak("Yes? How can I help?")
                # Listen again for the actual command
                text = listen(timeout=8, phrase_time_limit=15)
                if text is None:
                    continue

        # Process the command
        keep_running = handle_command(text)
        if not keep_running:
            break


def main_text():
    """Run the assistant in text mode (for testing without a microphone)."""
    speak("Hello! I'm your AI assistant. Type your commands below.")
    print("(Type 'exit' or 'quit' to stop)\n")

    while True:
        try:
            text = input("You: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            speak("Goodbye!")
            break

        if not text:
            continue

        keep_running = handle_command(text)
        if not keep_running:
            break


if __name__ == "__main__":
    if "--text" in sys.argv:
        main_text()
    else:
        main_voice()
