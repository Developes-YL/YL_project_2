import os
import telebot
from telebot import types
from telebot.types import Message
from modules_for_db import is_user_in_db, get_name_from_db, add_inf_to_db


data_names = ['Пушкин Руслан Сергеевич', 'Панов Александр Максимович', 'Волков Александр Алексеевич']
all_forms = ['8', '9', '10', '11']
all_forms_letter = ['О', 'М', 'Н', 'П', 'Р']
db = []
db1 = []
brekfast_cost = 185
lunch_cost = 348
with open("Support/TOKEN.txt", 'r') as file:
    token = file.readline()
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["start"])
def start(message: Message, first_message=True):
    user_id = message.from_user.id
    user_in_db = is_user_in_db(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = []
    if user_in_db:
        # юзер уже зарегестрирован
        name, surname = get_name_from_db(user_id)
        items.append(types.KeyboardButton("Получить QR"))
        items.append(types.KeyboardButton("Запланировать обеды/завтраки"))
        # здесь размещаются остальные кнопки
        answer = "Выберите действие"
        if first_message:
            answer = f'Привет, {surname} {name}!'
    else:
        items.append(types.KeyboardButton("Зарегистрироваться"))
        answer = "Привет! Я - Бот ТРИАДА!"

    for item in items:
        markup.add(item)
    bot.send_message(message.chat.id, answer, reply_markup=markup)


def handle_name(message: Message):
    answer = ""
    next_function = None
    name_lst = message.text.split(' ')
    if len(name_lst) in [2, 3]:
        flag = True
        for i in range(len(name_lst)):
            if not name_lst[i].isalpha() or len(name_lst[i]) < 2:
                answer = 'Ваше имя содержит цифры или слишком короткое, попробуйте еще раз!'
                next_function = handle_name
                flag = False
                break
        if flag:
            answer = 'Введите класс (через пробел)'
            inf = {"surname": name_lst[0], "name": name_lst[1], "patronymic": name_lst[2],
                   "tg_id": message.from_user.id}
            next_function = (lambda x: handle_grade(x, inf))
    else:
        answer = 'Ваше имя должно состоять из 2 или 3 слов!'
        next_function = handle_name

    bot.send_message(message.chat.id, answer)
    bot.register_next_step_handler(message, next_function)


def handle_grade(message: Message, inf: dict):
    grade_number, grade_letter = message.text.split()
    if grade_number in all_forms:
        res = message.text.split()
        if grade_letter.upper() in all_forms_letter:
            answer = 'Класс успешно определён!\nОтправьте ваше фото :)'
            inf["grade_letter"] = grade_letter
            inf["grade_number"] = grade_number
            next_function = (lambda x: handle_docs_photo(x, inf))
        else:
            answer = 'Не можем определить ваш класс! Попробуйте еще раз!\n ' \
                     'Напоминание: введите букву класса на русской раскладке!'
            next_function = (lambda x: handle_grade(x, inf))
            handle_text()
    else:
        answer = 'Не можем определить ваш класс! Попробуйте еще раз!\n ' \
                 'Напоминание: введите букву класса на русской раскладке!'
        next_function = (lambda x: handle_grade(x, inf))

    bot.send_message(message.chat.id, answer)
    bot.register_next_step_handler(message, next_function)


def handle_docs_photo(message: Message, inf: dict):
    data_path = f"../DB/Data/{inf['tg_id']}."
    if os.path.exists(data_path + "png"):
        os.remove(data_path + "png")
    if os.path.exists(data_path + "jpg"):
        os.remove(data_path + "jpg")
    if message.content_type == 'photo':
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        data_path += file_info.file_path.replace('photos/', '').split('.')[1]
        with open(data_path, 'wb') as new_file:
            new_file.write(downloaded_file)

    elif message.content_type == 'document':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        data_path += message.document.file_name.split('.')[1]
        with open(data_path, 'wb') as new_file:
            new_file.write(downloaded_file)

    add_inf_to_db(inf)
    bot.send_message(message.chat.id, 'Фото успешно сохранено')
    start(message, False)


def choice_day(message):
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
    bot.register_next_step_handler(message, choice_day_finish)


def choice_day_finish(message):
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
            for i in range(len(db)):
                if str(message.chat.id) in db[i]:
                    n = db[i]
                    n = n.split('-')
                    n = n[1:]
                    for j in range(len(n)):
                        bot.send_message(message.chat.id, 'Вы выбрали:' + n[j])
            pay_bot(message)

        else:
            bot.send_message(message.chat.id, 'Вы ничего не выбрали')
            choice_day(message)


def pay_bot(message):
    brekfast = 0
    lunch = 0
    db_1 = []
    brekfast_cost = 185
    lunch_cost = 348
    for i in range(len(db)):
        if str(message.chat.id) in db[i]:
            db_1.append(db[i])
    for j in range(len(db_1)):
        if 'завтрак' in db_1[j]:
            brekfast += 1
        if 'обед' in db_1[j]:
            lunch += 1
    brekfast_final_cost = brekfast_cost * brekfast
    lunch_final_cost = lunch_cost * lunch
    bot.send_message(message.chat.id, 'Стоимость Завтраков:' + str(brekfast_final_cost))
    bot.send_message(message.chat.id, 'Стоимость Обедов:' + str(lunch_final_cost))
    bot.send_message(message.chat.id, 'Общая стоимость:' + str((brekfast_final_cost + lunch_final_cost)))
    bot.send_message(message.chat.id, 'Что бы оплатить обед, переведите ' + str((brekfast_final_cost + lunch_final_cost)) +
                                      ' на QIWI кошелек по номеру +79253503525')



def add_day_to_db1(message):
    if message.text.strip() == 'Завтрак':
        db.append(str(message.chat.id) + '-понедельник-завтрак')
        bot.send_message(message.chat.id, 'Добавлено: Понедельник - Завтрак')
        choice_day(message)
    elif message.text.strip() == 'Обед':
        db.append(str(message.chat.id) + '-понедельник-обед')
        bot.send_message(message.chat.id, 'Добавлено: Понедельник - обед')
        choice_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db.append(str(message.chat.id) + '-понедельник-завтрак-обед')
        bot.send_message(message.chat.id, 'Добавлено: Понедельник - Завтрак и обед')
        choice_day(message)
    print(db)


def add_day_to_db2(message):
    if message.text.strip() == 'Завтрак':
        db.append(str(message.chat.id) + '-вторник-завтрак')
        bot.send_message(message.chat.id, 'Добавлено: Вторник - Завтрак')
        choice_day(message)
    elif message.text.strip() == 'Обед':
        db.append(str(message.chat.id) + '-вторник-обед')
        bot.send_message(message.chat.id, 'Добавлено: Вторник - Обед')
        choice_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db.append(str(message.chat.id) + '-вторник-завтрак-обед')
        bot.send_message(message.chat.id, 'Добавлено: Вторник - Завтрак и обед')
        choice_day(message)
    print(db)


def add_day_to_db3(message):
    if message.text.strip() == 'Завтрак':
        db.append(str(message.chat.id) + '-среда-завтрак')
        bot.send_message(message.chat.id, 'Добавлено: Среда - Завтрак')
        choice_day(message)
    elif message.text.strip() == 'Обед':
        db.append(str(message.chat.id) + '-среда-обед')
        bot.send_message(message.chat.id, 'Добавлено: Среда - Обед')
        choice_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db.append(str(message.chat.id) + '-среда-завтрак-обед')
        bot.send_message(message.chat.id, 'Добавлено: Среда - Завтрак и обед')
        choice_day(message)
    print(db)


def add_day_to_db4(message):
    if message.text.strip() == 'Завтрак':
        db.append(str(message.chat.id) + '-четверг-завтрак')
        bot.send_message(message.chat.id, 'Добавлено: Четверг - Завтрак')
        choice_day(message)
    elif message.text.strip() == 'Обед':
        db.append(str(message.chat.id) + '-четверг-обед')
        bot.send_message(message.chat.id, 'Добавлено: Четверг - Обед')
        choice_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db.append(str(message.chat.id) + '-четверг-завтрак-обед')
        bot.send_message(message.chat.id, 'Добавлено: Четверг - Завтрак и обед')
        choice_day(message)
    print(db)


def add_day_to_db5(message):
    if message.text.strip() == 'Завтрак':
        db.append(str(message.chat.id) + '-пятница-завтрак')
        bot.send_message(message.chat.id, 'Добавлено: Пятница - Завтрак')
        choice_day(message)
    elif message.text.strip() == 'Обед':
        db.append(str(message.chat.id) + '-пятница-обед')
        bot.send_message(message.chat.id, 'Добавлено: Пятница - Обед')
        choice_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db.append(str(message.chat.id) + '-пятница-завтрак-обед')
        bot.send_message(message.chat.id, 'Добавлено: Пятница - Завтрак и обед')
        choice_day(message)
    print(db)


def add_day_to_db6(message):
    if message.text.strip() == 'Завтрак':
        db.append(str(message.chat.id) + '-суббота-завтрак')
        bot.send_message(message.chat.id, 'Добавлено: Суббота - Завтрак')
        choice_day(message)
    elif message.text.strip() == 'Обед':
        db.append(str(message.chat.id) + '-суббота-обед')
        bot.send_message(message.chat.id, 'Добавлено: Суббота - Обед')
        choice_day(message)
    elif message.text.strip() == 'И завтрак и обед':
        db.append(str(message.chat.id) + '-суббота-завтрак-обед')
        bot.send_message(message.chat.id, 'Добавлено: Суббота - Завтрак и обед')
        choice_day(message)
    print(db)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Зарегистрироваться':
        answer = "Введите ФИО"
        bot.send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_name)

    elif message.text.strip() == 'Получить QR':
        bot.send_message(message.chat.id, 'В разработке...')
        start(message)

    elif message.text.strip() == 'Запланировать обеды/завтраки':
        choice_day(message)
    else:
        pass


if __name__ == "__main__":
    print("Бот начал работу")
    bot.infinity_polling()
    print("Бот завершил работу")
