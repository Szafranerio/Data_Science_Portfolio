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
import show
import validation
from validation import selected_subcategory, updated_subcategories

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

global_list_of_eu = []
global_branches_value = []
load_dotenv()

#Functions
def recive_data(window):
    validation.recive_data(window)
    
def show_data(window):
    show.show_data(window)

def show_map_window(window):
    map.show_map_window(window)   

#UI 
window = Tk()
window.config(width=500, height=500, padx=25, pady=25)
window.title('Data Collection')       
       
form_frame = Frame(window)
form_frame.grid(row=0, column=0, columnspan=3, pady=10)

Label(form_frame, text='Choose country:', font=(FONT_NAME, 12)).grid(column=0, row=0, sticky='e', padx=10, pady=5)
country_var = StringVar()
country_dropdown = ttk.Combobox(form_frame, textvariable=country_var, values=list_of_eu, state="readonly", width=27)
country_dropdown.grid(column=1, row=0, padx=10, pady=5)

Label(form_frame, text="Select Category").grid(row=1, column=0, padx=10, pady=10, sticky='e')
category_var = StringVar()
category_dropdown = ttk.Combobox(form_frame, textvariable=category_var, values=list(categories.keys()), state="readonly", width=30)
category_dropdown.grid(row=1, column=1, padx=10, pady=10)
category_dropdown.bind("<<ComboboxSelected>>", updated_subcategories)

Label(form_frame, text="Select Subcategory").grid(row=2, column=0, padx=10, pady=10, sticky='e')
subcategory_var = StringVar()
subcategory_dropdown = ttk.Combobox(form_frame, textvariable=subcategory_var, state="readonly", width=30)
subcategory_dropdown.grid(row=2, column=1, padx=10, pady=10)
    
Label(form_frame, text = 'Name', font=(FONT_NAME, 12)).grid(column=0, row=3, sticky='e', padx=10, pady=5)
input_name = Entry(form_frame, width=30)
input_name.grid(column=1, row=3)
    
Label(form_frame, text = 'City', font=(FONT_NAME, 12)).grid(column=0, row=4, sticky='e', padx=10, pady=5)
input_city = Entry(form_frame, width=30)
input_city.grid(column=1, row=4)

Label(form_frame, text = 'Address', font=(FONT_NAME, 12)).grid(column=0, row=5, sticky='e', padx=10, pady=5)
input_address = Entry(form_frame, width=30)
input_address.grid(column=1, row=5)

Label(form_frame, text = 'Postal', font=(FONT_NAME, 12)).grid(column=0, row=6, sticky='e', padx=10, pady=5)
input_postal = Entry(form_frame, width=30)
input_postal.grid(column=1, row=6)

Label(form_frame, text = 'Company registration', font=(FONT_NAME, 12)).grid(column=0, row=7, sticky='e', padx=10, pady=5)
input_cvr = Entry(form_frame, width=30)
input_cvr.grid(column=1, row=7)

Label(form_frame,text = 'Mail', font=(FONT_NAME, 12)).grid(column=0, row=8, sticky='e', padx=10, pady=5)
input_mail = Entry(form_frame, width=30)
input_mail.grid(column=1, row=8)

Label(form_frame, text = 'Phone number', font=(FONT_NAME, 12)).grid(column=0, row=9, sticky='e', padx=10, pady=5)
input_number = Entry(form_frame, width=30)
input_number.grid(column=1, row=9)

Label(form_frame, text = 'Latitude', font=(FONT_NAME, 12)).grid(column=0, row=10, sticky='e', padx=10, pady=5)
input_latitude = Entry(form_frame, width=30)
input_latitude.grid(column=1, row=10)

Label(form_frame, text = 'Longitude', font=(FONT_NAME, 12)).grid(column=0, row=11, sticky='e', padx=10, pady=5)
input_longitude = Entry(form_frame, width=30)
input_longitude.grid(column=1, row=11)

button_frame = Frame(window)
button_frame.grid(row=12, column=1, pady=10)

button = Button(form_frame, text='Save', command=lambda: [selected_subcategory(), recive_data()])
button.grid(column=1, row=12)

button_show = Button(form_frame, text='Show data', command=lambda: show_data(window))
button_show.grid(column=1, row=13)

button_map = Button(form_frame, text='Show Map', command=lambda: show_map_window(window))

button_map.grid(column=1, row=14)

window.mainloop()