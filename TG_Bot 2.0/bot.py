import sqlite3

import telebot
import random
from telebot import types


path = r"my/path/to/file.txt"

data_names = ['Пушкин Руслан Сергеевич', 'Панов Александр Максимович', 'Волков Александр Алексеевич']
all_forms = ['8', '9', '10', '11']
all_forms_letter = ['О', 'М', 'Н', 'П', 'Р']
db = {}
data_db = []
f = open('reg.txt', 'r', encoding='UTF-8')
registration = f.read().split('\n')
f.close()
f = open('giveQR.txt', 'r', encoding='UTF-8')
giveQR = f.read().split('\n')
f.close()

bot = telebot.TeleBot('5929196657:AAFXnXvCbjGsWweOx3aDJhh8zvxixSAzeSY')


@bot.message_handler(commands=["start"])
def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Зарегестрироваться")
        item2 = types.KeyboardButton("Получить QR")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Привет, Я - Бот ТРИАДА! Выбери, что ты хочешь сделать',
                         reply_markup=markup)


def f(message):
    name_lst = message.text.split(' ')
    if True: # message.text in data_names:
        if len(name_lst) in [2, 3]:
            flag = True
            for i in range(len(name_lst)):
                if not name_lst[i].isalpha() or len(name_lst[i]) < 2:
                    bot.send_message(message.chat.id, 'Ваше имя содержит цифры или слишком короткое, попробуйте еще раз!')
                    bot.register_next_step_handler(message, f)
                    flag = False
                    break
            if flag:
                bot.send_message(message.chat.id, 'Введите класс (через пробел):')
                bot.register_next_step_handler(message, form)
        else:
            bot.send_message(message.chat.id, 'Ваше имя должно состоять из 3 слов!')
            bot.register_next_step_handler(message, f)
    else:
        bot.send_message(message.chat.id, 'Ваше имя не найдено в базе данных! Попробуйте еще раз!')
        bot.register_next_step_handler(message, f)

# добавить!!!
#res = add_to_db(name, grade, tg_id, photo)if res["OK"]:
   # bot.send_message(m.chat.id, "Все успешно")else:
    #bot.send_message(m.chat.id, "Что-то пошло не так :(")    bot.send_message(m.chat.id, res["description"])


def add_to_db(name, grade, tg_id, photo):
    inf_to_check = f"{name} {grade} {tg_id}"
    con = sqlite3.connect("../DB/MainDB.db")
    cur = con.cursor()
    que = "SELECT name, surname, patronymic, grade, tg_id FROM Students"
    res = cur.execute(que).fetchall()
    name_in_db = False
    for elem in res:
        inf = ' '.join(map(str, elem))
        if inf_to_check == inf:
            name_in_db = True
            break
    if name_in_db:
        ans = {"OK": False, "description": "ваше имя уже есть в DB"}
    else:
        ans = {"OK": True}
    return ans


def form(message):
    x = message.text
    x = x.split(' ')
    if x[0] in all_forms:
        if x[1].upper() in all_forms_letter:
            bot.send_message(message.chat.id, 'Класс успешно определён!')
            bot.send_message(message.chat.id, 'Отправьте ваше фото :)')
            bot.register_next_step_handler(message, handle_docs_photo)
        else:
            bot.send_message(message.chat.id, 'Не можем определить ваш класс! Попробуйте еще раз! (Напоминание: введите букву класса в верхем регистре и на русской раскладке!)')
            bot.register_next_step_handler(message, form)
    else:
        bot.send_message(message.chat.id, 'Не можем определить ваш класс! Попробуйте еще раз! (Напоминание: введите букву класса в верхем регистре и на русской раскладке!)')
        bot.register_next_step_handler(message, form)


def handle_docs_photo(message):
    from pathlib import Path
    Path(f'files/{message.chat.id}/').mkdir(parents=True, exist_ok=True)
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/{message.chat.id}/' + file_info.file_path.replace('photos/', '')
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = f'files/{message.chat.id}/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    bot.send_message(message.chat.id, 'Фото успешно сохранено')
    choise_day(message)


def choise_day(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Понедельник")
    item2 = types.KeyboardButton("Вторник")
    item3 = types.KeyboardButton("Среда")
    item4 = types.KeyboardButton("Четверг")
    item5 = types.KeyboardButton("Пятница")
    item6 = types.KeyboardButton("Суббота")
    item7 = types.KeyboardButton("Далее")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    bot.send_message(message.chat.id, 'Выберите дни пользования столовой', reply_markup=markup)
    bot.register_next_step_handler(message, choise_day_finish)


def choise_day_finish(message):
    if message.text.strip() == "Понедельник":
        x = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Завтрак")
        item2 = types.KeyboardButton("Обед")
        item3 = types.KeyboardButton("И завтрак и обед")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, add_day_to_db1)
    elif message.text.strip() == "Вторник":
        x = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Завтрак")
        item2 = types.KeyboardButton("Обед")
        item3 = types.KeyboardButton("И завтрак и обед")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, add_day_to_db2)
    elif message.text.strip() == "Среда":
        x = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Завтрак")
        item2 = types.KeyboardButton("Обед")
        item3 = types.KeyboardButton("И завтрак и обед")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, add_day_to_db3)
    elif message.text.strip() == "Четверг":
        x = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Завтрак")
        item2 = types.KeyboardButton("Обед")
        item3 = types.KeyboardButton("И завтрак и обед")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, add_day_to_db4)
    elif message.text.strip() == "Пятница":
        x = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Завтрак")
        item2 = types.KeyboardButton("Обед")
        item3 = types.KeyboardButton("И завтрак и обед")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, add_day_to_db5)
    elif message.text.strip() == "Суббота":
        x = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Завтрак")
        item2 = types.KeyboardButton("Обед")
        item3 = types.KeyboardButton("И завтрак и обед")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, add_day_to_db6)
    elif message.text.strip() == "Далее":
        if len(db) > 0:
            bot.send_message(message.chat.id, db)
        else:
            bot.send_message(message.chat.id, 'Вы ничего не выбрали')
            choise_day(message)


