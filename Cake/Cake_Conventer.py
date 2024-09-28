from tkinter import *
from tkinter import messagebox
import json
import pandas as pd
import numpy as np
import os

FONT = ('Comic Sans MS', 15, 'bold')
data = []

# Delete all data from data.json before using the program
def initialize_data_file():
    data_file_path = './data/data.json'

    if not os.path.exists('./data'):
        print("Creating data directory...")
        os.makedirs('./data')

    with open(data_file_path, mode="w") as data_file:
        json.dump([], data_file)


initialize_data_file()


def show_help():
    messagebox.showinfo(
        'Help', 'Enter the orginial recipe and press add. Press calculate and program will calculate how much products you need! Press Clear data to delete whole data from program.')


# Add data and calculate
def add():
    recipe_amount = input_recipe.get()
    weight = input_weight.get()
    name = input_product_name.get()
    aimed_amount = input_aimed.get()

    # Validation
    try:
        weight = float(weight)
    except ValueError:
        messagebox.showwarning(
            title="Warning", message="Weight must be a number!")
        return

    if not name:
        messagebox.showwarning(
            title="Warning", message="Product name cannot be empty!")
        return

    try:
        aimed_amount = int(aimed_amount)
    except ValueError:
        messagebox.showwarning(
            title="Warning", message="Aimed portion must be a number!")
        return

    new_data = {
        "name": name,
        "weight": weight,
        "aimed": aimed_amount,
        "recipe": recipe_amount
    }

    try:
        data_file_path = './data/data.json'

        # Ensure the directory exists
        if not os.path.exists('./data'):
            print("Creating data directory...")
            os.makedirs('./data')

        if os.path.exists(data_file_path):
            try:
                with open(data_file_path, mode="r") as data_file:
                    try:
                        data = json.load(data_file)
                        print(f"Existing data: {data}")
                    except json.JSONDecodeError:
                        data = []
            except Exception as e:
                messagebox.showerror("Error", f"Could not read data file: {e}")
                return
        else:
            data = []

        # Add to data.json
        data.append(new_data)
        print(f"Appending new data: {new_data}")

        # Write the updated data back to the file
        with open(data_file_path, mode="w") as data_file:
            json.dump(data, data_file, indent=4)
            print("Data saved successfully!")

        messagebox.showinfo(
            title="Success", message="Data saved successfully!")

    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")

    finally:
        input_weight.delete(0, END)
        input_product_name.delete(0, END)


def calculate():
    data = pd.read_json('./data/data.json')
    data = pd.DataFrame(data)

    proportion_data = data['aimed']
    original_recipe = data['recipe']
    data.drop(['aimed', 'recipe'], axis=1, inplace=True)
    data_for_proportion = pd.Series(proportion_data).iloc[-1]
    original_data = pd.Series(original_recipe).iloc[-1]

    data['per_one_portion'] = pd.DataFrame(data.weight / original_data)
    data['final_proportions'] = pd.DataFrame(
        data.per_one_portion) * data_for_proportion
    data['final_proportions'] = data['final_proportions'].apply(
        lambda x: round(x, 2))
    messages = []

    for index, row in data.iterrows():
        message = f"For {data_for_proportion} portions, you need: \n {row['final_proportions']} of {row['name'].lower()}"
        messages.append(message)

    messagebox.showinfo(f'Final data', '\n'.join(messages))


def clear():
    data_file_path = './data/data.json'
    with open(data_file_path, mode="w") as data_file:
        data_file.truncate()
    input_recipe.delete(0, END)
    input_aimed.delete(0, END)
    input_weight.delete(0, END)
    input_product_name.delete(0, END)


# UI
window = Tk()
window.config(padx=25, pady=25, bg="#ffccdd")
window.geometry('700x300')
window.title('Cake Converter')

# Label, Buttons
Label(window, text="Pick amount from recepie: ",
      bg="#ffccdd", font=FONT).grid(column=0, row=1)
input_recipe = Entry(window)
input_recipe.config(highlightbackground="#ffccdd", highlightthickness=2)
input_recipe.grid(column=1, row=1)

Label(window, text="Pick amount and weight: ",
      bg="#ffccdd", font=FONT).grid(column=0, row=2)
input_weight = Entry(window)
input_weight.config(highlightbackground="#ffccdd", highlightthickness=2)
input_weight.grid(column=1, row=2)

Label(window, text='What kind of product: ',
      bg="#ffccdd", font=FONT).grid(column=0, row=3)
input_product_name = Entry(window)
input_product_name.config(highlightbackground="#ffccdd", highlightthickness=2)
input_product_name.grid(column=1, row=3)

Label(window, text='For how many portions do you need?',
      bg="#ffccdd", font=FONT).grid(column=0, row=5)
input_aimed = Entry(window)
input_aimed.config(highlightbackground="#ffccdd", highlightthickness=2)
input_aimed.grid(column=1, row=5)

Button(window, text='Help?', command=show_help, highlightbackground="#ffccdd",
       highlightcolor="#ffccdd", highlightthickness=4, relief='solid').grid(column=0, row=6)
Button(window, text='Clear data', command=clear, highlightbackground="#ffccdd",
       highlightcolor="#ffccdd", highlightthickness=4, relief='solid').grid(column=1, row=6)
Button(window, text='Add', command=add, highlightbackground="#ffccdd",
       highlightcolor="#ffccdd", highlightthickness=4, relief='solid').grid(column=2, row=5)
Button(window, text='Calculate', command=calculate, highlightbackground="#ffccdd",
       highlightcolor="#ffccdd", highlightthickness=4, relief='solid').grid(column=2, row=6)

window.mainloop()
