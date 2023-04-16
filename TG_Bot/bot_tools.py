from TG_Bot import bot


def reject(tg_id: int):
    bot.bot.send_message(tg_id, "!!Ваша оплата некорректна!!")


def accept(tg_id: int):
    bot.bot.send_message(tg_id, "Ваша оплата принята")
