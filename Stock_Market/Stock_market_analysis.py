from tkinter import *
from tkinter import messagebox, ttk, END
import json


FONT_NAME = "Courier"
analysis = ['Price', 'RSI', 'MACD', 'Bollinger Bands', 'M10&M20', 'ALL']

# Functions


def send_data():
    ticker = input_ticker.get().title()
    days = int(input_time.get())
    mail = input_mail.get()
    new_data = {
        "stock": {
            "ticker