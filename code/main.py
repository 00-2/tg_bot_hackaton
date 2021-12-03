import telebot
import os
import logging
from telebot import types

simp_path = 'credentials/bot_token'
abs_path = os.path.abspath(simp_path)
with open(abs_path, 'r') as file:
    pass
    TOKEN = file.read().replace('\n', '')


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='server.log', level=logging.DEBUG, format=FORMAT)


logging.info('bot start')
bot = telebot.TeleBot(TOKEN)

name = ''
surname = ''


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Напишите ваше имя:")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


# @bot.message_handler(content_types=['text'])
def get_name(message): #получаем фамилию и имя
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Напишите вашу Фамилию:')
    bot.register_next_step_handler(message, get_surname)
    bot.register_next_step_handler(message, get_unit)


def get_surname(message):
    global surname
    surname = message.text


def get_unit(message: types.Message):
# def get_unit(message):

    markup_inline = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Подразделение 1', callback_data=1)
    button_2 = types.InlineKeyboardButton(text='Подразделение 2', callback_data=2)
    button_3 = types.InlineKeyboardButton(text='Подразделение 3', callback_data=3)
    markup_inline.add(button_1)
    markup_inline.add(button_2)
    markup_inline.add(button_3)
    bot.send_message(message.from_user.id, f"Имя, {name}, фамилия {surname}")   # тест
    bot.send_message(message.chat.id, 'Выберите подразделение в котором работаете:', reply_markup=markup_inline)



bot.polling(none_stop=True)
