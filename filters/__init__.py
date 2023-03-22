from aiogram import Dispatcher

from loader import dp
from .is_admin import AdminFilter
from .is_group import IsGroup
from .is_private import IsPrivate
from .channel_post import ChannelPost

if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(ChannelPost)