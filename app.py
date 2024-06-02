import os

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from salvia import query_engine


BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

def create_buttons():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Clar! 👍", callback_data="1"),
               InlineKeyboardButton("N-ai ajutat 👎", callback_data="2"))
    return markup


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Hi, my name is SalvIA and I'm here to help you with agroecological questions")


@bot.message_handler(commands=['salut', 'buna ziua'])
def send_welcome(message):
    print(message)
    bot.reply_to(message, "Salut, mă numesc SalvIA. Pot să te consult cu privire la problemele agroecologice.")


@bot.message_handler(commands=['привет', 'здравствуйте'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я SalvIA. Можешь спросить меня любой интересующий вопрос по агроэкологии")


@bot.message_handler(func=lambda msg: True)
def response(message):
    streaming_response = query_engine.query(message.text)
    for text in streaming_response.response_gen:
        try:
            bot.reply_to(message, text)
        except telebot.apihelper.ApiTelegramException:
            pass
            #bot.reply_to(message, ".")
    bot.send_message(message.chat.id, "Daca v-am ajutat, va rog estimati raspunsul meu:", reply_markup=create_buttons())
   # response.print_response()
    


if __name__ == "__main__":
    bot.infinity_polling()
