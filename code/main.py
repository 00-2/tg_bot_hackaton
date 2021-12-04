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

class User:
    def __init__(self, name, surname, subdivision):
        self.name = name
        self.surname = surname
        self.subdivision = subdivision

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_surname(self):
        return self.surname

    def set_surname(self, surname):
        self.surname = surname

    def get_subdivision(self):
        return self.subdivision

    def set_subdivision(self, subdivision):
        self.subdivision = subdivision

    def __str__(self):
        return f'{self.name}, {self.surname}, {self.subdivision}'


@bot.message_handler(commands=['start', 'help'])   #
def start(message: telebot.types.Message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Напишите ваше имя:")
        bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name


def get_name(message):   # получаем фамилию и имя
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Напишите вашу Фамилию:')
    bot.register_next_step_handler(message, get_surname)
    bot.register_next_step_handler(message, get_unit)


def get_surname(message):
    global surname
    surname = message.text


def get_unit(message: types.Message):   # кнопки выбора подразделения
    markup_inline = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Подразделение 1', callback_data=1)
    button_2 = types.InlineKeyboardButton(text='Подразделение 2', callback_data=2)
    button_3 = types.InlineKeyboardButton(text='Подразделение 3', callback_data=3)
    markup_inline.add(button_1)
    markup_inline.add(button_2)
    markup_inline.add(button_3)
    bot.send_message(message.from_user.id, f"Имя, {name}, фамилия {surname}")   # тест, в дальнейшем удалить!!!
    bot.send_message(message.chat.id, 'Выберите подразделение в котором работаете:', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)   # получаем значение нажатой кнопки. call.data - это callback_data
def callback_worker(call):
    t = call.data
    msg = t
    bot.send_message(call.message.chat.id, f'{t}')      # тест, в дальнейшем удалить!!!
    bot.register_next_step_handler(call, test_before_lesson)


def test_before_lesson(message: types.Message):   # приветствие перед вводным тестом
    bot.send_message(message.from_user.id, f'Здравствуйте, {name} {surname}')
    bot.send_message(message.from_user.id, f'Предлагаем вам пройти тест, если готовы нажмите "Далее". ')
    bot.send_message(message.from_user.id, f'Если нет, нажмите "Выход".')
    markup_inline = types.InlineKeyboardMarkup()
    markup_inline.add(types.InlineKeyboardButton(text='Далее', callback_data=True))
    markup_inline.add(types.InlineKeyboardButton(text='Выход', callback_data=False))


@bot.callback_query_handler(func=lambda call: True)   # получаем значение нажатой кнопки. call.data - это callback_data
def callback_worker(call):
    button_value = call.data
    bot.send_message(call.message.chat.id, f'{button_value}')   # тест, в дальнейшем удалить!!!
    if button_value:
        bot.register_next_step_handler(get_name)
    else:
        bot.register_next_step_handler(get_surname)


bot.polling(none_stop=True)

