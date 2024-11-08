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

load_dotenv()
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
FONT_NAME = "Courier"

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
    
# Progress function
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

def add_word():
    global input_word
    add_window = Toplevel(window)
    add_window.title("New word")
    word = Label(add_window, text='Input new word (danish_word,english_word): ', font=(FONT_NAME, 12)).grid(
        column=0, row=0, sticky='e', padx=10, pady=5)
    input_word = Entry(add_window, width=30)
    input_word.grid(column=1, row=0)

    send_button = Button(add_window, text='Send',
                         command=lambda: add(input_word))
    send_button.grid(column=2, row=0)
    
def add(input_word):
    add_word = input_word.get()
    
    if not re.search(r"^[\wÀ-ÖØ-öø-ÿ ]+,[\wÀ-ÖØ-öø-ÿ ]+$", add_word):
        messagebox.showwarning(
            title="Warning", message="Check the word!")
        return
    
    danish, english = add_word.split(',')

    try:
        existing_data = pd.read_csv('./data/data/danish_words.csv')
        existing_data_set = set(
            (row['Danish'].strip(), row['English'].strip()) for _, row in existing_data.iterrows()
        )
    except FileNotFoundError:
        existing_data_set = set()

    if (danish, english) in existing_data_set:
        messagebox.showinfo(title="Duplicate", message="This word pair already exists!")
        return
    
    with open('./data/data/danish_words.csv','a') as fd:
        fd.write(f"\n{add_word.strip()}")
    messagebox.showinfo(title="Success", message="Word added successfully!")
    input_word.delete(0,END)


locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')

def show_data():
    try:
        data = pd.read_csv('./data/data/danish_words.csv')
        prefixes_to_exclude = ('en ', 'et ', 'at ', 'af ', 'i ', 'på ', 'til ', 'med ', 'om ', 'ud ')

        def remove_prefix(word):
            for prefix in prefixes_to_exclude:
                if word.startswith(prefix):
                    return word[len(prefix):]
            return word

        data['sort_key'] = data['Danish'].apply(remove_prefix)

        data = data.loc[natsorted(data.index, key=lambda x: data.loc[x, 'sort_key'], alg=ns.LOCALE)].reset_index(drop=True)

        data = data.drop(columns='sort_key')
        data_str = data.to_string(index=False)

        data_window = Toplevel(window)
        data_window.title("Saved Data")
        text_area = Text(data_window, wrap='word', width=80, height=20)
        text_area.pack(padx=10, pady=10)
        text_area.insert(END, data_str)
        text_area.config(state=DISABLED)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found!")
    except pd.errors.EmptyDataError:
        messagebox.showerror(title="Error", message="The data file is empty!")
    except locale.Error as e:
        messagebox.showerror(title="Locale Error", message=f"Locale error: {e}")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")
    
def send_to_mail():
    global input_send_mail
    mail_window = Toplevel(window)
    mail_window.title('Send Mail')
    mailing = Label(mail_window, text='Input your mail: ', font=(FONT_NAME, 12)).grid(
        column=0, row=0, sticky='e', padx=10, pady=5)
    input_send_mail = Entry(mail_window, width=30)
    input_send_mail.grid(column=1, row=0)

    send_button = Button(mail_window, text='Send',
                         command=lambda: send(input_send_mail))
    send_button.grid(column=2, row=0)

def send(input_send_mail):
    send_mail = input_send_mail.get()

    if not re.search(r"^\w+@\w+\.\w+$", send_mail):
        messagebox.showwarning(
            title="Warning", message="Invalid email address!")
        return

    mail = os.getenv('MAIL')
    password = os.getenv('PASSWORD')
    recipients = send_mail
    subject = 'Data Export'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = recipients
    msg['Subject'] = subject

    body = "Please find the attached data.json file."
    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

    data_file_path = './data/data/words_to_learn.csv'

    try:
        with open(data_file_path, 'rb') as file:
            file_part = MIMEApplication(file.read(), Name="data.txt")
            file_part['Content-Disposition'] = 'attachment; filename="data.txt"'
            msg.attach(file_part)
    except Exception as e:
        messagebox.showerror(
            title="Error", message=f"Could not attach file: {e}")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(user=mail, password=password)
            connection.sendmail(
                from_addr=mail, to_addrs=recipients, msg=msg.as_string())
        messagebox.showinfo(
            title="Success", message="Email sent successfully!")
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
            messagebox.showinfo(
                title="File Removed", message="words_to_learn.csv has been deleted.")
        else:
            messagebox.showwarning(
                title="File Not Found", message="The file was not found for deletion.")
    except Exception as e:
        messagebox.showerror(
            title="Error", message=f"Error sending email: {e}")
    finally:
        input_send_mail.delete(0,END)

# User Interface
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flash Cards')

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front_card = PhotoImage(file='./data/images/card_front.png')
back_card = PhotoImage(file='./data/images/card_back.png')
card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(
    400, 150, text='Title', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(
    400, 263, text='WORD', font=('Ariel', 60, 'bold'))
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=3)

progress = ttk.Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate')
progress.grid(column=0, row=3, columnspan=3, pady=20)

# Button images
ok_button = PhotoImage(file='./data/images/right.png')
false_button = PhotoImage(file='./data/images/wrong.png')
correct_button = Button(
    image=ok_button,  highlightbackground=BACKGROUND_COLOR,
       highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=is_known)
correct_button.grid(column=2, row=1)
wrong_button = Button(image=false_button,
                      highlightbackground=BACKGROUND_COLOR,
       highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=next_card)
wrong_button.grid(column=0, row=1)
send_button = Button(text='Send to mail',
                      highlightbackground=BACKGROUND_COLOR,
       highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=send_to_mail)
send_button.grid(column=0, row=2)
add_button = Button(text='Add to list',
                      highlightbackground=BACKGROUND_COLOR,
       highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=add_word)
add_button.grid(column=2, row=2)

button_show = Button(text='Show data', highlightbackground=BACKGROUND_COLOR,
       highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=show_data)
button_show.grid(column=1, row=2)

window.mainloop()