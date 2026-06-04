"""
speaker.py - Text-to-Speech Module
Handles converting text responses to spoken audio output.
"""

import pyttsx3

# Initialize the TTS engine globally
_engine = pyttsx3.init()

# Configure voice properties
_engine.setProperty('rate', 175)    # Speed of speech
_engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

# Try to set a female voice if available
_voices = _engine.getProperty('voices')
for _voice in _voices:
    if 'female' in _voice.name.lower() or 'zira' in _voice.name.lower():
        _engine.setProperty('voice', _voice.id)
        break


def speak(text):
    """
    Convert text to speech and play it.

    Args:
        text (str): The text to speak aloud.
    """
    print(f"🤖 Assistant: {text}")
    _engine.say(text)
    _engine.runAndWait()
