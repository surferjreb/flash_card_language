from tkinter import Tk
from tkinter import Button
from tkinter import Canvas
from tkinter import PhotoImage
from tkinter import messagebox
from random import choice
import pandas


BG2 = "#B1DDC6"
FONT = "Arial"
FILE = "data/Spanish_Frequency_1000.csv"
BUTTON_FONT = ('Arial', 25, 'bold')

"""1.) Read in csv data.
   2.) Display csv data for card.
   3.) Flip Card to see answer.
   4.) Display next card.
"""


def read_csv():
    try:
        data = pandas.read_csv(FILE)
        return data
    except FileNotFoundError:
        messagebox.showinfo(title="Error",
                            message="Check file path and try again...")


def update_card(card_data, current_lang, current_card):
    new_card = choice(card_data[current_lang])

    if new_card == current_card:
        update_card()
    else:
        return new_card


def see_card_answer(card_data, current_lang, current_card, answer_lang):

    current_card_index = pandas.Index(
                                      card_data[current_lang]
                                      ).get_loc(current_card)

    card_answer = (answer_lang, card_data[answer_lang][current_card_index])

    return card_answer


def main():
    card_data = read_csv()
    data_index = card_data.keys()
    lang_type = data_index[0]
    word = "word"

    # Window
    window = Tk()
    window.config(padx=50, pady=50, bg=BG2)
    window.title("Flash Spanish")

    # Images
    card_back = PhotoImage(file="images/card_back.png")
    card_front = PhotoImage(file="images/card_front.png")

    # Canvas
    canvas = Canvas(width=800, height=526, highlightthickness=0)
    card = canvas.create_image(410, 267, image=card_front)
    canvas.config(bg=BG2, highlightthickness=0)

    # Language type
    card_lang = canvas.create_text(400, 150, text=lang_type,
                                   font=(FONT, 40, "italic"))
    # Language word
    card_word = canvas.create_text(400, 263, text=word,
                                   font=(FONT, 60, "bold"))

    def quit_program():
        window.destroy()

    def show_card():
        current_card = canvas.itemcget(card_word, 'text')
        current_lang = canvas.itemcget(card_lang, 'text')

        if current_lang == data_index[1]:
            answer_lang = data_index[0]
        else:
            answer_lang = data_index[1]

        new_values = see_card_answer(card_data, current_lang,
                                     current_card, answer_lang)

        canvas.itemconfigure(card, image=card_back)
        canvas.itemconfigure(card_lang, text=new_values[0])
        canvas.itemconfigure(card_word, text=new_values[1])

    def new_card():
        current_card = canvas.itemcget(card_word, 'text')

        new_card = update_card(card_data, lang_type, current_card)
        canvas.itemconfigure(card, image=card_front)
        canvas.itemconfigure(card_lang, text=lang_type)
        canvas.itemconfigure(card_word, text=new_card)

    def start_new_game():
        new_card = choice(card_data[lang_type])

        return (lang_type, new_card)

    canvas.itemconfigure(card_lang, text=data_index[0])
    canvas.itemconfigure(card_word, text=choice(card_data[data_index[0]]))

    next_button = Button(text="Next", highlightthickness=0, bg='green',
                         font=BUTTON_FONT, command=new_card)
    flip_button = Button(text="Flip", highlightthickness=0, bg='blue',
                         font=BUTTON_FONT, command=show_card)
    quit_button = Button(text="Quit", font=BUTTON_FONT, bg='red',
                         command=quit_program)

    canvas.grid(column=0, row=0, columnspan=3)
    flip_button.grid(column=0, row=1)
    quit_button.grid(column=1, row=1)
    next_button.grid(column=2, row=1)

    window.mainloop()


if __name__ == '__main__':
    main()
