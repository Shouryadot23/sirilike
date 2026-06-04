"""
listener.py - Speech Recognition Module
Handles microphone input and converts speech to text.
"""

import speech_recognition as sr


def listen(timeout=5, phrase_time_limit=10):
    """
    Listen to the microphone and return recognized text.

    Args:
        timeout (int): Max seconds to wait for speech to start.
        phrase_time_limit (int): Max seconds for a single phrase.

    Returns:
        str or None: Recognized text in lowercase, or None if not understood.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("🔄 Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"🗣️  You said: {text}")
            return text.lower()
        except sr.WaitTimeoutError:
            return None
        except sr.UnknownValueError:
            print("❓ Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            print(f"⚠️  Speech recognition service error: {e}")
            return None
