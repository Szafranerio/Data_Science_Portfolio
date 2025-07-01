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


def show_map_window(window):
    def generate_filtered_map(country_filter=None, category_filter=None):
        script_directory = os.path.dirname(__file__)
        data_file_path = os.path.join(script_directory, 'data', 'data.json')

        try:
            with open(data_file_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load data: {e}")
            return

        m = folium.Map(location=[20, 0], zoom_start=2)

        for item in data:
            entry = item.get("data", {})
            country = entry.get("country")
            category = entry.get("category")
            coords = entry.get("coordinates")

            if not coords or ',' not in coords:
                continue

            lat, lon = map(float, coords.split(","))
            
            if country_filter and country != country_filter:
                continue
            if category_filter and category != category_filter:
                continue

            popup_info = f"{entry.get('name')}<br>{entry.get('subcategory')}<br>{entry.get('address')}<br>{entry.get('mail')}"
            folium.Marker(location=[lat, lon], popup=popup_info).add_to(m)

        map_path = os.path.join(script_directory, "footprint.html")
        m.save(map_path)
        webbrowser.open(f"file://{map_path}")

    # UI: Filter window
    filter_win = Toplevel(window)
    filter_win.title("Map Filters")
    filter_win.geometry("350x200")

    Label(filter_win, text="Country:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
    selected_country = StringVar()
    ttk.Combobox(filter_win, textvariable=selected_country, values=[''] + list_of_eu, state="readonly").grid(row=0, column=1)

    Label(filter_win, text="Category:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
    selected_category = StringVar()
    ttk.Combobox(filter_win, textvariable=selected_category, values=[''] + list(categories.keys()), state="readonly").grid(row=1, column=1)

    def on_generate():
        generate_filtered_map(
            country_filter=selected_country.get() or None,
            category_filter=selected_category.get() or None
        )
        filter_win.destroy()

    Button(filter_win, text="Generate Map", command=on_generate).grid(row=2, column=1, pady=20)