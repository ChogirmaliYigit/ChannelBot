import sqlite3
from keyboards.inline.markup import add_group
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.default.main import markup
from data.config import ADMINS
from loader import dp, db, bot
from filters import IsPrivate

@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    name = message.from_user.full_name
    data = await bot.get_me()
    bot_username = data.username
    user_id = message.from_user.id
    if not name.startswith("<") and not name.endswith(">"):
        # Foydalanuvchini bazaga qo'shamiz
        try:
            db.add_user(id=user_id, name=name)
            if str(user_id) in ADMINS:
                await message.answer(f"Xush kelibsiz! {name}", reply_markup=markup)
            else:
                inline_markup = add_group(username=bot_username)
                await message.answer(f"Xush kelibsiz! {name}\n\nBu botdan faqat guruhlarda foydalanishingiz mumkin.", reply_markup=inline_markup)
            # Adminga xabar beramiz
            count = db.count_users()[0]
            msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
            await bot.send_message(chat_id=ADMINS[0], text=msg)

        except sqlite3.IntegrityError as err:
            await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
            if str(user_id) in ADMINS:
                await message.answer(f"Xush kelibsiz! {name}", reply_markup=markup)
            else:
                inline_markup = add_group(username=bot_username)
                await message.answer(f"Xush kelibsiz! {name}\n\nBu botdan faqat guruhlarda foydalanishingiz mumkin.", reply_markup=inline_markup)

        except Exception as err:
            await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
            if str(user_id) in ADMINS:
                await message.answer(f"Xush kelibsiz! {name}", reply_markup=markup)
            else:
                inline_markup = add_group(username=bot_username)
                await message.answer(f"Xush kelibsiz! {name}\n\nBu botdan faqat guruhlarda foydalanishingiz mumkin.", reply_markup=inline_markup)
    else:
        if str(user_id) in ADMINS:
            await message.answer(f"Xush kelibsiz!", reply_markup=markup)
        else:
            if message.from_user.username:
                await bot.send_message(chat_id=ADMINS[0], text=f"@{message.from_user.username} bazaga oldin qo'shilgan yoki qo'shildi!")
                inline_markup = add_group(username=bot_username)
                await message.answer(f"Xush kelibsiz!\n\nBu botdan faqat guruhlarda foydalanishingiz mumkin.", reply_markup=inline_markup)
            else:
                await bot.send_message(chat_id=ADMINS[0], text=f"{message.from_user.id} bazaga oldin qo'shilgan yoki qo'shildi!")
