is_night_mode = False
DAY_BACKGROUND_COLOR = "#E8E8E8"
BACKGROUND_COLOR = DAY_BACKGROUND_COLOR
NIGHT_BACKGROUND_COLOR = "#1E1E1E"
DAY_TEXT_COLOR = "black"
NIGHT_TEXT_COLOR = "#E0E0E0"
TEXT_COLOR = DAY_TEXT_COLOR
current_card = {}
to_learn = {}
missed_word = []
FONT_NAME = "Courier"

def switch_color(window, canvas, card_title, card_word, buttons, current_card):
    global is_night_mode, TEXT_COLOR, BACKGROUND_COLOR
    is_night_mode = not is_night_mode

    if is_night_mode:
        BACKGROUND_COLOR = NIGHT_BACKGROUND_COLOR
        TEXT_COLOR = NIGHT_TEXT_COLOR
    else:
        BACKGROUND_COLOR = DAY_BACKGROUND_COLOR
        TEXT_COLOR = DAY_TEXT_COLOR

    # Update UI 
    window.config(bg=BACKGROUND_COLOR)
    canvas.config(bg=BACKGROUND_COLOR)
    canvas.itemconfig(card_title, fill=TEXT_COLOR)
    canvas.itemconfig(card_word, fill=TEXT_COLOR)

    # Update buttons
    for button in buttons:
        button.config(highlightbackground=BACKGROUND_COLOR)
