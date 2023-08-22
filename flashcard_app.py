from tkinter import *
import pandas as pd
import random

# constants
BACKGROUND_COLOR = "#B1DDC6"
FONT_ONE = ("Arial", 40, "italic")
FONT_TWO = ("Arial", 60, "bold")
current_card = {}

# read from csv file
try:
    df = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    orig_file = pd.read_csv("./data/french_words.csv")
    to_learn = orig_file.to_dict(orient="records")
else:
    to_learn = df.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    flash_card.itemconfig(card_title, text="French Word", fill="black")
    flash_card.itemconfig(card_word, text=current_card["French"], fill="black")
    flash_card.itemconfig(card_img, image=front_image)
    flip_timer = window.after(3000, flip_card)


def flip_card():
    flash_card.itemconfig(card_img, image=back_image)
    flash_card.itemconfig(card_title, text="English Word", fill="white")
    flash_card.itemconfig(card_word, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    # create new file with the words to learn
    data_to_learn = pd.DataFrame(to_learn)
    data_to_learn.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


# Setup GUI
window = Tk()
window.title("FlashCard Generator")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

# create flashcard canvas
flash_card = Canvas(width=800, height=526, )
flash_card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="./images/card_front.png")
back_image = PhotoImage(file="./images/card_back.png")
card_img = flash_card.create_image(400, 263, image=front_image)
card_title = flash_card.create_text(400, 150, text="", font=FONT_ONE)
card_word = flash_card.create_text(400, 263, text="", font=FONT_TWO)
flash_card.grid(row=0, column=0, columnspan=2)

# create buttons
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, command=is_known, highlightthickness=0)
right_button.grid(row=1, column=0)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, command=next_card, highlightthickness=0)
wrong_button.grid(row=1, column=1)

# call the next card function each time the program run
next_card()
window.mainloop()
