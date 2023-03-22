from loader import db
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def add_group(username):
    url = f"https://t.me/{username}?startgroup=new"
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text="👥 Botni guruhga qo'shish", url=url))
    return markup

confirm = InlineKeyboardMarkup(row_width=2)
confirm.insert(InlineKeyboardButton(text="✅ HA", callback_data="yes"))
confirm.insert(InlineKeyboardButton(text="❌ YO'Q", callback_data="no"))

def show_channel(username):
    return InlineKeyboardMarkup(row_width=1, inline_keyboard=[[InlineKeyboardButton(text="Kanalni ko'rish", url=f"https://t.me/{username}")]])



back_button_inline = InlineKeyboardButton(text="⬅️ Orqaga", callback_data="back")

def payment_markup(providers):
    markup = InlineKeyboardMarkup(row_width=2)
    for provider in providers:
        markup.insert(InlineKeyboardButton(text=provider[1], callback_data=provider[1]))
    markup.row(back_button_inline)
    return markup


def make_price_markup(prices):
    subs_types = InlineKeyboardMarkup(row_width=2)
    subs_types.insert(InlineKeyboardButton(text="Tekin", callback_data="tekin"))
    for price in prices:
        subs_types.insert(InlineKeyboardButton(text=price[2].title(), callback_data=price[2]))
    return subs_types

free_confirm = InlineKeyboardMarkup(row_width=1)
free_confirm.add(InlineKeyboardButton(text="✅ Tushunarli, davom etish", callback_data="continue"))
free_confirm.add(InlineKeyboardButton(text="🔄 Obuna turini o'zgartirish", callback_data="rechange"))


add_subs = InlineKeyboardMarkup(row_width=1)
add_subs.row(InlineKeyboardButton(text="Qo'shish", callback_data="add_true"))
add_subs.row(InlineKeyboardButton(text="Bekor qilish", callback_data="add_false"))