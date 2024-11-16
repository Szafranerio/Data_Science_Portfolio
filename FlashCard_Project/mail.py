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

load_dotenv()
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
FONT_NAME = "Courier"

def send_to_mail(window):
    mail_window = Toplevel(window)
    mail_window.title('Send Mail')
    Label(mail_window, text='Input your mail: ', font=(FONT_NAME, 12)).grid(
        column=0, row=0, sticky='e', padx=10, pady=5)
    input_send_mail = Entry(mail_window, width=30)
    input_send_mail.grid(column=1, row=0)

    Button(mail_window, text='Send',
           command=lambda: send(input_send_mail.get())).grid(column=2, row=0)

def send(send_mail):
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

    body = "Please find the attached data.txt file."
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
            messagebox.showinfo(title="File Removed",
                                message="words_to_learn.csv has been deleted.")
        else:
            messagebox.showwarning(
                title="File Not Found", message="The file was not found for deletion.")
    except Exception as e:
        messagebox.showerror(
            title="Error", message=f"Error sending email: {e}")
    finally:
        input_send_mail.delete(0, END)
