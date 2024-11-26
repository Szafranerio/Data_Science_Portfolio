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


def review_words(window):
    try:
        data = pd.read_csv('./data/data/words_to_learn.csv')
        prefixes_to_exclude = ('en ', 'et ', 'at ', 'af ',
                               'i ', 'på ', 'til ', 'med ', 'om ', 'ud ')

        def remove_prefix(word):
            for prefix in prefixes_to_exclude:
                if word.startswith(prefix):
                    return word[len(prefix):]
            return word

        data['sort_key'] = data['Danish'].apply(remove_prefix)
        data = data.loc[natsorted(
            data.index, key=lambda x: data.loc[x, 'sort_key'], alg=ns.LOCALE)].reset_index(drop=True)
        data = data.drop(columns='sort_key')

        data_window = Toplevel(window)
        data_window.title("Saved Data")

        # Search bar
        search_frame = Frame(data_window)
        search_frame.pack(pady=5)
        Label(search_frame, text="Search:", font=(
            FONT_NAME, 12)).pack(side=LEFT, padx=5)
        search_entry = Entry(search_frame, width=30)
        search_entry.pack(side=LEFT, padx=5)

        # Create a Treeview widget
        tree = ttk.Treeview(data_window, columns=(
            "Danish", "English"), show='headings', height=15)
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
        messagebox.showerror(title="Locale Error",
                             message=f"Locale error: {e}")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")
