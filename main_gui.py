#!/usr/bin/env python3
"""
🤖 Siri-like AI Voice Assistant — Beautiful GUI Edition
======================================================
A modern, animated voice assistant with a stunning dark UI.

Usage:
    python main_gui.py
"""

import tkinter as tk
from tkinter import font as tkfont
import threading
import math
import time
import datetime
import webbrowser
import urllib.parse
import random
import sys
import os

# ---------------------------------------------------------------------------
# Import assistant modules
# ---------------------------------------------------------------------------
from assistant.utils import (
    get_weather,
    get_wikipedia_summary,
    get_system_info,
    save_note,
    recall_notes,
    get_joke,
)

# Try importing speech/tts — graceful fallback if unavailable
try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


# ===========================================================================
# COLOR THEME
# ===========================================================================
class Theme:
    BG = "#0f0f1a"              # Deep dark background
    BG_SECONDARY = "#1a1a2e"    # Card background
    BG_INPUT = "#16213e"        # Input field background
    ACCENT = "#00d4ff"          # Cyan accent
    ACCENT_DARK = "#0a84ff"     # Blue accent
    ACCENT_GLOW = "#00d4ff"     # Glow color
    TEXT = "#e0e0e0"            # Primary text
    TEXT_DIM = "#7a7a8a"        # Dimmed text
    TEXT_USER = "#00d4ff"       # User message color
    TEXT_BOT = "#a78bfa"        # Bot message color (purple)
    SUCCESS = "#10b981"         # Green
    ERROR = "#ef4444"           # Red
    BORDER = "#2a2a4a"          # Border color
    BUTTON_BG = "#1e3a5f"       # Button background
    BUTTON_HOVER = "#264d73"    # Button hover
    PULSE_COLORS = ["#00d4ff", "#0a84ff", "#a78bfa", "#6366f1", "#00d4ff"]


# ===========================================================================
# ANIMATED ORB CANVAS (Siri-like pulsing orb)
# ===========================================================================
class AnimatedOrb(tk.Canvas):
    """A Siri-style animated pulsing orb."""

    def __init__(self, parent, size=200, **kwargs):
        super().__init__(parent, width=size, height=size,
                         bg=Theme.BG, highlightthickness=0, **kwargs)
        self.size = size
        self.center = size // 2
        self.phase = 0.0
        self.is_listening = False
        self.is_speaking = False
        self.is_idle = True
        self._animate()

    def set_state(self, state):
        """Set orb state: 'idle', 'listening', 'speaking', 'thinking'."""
        self.is_idle = (state == "idle")
        self.is_listening = (state == "listening")
        self.is_speaking = (state == "speaking")

    def _animate(self):
        self.delete("all")
        self.phase += 0.05
        cx, cy = self.center, self.center

        # Draw multiple concentric pulsing rings
        num_rings = 5
        for i in range(num_rings):
            offset = i * 0.4
            pulse = math.sin(self.phase + offset) * 0.5 + 0.5

            if self.is_listening:
                # Bright pulsing when listening
                base_r = 25 + i * 12
                r = base_r + pulse * 15
                alpha_hex = hex(int(180 - i * 30))[2:].zfill(2)
                colors = ["#00d4ff", "#00b4d8", "#0096c7", "#0077b6", "#005f99"]
            elif self.is_speaking:
                # Purple pulsing when speaking
                base_r = 25 + i * 12
                r = base_r + pulse * 10
                colors = ["#a78bfa", "#8b5cf6", "#7c3aed", "#6d28d9", "#5b21b6"]
            else:
                # Gentle breathing when idle
                base_r = 30 + i * 10
                r = base_r + pulse * 5
                colors = ["#4a4a6a", "#3a3a5a", "#2a2a4a", "#1a1a3a", "#0f0f2a"]

            color = colors[i % len(colors)]
            self.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                outline=color, width=2, fill=""
            )

        # Center filled circle
        if self.is_listening:
            cr = 20 + math.sin(self.phase * 2) * 5
            self.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,
                             fill="#00d4ff", outline="#00b4d8", width=2)
        elif self.is_speaking:
            cr = 20 + math.sin(self.phase * 3) * 3
            self.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,
                             fill="#a78bfa", outline="#8b5cf6", width=2)
        else:
            cr = 18 + math.sin(self.phase) * 2
            self.create_oval(cx - cr, cy - cr, cx + cr, cy + cr,
                             fill="#3a3a5a", outline="#4a4a6a", width=2)

        # Status text below orb
        if self.is_listening:
            label = "🎤 Listening..."
            lcolor = Theme.ACCENT
        elif self.is_speaking:
            label = "🔊 Speaking..."
            lcolor = Theme.TEXT_BOT
        else:
            label = "⏸ Ready"
            lcolor = Theme.TEXT_DIM

        self.create_text(cx, self.size - 15, text=label,
                         fill=lcolor, font=("Segoe UI", 10))

        self.after(33, self._animate)  # ~30 FPS


