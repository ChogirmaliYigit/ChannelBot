import asyncio
from loader import dp, db
from aiogram import types
from filters import ChannelPost


@dp.channel_post_handler(ChannelPost(), content_types=types.ContentTypes.ANY)
async def forward_all_messages(message: types.Message):
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await message.bot.forward_message(chat_id=group[1], from_chat_id=message.chat.id, message_id=message.message_id)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass