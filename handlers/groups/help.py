from aiogram import types
from filters import IsGroup, AdminFilter
from loader import dp
from aiogram.dispatcher.filters import Command

@dp.message_handler(IsGroup(), Command("help", prefixes="!/"), AdminFilter())
async def do_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    
    await message.answer("\n".join(text))

@dp.message_handler(IsGroup(), Command("help", prefixes="!/"))
async def do_help(message: types.Message):
    await message.reply(text="Bu botdan faqat admin foydalana oladi.")