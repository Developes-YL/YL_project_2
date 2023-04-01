import os

from telebot import TeleBot
from telebot.types import Message

from modules_for_db import add_inf_to_db, get_classes


bot: TeleBot = None
start = None


def set_bot(new_bot: TeleBot, func):
    global bot, start
    bot = new_bot
    start = func


def handle_name(message: Message):
    answer = ""
    next_function = None

    if message.text is None:
        bot.register_next_step_handler(message, handle_name)
        return

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
            if len(name_lst) == 2:
                name_lst.append("-")
            inf = {"surname": name_lst[0], "name": name_lst[1], "patronymic": name_lst[2],
                   "tg_id": message.from_user.id}
            next_function = (lambda x: handle_grade(x, inf))
    else:
        answer = 'Ваше имя должно состоять из 2 или 3 слов!'
        next_function = handle_name

    bot.send_message(message.chat.id, answer)
    bot.register_next_step_handler(message, next_function)


def handle_grade(message: Message, inf: dict):
    if message.text is None:
        bot.register_next_step_handler(message, lambda x: handle_grade(x, inf))
        return
    grade_number, grade_letter = message.text.split()
    class_numbers, class_letters = get_classes()
    if grade_number in class_numbers:
        if grade_letter.upper() in class_letters:
            answer = 'Класс успешно определён!\nОтправьте ваше фото :)'
            inf["grade_letter"] = grade_letter
            inf["grade_number"] = grade_number
            next_function = (lambda x: handle_docs_photo(x, inf))
        else:
            answer = 'Не можем определить ваш класс! Попробуйте еще раз!\n ' \
                     'Напоминание: введите букву класса на русской раскладке!'
            next_function = (lambda x: handle_grade(x, inf))
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

    else:
        bot.register_next_step_handler(message, lambda x: handle_docs_photo(x, inf))
        return

    add_inf_to_db(inf)
    bot.send_message(message.chat.id, 'Регистрация прошла успешно')
    start(message, False)
