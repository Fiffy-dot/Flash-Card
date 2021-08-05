import csv
from tkinter import *
import pandas
import random

card = {}

BACKGROUND_COLOR = "#B1DDC6"

# ---------------------------- CREATE NEW FLASHCARDS ------------------------------- #
data_file = pandas.read_csv("data/german_words.csv")
data = data_file.to_dict(orient="records")
print(data)


def new_random_word():
    global card, timer
    window.after_cancel(timer)
    card = random.choice(data)
    canvas.itemconfig(language_text, text="German", fill="black")
    canvas.itemconfig(word_text, text=card["German"], fill="black")
    canvas.itemconfig(canvas_image, image=card_front)
    timer = window.after(3000, func=flip_card)


# ---------------------------- FLIP THE CARDS -------------------------------------- #
def flip_card():
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=card["English"], fill="white")
    canvas.itemconfig(canvas_image, image=card_back)


# ---------------------------- SAVE YOUR PROGRESS ---------------------------------- #
def save_progress():
    global data_file
    try:
        data_file = pandas.read_csv("data/words_to_learn.csv")
    except FileNotFoundError:
        data_file = pandas.read_csv("data/german_words.csv")
    finally:
        data = data_file.to_dict(orient="records")
        data.remove(card)
        new_data = pandas.DataFrame(data)
        new_data.to_csv("data/words_to_learn.csv", index=False)
        new_random_word()


# ---------------------------- UI SETUP -------------------------------------------- #
window = Tk()
window.title("Language Easy!")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

timer = window.after(3000, func=flip_card)

# images
tick_image = PhotoImage(file="images/right.png")
x_image = PhotoImage(file="images/wrong.png")
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(row=0, column=0, columnspan=2)

right_button = Button(image=tick_image, highlightthickness=0, command=save_progress)
right_button.grid(row=1, column=0)
wrong_button = Button(image=x_image, highlightthickness=0, command=new_random_word)
wrong_button.grid(row=1, column=1)

language_text = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
canvas.grid(row=0, column=0, columnspan=2)
word_text = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

new_random_word()  # generate a german word immediately program is run

window.mainloop()
