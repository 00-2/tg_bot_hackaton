import telebot
from telebot import types

import os
import json
import logging

import mysql.connector

#import our classes
from User import User
import Module
import Question

# GET TG TOKEN
simp_path = 'credentials/bot_token'
abs_path = os.path.abspath(simp_path)
with open(abs_path, 'r') as file:
    TOKEN = file.read().replace('\n', '')

# GET DB credentials
simp_path = 'credentials/db.json'
abs_path = os.path.abspath(simp_path)
with open(abs_path, 'r') as file:
    db_credentials = json.load(file)

mydb = mysql.connector.connect(
  host=db_credentials["host"],
  user=db_credentials["user"],
  password=db_credentials["password"],
  database=db_credentials["database"]
)
mycursor = mydb.cursor()

# logging format
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='server.log', format=FORMAT)
logging.info('bot start')

FINAL = 999

bot = telebot.TeleBot(TOKEN)

set_of_users = {}
passwords = ['P1ssword!']


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Вы перенаправлены на страницу входа:")
        # Получение данных пользователя
        auth(message)


def auth(message):
    message=bot.send_message(message.from_user.id, 'Введите Пароль:')
    bot.register_next_step_handler(message, get_reg_info)



def get_reg_info(message):
    tg_id = message.from_user.id
    password = message.text

    if password in passwords:
        bot.send_message(message.from_user.id, 'Доступ разрешен')
        logging.info(f'/start:{tg_id}')
        temp_user = User
        temp_user.set_id(temp_user,tg_id)
        message=bot.send_message(message.from_user.id, 'Введите Ваше имя:')
        bot.register_next_step_handler(message, process_name_step, temp_user)
    else:
        bot.send_message(message.from_user.id, 'Доступ запрещен. Пароль неверный')
        message.text = '/start'
        start(message)


def process_name_step(message, temp_user):
    try:
        name = message.text
        print(name)
        temp_user.set_name(temp_user,name)
        logging.info(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)}')
        print(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)}')
        bot.send_message(message.from_user.id, 'Введите Вашу фамилию:')
        bot.register_next_step_handler(message, process_surname_step, temp_user)
    except Exception as e:
        logging.warning(str(e)+f':{temp_user.get_id(temp_user)}')
        bot.reply_to(message, 'Произошла ошибка. Введите команду /start ещё раз')

def process_surname_step(message,temp_user):
    try:
        surname = message.text
        print(surname)
        temp_user.set_surname(temp_user,surname)
        logging.info(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)}, {temp_user.get_surname(temp_user)}')
        print(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)},{temp_user.get_surname(temp_user)}')
        bot.send_message(message.from_user.id, 'Введите Ваше отчество:')
        bot.register_next_step_handler(message,process_last_name_step, temp_user)
    except Exception as e:
        logging.warning(str(e)+f':{temp_user.get_id(temp_user)}')
        bot.reply_to(message, 'Произошла ошибка. Введите команду /start ещё раз')

def process_last_name_step(message,temp_user):
    try:
        last_name = message.text
        print(last_name)
        temp_user.set_last_name(temp_user,last_name)
        logging.info(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)},{temp_user.get_surname(temp_user)},{temp_user.get_last_name(temp_user)}')
        print(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)},{temp_user.get_surname(temp_user)},{temp_user.get_last_name(temp_user)}')
        bot.send_message(message.from_user.id, 'Введите Вашу почту:')
        bot.register_next_step_handler(message,process_mail, temp_user)
    except Exception as e:
        logging.warning(str(e)+f':{temp_user.get_id(temp_user)}')
        bot.reply_to(message, 'oooops')

def process_mail(message, temp_user):
    try:
        mail = message.text
        print(mail)
        temp_user.set_mail(temp_user,mail)
        logging.info(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)},{temp_user.get_surname(temp_user)},{temp_user.get_last_name(temp_user)}')
        print(f'/start name_step:{temp_user.get_id(temp_user)},{temp_user.get_name(temp_user)},{temp_user.get_surname(temp_user)},{temp_user.get_last_name(temp_user)}')
        confirm(message, temp_user,1)
    except Exception as e:
        logging.warning(str(e)+f':{temp_user.get_id(temp_user)}')
        bot.reply_to(message, 'oooops')

def confirm(message,temp_user,step):
    global set_of_users
    if step==1:
        set_of_users[message.from_user.id] = temp_user
        markup_inline = types.InlineKeyboardMarkup()
        yes = types.InlineKeyboardButton(text='Всё верно', callback_data=1)
        no = types.InlineKeyboardButton(text='Исправить данные', callback_data=2)
        markup_inline.add(yes)
        markup_inline.add(no)
        bot.send_message(message.chat.id, 'Подтвердите данные', reply_markup=markup_inline)
        


