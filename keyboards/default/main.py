from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.row("➕ Kanal qo'shish", "➕ Guruh qo'shish")
markup.row("📕 Kanallar ro'yxati", "📘 Guruhlar ro'yxati")
markup.row("🗣 Reklama")
markup.add(KeyboardButton(text="Guruhlarda ishlovchi bot yasash qo'llanmasi", web_app=WebAppInfo(url="https://bekzod030900.gitbook.io/django/guruhlarda-ishlaydigan-bot")))

