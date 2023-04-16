from telebot import TeleBot, types
from telebot.types import Message

from modules_for_db import get_prices, add_days_to_db

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
bot: TeleBot = None
start = None
lunch = set()
breakfast = set()


def set_bot(new_bot: TeleBot, func):
    global bot, start
    bot = new_bot
    start = func


def choice_day(message: Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for day in days:
        item = types.KeyboardButton(day)
        markup.add(item)
    item2 = types.KeyboardButton("Далее")
    item3 = types.KeyboardButton("Назад")
    markup.add(item2)
    markup.add(item3)
    bot.send_message(message.chat.id, 'Выберите дни пользования столовой', reply_markup=markup)
    bot.register_next_step_handler(message, choice_day_finish)


def choice_day_finish(message: Message):
    if message.text is None:
        bot.register_next_step_handler(message, choice_day_finish)
        return

    if message.text.strip() in days:
        day = message.text.strip()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if day in breakfast:
            item1 = types.KeyboardButton("Отменить завтрак")
        else:
            item1 = types.KeyboardButton("Завтрак")

        if day in lunch:
            item2 = types.KeyboardButton("Отменить обед")
        else:
            item2 = types.KeyboardButton("Обед")

        markup.add(item1)
        markup.add(item2)
        if day not in lunch and day not in breakfast:
            item3 = types.KeyboardButton("И завтрак и обед")
            markup.add(item3)
        elif day in lunch and day in breakfast:
            item3 = types.KeyboardButton("Отменить и завтрак и обед")
            markup.add(item3)
        item4 = types.KeyboardButton("Назад")
        markup.add(item4)
        bot.send_message(message.chat.id, 'Завтрак или обед?', reply_markup=markup)
        bot.register_next_step_handler(message, lambda x: add_day_to_list(x, message.text.strip()))

    elif message.text.strip() == "Далее":
        if len(breakfast) + len(lunch) > 0:
            ans = "Вы выбрали:\n"
            for day in days:
                ans += day + ": "
                if day in breakfast:
                    ans += "завтрак "
                if day in lunch:
                    ans += "обед "
                ans += "\n"
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, ans, reply_markup=markup)
            pay_bot(message)

        else:
            bot.send_message(message.chat.id, 'Вы ничего не выбрали')
            choice_day(message)

    elif message.text.strip() == "Назад":
        start(message, False)
        return

    else:
        bot.register_next_step_handler(message, choice_day_finish)


def add_day_to_list(message: Message, day: str):
    if message.text is None:
        bot.register_next_step_handler(message, lambda x: add_day_to_list(x, day))
        return

    if message.text.strip() == 'Завтрак':
        breakfast.add(day)
        choice_day(message)
    elif message.text.strip() == 'Отменить завтрак':
        if day in breakfast:
            breakfast.remove(day)
        choice_day(message)

    elif message.text.strip() == 'Обед':
        lunch.add(day)
        choice_day(message)
    elif message.text.strip() == 'Отменить обед':
        if day in lunch:
            lunch.remove(day)
        choice_day(message)

    elif message.text.strip() == 'И завтрак и обед':
        lunch.add(day)
        breakfast.add(day)
        choice_day(message)
    elif message.text.strip() == 'Отменить и завтрак и обед':
        if day in lunch:
            lunch.remove(day)
        if day in breakfast:
            breakfast.remove(day)
        choice_day(message)

    elif message.text.strip() == "Назад":
        choice_day(message)

    else:
        bot.register_next_step_handler(message, lambda x: add_day_to_list(x, day))


def pay_bot(message):
    days_in_month = dict()
    with open("../DB/days_next.txt") as file:
        for day in days:
            d = file.readline().strip().split(':')[1].split(';')
            d.remove('')
            days_in_month[day] = d

    breakfast_cost, lunch_cost = get_prices()[2:]
    count_lunch = 0
    count_breakfast = 0
    # здесь могут происходить пересчеты дней,
    # если пользователь хочет отказаться от питания в конкретные дни
    for day in days:
        print(day, days_in_month[day])
        if day in breakfast:
            count_breakfast += len(days_in_month[day])
        if day in lunch:
            count_lunch += len(days_in_month[day])
    print(count_breakfast, count_lunch)
    brekfast_final_cost = breakfast_cost * count_breakfast
    lunch_final_cost = lunch_cost * count_lunch
    bot.send_message(message.chat.id, 'Стоимость завтраков:' + str(brekfast_final_cost))
    bot.send_message(message.chat.id, 'Стоимость обедов:' + str(lunch_final_cost))
    bot.send_message(message.chat.id, 'Общая стоимость:' + str((brekfast_final_cost + lunch_final_cost)))
    bot.send_message(message.chat.id, 'Что бы оплатить питание, переведите ' + str((brekfast_final_cost +
                                                                                    lunch_final_cost)) +
                     ' на карту по номеру телефона:  +7**********')
    bot.send_message(message.chat.id, "Для подтверждения оплаты пришлите номер перевода\n(введите 0 для отмены)")
    bot.register_next_step_handler(message, lambda x: get_number(x, brekfast_final_cost + lunch_final_cost))


def get_number(message: Message, sum: int):
    number = message.text
    if not number.isdigit():
        bot.send_message(message.chat.id, 'Номер перевода некорректный\n(введите 0 для отмены)')
        bot.register_next_step_handler(message, lambda x: get_number(x, sum))
        return
    if number == "0":
        start(message, False)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes = types.KeyboardButton("Да")
    no = types.KeyboardButton("Нет")
    reject = types.KeyboardButton("Отмена")
    markup.add(yes)
    markup.add(no)
    markup.add(reject)
    bot.send_message(message.chat.id, 'Уверены, что номер перевода корректен?\n'
                                      '(после подтверждения нельзя будет исправить)', reply_markup=markup)
    bot.register_next_step_handler(message, lambda x: add_to_db(x, number, sum))


def add_to_db(message: Message, number: str, sum: int):
    if message.text == "Да":
        a = dict()
        a["lunch"] = lunch
        a["breakfast"] = breakfast
        bot.send_message(message.chat.id, 'Теперь дождитесь проверки от администратора')
        add_days_to_db(a, message.chat.id, number, sum)
        start(message, False)
    elif message.text == "Отмена":
        start(message, False)
    else:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Введите правильный номер перевода\n(введите 0 для отмены)',
                         reply_markup=markup)
        bot.register_next_step_handler(message, get_number)
