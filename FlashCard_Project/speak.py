from tkinter import *
from tkinter import messagebox, ttk, END
import os
import re
import smtplib
import locale
from dotenv import load_dotenv
from tkinter import ttk
from natsort import natsorted, ns
import pyttsx3

load_dotenv()
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
FONT_NAME = "Courier"


def speak(window, current_card):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        danish_voice_id = None

        for voice in voices:
            if 'da' in voice.languages or 'Danish' in voice.name:
                danish_voice_id = voice.id
                break

        engine.setProperty('voice', danish_voice_id)
        engine.setProperty('rate', 125)
        engine.say(current_card.get('Danish', 'No word to speak'))  # Use .get() to avoid KeyError
        engine.runAndWait()

    except Exception as e:
        messagebox.showerror(
            "Error", f"An error occurred while trying to speak: {e}")
