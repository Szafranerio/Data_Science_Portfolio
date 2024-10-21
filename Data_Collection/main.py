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
    nation = input_nation.get()
    address = input_address.get()
    cpr = input_cpr.get()
    mail = input_mail.get()
    number = input_number.get()
    
    try:
        number = int(number)
        birthday = int(birthday)
    except ValueError:
        messagebox.showwarning(title="Warning", message="Enter only numbers!")
        return
    
    new_data = {
        'personal_data': {
            'name': name + " " + surname,
            'birthday': birthday,
            'nation': nation,
            'address': address,
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

Label(text = 'Birthday', font=(FONT_NAME, 12)).grid(column=0, row=4, sticky='e', padx=10, pady=5)
input_age = Entry(width=30)
input_age.grid(column=1, row=4)
    
Label(text = 'Nationality', font=(FONT_NAME, 12)).grid(column=0, row=5, sticky='e', padx=10, pady=5)
input_nation = Entry(width=30)
input_nation.grid(column=1, row=5)
    
Label(text = 'Address', font=(FONT_NAME, 12)).grid(column=0, row=6, sticky='e', padx=10, pady=5)
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


window.mainloop()