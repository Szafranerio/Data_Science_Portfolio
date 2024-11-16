from tkinter import *
import pandas as pd
import random
import json
from tkinter import messagebox, ttk, END
import os
import re
import smtplib
import locale
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tkinter import ttk
from natsort import natsorted, ns
import pyttsx3
import add_edit_delete
import mail
from mail import send_to_mail
import show
import speak
import random_words

load_dotenv()
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
FONT_NAME = "Courier"
locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')

try:
    danish_data = pd.read_csv('./data/data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('./data/data/danish_words.csv')
    to_learn = original_data.to_dict(orient='records')
    original_data.to_csv('./data/data/words_to_learn.csv', index=False)
else:
    to_learn = danish_data.to_dict(orient='records')

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text='Danish', fill='black')
    canvas.itemconfig(card_word, text=current_card['Danish'], fill='black')
    canvas.itemconfig(card_background, image=front_card)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')
    canvas.itemconfig(card_background, image=back_card)
    
def update_progress(value):
    progress['value'] = value
    window.update_idletasks()

def increment_progress(current, total):
    value = (current / total) * 100
    update_progress(value)

total_words = len(to_learn) 

def is_known():
    global current_card
    if current_card in to_learn:
        to_learn.remove(current_card)
        data = pd.DataFrame(to_learn)
        data.to_csv('./data/data/words_to_learn.csv', index=False)
        next_card()

def show_data():
    show.show_data(window)

def send_to_mail():
    mail.send_to_mail(window)

def add_edit_or_delete_word():
    add_edit_delete.add_edit_or_delete_word(window)

def say_word():
    speak.speak(window, current_card)

def random_50():
    random_words.random_number_50(window)

def numbers():
    pass

# User Interface
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flash Cards')

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file='./data/images/card_front.png')
back_card = PhotoImage(file='./data/images/card_back.png')
card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(
    400, 150, text='Title', font=('Ariel', 40, 'italic'), fill='black')
card_word = canvas.create_text(
    400, 263, text='WORD', font=('Ariel', 60, 'bold'), fill='black')
canvas.grid(column=0, row=0, columnspan=3)

# Button images
ok_button = PhotoImage(file='./data/images/right.png')
false_button = PhotoImage(file='./data/images/wrong.png')
speaker_button = PhotoImage(file='./data/images/speaker.png')

correct_button = Button(image=ok_button, highlightbackground=BACKGROUND_COLOR,
                        highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=is_known)
correct_button.grid(column=2, row=1)

wrong_button = Button(image=false_button, highlightbackground=BACKGROUND_COLOR,
                      highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=next_card)
wrong_button.grid(column=0, row=1)
send_button = Button(text='Send to mail', highlightbackground=BACKGROUND_COLOR,
                     highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=send_to_mail)
send_button.grid(column=3, row=3)

button_show = Button(text='Show data', highlightbackground=BACKGROUND_COLOR,
                     highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=show_data)
button_show.grid(column=3, row=0)

edit_button_main = Button(text='Add/Edit/Delete Words', highlightbackground=BACKGROUND_COLOR,
                          highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=add_edit_or_delete_word)
edit_button_main.grid(column=3, row=1)

random_button = Button(text='Random 50 Words', highlightbackground=BACKGROUND_COLOR,
                          highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=random_50)
random_button.grid(column=3, row=2)

speak_button = Button(image=speaker_button, highlightbackground=BACKGROUND_COLOR,
                      highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=say_word)
speak_button.grid(column=1, row=1)

window.mainloop()