# ===========================================================================
# CHAT BUBBLE
# ===========================================================================
class ChatBubble(tk.Frame):
    """A single chat message bubble."""

    def __init__(self, parent, text, is_user=True, **kwargs):
        super().__init__(parent, bg=Theme.BG_SECONDARY, **kwargs)

        if is_user:
            icon = "🗣️"
            label = "You"
            color = Theme.TEXT_USER
            msg_bg = "#16213e"
        else:
            icon = "🤖"
            label = "Assistant"
            color = Theme.TEXT_BOT
            msg_bg = "#1e1e3a"

        # Header
        header = tk.Frame(self, bg=Theme.BG_SECONDARY)
        header.pack(fill="x", padx=15, pady=(10, 2))

        tk.Label(header, text=f"{icon} {label}", bg=Theme.BG_SECONDARY,
                 fg=color, font=("Segoe UI", 10, "bold")).pack(side="left")

        timestamp = datetime.datetime.now().strftime("%I:%M %p")
        tk.Label(header, text=timestamp, bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_DIM, font=("Segoe UI", 8)).pack(side="right")

        # Message body
        msg_frame = tk.Frame(self, bg=msg_bg, padx=12, pady=8)
        msg_frame.pack(fill="x", padx=15, pady=(2, 10))

        msg_label = tk.Label(msg_frame, text=text, bg=msg_bg, fg=Theme.TEXT,
                             font=("Segoe UI", 11), wraplength=480,
                             justify="left", anchor="w")
        msg_label.pack(fill="x")


