from tkinter import *
from tkinter import messagebox, ttk, END
import json


FONT_NAME = "Courier"
analysis = ['Price', 'RSI', 'MACD', 'Bollinger Bands', 'M10&M20', 'ALL']

# Functions


def send_data():
    ticker = input_ticker.get().title()
    days = int(input_time.get())
    mail = input_mail.get()
    new_data = {
        "stock": {
            "ticker": ticker,
            "days": days,
            'mail': mail,
            

        }
    }

    if len(ticker) == 0 or days == 0 or len(mail) == 0:
        messagebox.showwarning(title="Warning", message="Check your data")
    elif len(ticker) > 8:
        messagebox.showwarning(title="Warning", message='Ticker to long')
    elif days < 1 or days > 720:
        messagebox.showwarning(
            title="Warning", message='Check your date period')
    elif "@" not in mail or "." not in mail:
        messagebox.showwarning(
            title="Warning", message='Check your mail, there is no @')
        return
    else:
        messagebox.showwarning(title="Check your mail",
                               message='Data was sent')

    try:
        data_file_path = './data/data.json'
        try:
            with open('./data/data.json', mode="r") as data_file:
                data = json.load(data_file)
        except json.JSONDecodeError:
            data = {}

        data.update(new_data)

        with open('./data/data.json', mode="w") as data_file:
            json.dump(data, data_file, indent=4)


    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {e}")
    finally:
        input_ticker.delete(0, END)
        input_time.delete(0, END)

# UI
window = Tk()
window.config(padx=25, pady=25)
window.title('Stock Market Analysis')


canvas = Canvas(width=500, height=500, highlightthickness=0)
stock_png = PhotoImage(file='./images/stock_graph.png')
canvas.create_image(250, 250, image=stock_png)
canvas.grid(column=1, row=0)

stock = Label(text='Ticker Name', font=(FONT_NAME, 12))
stock.grid(column=0, row=1)

input_ticker = Entry(width=21)
input_ticker.grid(column=1, row=1)

time = Label(text='Time period in days (max 720)', font=(FONT_NAME, 12))
time.grid(column=0, row=2)

input_time = Entry(width=21)
input_time.grid(column=1, row=2)

email = Label(text='Write your email', font=(FONT_NAME, 12))
email.grid(column=0, row=3)

input_mail = Entry(width=21)
input_mail.grid(column=1, row=3)

analysis_type = Label(text='Choose analysis type', font=(FONT_NAME, 12))
analysis_type.grid(column=0, row=4)

listbox = Listbox(window, selectmode='multiple', exportselection=0, width=21)
listbox.grid(column=1, row=4)

for value in analysis:
    listbox.insert(END, value)


def selected_item():
    for i in listbox.curselection():
        print(listbox.get(i))


button = Button(text='Send', command=send_data)
button.grid(column=2, row=4)

window.mainloop()
