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
import numbers_practice

load_dotenv()
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
missed_word = []
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
    global current_card, flip_timer, missed_word
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text='Danish', fill='black')
    canvas.itemconfig(card_word, text=current_card['Danish'], fill='black')
    flip_timer = window.after(3000, func=flip_card)
    missed_word.append(current_card)
    
def review():
    try:
        data = pd.read_csv('./data/data/words_to_learn.csv')
        prefixes_to_exclude = ('en ', 'et ', 'at ', 'af ', 'i ', 'på ', 'til ', 'med ', 'om ', 'ud ')

        def remove_prefix(word):
            for prefix in prefixes_to_exclude:
                if word.startswith(prefix):
                    return word[len(prefix):]
            return word

        data['sort_key'] = data['Danish'].apply(remove_prefix)
        data = data.loc[natsorted(data.index, key=lambda x: data.loc[x, 'sort_key'], alg=ns.LOCALE)].reset_index(drop=True)
        data = data.drop(columns='sort_key')

        data_window = Toplevel(window)
        data_window.title("Saved Data")

        # Search bar
        search_frame = Frame(data_window)
        search_frame.pack(pady=5)
        Label(search_frame, text="Search:", font=(FONT_NAME, 12)).pack(side=LEFT, padx=5)
        search_entry = Entry(search_frame, width=30)
        search_entry.pack(side=LEFT, padx=5)

        # Create a Treeview widget
        tree = ttk.Treeview(data_window, columns=("Danish", "English"), show='headings', height=15)
        tree.heading("Danish", text="Danish")
        tree.heading("English", text="English")
        tree.pack(padx=10, pady=10)

        def populate_tree(data_subset):
            for item in tree.get_children():
                tree.delete(item)
            for _, row in data_subset.iterrows():
                tree.insert('', END, values=(row['Danish'], row['English']))

        populate_tree(data)

        # Search functionality
        def search_word():
            search_text = search_entry.get().strip().lower()
            filtered_data = data[(data['Danish'].str.lower().str.contains(search_text)) | 
                                 (data['English'].str.lower().str.contains(search_text))]
            populate_tree(filtered_data)

        search_entry.bind("<KeyRelease>", lambda event: search_word())
        
        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning(
                    "Warning", "Please select a word to delete.")
                return

            delete_item = tree.item(selected_item)['values']
            result = messagebox.askyesno(
                "Confirmation", f"Are you sure you want to delete '{delete_item[0]}'?")
            if result:
                data.drop(data[(data['Danish'] == delete_item[0]) & (
                    data['English'] == delete_item[1])].index, inplace=True)
                data.to_csv('./data/data/words_to_learn.csv', index=False)
                messagebox.showinfo("Success", "Word deleted successfully!")
                data_list = data.to_dict(orient='records')
                populate_tree(data_list)

        Button(search_frame, text="Remove from list", command=delete_selected).pack(
            side=LEFT, padx=10, pady=5)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found!")
    except pd.errors.EmptyDataError:
        messagebox.showerror(title="Error", message="The data file is empty!")
    except locale.Error as e:
        messagebox.showerror(title="Locale Error", message=f"Locale error: {e}")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")

    

def flip_card():
    canvas.itemconfig(card_title, text='English', fill='black')
    canvas.itemconfig(card_word, text=current_card['English'], fill='black')


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

def practice_numbers():
    numbers_practice.numbers_practice(window)
    
# User Interface
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flash Cards')

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=300, highlightthickness=0, bg=BACKGROUND_COLOR)
card_title = canvas.create_text(
    400, 60, text='Title', font=('Ariel', 40, 'italic'), fill='black')
card_word = canvas.create_text(
    400, 150, text='WORD', font=('Ariel', 60, 'bold'), fill='black')
canvas.grid(column=1, row=0, padx=10, pady=10)

# Button images
ok_button = PhotoImage(file='./data/images/right.png')
false_button = PhotoImage(file='./data/images/wrong.png')
speaker_button = PhotoImage(file='./data/images/speaker.png')


wrong_button = Button(image=false_button, highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=next_card)
wrong_button.grid(column=0, row=1, padx=5, pady=5)

speak_button = Button(image=speaker_button, highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=say_word)
speak_button.grid(column=1, row=1, padx=5, pady=5)

correct_button = Button(image=ok_button, highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=is_known)
correct_button.grid(column=2, row=1, padx=5, pady=5)

button_show = Button(text='Show data', highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=show_data)
button_show.grid(column=0, row=2)

edit_button_main = Button(text='Add/Edit/Delete Words', highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=add_edit_or_delete_word)
edit_button_main.grid(column=1, row=2)

random_button = Button(text='Random 50 Words', highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=random_50)
random_button.grid(column=2, row=2)

button_number = Button(text='Number data', highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=practice_numbers)
button_number.grid(column=0, row=3)

send_button = Button(text='Send to mail', highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=send_to_mail)
send_button.grid(column=1, row=3)

review_button = Button(text='Review', highlightbackground=BACKGROUND_COLOR,
highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=review)
review_button.grid(column=2, row=3)

window.mainloop()