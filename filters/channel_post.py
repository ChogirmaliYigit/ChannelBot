from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import db

class ChannelPost(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        channels = db.select_all_channels(user_id=message.from_user.id)
        if message.chat.type == types.ChatType.CHANNEL:
            channel_id = message.chat.id
            for channel in channels:
                if channel[1] == channel_id:
                    return True
        return False
