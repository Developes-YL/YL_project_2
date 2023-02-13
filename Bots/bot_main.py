import os
import sys
import logging

from aiogram import Dispatcher, executor

from Bots.CanteenMephibot import CanteenMephiBot
from Bots.Handlers import set_handlers

FILE = 'token.txt'  # сам файл в репозитории отсутствует для его сохранности


def new_path(name: str = ''):
    """функция для обновления пути до файла при конвертации в .exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, name)
    return os.path.join(name)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = CanteenMephiBot(new_path(FILE))
    dispatcher = Dispatcher(bot)
    set_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True)
