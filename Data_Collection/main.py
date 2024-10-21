import json
from tkinter import *
from tkinter import messagebox, ttk, END
import os
import re

FONT_NAME = "Courier"
branches = ['Kitchen', 'Floor', 'Cleaning', 'Stakeholder', 'Customers', 'Management']

global_branches_value = []

#Functions

def recive_data():
    global global_branches_value
    name = input_name.get().capitalize()
    surname = input_surname.get().capitalize()
    birthday = input_age.get()
    nation = input_nation.get().capitalize()
    city = input_address.get()
    cpr = input_cpr.get()
    mail = input_mail.get()
    number = input_number.get()
    
    #Validation of data
    if not re.search(r"[a-zA-Z]+", name) or not re.search(r"[a-zA-Z]+", surname):
        messagebox.showwarning(title="Warning", message="Name and Surname should only contain alphabetic characters.")
        return

    # Validate birthday
    if not re.search(r"^([0-2]?[1-9]|[12][0-9]|3[01])[-](0?[1-9]|1[0-2])[-](19[5-9]\d|20[0-1]\d|202[0-4])$", birthday):
        messagebox.showwarning(title="Warning", message="Invalid birthday! Make sure the date is between 1951 and 2024 in the format DD-MM-YYYY.")
        return

    # Validate CPR number
    if not re.search(r"^\d{6}[-.]?\d{4}$", cpr):
        messagebox.showwarning(title="Warning", message="Invalid CPR number! It should follow the format XXXXXX-XXXX or XXXXXX.XXXX.")
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
        'personal_data': {
            'name': name + " " + surname,
            'birthday': birthday,
            'nation': nation,
            'address': city,
            'cpr': cpr,
            'mail': mail,
            'number': number,
            'type': global_branches_value
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
        # Clear the input fields
        input_name.delete(0, END)
        input_surname.delete(0, END)
        input_age.delete(0, END)
        input_nation.delete(0, END)
        input_address.delete(0, END)
        input_cpr.delete(0, END)
        input_mail.delete(0, END)
        input_number.delete(0, END)
        
def selected_item():
    global global_branches_value  
    global_branches_value.clear()  
    chosen = listbox.curselection()  
    for v in chosen:
        op = listbox.get(v)
        global_branches_value.append(op)

def show_data():
    script_directory = os.path.dirname(__file__)
    data_file_path = os.path.join(script_directory, 'data', 'data.json')

    try:
        with open(data_file_path, mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data file found!")
        return
    except json.JSONDecodeError:
        messagebox.showerror(title="Error", message="Error reading data!")
        return

    
    data_window = Toplevel(window)
    data_window.title("Saved Data")
    text_area = Text(data_window, wrap='word', width=80, height=20)
    text_area.pack(padx=10, pady=10)
    text_area.insert(END, json.dumps(data, indent=4))
    text_area.config(state=DISABLED)

def send_to_mail_csv():
    pass  

#UI 

window = Tk()
window.config(width=500, height=500, padx=25, pady=25)
window.title('Data Collection')

#Inputs and buttons

Label(text='Choose type:', font=(FONT_NAME, 12)).grid(column=0, row=1, sticky='e', padx=10, pady=5)
listbox = Listbox(window, selectmode='multiple', exportselection=0, width=30, height=5)
listbox.grid(column=1, row=1, padx=10, pady=5)

for type in branches:
    listbox.insert(END, type)
    
Label(text = 'Name', font=(FONT_NAME, 12)).grid(column=0, row=2, sticky='e', padx=10, pady=5)
input_name = Entry(width=30)
input_name.grid(column=1, row=2)

Label(text = 'Surname', font=(FONT_NAME, 12)).grid(column=0, row=3, sticky='e', padx=10, pady=5)
input_surname = Entry(width=30)
input_surname.grid(column=1, row=3)

Label(text = 'Birthday (DD-MM-YYYY)', font=(FONT_NAME, 12)).grid(column=0, row=4, sticky='e', padx=10, pady=5)
input_age = Entry(width=30)
input_age.grid(column=1, row=4)
    
Label(text = 'Nationality', font=(FONT_NAME, 12)).grid(column=0, row=5, sticky='e', padx=10, pady=5)
input_nation = Entry(width=30)
input_nation.grid(column=1, row=5)
    
Label(text = 'City', font=(FONT_NAME, 12)).grid(column=0, row=6, sticky='e', padx=10, pady=5)
input_address = Entry(width=30)
input_address.grid(column=1, row=6)

Label(text = 'CPR', font=(FONT_NAME, 12)).grid(column=0, row=7, sticky='e', padx=10, pady=5)
input_cpr = Entry(width=30)
input_cpr.grid(column=1, row=7)

Label(text = 'Mail', font=(FONT_NAME, 12)).grid(column=0, row=8, sticky='e', padx=10, pady=5)
input_mail = Entry(width=30)
input_mail.grid(column=1, row=8)

Label(text = 'Phone number', font=(FONT_NAME, 12)).grid(column=0, row=9, sticky='e', padx=10, pady=5)
input_number = Entry(width=30)
input_number.grid(column=1, row=9)

#Save data
button = Button(text='Save', command=lambda:[selected_item(), recive_data()])
button.grid(column=1, row=10)

button_show = Button(text='Show data', command=show_data)
button_show.grid(column=1, row=11)

#An option for the future if there would be more data for BI analysis
button_export = Button(text='Export to CSV') 
button_export.grid(column=1, row=12)


window.mainloop()