def add_day_to_db1(message):
    if message.text.strip() == 'Завтрак':
        db[message.chat.id] = 'Понедельник,Завтрак'
        bot.send_message(message.chat.id, 'Добавлено: Понедельник - Завтрак')
        choise_day(message)
    elif message.text.strip() == 'Обед':
        db[message.chat.id] = 'Понедельник,Обед'
        bot.send_message(message.chat.id, 'Добавлено: Понедельник - Обед')
        choise_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db[message.chat.id] = 'Понедельник,Завтрак,обед'
        bot.send_message(message.chat.id, 'Добавлено: Понедельник - Завтрак и обед')
        choise_day(message)
    print(db)


def add_day_to_db2(message):
    if message.text.strip() == 'Завтрак':
        db[message.chat.id] = 'Вторник,Завтрак'
        bot.send_message(message.chat.id, 'Добавлено: Вторник - Завтрак')
        choise_day(message)
    elif message.text.strip() == 'Обед':
        db[message.chat.id] = 'Вторник,Обед'
        bot.send_message(message.chat.id, 'Добавлено: Вторник - Обед')
        choise_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db[message.chat.id] = 'Вторник,Завтрак,обед'
        bot.send_message(message.chat.id, 'Добавлено: Вторник - Завтрак и обед')
        choise_day(message)
    print(db)


def add_day_to_db3(message):
    if message.text.strip() == 'Завтрак':
        db[message.chat.id] = 'Среда,Завтрак'
        bot.send_message(message.chat.id, 'Добавлено: Среда - Завтрак')
        choise_day(message)
    elif message.text.strip() == 'Обед':
        db[message.chat.id] = 'Среда,Обед'
        bot.send_message(message.chat.id, 'Добавлено: Среда - Обед')
        choise_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db[message.chat.id] = 'Среда,Завтрак,обед'
        bot.send_message(message.chat.id, 'Добавлено: Среда - Завтрак и обед')
        choise_day(message)
    print(db)


def add_day_to_db4(message):
    if message.text.strip() == 'Завтрак':
        db[message.chat.id] = 'Четверг,Завтрак'
        bot.send_message(message.chat.id, 'Добавлено: Четверг - Завтрак')
        choise_day(message)
    elif message.text.strip() == 'Обед':
        db[message.chat.id] = 'Четверг,Обед'
        bot.send_message(message.chat.id, 'Добавлено: Четверг - Обед')
        choise_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db[message.chat.id] = 'Четверг,Завтрак,обед'
        bot.send_message(message.chat.id, 'Добавлено: Четверг - Завтрак и обед')
        choise_day(message)
    print(db)


def add_day_to_db5(message):
    if message.text.strip() == 'Завтрак':
        db[message.chat.id] = 'Пятница,Завтрак'
        bot.send_message(message.chat.id, 'Добавлено: Пятница - Завтрак')
        choise_day(message)
    elif message.text.strip() == 'Обед':
        db[message.chat.id] = 'Пятница,Обед'
        bot.send_message(message.chat.id, 'Добавлено: Пятница - Обед')
        choise_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db[message.chat.id] = 'Пятница,Завтрак,обед'
        bot.send_message(message.chat.id, 'Добавлено: Пятница - Завтрак и обед')
        choise_day(message)
    print(db)


def add_day_to_db6(message):
    if message.text.strip() == 'Завтрак':
        db[message.chat.id] = 'Суббота,Завтрак'
        bot.send_message(message.chat.id, 'Добавлено: Суббота - Завтрак')
        choise_day(message)
    elif message.text.strip() == 'Обед':
        db[message.chat.id] = 'Суббота,Обед'
        bot.send_message(message.chat.id, 'Добавлено: Суббота - Обед')
        choise_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db[message.chat.id] = 'Суббота,Завтрак,обед'
        bot.send_message(message.chat.id, 'Добавлено: Суббота - Завтрак и обед')
        choise_day(message)
    print(db)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Зарегестрироваться':
        answer = "Введите ФИО"
        bot.send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, f)

    elif message.text.strip() == 'Получить QR':
        bot.send_message(message.chat.id, 'В разработке...')
        start(message)
    else:
        pass


bot.infinity_polling()