@bot.callback_query_handler(func=lambda call: True)   # получаем значение нажатой кнопки. call.data - это callback_data
def callback_worker(call):
    global set_of_users
    button_value = call.data        
    if button_value=='2':
        bot.send_message(call.message.chat.id, f'Введите ок для подтверждения')
        bot.register_next_step_handler(call.message,get_reg_info)
    elif button_value == '1':
        bot.send_message(call.message.chat.id, 'Сохранение данных. Ожидайте')
        temp_user = set_of_users[call.message.chat.id]
        print(f"to db:{call.message.chat.id}")
        logging.info(f"to db:{call.message.chat.id}")
        # Запись в базу юзеров
        try:
            mycursor.execute(
            f"""
                INSERT INTO users_data(first_name, last_name, surname, tg_client_id)
                VALUES('{temp_user.get_name(temp_user)}','{temp_user.get_last_name(temp_user)}','{temp_user.get_surname(temp_user)}','{temp_user.get_id(temp_user)}');
            """
            )
            bot.send_message(call.message.chat.id, 'Сохраненяем..')
        except Exception as e:
            logging.warning(str(e)+f':{temp_user.get_id(temp_user)}')
            bot.send_message(call.message.chat.id, 'Какая-то ошибка( с базами данных. Чиним.')

        # Запись о пройденном первом уровне
        try:
            mycursor.execute(
            f"""
                INSERT INTO users_level(tg_client_id, level_number)
                VALUES('{temp_user.get_id(temp_user)}',1);
            """
            )
            bot.send_message(call.message.chat.id, 'Сохранено')
            show_module(call.message.chat.id,1)
            # markup_module = types.InlineKeyboardMarkup()
            # study = types.InlineKeyboardButton(text='Модуль обучения', callback_data="command_study")
            # tests = types.InlineKeyboardButton(text='Модуль тестирования', callback_data="command_test")
            # estimation = types.InlineKeyboardButton(text='Модуль оценки', callback_data="command_estimation")
            # markup_module.add(study, tests, estimation)
            # bot.send_message(call.message.chat.id, text="Выберите тему для изучения(лучше начать с первой)",reply_markup = markup_module)
            
            
        except Exception as e:
            logging.warning(str(e)+f':{temp_user.get_id(temp_user)}')
            bot.send_message(call.message.chat.id, 'Какая-то ошибка( с базами данных. Чиним.')

    

# module 1 - authorized guy

def show_module(tg_id,level=1):
    bot.send_message(tg_id, f'Вы на {level} уровне.')
    if level == 1:
        module1 = Module.Module
        mycursor.execute(
            '''
                SELECT title, data, task, answers
                FROM
                    module
                    INNER JOIN questions ON module.module_id = questions.module_id
                WHERE module.module_id = 1;
            '''
        )
        result = mycursor.fetchall()
        module1.title = result[0][0]
        module1.data = result[0][1]
        module1.arr_of_question = []
        for question in result:
            temp = Question.Question(question[2], question[3])
            module1.arr_of_question.append(temp)

        bot.send_message(tg_id, f'Тема:{module1.title}')
        

        mes_length = 1024
        if len(module1.data) > mes_length:
            for x in range(0, len(module1.data), mes_length):
                bot.send_message(tg_id, module1.data[x:x+mes_length])
            else:
                bot.send_message(tg_id,tg_id, module1.data)
        message = bot.send_message(tg_id,'ВАЖНО! КОГДА БУДЕТЕ ГОТОВЫ - ВВЕДИТЕ ОК. На решение у Вас будет 10 минут')
        bot.register_next_step_handler(message, show_questions_1,module1.arr_of_question,tg_id)

    if level == 2:
        module1 = Module.Module
        mycursor.execute(
            '''
                SELECT title, data, task, answers
                FROM
                    module
                    INNER JOIN questions ON module.module_id = questions.module_id
                WHERE module.module_id = 2;
            '''
        )
        result = mycursor.fetchall()
        module1.title = result[0][0]
        module1.data = result[0][1]
        module1.arr_of_question = []
        for question in result:
            temp = Question.Question(question[2], question[3])
            module1.arr_of_question.append(temp)

        bot.send_message(tg_id, f'Тема:{module1.title}')
        

        mes_length = 1024
        if len(module1.data) > mes_length:
            for x in range(0, len(module1.data), mes_length):
                bot.send_message(tg_id, module1.data[x:x+mes_length])
            else:
                bot.send_message(tg_id,tg_id, module1.data)    
        message = bot.send_message(tg_id,'ВАЖНО! КОГДА БУДЕТЕ ГОТОВЫ - ВВЕДИТЕ ОК. На решение у Вас будет 10 минут')
        bot.register_next_step_handler(message, show_questions_2,module1.arr_of_question,tg_id)
    if level == 3:
        try:
            #падает
            module1 = Module.Module
            mycursor.execute(
                '''
                    SELECT title, data, task, answers
                    FROM
                        module
                        INNER JOIN questions ON module.module_id = questions.module_id
                    WHERE module.module_id = 3;
                '''
            )
            result = mycursor.fetchall()
            module1.title = result[0][0]
            module1.data = result[0][1]
            module1.arr_of_question = []
            for question in result:
                temp = Question.Question(question[2], question[3])
                module1.arr_of_question.append(temp)

            bot.send_message(tg_id, f'Тема:{module1.title}')
        

            mes_length = 1024
            if len(module1.data) > mes_length:
                for x in range(0, len(module1.data), mes_length):
                    bot.send_message(tg_id, module1.data[x:x+mes_length])
            else:
                bot.send_message(tg_id,tg_id, module1.data)    
            message = bot.send_message(tg_id,'ВАЖНО! КОГДА БУДЕТЕ ГОТОВЫ - ВВЕДИТЕ ОК. На решение у Вас будет 10 минут')
            bot.register_next_step_handler(message, show_questions_3,module1.arr_of_question,tg_id)
        except Exception as e:
            bot.send_message(tg_id,'Возникла ошибка, ожидайте')
