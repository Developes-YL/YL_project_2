import sys

from aiogram import Bot
from aiogram.utils.exceptions import ValidationError


class CanteenMephiBot(Bot):
    """доработанная версия класса Bot для чтения токена из файла и для его проверки"""
    def __init__(self, file_name: str):
        try:
            with open(file_name, 'r') as f:
                self.token = f.read()
        except FileNotFoundError:
            print('файл с токеном не найден')
            sys.exit()

        try:
            super().__init__(token=self.token)
        except ValidationError:
            print('неверный токен')
            sys.exit()
