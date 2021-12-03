import telebot
import os
import logging

simp_path = 'credentials/bot_token'
abs_path = os.path.abspath(simp_path)
with open(abs_path, 'r') as file:
    pass
    TOKEN = file.read().replace('\n', '')


FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='server.log', level=logging.DEBUG, format=FORMAT)


logging.info('bot start')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.reply_to(message, f"Welcome, {message.chat.username}")

bot.polling(none_stop=True)