def show_questions_1(message,arr_questions,tg_id):
    show_question_1(message, arr_questions, 0,[])
def show_questions_2(message,arr_questions,tg_id):
    show_question_2(message, arr_questions, 0,[])
def show_questions_3(message,arr_questions,tg_id):
    show_question_3(message, arr_questions, 0,[])

def show_question_1(message, arr_questions,j,arr_answers):
    tg_id = message.chat.id
    if j<len(arr_questions):
        arr_answers.append(message.text)
        message = bot.send_message(tg_id,f'ВОПРОС:{arr_questions[j].task}')
        s = ''
        i = 0 
        for answer in json.loads(arr_questions[j].answers):
            s=s+str(i)+")"+answer+"\n"
            i=i+1
        bot.send_message(tg_id,f'Варианты ОТВЕТОВ:\n{s}')
        bot.register_next_step_handler(message, show_question_1,arr_questions, j+1,arr_answers)
    if j == len(arr_questions):
        arr_answers.append(message.text)
        bot.send_message(tg_id,f'Введите РЕЗУЛЬТАТ чтобы посмотреть свой результат')
        bot.register_next_step_handler(message, show_result_1,arr_questions, arr_answers)
def show_result_1(message, arr_questions,arr_answers):
    result = 0
    for i in range(0,len(arr_questions)):
        index = []
        for x in json.loads(arr_questions[i].answers):
            index.append(x)
        if int(arr_answers[i+1])<len(index):
            result = result + int(json.loads(arr_questions[i].answers)[index[int(arr_answers[i+1])]])
    bot.send_message(message.chat.id,f'Вы набрали {result}/{len(arr_questions)}')
    if result<len(arr_questions):
        bot.send_message(message.chat.id,f'Чтобы пройти дальше - необходимо набрать {len(arr_questions)}/{len(arr_questions)}')
        bot.send_message(message.chat.id,f'Отправляем Вас на страницу подготовки, введите ОК, чтобы продолжить')
        del(arr_questions)
        del(arr_answers)
        bot.register_next_step_handler(message, lambda x:(show_module(message.chat.id,level=1)))
    else:
        bot.send_message(message.chat.id,f'Вы огромный молодец! Сейчас перенаправим Вас на следующий модуль.Введите ОК, чтобы продолжить')
        print(
            f'''
            UPDATE users_level
            SET level_number=2
            WHERE tg_client_id='{message.chat.id}';
            '''
        )
        bot.register_next_step_handler(message, lambda x:(show_module(message.chat.id,level=2)))
def show_question_2(message, arr_questions,j,arr_answers):
    tg_id = message.chat.id
    if j<len(arr_questions):
        arr_answers.append(message.text)
        message = bot.send_message(tg_id,f'ВОПРОС:{arr_questions[j].task}')
        s = ''
        i = 0 
        for answer in json.loads(arr_questions[j].answers):
            s=s+str(i)+")"+answer+"\n"
            i=i+1
        bot.send_message(tg_id,f'Варианты ОТВЕТОВ:\n{s}')
        bot.register_next_step_handler(message, show_question_2,arr_questions, j+1,arr_answers)
    if j == len(arr_questions):
        arr_answers.append(message.text)
        bot.send_message(tg_id,f'Введите РЕЗУЛЬТАТ чтобы посмотреть свой результат')
        bot.register_next_step_handler(message, show_result_2,arr_questions, arr_answers)
