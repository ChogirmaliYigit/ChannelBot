from aiogram import types
from keyboards.inline.markup import add_group
from loader import dp, bot
from filters import IsPrivate

# Echo bot
@dp.message_handler(IsPrivate(), state=None)
async def bot_echo(message: types.Message):
    data = await bot.get_me()
    bot_username = data.username
    markup = add_group(username=bot_username)
    await message.answer("Bu botdan faqat guruhlarda foydalanishingiz mumkin.", reply_markup=markup)
