import telebot
import random
from telebot import types


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


def f(m):
    print(m.text)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Зарегестрироваться':
        answer = random.choice(registration)
        bot.send_message(message.chat.id, answer)
        bot.register_next_step_handler(message, f)
    elif message.text.strip() == 'Получить QR':
        answer = random.choice(giveQR)
        bot.send_message(message.chat.id, answer)
    else:
        pass


bot.infinity_polling()