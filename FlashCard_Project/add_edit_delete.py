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


def add_edit_or_delete_word(window):
    edit_window = Toplevel(window)
    edit_window.title("Add/Edit/Delete Words")

    try:
        data = pd.read_csv('./data/data/danish_words.csv')
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
        data_list = data.to_dict(orient='records')

        # Search bar
        search_frame = Frame(edit_window)
        search_frame.pack(pady=5)
        Label(search_frame, text="Search:", font=(
            FONT_NAME, 12)).pack(side=LEFT, padx=5)
        search_entry = Entry(search_frame, width=30)
        search_entry.pack(side=LEFT, padx=5)

        # Frame for Treeview and buttons
        frame = Frame(edit_window)
        frame.pack(pady=10)

        # Create a Treeview widget
        tree = ttk.Treeview(frame, columns=(
            "Danish", "English"), show='headings', height=15)
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
            filtered_data = [row for row in data_list if search_text in row['Danish'].lower(
            ) or search_text in row['English'].lower()]
            populate_tree(filtered_data)

        search_entry.bind("<KeyRelease>", lambda event: search_word())

        def add_new_word():
            add_window = Toplevel(edit_window)
            add_window.title("Add New Word")

            Label(add_window, text="Danish:", font=(FONT_NAME, 12)).grid(
                row=0, column=0, padx=10, pady=5)
            danish_entry = Entry(add_window, width=30)
            danish_entry.grid(row=0, column=1, padx=10, pady=5)

            Label(add_window, text="English:", font=(FONT_NAME, 12)).grid(
                row=1, column=0, padx=10, pady=5)
            english_entry = Entry(add_window, width=30)
            english_entry.grid(row=1, column=1, padx=10, pady=5)

            def save_new_word():
                danish = danish_entry.get().strip()
                english = english_entry.get().strip()

                if not danish or not english:
                    messagebox.showwarning(
                        "Warning", "Both fields must be filled.")
                    return

                if (danish, english) in [(row['Danish'], row['English']) for row in data_list]:
                    messagebox.showinfo(
                        "Duplicate", "This word pair already exists!")
                    return

                with open('./data/data/danish_words.csv', 'a') as fd:
                    fd.write(f"\n{danish},{english}")
                messagebox.showinfo("Success", "Word added successfully!")
                data_list.append({'Danish': danish, 'English': english})
                populate_tree(data_list)
                add_window.destroy()

            Button(add_window, text="Save", command=save_new_word).grid(
                row=2, column=0, columnspan=2, pady=10)

        def edit_selected():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning(
                    "Warning", "Please select a word to edit.")
                return

            edit_item = tree.item(selected_item)['values']
            edit_window_inner = Toplevel(edit_window)
            edit_window_inner.title("Edit Word")

            Label(edit_window_inner, text="Danish:", font=(
                FONT_NAME, 12)).grid(row=0, column=0, padx=10, pady=5)
            danish_entry = Entry(edit_window_inner, width=30)
            danish_entry.grid(row=0, column=1, padx=10, pady=5)
            danish_entry.insert(0, edit_item[0])

            Label(edit_window_inner, text="English:", font=(
                FONT_NAME, 12)).grid(row=1, column=0, padx=10, pady=5)
            english_entry = Entry(edit_window_inner, width=30)
            english_entry.grid(row=1, column=1, padx=10, pady=5)
            english_entry.insert(0, edit_item[1])

            def save_changes():
                new_danish = danish_entry.get().strip()
                new_english = english_entry.get().strip()

                if not new_danish or not new_english:
                    messagebox.showwarning(
                        "Warning", "Both fields must be filled.")
                    return

                data.loc[(data['Danish'] == edit_item[0]) & (data['English'] == edit_item[1]), [
                    'Danish', 'English']] = [new_danish, new_english]
                data.to_csv('./data/data/danish_words.csv', index=False)
                messagebox.showinfo("Success", "Word updated successfully!")
                data_list = data.to_dict(orient='records')
                populate_tree(data_list)
                edit_window_inner.destroy()

            Button(edit_window_inner, text="Save", command=save_changes).grid(
                row=2, column=0, columnspan=2, pady=10)

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
                data.to_csv('./data/data/danish_words.csv', index=False)
                messagebox.showinfo("Success", "Word deleted successfully!")
                data_list = data.to_dict(orient='records')
                populate_tree(data_list)

        Button(frame, text="Add New Word", command=add_new_word).pack(
            side=LEFT, padx=10, pady=5)
        Button(frame, text="Edit Selected", command=edit_selected).pack(
            side=LEFT, padx=10, pady=5)
        Button(frame, text="Delete Selected", command=delete_selected).pack(
            side=RIGHT, padx=10, pady=5)

    except FileNotFoundError:
        messagebox.showerror("Error", "No data file found!")
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "The data file is empty!")
