import telebot
import random
from telebot import types

data_names = ['Пушкин Руслан Сергеевич', 'Панов Александр Максимович']
all_forms = ['8', '9', '10', '11']
all_forms_letter = ['О', 'М', 'Н', 'П', 'Р']

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
    if message.text in data_names:
        bot.send_message(message.chat.id, 'Введите класс (через пробел):')
        bot.register_next_step_handler(message, form)
    else:
        bot.send_message(message.chat.id, 'Ваше имя не найдено в базе данных! Попробуйте еще раз!')
        bot.register_next_step_handler(message, f)


def form(message):
    x = message.text
    x = x.split(' ')
    if x[0] in all_forms:
        if x[1] in all_forms_letter:
            bot.send_message(message.chat.id, 'Класс успешно определён!')
    else:
        bot.send_message(message.chat.id, 'Не можем определить ваш класс! Попробуйте еще раз! (Напоминание: введите букву класса в верхем регистре и на русской раскладке!)')
        bot.register_next_step_handler(message, form)





@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Зарегестрироваться':
        answer = "Введите ФИО"
        bot.send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, f)

    elif message.text.strip() == 'Получить QR':
        answer = random.choice(giveQR)
        bot.send_message(message.chat.id, answer)
    else:
        pass


bot.infinity_polling()