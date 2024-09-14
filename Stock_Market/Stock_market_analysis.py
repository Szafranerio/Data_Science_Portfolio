from tkinter import *
from tkinter import messagebox

FONT_NAME = "Courier"
ANALYSIS = ['Price', 'RSI', 'MACD', 'Bollinger Bands', 'M10&M20', 'ALL']

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
input_time.grid(column = 1, row=2)

email = Label(text='Write your email', font=(FONT_NAME, 12))
email.grid(column=0, row=3)

input_mail = Entry(width=21)
input_mail.grid(column=1, row=3)

analysis_type = Label(text='Choose analysis type', font=(FONT_NAME, 12))
analysis_type.grid(column=0, row=4)









window.mainloop()
