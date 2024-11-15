from tkinter import *
import pandas as pd
import random
import os
import re
import smtplib
import locale
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tkinter import messagebox, ttk, END
from natsort import natsorted, ns
import pyttsx3

load_dotenv()

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Courier"

def run_flashcards():
    window = Tk()
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
    window.title('Flash Cards')

    current_card = {}
    to_learn = {}

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

    progress = ttk.Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate')
    progress.grid(column=0, row=4, columnspan=3, pady=20)

    def update_progress(value):
        progress['value'] = value
        window.update_idletasks()

    def increment_progress(current, total):
        value = (current / total) * 100
        update_progress(value)

    current_word_index = 0
    total_words = len(to_learn)

    def is_known():
        global current_word_index, current_card
        if current_card in to_learn:
            to_learn.remove(current_card)
            current_word_index += 1
            increment_progress(current_word_index, total_words)
            data = pd.DataFrame(to_learn)
            data.to_csv('./data/data/words_to_learn.csv', index=False)
            next_card()

    canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
    front_card = PhotoImage(file='./data/images/card_front.png')
    back_card = PhotoImage(file='./data/images/card_back.png')
    card_background = canvas.create_image(400, 263, image=front_card)
    card_title = canvas.create_text(400, 150, text='Title', font=('Ariel', 40, 'italic'))
    card_word = canvas.create_text(400, 263, text='WORD', font=('Ariel', 60, 'bold'))
    canvas.grid(column=0, row=0, columnspan=3)

    ok_button = PhotoImage(file='./data/images/right.png')
    false_button = PhotoImage(file='./data/images/wrong.png')

    correct_button = Button(image=ok_button, highlightbackground=BACKGROUND_COLOR, command=is_known)
    correct_button.grid(column=2, row=1)

    wrong_button = Button(image=false_button, highlightbackground=BACKGROUND_COLOR, command=next_card)
    wrong_button.grid(column=0, row=1)

    def send_to_mail():
        mail_window = Toplevel(window)
        mail_window.title('Send Mail')
        Label(mail_window, text='Input your mail:', font=(FONT_NAME, 12)).grid(column=0, row=0, sticky='e', padx=10, pady=5)
        input_send_mail = Entry(mail_window, width=30)
        input_send_mail.grid(column=1, row=0)
        Button(mail_window, text='Send', command=lambda: send(input_send_mail)).grid(column=2, row=0)

    send_button = Button(text='Send to mail', highlightbackground=BACKGROUND_COLOR, command=send_to_mail)
    send_button.grid(column=0, row=2)

    def show_data():
        data_window = Toplevel(window)
        data_window.title("Saved Data")

    button_show = Button(text='Show data', highlightbackground=BACKGROUND_COLOR, command=show_data)
    button_show.grid(column=1, row=2)

    def go_back():
        window.destroy()

    back_button = Button(text='Back', highlightbackground=BACKGROUND_COLOR, command=go_back)
    back_button.grid(column=1, row=3, pady=10)

    flip_timer = window.after(5000, func=flip_card)
    next_card()
    window.mainloop()
