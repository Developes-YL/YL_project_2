from telebot import TeleBot
from telebot import types
import sqlite3
from telebot.types import Message
from modules_for_db import is_user_in_db, get_name_from_db, get_code, check_time_in_interval
from registration import handle_name
from payment import choice_day
import registration
import payment
import qrcode
import tempfile

with open("Support/TOKEN.txt", 'r') as file:
    token = file.readline()

bot = TeleBot(token)


def set_bot(new_bot: TeleBot):
    registration.set_bot(new_bot, start)
    payment.set_bot(new_bot, start)


@bot.message_handler(commands=["start"])
def start(message: Message, first_message: bool = True):
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


def lunch_choise(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = []
    items.append(types.KeyboardButton("Завтрак"))
    items.append(types.KeyboardButton("Обед"))
    for item in items:
        markup.add(item)
    bot.send_message(message.chat.id, 'Выберите что сейчас, обед или завтрак?', reply_markup=markup)
    bot.register_next_step_handler(message, lunch_choise1)

def lunch_choise1(message):
    if message.text.strip() == 'Завтрак':
        if check_time_in_interval('09:25', '9:50'):
            qr_generation(message)
        else:
            bot.send_message(message.chat.id, 'Сейчас не время для завтрака!')
            start(message, False)
    elif message.text.strip() == 'Обед':
        if check_time_in_interval('12:25', '12:50'):
            qr_generation(message)
        elif check_time_in_interval('13:30', '13:55'):
            qr_generation(message)
        else:
            bot.send_message(message.chat.id, 'Сейчас не время для обеда!')
            start(message, False)
    else:
        bot.send_message(message.chat.id, 'Вы неверно выбрали действие', reply_markup=types.ReplyKeyboardRemove())
        lunch_choise(message)


def qr_generation(message):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(str(message.chat.id) + ' ' + get_code(message.chat.id))
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        img.save(temp.name)
        temp.flush()
        temp.seek(0)
        bot.send_photo(chat_id=message.chat.id, photo=temp, reply_markup=types.ReplyKeyboardRemove())
        start(message, False)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text is None:
        return

    if message.text.strip() == 'Зарегистрироваться':
        answer = "Введите ФИО"
        bot.send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_name)

    elif message.text.strip() == 'Получить QR':

        lunch_choise(message)

    elif message.text.strip() == 'Запланировать обеды/завтраки':
        choice_day(message)


set_bot(bot)

if __name__ == "__main__":
    print("Бот начал работу")
    bot.infinity_polling()
    print("Бот завершил работу")
