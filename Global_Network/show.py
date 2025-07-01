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
import folium
import webbrowser
import map

FONT_NAME = "Courier"
list_of_eu = [
    'Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan',
    'Belarus', 'Belgium', 'Bosnia and Herzegovina', 'Bulgaria',
    'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia',
    'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary',
    'Iceland', 'Ireland', 'Italy', 'Kazakhstan', 'Kosovo', 'Latvia',
    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova',
    'Monaco', 'Montenegro', 'Netherlands', 'North Macedonia',
    'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'San Marino',
    'Serbia', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'Switzerland',
    'Turkey', 'Ukraine', 'United Kingdom', 'Vatican City'
]
categories = {
    'Education': ['Universities', 'Colleges', 'High Schools', 'Language Schools', 'Training Centers'],
    'Healthcare': ['Hospitals', 'Clinics', 'Pharmacies', 'Dental Offices', 'Veterinarians'],
    'Retail': ['Supermarkets', 'Shopping Malls', 'Clothing Stores', 'Electronics Stores', 'Bookstores'],
    'Food': ['Restaurants', 'Cafés', 'Bakeries', 'Fast Food'],
    'Hospitality': ['Hotels', 'Hostels', 'Bed and Breakfasts'],
    'Culture': ['Museums', 'Cinemas', 'Theaters', 'Libraries'],
    'Transport': ['Airports', 'Train Stations', 'Metro Stops', 'Bus Terminals']
}

def show_data(window):
    def on_filter_apply(window):
        country = selected_country.get()
        category = selected_category.get()

        try:
            with open(os.path.join(os.path.dirname(__file__), 'data', 'data.json')) as f:
                all_data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading data: {e}")
            return

        results = []
        for item in all_data:
            d = item.get("data", {})
            if country and d.get("country") != country:
                continue
            if category and d.get("category") != category:
                continue
            results.append(d)

        if not results:
            messagebox.showinfo("Info", "No matching records found.")
            return

        # Show formatted results
        result_win = Toplevel(window)
        result_win.title("Filtered Results")

        scrollbar = Scrollbar(result_win)
        scrollbar.pack(side=RIGHT, fill=Y)

        output = Text(result_win, wrap='word', width=80, height=25, yscrollcommand=scrollbar.set)
        output.pack(padx=10, pady=10)
        scrollbar.config(command=output.yview)

        for d in results:
            entry = (
                f"Name: {d.get('name', '')}\n"
                f"Category: {d.get('category', '')}\n"
                f"Subcategory: {d.get('subcategory', '')}\n"
                f"Country: {d.get('country', '')}\n"
                f"Address: {d.get('address', '')}\n"
                f"Phone: {d.get('number', '')}\n"
                f"Mail: {d.get('mail', '')}\n"
                f"Coordinates: {d.get('coordinates', '')}\n"
                f"{'-'*50}\n"
            )
            output.insert(END, entry)

        output.config(state=DISABLED)

    # Filter window
    filter_win = Toplevel(window)
    filter_win.title("Filter Data")
    filter_win.geometry("350x180")

    Label(filter_win, text="Country:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    selected_country = StringVar()
    ttk.Combobox(filter_win, textvariable=selected_country, values=[''] + list_of_eu, state="readonly", width=30).grid(row=0, column=1)

    Label(filter_win, text="Category:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    selected_category = StringVar()
    ttk.Combobox(filter_win, textvariable=selected_category, values=[''] + list(categories.keys()), state="readonly", width=30).grid(row=1, column=1)

    Button(filter_win, text="Show Data", command=lambda: on_filter_apply(window)).grid(row=2, column=1, pady=20)