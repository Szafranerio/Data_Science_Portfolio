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
    Label(mail_window, text='Input your mail: ', font=(FONT_NAME, 12)).grid(
        column=0, row=0, sticky='e', padx=10, pady=5)
    input_send_mail = Entry(mail_window, width=30)
    input_send_mail.grid(column=1, row=0)

    Button(mail_window, text='Send',
           command=lambda: send(input_send_mail)).grid(column=2, row=0)

def send(input_send_mail):
    send_mail = input_send_mail.get()
    if not re.search(r"^\w+@\w+\.\w+$", send_mail):
        messagebox.showwarning(title="Warning", message="Invalid email address!")
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
        messagebox.showerror(title="Error", message=f"Could not attach file: {e}")
        return

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(user=mail, password=password)
            connection.sendmail(from_addr=mail, to_addrs=recipients, msg=msg.as_string())
        messagebox.showinfo(title="Success", message="Email sent successfully!")
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
            messagebox.showinfo(title="File Removed", message="words_to_learn.csv has been deleted.")
        else:
            messagebox.showwarning(title="File Not Found", message="The file was not found for deletion.")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"Error sending email: {e}")
    finally:
        input_send_mail.delete(0, END)

def add_edit_or_delete_word():
    edit_window = Toplevel(window)
    edit_window.title("Add/Edit/Delete Words")

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
        data_list = data.to_dict(orient='records')

        # Search bar
        search_frame = Frame(edit_window)
        search_frame.pack(pady=5)
        Label(search_frame, text="Search:", font=(FONT_NAME, 12)).pack(side=LEFT, padx=5)
        search_entry = Entry(search_frame, width=30)
        search_entry.pack(side=LEFT, padx=5)

        # Frame for Treeview and buttons
        frame = Frame(edit_window)
        frame.pack(pady=10)

        # Create a Treeview widget
        tree = ttk.Treeview(frame, columns=("Danish", "English"), show='headings', height=15)
        tree.heading("Danish", text="Danish")
        tree.heading("English", text="English")
        tree.pack()

        def populate_tree(data_subset):
            for item in tree.get_children():
                tree.delete(item)
            for row in data_subset:
                tree.insert('', END, values=(row['Danish'], row['English']))

        populate_tree(data_list)

        # Search words
        def search_word():
            search_text = search_entry.get().strip().lower()
            filtered_data = [row for row in data_list if search_text in row['Danish'].lower() or search_text in row['English'].lower()]
            populate_tree(filtered_data)

        search_entry.bind("<KeyRelease>", lambda event: search_word())

        def add_new_word():
            add_window = Toplevel(edit_window)
            add_window.title("Add New Word")

            Label(add_window, text="Danish:", font=(FONT_NAME, 12)).grid(row=0, column=0, padx=10, pady=5)
            danish_entry = Entry(add_window, width=30)
            danish_entry.grid(row=0, column=1, padx=10, pady=5)

            Label(add_window, text="English:", font=(FONT_NAME, 12)).grid(row=1, column=0, padx=10, pady=5)
            english_entry = Entry(add_window, width=30)
            english_entry.grid(row=1, column=1, padx=10, pady=5)

            def save_new_word():
                danish = danish_entry.get().strip()
                english = english_entry.get().strip()

                if not danish or not english:
                    messagebox.showwarning("Warning", "Both fields must be filled.")
                    return

                if (danish, english) in [(row['Danish'], row['English']) for row in data_list]:
                    messagebox.showinfo("Duplicate", "This word pair already exists!")
                    return

                with open('./data/data/danish_words.csv', 'a') as fd:
                    fd.write(f"\n{danish},{english}")
                messagebox.showinfo("Success", "Word added successfully!")
                data_list.append({'Danish': danish, 'English': english})
                populate_tree(data_list)
                add_window.destroy()

            Button(add_window, text="Save", command=save_new_word).grid(row=2, column=0, columnspan=2, pady=10)

        def edit_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a word to edit.")
                return

            edit_item = tree.item(selected_item)['values']
            edit_window_inner = Toplevel(edit_window)
            edit_window_inner.title("Edit Word")

            Label(edit_window_inner, text="Danish:", font=(FONT_NAME, 12)).grid(row=0, column=0, padx=10, pady=5)
            danish_entry = Entry(edit_window_inner, width=30)
            danish_entry.grid(row=0, column=1, padx=10, pady=5)
            danish_entry.insert(0, edit_item[0])

            Label(edit_window_inner, text="English:", font=(FONT_NAME, 12)).grid(row=1, column=0, padx=10, pady=5)
            english_entry = Entry(edit_window_inner, width=30)
            english_entry.grid(row=1, column=1, padx=10, pady=5)
            english_entry.insert(0, edit_item[1])

            def save_changes():
                new_danish = danish_entry.get().strip()
                new_english = english_entry.get().strip()

                if not new_danish or not new_english:
                    messagebox.showwarning("Warning", "Both fields must be filled.")
                    return

                data.loc[(data['Danish'] == edit_item[0]) & (data['English'] == edit_item[1]), ['Danish', 'English']] = [new_danish, new_english]
                data.to_csv('./data/data/danish_words.csv', index=False)
                messagebox.showinfo("Success", "Word updated successfully!")
                data_list = data.to_dict(orient='records')
                populate_tree(data_list)
                edit_window_inner.destroy()

            Button(edit_window_inner, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

        def delete_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Warning", "Please select a word to delete.")
                return

            delete_item = tree.item(selected_item)['values']
            result = messagebox.askyesno("Confirmation", f"Are you sure you want to delete '{delete_item[0]}'?")
            if result:
                data.drop(data[(data['Danish'] == delete_item[0]) & (data['English'] == delete_item[1])].index, inplace=True)
                data.to_csv('./data/data/danish_words.csv', index=False)
                messagebox.showinfo("Success", "Word deleted successfully!")
                data_list = data.to_dict(orient='records')
                populate_tree(data_list)

        Button(frame, text="Add New Word", command=add_new_word).pack(side=LEFT, padx=10, pady=5)
        Button(frame, text="Edit Selected", command=edit_selected).pack(side=LEFT, padx=10, pady=5)
        Button(frame, text="Delete Selected", command=delete_selected).pack(side=RIGHT, padx=10, pady=5)

    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found!")
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "The data file is empty!")

