"""
commands.py - Command / Intent Handler
Parses user input and routes to the appropriate action.
"""

import webbrowser
import datetime
import urllib.parse

from assistant.speaker import speak
from assistant.utils import (
    get_weather,
    get_wikipedia_summary,
    get_system_info,
    save_note,
    recall_notes,
    get_joke,
)


def handle_command(text):
    """
    Match user input to an intent and execute the corresponding action.

    Args:
        text (str): The recognized speech text (lowercase).

    Returns:
        bool: False if the user wants to exit, True otherwise.
    """

    # --- Exit ---
    if any(word in text for word in ["goodbye", "exit", "quit", "stop", "bye", "shut down"]):
        speak("Goodbye! Have a great day!")
        return False

    # --- Greetings ---
    elif any(word in text for word in ["hello", "hi ", "hey", "greetings", "howdy"]):
        speak("Hey there! How can I help you?")

    # --- Time ---
    elif "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}.")

    # --- Date ---
    elif "date" in text or "day is it" in text:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}.")

    # --- Weather ---
    elif "weather" in text:
        # Try to extract city name after "in" or "for"
        city = None
        for prep in [" in ", " for ", " at "]:
            if prep in text:
                city = text.split(prep, 1)[1].strip()
                break
        if not city:
            speak("Which city would you like the weather for?")
        else:
            result = get_weather(city)
            speak(result)

    # --- Web Search ---
    elif text.startswith("search") or "search for" in text:
        query = text.replace("search for", "").replace("search", "").strip()
        if query:
            url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            speak(f"Searching Google for {query}.")
            webbrowser.open(url)
        else:
            speak("What would you like me to search for?")

    # --- Open Website ---
    elif "open" in text:
        sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://www.github.com",
            "reddit": "https://www.reddit.com",
            "twitter": "https://www.twitter.com",
            "facebook": "https://www.facebook.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "stackoverflow": "https://www.stackoverflow.com",
            "stack overflow": "https://www.stackoverflow.com",
            "wikipedia": "https://www.wikipedia.org",
            "netflix": "https://www.netflix.com",
            "spotify": "https://www.spotify.com",
        }
        opened = False
        for name, url in sites.items():
            if name in text:
                speak(f"Opening {name}.")
                webbrowser.open(url)
                opened = True
                break
        if not opened:
            # Try opening as a raw URL
            site_name = text.replace("open", "").strip()
            if site_name:
                url = f"https://www.{site_name}.com"
                speak(f"Trying to open {site_name}.")
                webbrowser.open(url)
            else:
                speak("Which website would you like me to open?")

    # --- Joke ---
    elif "joke" in text:
        joke = get_joke()
        speak(joke)

    # --- Wikipedia ---
    elif any(text.startswith(w) for w in ["who is", "what is", "tell me about", "who was", "what was", "define"]):
        for prefix in ["who is", "what is", "tell me about", "who was", "what was", "define"]:
            if text.startswith(prefix):
                query = text[len(prefix):].strip()
                break
        if query:
            result = get_wikipedia_summary(query)
            speak(result)
        else:
            speak("What would you like to know about?")

    # --- System Info ---
    elif "battery" in text:
        info = get_system_info("battery")
        speak(info)

    elif "cpu" in text or "processor" in text:
        info = get_system_info("cpu")
        speak(info)

    elif "system" in text and "info" in text:
        info = get_system_info("all")
        speak(info)

    # --- Notes / Remember ---
    elif "remember" in text and ("that" in text or "this" in text):
        # Extract note after "remember that" or "remember this"
        for keyword in ["remember that ", "remember this "]:
            if keyword in text:
                note = text.split(keyword, 1)[1].strip()
                result = save_note(note)
                speak(result)
                break

    elif "what do you remember" in text or "my notes" in text or "recall" in text:
        result = recall_notes()
        speak(result)

    # --- Fallback ---
    else:
        speak("I'm not sure how to help with that. Try asking me about the time, weather, or to search something!")

    return True
