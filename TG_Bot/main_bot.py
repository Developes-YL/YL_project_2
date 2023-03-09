import os
import sys
import logging

from aiogram import Dispatcher, executor

from TG_Bot.CanteenMephibot import CanteenMephiBot
from TG_Bot.Handlers import set_handlers
from TG_Bot.Support.variables import FILE

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = CanteenMephiBot(FILE)
    dispatcher = Dispatcher(bot)
    set_handlers(dispatcher)
    executor.start_polling(dispatcher, skip_updates=True)
