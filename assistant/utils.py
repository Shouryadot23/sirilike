"""
utils.py - Utility / Helper Functions
Provides weather, Wikipedia, system info, and other helper functions.
"""

import json
import urllib.request
import urllib.parse

# ---------------------------------------------------------------------------
# Weather (using wttr.in free API)
# ---------------------------------------------------------------------------

def get_weather(city):
    """
    Fetch current weather for a city using wttr.in.

    Args:
        city (str): City name.

    Returns:
        str: Weather description string.
    """
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        current = data["current_condition"][0]
        desc = current["weatherDesc"][0]["value"]
        temp_c = current["temp_C"]
        feels = current["FeelsLikeC"]
        humidity = current["humidity"]
        return (
            f"In {city} it's currently {desc}, {temp_c}°C "
            f"(feels like {feels}°C) with {humidity}% humidity."
        )
    except Exception as e:
        return f"Sorry, I couldn't fetch the weather for {city}. ({e})"


# ---------------------------------------------------------------------------
# Wikipedia summary
# ---------------------------------------------------------------------------

def get_wikipedia_summary(query, sentences=2):
    """
    Fetch a short summary from Wikipedia.

    Args:
        query (str): The search term.
        sentences (int): Number of sentences to return.

    Returns:
        str: Summary text.
    """
    try:
        url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + urllib.parse.quote(query)
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        extract = data.get("extract", "")
        # Limit to requested number of sentences
        parts = extract.split(". ")
        summary = ". ".join(parts[:sentences])
        if not summary.endswith("."):
            summary += "."
        return summary
    except Exception as e:
        return f"Sorry, I couldn't find information about that. ({e})"


# ---------------------------------------------------------------------------
# System Info
# ---------------------------------------------------------------------------

def get_system_info(kind="all"):
    """
    Return system information (CPU, battery).

    Args:
        kind (str): 'cpu', 'battery', or 'all'.

    Returns:
        str: System info string.
    """
    try:
        import psutil
    except ImportError:
        return "psutil is not installed. Run: pip install psutil"

    parts = []
    if kind in ("cpu", "all"):
        cpu = psutil.cpu_percent(interval=1)
        parts.append(f"CPU usage is at {cpu}%.")
    if kind in ("battery", "all"):
        battery = psutil.sensors_battery()
        if battery:
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            parts.append(f"Battery is at {battery.percent}%, {plugged}.")
        else:
            parts.append("No battery detected.")
    return " ".join(parts) if parts else "Unknown system info request."


# ---------------------------------------------------------------------------
# Notes / Memory
# ---------------------------------------------------------------------------

_notes = []


def save_note(note):
    """Save a note to memory."""
    _notes.append(note)
    return f"Got it! I'll remember: {note}"


def recall_notes():
    """Recall all saved notes."""
    if not _notes:
        return "I don't have any notes saved yet."
    result = "Here's what I remember: " + "; ".join(_notes)
    return result


# ---------------------------------------------------------------------------
# Jokes
# ---------------------------------------------------------------------------

import random

_jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why was the JavaScript developer sad? Because he didn't Node how to Express himself.",
    "What's a computer's favorite snack? Microchips!",
    "Why do Java developers wear glasses? Because they can't C#.",
    "What did the router say to the doctor? It hurts when IP.",
    "Why did the developer go broke? Because he used up all his cache.",
    "There are only 10 types of people in the world: those who understand binary and those who don't.",
    "A SQL query walks into a bar, sees two tables, and asks: Can I join you?",
    "Why do Python programmers have low self-esteem? They're constantly comparing themselves to others.",
    "What's a pirate's favorite programming language? R!",
]


def get_joke():
    """Return a random joke."""
    return random.choice(_jokes)
