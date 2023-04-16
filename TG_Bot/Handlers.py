from aiogram import types, Dispatcher


def set_handlers(dp: Dispatcher):
    """настраиваем логику работы бота"""
    @dp.message_handler(commands=['start', 'help'])
    async def send_welcome(message: types.Message):
        await message.reply("Hi!\nI'm Bot!\nMade by Developers-YL.")

    @dp.message_handler()
    async def echo(message: types.Message):
        await message.answer(message.text)
