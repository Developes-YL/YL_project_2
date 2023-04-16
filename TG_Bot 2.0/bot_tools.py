import bot


def reject(tg_ids: list):
    for tg_id in tg_ids:
        bot.bot.send_message(tg_id, "!!Ваша оплата некорректна!!")


def accept(tg_ids: list):
    for tg_id in tg_ids:
        bot.bot.send_message(tg_id, "Ваша оплата принята")
