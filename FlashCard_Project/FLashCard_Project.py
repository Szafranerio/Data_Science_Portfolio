from tkinter import *
import pandas
import random
import json
from tkinter import *
from tkinter import messagebox, ttk, END
import os
import re
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


load_dotenv()
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
FONT_NAME = "Courier"

try:
    danish_data = pandas.read_csv('./data/data/words_to_learn.csv')
except FileNotFoundError:
    orignal_data = pandas.read_csv('./data/data/danish_words.csv')
    to_learn = original_data.to_dict(orient='records')
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


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv('./data/data/words_to_learn.csv', index=False)
    next_card()


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
            file_part = MIMEApplication(file.read(), Name="data.json")
            file_part['Content-Disposition'] = 'attachment; filename="data.json"'
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
    except Exception as e:
        messagebox.showerror(
            title="Error", message=f"Error sending email: {e}")


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
canvas.grid(column=0, row=0, columnspan=2)

# Button images
ok_button = PhotoImage(file='./data/images/right.png')
false_button = PhotoImage(file='./data/images/wrong.png')
correct_button = Button(
    image=ok_button, highlightthickness=0, command=is_known)
correct_button.grid(column=3, row=2)
wrong_button = Button(image=false_button,
                      highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=2)
send_button = Button(text='Send to mail',
                      highlightthickness=0, command=send_to_mail)
send_button.grid(column=2, row=3)

add_button = Button(text='Add to list',
                      highli