def speak():
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
        engine.say(current_card['Danish'])
        engine.runAndWait()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while trying to speak: {e}")

# User Interface
window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flash Cards')

flip_timer = window.after(5000, func=flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front_card = PhotoImage(file='./data/images/card_front.png')
back_card = PhotoImage(file='./data/images/card_back.png')
card_background = canvas.create_image(400, 263, image=front_card)
card_title = canvas.create_text(400, 150, text='Title', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='WORD', font=('Ariel', 60, 'bold'))
canvas.config(bg=BACKGROUND_COLOR)
canvas.grid(column=0, row=0, columnspan=3)

progress = ttk.Progressbar(window, orient=HORIZONTAL, length=300, mode='determinate')
progress.grid(column=0, row=4, columnspan=3, pady=20)

# Button images
ok_button = PhotoImage(file='./data/images/right.png')
false_button = PhotoImage(file='./data/images/wrong.png')
correct_button = Button(image=ok_button, highlightbackground=BACKGROUND_COLOR,
                        highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=is_known)
correct_button.grid(column=2, row=1)
wrong_button = Button(image=false_button, highlightbackground=BACKGROUND_COLOR,
                      highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=next_card)
wrong_button.grid(column=0, row=1)
send_button = Button(text='Send to mail', highlightbackground=BACKGROUND_COLOR,
                     highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=send_to_mail)
send_button.grid(column=0, row=2)

button_show = Button(text='Show data', highlightbackground=BACKGROUND_COLOR,
                     highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=show_data)
button_show.grid(column=1, row=2)

edit_button_main = Button(text='Add/Edit/Delete Words', highlightbackground=BACKGROUND_COLOR,
                          highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=add_edit_or_delete_word)
edit_button_main.grid(column=1, row=3)

speak_button = Button(text='Speaker', highlightbackground=BACKGROUND_COLOR,
                      highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid', command=speak)
speak_button.grid(column=1, row=1)

window.mainloop()