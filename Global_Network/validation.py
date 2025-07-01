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

def recive_data(window, input_name, input_city, input_address, input_postal, input_cvr, input_mail, input_number, input_latitude, input_longitude):
    
    name = input_name.get().capitalize()
    city = input_city.get()
    address = input_address.get()
    postal = input_postal.get()
    cvr = input_cvr.get()
    mail = input_mail.get()
    number = input_number.get()
    latitude = input_latitude.get()
    longitude = input_longitude.get()

    #Validation of data
    if not re.search(r"[a-zA-Z]+", name):
        messagebox.showwarning(title="Warning", message="Name should only contain alphabetic characters.")
        return

    # Validate CVR number
    if not re.search(r"^\d{8}$", cvr):
        messagebox.showwarning(title="Warning", message="Invalid CVR number! It should follow the format XXXXXXXX")
        return

    # Validate email
    if not re.search(r"^\w+@\w+\.\w+$", mail):
        messagebox.showwarning(title="Warning", message="Invalid email address!")
        return

    # Validate phone number
    if not re.search(r"^[1-9]\d{7}$", number):
        messagebox.showwarning(title="Warning", message="Invalid phone number! It should be 8 digits starting with a number between 1 and 9.")
        return

    new_data = {
        'data': {
            'country': country_var.get(),
            'category': category_var.get(),
            'subcategory': subcategory_var.get(),
            'name': name,
            'address': address + ' ' + city + ' ' + postal,
            'cvr': cvr,
            'mail': mail,
            'number': number,
            'coordinates': latitude + ', ' + longitude
        }
    }
    
    try:
        script_directory = os.path.dirname(__file__)
        data_folder_path = os.path.join(script_directory, 'data')
        
        if not os.path.exists(data_folder_path):
            os.makedirs(data_folder_path)

        data_file_path = os.path.join(data_folder_path, 'data.json')
        
        if os.path.exists(data_file_path):
            try:
                with open(data_file_path, mode="r") as data_file:
                    try:
                        data = json.load(data_file)
                    except json.JSONDecodeError:
                        data = []
            except Exception as e:
                messagebox.showerror("Error", f"Could not read data file: {e}")
                return
        else:
            data = []

        data.append(new_data)

        with open(data_file_path, mode="w") as data_file:
            json.dump(data, data_file, indent=4)

        messagebox.showinfo(title="Success", message="Data saved successfully!")

    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")

    finally:
        input_name.delete(0, END)
        input_city.delete(0, END)
        input_address.delete(0, END)
        input_postal.delete(0, END) 
        input_cvr.delete(0, END)
        input_mail.delete(0, END)
        input_number.delete(0, END)
        input_latitude.delete(0, END)
        input_longitude.delete(0, END)

def selected_subcategory(window):
    global global_branches_value
    global_branches_value.clear()
    sub = subcategory_var.get()
    if sub:
        global_branches_value.append(sub) 
        
def updated_subcategories(window, event):
       selected_category = category_var.get()
       sub_items = categories.get(selected_category, [])
       subcategory_dropdown['values'] = sub_items
       subcategory_var.set('')
       
