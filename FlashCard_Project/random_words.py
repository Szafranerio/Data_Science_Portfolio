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

def random_number_50(window):

    data_window = Toplevel(window)
    data_window.title("Random 50 words to practice")

    data = pd.read_csv('./data/data/danish_words.csv')
    data = data.sample(frac=1)[:50]

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