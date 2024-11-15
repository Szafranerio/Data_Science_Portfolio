from tkinter import Tk, Button
import flashcards 
import os

BACKGROUND_COLOR = "#B1DDC6"
main_window = Tk()
main_window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
main_window.title('Main Menu')
main_window.geometry('800x526')


def open_flashcards():
    flashcards.run_flashcards()


flashcards_button = Button(
    text='Flashcards', font=('Arial', 16), padx=10, pady=5,
    highlightbackground=BACKGROUND_COLOR, highlightcolor=BACKGROUND_COLOR,
    highlightthickness=4, relief='solid', command=open_flashcards
)
flashcards_button.grid(column=0, row=1, pady=10)

dictionary = Button(text='Dictionary', highlightbackground=BACKGROUND_COLOR,
                    highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid')
dictionary.grid(column=0, row=2)

random_game = Button(text='Random Guessing Game', highlightbackground=BACKGROUND_COLOR,
                          highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid')
random_game.grid(column=0, row=3)

gramma_book = Button(text='Gramma Book', highlightbackground=BACKGROUND_COLOR,
                          highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid')
gramma_book.grid(column=0, row=4)

help = Button(text='Help', highlightbackground=BACKGROUND_COLOR,
              highlightcolor=BACKGROUND_COLOR, highlightthickness=4, relief='solid')
help.grid(column=0, row=5)


main_window.mainloop()
