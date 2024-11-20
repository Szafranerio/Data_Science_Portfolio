from tkinter import *
import pandas as pd
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

def numbers_practice(window):
    try:
        number_data = pd.read_csv('./data/data/danish_numbers.csv')
        data_window = Toplevel(window)
        data_window.title("Number Data")

        search_frame = Frame(data_window)
        search_frame.pack(pady=5)
        Label(search_frame, text="Search:", font=(
            FONT_NAME, 12)).pack(side=LEFT, padx=5)
        search_entry = Entry(search_frame, width=30)
        search_entry.pack(side=LEFT, padx=5)

        # Create a Treeview widget
        tree = ttk.Treeview(data_window, columns=(
            "Number", "Danish"), show='headings', height=15)
        tree.heading("Number", text="Number")
        tree.heading("Danish", text="Danish")
        tree.pack(padx=10, pady=10)

        def populate_tree(data_subset):
            for item in tree.get_children():
                tree.delete(item)
            for _, row in data_subset.iterrows():
                tree.insert('', END, values=(row['Number'], row['Danish']))
        populate_tree(number_data)

    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found!")
    except pd.errors.EmptyDataError:
        messagebox.showerror(title="Error", message="The data file is empty!")
    except locale.Error as e:
        messagebox.showerror(title="Locale Error",
                             message=f"Locale error: {e}")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")