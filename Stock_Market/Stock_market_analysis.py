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
c