# ===========================================================================
# MAIN APPLICATION
# ===========================================================================
class VoiceAssistantApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 SiriLike — AI Voice Assistant")
        self.root.geometry("700x850")
        self.root.configure(bg=Theme.BG)
        self.root.resizable(False, False)

        # Try to set icon
        try:
            self.root.iconbitmap(default="")
        except:
            pass

        # TTS engine
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 175)
                self.tts_engine.setProperty('volume', 1.0)
            except:
                pass

        # Speech recognizer
        self.recognizer = sr.Recognizer() if SPEECH_AVAILABLE else None

        self._build_ui()

    # -----------------------------------------------------------------------
    # UI CONSTRUCTION
    # -----------------------------------------------------------------------
    def _build_ui(self):
        # --- Title Bar ---
        title_frame = tk.Frame(self.root, bg=Theme.BG_SECONDARY, height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="🤖 SiriLike", bg=Theme.BG_SECONDARY,
                 fg=Theme.ACCENT, font=("Segoe UI", 20, "bold")).pack(side="left", padx=20, pady=10)

        tk.Label(title_frame, text="AI Voice Assistant", bg=Theme.BG_SECONDARY,
                 fg=Theme.TEXT_DIM, font=("Segoe UI", 11)).pack(side="left", pady=10)

        # Status indicator
        self.status_label = tk.Label(title_frame, text="● Online", bg=Theme.BG_SECONDARY,
                                     fg=Theme.SUCCESS, font=("Segoe UI", 10))
        self.status_label.pack(side="right", padx=20)

        # Separator
        tk.Frame(self.root, bg=Theme.BORDER, height=1).pack(fill="x")

        # --- Orb Section ---
        orb_frame = tk.Frame(self.root, bg=Theme.BG, height=180)
        orb_frame.pack(fill="x", pady=(5, 0))
        orb_frame.pack_propagate(False)

        self.orb = AnimatedOrb(orb_frame, size=170)
        self.orb.pack(expand=True)

        # --- Quick Action Buttons ---
        actions_frame = tk.Frame(self.root, bg=Theme.BG)
        actions_frame.pack(fill="x", padx=20, pady=(0, 5))

        quick_actions = [
            ("🕐 Time", "what time is it"),
            ("📅 Date", "what's the date"),
            ("😂 Joke", "tell me a joke"),
            ("🔋 Battery", "battery status"),
            ("💻 CPU", "cpu usage"),
            ("🌐 Google", "open google"),
        ]

        for i, (label, cmd) in enumerate(quick_actions):
            btn = tk.Button(
                actions_frame, text=label, bg=Theme.BUTTON_BG, fg=Theme.TEXT,
                font=("Segoe UI", 9), relief="flat", cursor="hand2",
                activebackground=Theme.BUTTON_HOVER, activeforeground=Theme.TEXT,
                padx=10, pady=5,
                command=lambda c=cmd: self._process_text_command(c)
            )
            btn.grid(row=0, column=i, padx=4, pady=5, sticky="ew")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=Theme.BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=Theme.BUTTON_BG))
            actions_frame.columnconfigure(i, weight=1)

        # --- Chat Area ---
        tk.Frame(self.root, bg=Theme.BORDER, height=1).pack(fill="x", padx=20)

        chat_container = tk.Frame(self.root, bg=Theme.BG_SECONDARY)
        chat_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.chat_canvas = tk.Canvas(chat_container, bg=Theme.BG_SECONDARY,
                                     highlightthickness=0, bd=0)
        self.scrollbar = tk.Scrollbar(chat_container, orient="vertical",
                                      command=self.chat_canvas.yview)
        self.chat_frame = tk.Frame(self.chat_canvas, bg=Theme.BG_SECONDARY)

        self.chat_frame.bind("<Configure>",
                             lambda e: self.chat_canvas.configure(
                                 scrollregion=self.chat_canvas.bbox("all")))

        self.chat_canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Enable mouse wheel scrolling
        self.chat_canvas.bind_all("<MouseWheel>",
            lambda e: self.chat_canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # Welcome message
        self._add_message("Hello! I'm SiriLike, your AI assistant. \n\n"
                          "🎤 Click the mic button to speak\n"
                          "⌨️ Or type a command below\n\n"
                          "Try: \"What time is it?\" or \"Tell me a joke\"", is_user=False)

        # --- Input Area ---
        tk.Frame(self.root, bg=Theme.BORDER, height=1).pack(fill="x", padx=20)

        input_frame = tk.Frame(self.root, bg=Theme.BG, height=70)
        input_frame.pack(fill="x", padx=20, pady=10)
        input_frame.pack_propagate(False)

        # Mic button
        self.mic_btn = tk.Button(
            input_frame, text="🎤", bg=Theme.ACCENT_DARK, fg="white",
            font=("Segoe UI", 16), relief="flat", cursor="hand2",
            width=3, activebackground=Theme.ACCENT,
            command=self._on_mic_click
        )
        self.mic_btn.pack(side="left", padx=(0, 10), fill="y")

        # Text input
        input_inner = tk.Frame(input_frame, bg=Theme.BG_INPUT, padx=2, pady=2)
        input_inner.pack(side="left", fill="both", expand=True)

        self.text_input = tk.Entry(
            input_inner, bg=Theme.BG_INPUT, fg=Theme.TEXT,
            font=("Segoe UI", 13), relief="flat", insertbackground=Theme.ACCENT,
            border=0
        )
        self.text_input.pack(fill="both", expand=True, padx=10, pady=8)
        self.text_input.insert(0, "Type a command...")
        self.text_input.bind("<FocusIn>", self._on_entry_focus)
        self.text_input.bind("<FocusOut>", self._on_entry_unfocus)
        self.text_input.bind("<Return>", self._on_enter)
        self.text_input.configure(fg=Theme.TEXT_DIM)

        # Send button
        self.send_btn = tk.Button(
            input_frame, text="➤", bg=Theme.ACCENT_DARK, fg="white",
            font=("Segoe UI", 16), relief="flat", cursor="hand2",
            width=3, activebackground=Theme.ACCENT,
            command=self._on_send_click
        )
        self.send_btn.pack(side="right", padx=(10, 0), fill="y")

        # --- Footer ---
        footer = tk.Frame(self.root, bg=Theme.BG, height=25)
        footer.pack(fill="x")
        tk.Label(footer, text="Built with ❤️ by Shouryadot23  |  Say \"goodbye\" to exit",
                 bg=Theme.BG, fg=Theme.TEXT_DIM, font=("Segoe UI", 8)).pack()

    # -----------------------------------------------------------------------
    # CHAT METHODS
    # -----------------------------------------------------------------------
    def _add_message(self, text, is_user=True):
        bubble = ChatBubble(self.chat_frame, text, is_user=is_user)
        bubble.pack(fill="x", pady=2)

        # Auto-scroll to bottom
        self.root.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def _speak(self, text):
        """Speak text using TTS."""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass

    # -----------------------------------------------------------------------
    # COMMAND PROCESSING
    # -----------------------------------------------------------------------
    def _process_text_command(self, text):
        text = text.strip().lower()
        if not text:
            return

        self._add_message(text, is_user=True)
        self.orb.set_state("speaking")

        # Process in a thread to keep UI responsive
        threading.Thread(target=self._handle_and_respond, args=(text,), daemon=True).start()

    def _handle_and_respond(self, text):
        response = self._get_response(text)

        # Update UI from main thread
        self.root.after(0, self._add_message, response, False)
        self.root.after(0, self.orb.set_state, "idle")

        # Speak the response
        self.orb.set_state("speaking")
        self._speak(response)
        self.root.after(0, self.orb.set_state, "idle")

        # Check for exit
        if any(word in text for word in ["goodbye", "exit", "quit", "bye"]):
            self.root.after(2000, self.root.destroy)

    def _get_response(self, text):
        """Get the appropriate response for a command."""

        # Exit
        if any(word in text for word in ["goodbye", "exit", "quit", "stop", "bye"]):
            return "Goodbye! Have a great day! 👋"

        # Greetings
        elif any(word in text for word in ["hello", "hi", "hey", "greetings", "howdy"]):
            greetings = [
                "Hey there! How can I help you? 😊",
                "Hello! What can I do for you today?",
                "Hi! I'm ready to assist you! 🚀",
            ]
            return random.choice(greetings)

        # Time
        elif "time" in text:
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {now} 🕐"

        # Date
        elif "date" in text or "day is it" in text:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"Today is {today} ���"

        # Weather
        elif "weather" in text:
            city = None
            for prep in [" in ", " for ", " at "]:
                if prep in text:
                    city = text.split(prep, 1)[1].strip()
                    break
            if not city:
                return "Which city would you like the weather for? Try: 'weather in London'"
            return get_weather(city) + " 🌤️"

        # Search
        elif text.startswith("search") or "search for" in text:
            query = text.replace("search for", "").replace("search", "").strip()
            if query:
                url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(url)
                return f"Searching Google for: {query} 🔍"
            return "What would you like me to search for?"

        # Open website
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
                "wikipedia": "https://www.wikipedia.org",
                "netflix": "https://www.netflix.com",
                "spotify": "https://www.spotify.com",
            }
            for name, url in sites.items():
                if name in text:
                    webbrowser.open(url)
                    return f"Opening {name.title()}! 🌐"
            site_name = text.replace("open", "").strip()
            if site_name:
                webbrowser.open(f"https://www.{site_name}.com")
                return f"Trying to open {site_name}... 🌐"
            return "Which website would you like me to open?"

        # Joke
        elif "joke" in text:
            return get_joke() + " 😂"

        # Wikipedia
        elif any(text.startswith(w) for w in ["who is", "what is", "tell me about", "who was", "what was", "define"]):
            query = text
            for prefix in ["who is", "what is", "tell me about", "who was", "what was", "define"]:
                if text.startswith(prefix):
                    query = text[len(prefix):].strip()
                    break
            if query:
                return get_wikipedia_summary(query) + " 📚"
            return "What would you like to know about?"

        # Battery
        elif "battery" in text:
            return get_system_info("battery") + " 🔋"

        # CPU
        elif "cpu" in text or "processor" in text:
            return get_system_info("cpu") + " 💻"

        # System info
        elif "system" in text and "info" in text:
            return get_system_info("all") + " 🖥️"

        # Notes - save
        elif "remember" in text and ("that" in text or "this" in text):
            for keyword in ["remember that ", "remember this "]:
                if keyword in text:
                    note = text.split(keyword, 1)[1].strip()
                    return save_note(note) + " 📝"
            return "What should I remember?"

        # Notes - recall
        elif "what do you remember" in text or "my notes" in text or "recall" in text:
            return recall_notes() + " 📝"

        # Fallback
        else:
            return "I'm not sure how to help with that. Try asking about the time, weather, or say 'tell me a joke'! 🤔"

    # -----------------------------------------------------------------------
    # EVENT HANDLERS
    # -----------------------------------------------------------------------
    def _on_entry_focus(self, event):
        if self.text_input.get() == "Type a command...":
            self.text_input.delete(0, "end")
            self.text_input.configure(fg=Theme.TEXT)

    def _on_entry_unfocus(self, event):
        if not self.text_input.get():
            self.text_input.insert(0, "Type a command...")
            self.text_input.configure(fg=Theme.TEXT_DIM)

    def _on_enter(self, event):
        self._on_send_click()

    def _on_send_click(self):
        text = self.text_input.get().strip()
        if text and text != "Type a command...":
            self.text_input.delete(0, "end")
            self._process_text_command(text)

    def _on_mic_click(self):
        if not SPEECH_AVAILABLE:
            self._add_message("Speech recognition is not available. Install SpeechRecognition and PyAudio.", is_user=False)
            return
        self.orb.set_state("listening")
        self.mic_btn.configure(bg=Theme.ERROR, text="⏹")
        threading.Thread(target=self._listen_voice, daemon=True).start()

    def _listen_voice(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=15)
                text = self.recognizer.recognize_google(audio).lower()
                self.root.after(0, self._reset_mic_btn)
                self.root.after(0, self._process_text_command, text)
        except sr.WaitTimeoutError:
            self.root.after(0, self._add_message, "I didn't hear anything. Try again! 🎤", False)
            self.root.after(0, self._reset_mic_btn)
            self.root.after(0, self.orb.set_state, "idle")
        except sr.UnknownValueError:
            self.root.after(0, self._add_message, "Sorry, I couldn't understand that. Try again! ❓", False)
            self.root.after(0, self._reset_mic_btn)
            self.root.after(0, self.orb.set_state, "idle")
        except Exception as e:
            self.root.after(0, self._add_message, f"Mic error: {e}", False)
            self.root.after(0, self._reset_mic_btn)
            self.root.after(0, self.orb.set_state, "idle")

    def _reset_mic_btn(self):
        self.mic_btn.configure(bg=Theme.ACCENT_DARK, text="🎤")

    # -----------------------------------------------------------------------
    # RUN
    # -----------------------------------------------------------------------
    def run(self):
        self.root.mainloop()


# ===========================================================================
# ENTRY POINT
# ===========================================================================
if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.run()
