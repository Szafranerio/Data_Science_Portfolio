from tkinter import *
import pandas as pd
import random
from tkinter import messagebox, ttk, END
from dotenv import load_dotenv
import locale
import add_edit_delete
import mail
from mail import send_to_mail
import show
import speak
import random_words
import numbers_practice
import review_words
from switch_color import switch_color

load_dotenv()
locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')

# Colors
is_night_mode = False
DAY_BACKGROUND_COLOR = "#E8E8E8"
NIGHT_BACKGROUND_COLOR = "#1E1E1E"
DAY_TEXT_COLOR = "black"
NIGHT_TEXT_COLOR = "#E0E0E0"
BACKGROUND_COLOR = DAY_BACKGROUND_COLOR
TEXT_COLOR = DAY_TEXT_COLOR

# Globals var
current_card = {}
to_learn = {}
missed_word = []
FONT_NAME = "Courier"

try:
    danish_data = pd.read_csv('./data/data/words_to_learn.csv')
    to_learn = danish_data.to_dict(orient='records')
except FileNotFoundError:
    original_data = pd.read_csv('./data/data/danish_words.csv')
    to_learn = original_data.to_dict(orient='records')
    original_data.to_csv('./data/data/words_to_learn.csv', index=False)

# Functions
def next_card():
    global current_card, flip_timer, missed_word
    if flip_timer is not None:
        window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # Set text and color
    canvas.itemconfig(card_title, text='Danish', fill=TEXT_COLOR)
    canvas.itemconfig(card_word, text=current_card['Danish'], fill=TEXT_COLOR)
    flip_timer = window.after(3000, func=flip_card)
    missed_word.append(current_card)

def flip_card():
    # Set text and color
    canvas.itemconfig(card_title, text='English', fill=TEXT_COLOR)
    canvas.itemconfig(card_word, text=current_card['English'], fill=TEXT_COLOR)

def is_known():
    global current_card
    if current_card in to_learn:
        to_learn.remove(current_card)
        data = pd.DataFrame(to_learn)
        data.to_csv('./data/data/words_to_learn.csv', index=False)
        next_card()
        
def review():   
    review_words.review_words(window)

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

def practice_numbers():
    numbers_practice.numbers_practice(window)
    
def night_mode():
    global is_night_mode, BACKGROUND_COLOR, TEXT_COLOR
    is_night_mode = not is_night_mode

    # Update colors of the UI, dependes from the choice, it can be for day or night mode
    if is_night_mode:
        BACKGROUND_COLOR = NIGHT_BACKGROUND_COLOR
        TEXT_COLOR = NIGHT_TEXT_COLOR
    else:
        BACKGROUND_COLOR = DAY_BACKGROUND_COLOR
        TEXT_COLOR = DAY_TEXT_COLOR

    window.config(bg=BACKGROUND_COLOR)
    canvas.config(bg=BACKGROUND_COLOR)
    canvas.itemconfig(card_title, fill=TEXT_COLOR)
    canvas.itemconfig(card_word, fill=TEXT_COLOR)

    for button in buttons:
        button.config(highlightbackground=BACKGROUND_COLOR)

# UI Setup
window = Tk()
window.title('Flash Cards')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=300, highlightthickness=0, bg=BACKGROUND_COLOR)
card_title = canvas.create_text(400, 60, text='Title', font=('Ariel', 40, 'italic'), fill=TEXT_COLOR)
card_word = canvas.create_text(400, 150, text='WORD', font=('Ariel', 60, 'bold'), fill=TEXT_COLOR)
canvas.grid(column=1, row=0, padx=10, pady=10)

# Button images
ok_button = PhotoImage(file='./data/images/right.png')
false_button = PhotoImage(file='./data/images/wrong.png')
speaker_button = PhotoImage(file='./data/images/speaker.png')

# Buttons
wrong_button = Button(image=false_button, highlightbackground=BACKGROUND_COLOR, command=next_card)
wrong_button.grid(column=0, row=1, padx=5, pady=5)

correct_button = Button(image=ok_button, highlightbackground=BACKGROUND_COLOR, command=is_known)
correct_button.grid(column=2, row=1, padx=5, pady=5)

speak_button = Button(image=speaker_button, highlightbackground=BACKGROUND_COLOR, command=say_word)
speak_button.grid(column=1, row=1, padx=5, pady=5)

button_show = Button(text='Show Data', highlightbackground=BACKGROUND_COLOR, command=show_data)
button_show.grid(column=0, row=2)

edit_button_main = Button(text='Add/Edit/Delete Words', highlightbackground=BACKGROUND_COLOR, command=add_edit_or_delete_word)
edit_button_main.grid(column=1, row=2)

random_button = Button(text='Random 50 Words', highlightbackground=BACKGROUND_COLOR, command=random_50)
random_button.grid(column=2, row=2)

button_number = Button(text='Practice Numbers', highlightbackground=BACKGROUND_COLOR, command=practice_numbers)
button_number.grid(column=0, row=3)

send_button = Button(text='Send to Mail', highlightbackground=BACKGROUND_COLOR, command=send_to_mail)
send_button.grid(column=1, row=3)

review_button = Button(text='Review', highlightbackground=BACKGROUND_COLOR, command=review)
review_button.grid(column=2, row=3)

night_mode_button = Button(text='Switch Mode', highlightbackground=BACKGROUND_COLOR, command=night_mode)
night_mode_button.grid(column=1, row=4)

buttons = [wrong_button, correct_button, speak_button, button_show, edit_button_main, random_button, button_number, send_button, review_button, night_mode_button]

window.mainloop()