def show_result_2(message, arr_questions,arr_answers):
    result = 0
    for i in range(0,len(arr_questions)):
        index = []
        for x in json.loads(arr_questions[i].answers):
            index.append(x)
        if int(arr_answers[i+1])<len(index):
            result = result + int(json.loads(arr_questions[i].answers)[index[int(arr_answers[i+1])]])
    bot.send_message(message.chat.id,f'Вы набрали {result}/{len(arr_questions)}')
    if result<len(arr_questions):
        bot.send_message(message.chat.id,f'Чтобы пройти дальше - необходимо набрать {len(arr_questions)}/{len(arr_questions)}')
        bot.send_message(message.chat.id,f'Отправляем Вас на страницу подготовки, введите ОК, чтобы продолжить')
        del(arr_questions)
        del(arr_answers)
        bot.register_next_step_handler(message, lambda x:(show_module(message.chat.id,level=2)))
    else:
        bot.send_message(message.chat.id,f'Вы огромный молодец! Сейчас перенаправим Вас на следующий модуль.Введите ОК, чтобы продолжить')
        print(
            f'''
            UPDATE users_level
            SET level_number=3
            WHERE tg_client_id='{message.chat.id}';
            '''
        )
        bot.register_next_step_handler(message, lambda x:(show_module(message.chat.id,level=3)))


def show_question_3(message, arr_questions,j,arr_answers):
    tg_id = message.chat.id
    if j<len(arr_questions):
        arr_answers.append(message.text)
        message = bot.send_message(tg_id,f'ВОПРОС:{arr_questions[j].task}')
        s = ''
        i = 0 
        for answer in json.loads(arr_questions[j].answers):
            s=s+str(i)+")"+answer+"\n"
            i=i+1
        bot.send_message(tg_id,f'Варианты ОТВЕТОВ:\n{s}')
        bot.register_next_step_handler(message, show_question_3,arr_questions, j+1,arr_answers)
    if j == len(arr_questions):
        arr_answers.append(message.text)
        bot.send_message(tg_id,f'Введите РЕЗУЛЬТАТ чтобы посмотреть свой результат')
        bot.register_next_step_handler(message, show_result_3,arr_questions, arr_answers)
def show_result_3(message, arr_questions,arr_answers):
    result = 0
    for i in range(0,len(arr_questions)):
        index = []
        for x in json.loads(arr_questions[i].answers):
            index.append(x)
        if int(arr_answers[i+1])<len(index):
            result = result + int(json.loads(arr_questions[i].answers)[index[int(arr_answers[i+1])]])
    bot.send_message(message.chat.id,f'Вы набрали {result}/{len(arr_questions)}')
    if result<len(arr_questions):
        bot.send_message(message.chat.id,f'Чтобы пройти дальше - необходимо набрать {len(arr_questions)}/{len(arr_questions)}')
        bot.send_message(message.chat.id,f'Отправляем Вас на страницу подготовки, введите ОК, чтобы продолжить')
        del(arr_questions)
        del(arr_answers)
        bot.register_next_step_handler(message, lambda x:(show_module(message.chat.id,level=3)))
    else:
        bot.send_message(message.chat.id,f'Вы огромный молодец! Сейчас перенаправим Вас на следующий модуль.Введите ОК, чтобы продолжить')
        print(
            f'''
            UPDATE users_level
            SET level_number=4
            WHERE tg_client_id='{message.chat.id}';
            '''
        )
        global FINAL
        bot.send_message(message.chat.id,'всё')
        #bot.register_next_step_handler(message, lambda x:(show_module(message.chat.id,level=FINAL)))


'''def get_unit(message: types.Message):   # кнопки выбора подразделения
    markup_inline = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text='Подразделение 1', callback_data=1)
    button_2 = types.InlineKeyboardButton(text='Подразделение 2', callback_data=2)
    button_3 = types.InlineKeyboardButton(text='Подразделение 3', callback_data=3)
    markup_inline.add(button_1)
    markup_inline.add(button_2)
    markup_inline.add(button_3)
    bot.send_message(message.from_user.id, f"Имя, {name}, фамилия {surname}")   # тест, в дальнейшем удалить!!!
    bot.send_message(message.chat.id, 'Выберите подразделение в котором работаете:', reply_markup=markup_inline)




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

'''
bot.polling(none_stop=True)