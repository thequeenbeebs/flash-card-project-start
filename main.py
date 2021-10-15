from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
new_word = {}
word_dictionary = {}

try:
    content = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    content = pandas.read_csv('data/french_words.csv')
finally:
    word_dictionary = content.to_dict(orient="records")


# ------------------------------------------CREATE FLASH CARDS ----------------------------------- #


def generate_flashcard():
    global new_word, flip_timer
    window.after_cancel(flip_timer)
    new_word = random.choice(word_dictionary)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=new_word['French'], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(language_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=new_word['English'], fill="white")

# -------------------------------------------- REMOVE WORD ------------------------------------------------ #


def remove_word():
    word_dictionary.remove(new_word)
    data_frame = pandas.DataFrame(word_dictionary)
    data_frame.to_csv('data/words_to_learn.csv', index=False)
    generate_flashcard()

# -------------------------------------------- UI ------------------------------------------------ #


window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file='./images/card_front.png')
card_back = PhotoImage(file='./images/card_back.png')
card = canvas.create_image(400, 263, image=card_front)
language_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

wrong = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong, highlightthickness=0, command=generate_flashcard)
wrong_button.grid(column=0, row=1)

right = PhotoImage(file="./images/right.png")
right_button = Button(image=right, highlightthickness=0, command=remove_word)
right_button.grid(column=1, row=1)

generate_flashcard()

# window.after_cancel(window)

window.mainloop()


