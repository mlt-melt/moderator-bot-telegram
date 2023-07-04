from config import dp, admins
from textsConfig import *
from aiogram import types
from states import *

@dp.message_handler(commands='start')
async def startCmd(message: types.Message):
    if message.from_user.id in admins:
        await message.answer("Hello, i'm chat management bot. I keep track of content and don't allow dangerous and harmful\n\nAdmin panel with settings by the comand /admin")
    else:
        await message.answer("Hello, i'm chat management bot. I keep track of content and don't allow dangerous and harmful")

@dp.message_handler(commands='id')
async def idCmd(message: types.Message):
    if message.from_user.id in admins:
        await message.answer(f"Chat id: <code>{message.chat.id}</code>")
