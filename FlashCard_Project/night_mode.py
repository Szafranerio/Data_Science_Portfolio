def switch_color():
    global is_night_mode, BACKGROUND_COLOR, TEXT_COLOR
    is_night_mode = not is_night_mode

    if is_night_mode:
        BACKGROUND_COLOR = NIGHT_BACKGROUND_COLOR
        TEXT_COLOR = NIGHT_TEXT_COLOR
    else:
        BACKGROUND_COLOR = DAY_BACKGROUND_COLOR
        TEXT_COLOR = DAY_TEXT_COLOR

    # Debug: Print the mode switch
    print(f"switch_color: BACKGROUND_COLOR={BACKGROUND_COLOR}, TEXT_COLOR={TEXT_COLOR}")

    # Update window and canvas colors
    window.config(bg=BACKGROUND_COLOR)
    canvas.config(bg=BACKGROUND_COLOR)
    canvas.itemconfig(card_title, fill=TEXT_COLOR)
    canvas.itemconfig(card_word, fill=TEXT_COLOR)

    # Update button background colors
    buttons = [
        wrong_button, speak_button, correct_button, button_show,
        edit_button_main, random_button, button_number,
        send_button, review_button, night_mode_button
    ]
    for button in buttons:
        button.config(highlightbackground=BACKGROUND_COLOR)