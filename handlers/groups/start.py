import sqlite3
from aiogram import types
from filters import IsGroup, AdminFilter
from loader import dp, db
from aiogram.dispatcher.filters import Command

@dp.message_handler(IsGroup(), Command("start", prefixes="!/"), AdminFilter())
async def add_group(message: types.Message):
    chat_id = message.chat.id
    title = message.chat.title
    try:
        db.add_group(user_id=message.from_user.id, group_id=chat_id, title=title)
        await message.answer(text=f"{title} guruhi bazaga muvaffaqiyatli qo'shildi.")
    except sqlite3.Error as error:
        await message.answer(text=f"{title} guruhi oldin bazaga qo'shilgan.")

@dp.message_handler(IsGroup(), Command("start", prefixes="!/"))
async def do_help(message: types.Message):
    await message.reply(text="Bu botdan faqat admin foydalana oladi.")