from aiogram.dispatcher.filters.state import State, StatesGroup


class Controls(StatesGroup):
    add_channel = State()
    ads = State()
    send_text = State()
    send_photo = State()
    send_sticker = State()
    send_document = State()
    send_location = State()
    send_audio = State()
    send_video = State()
    send_voice = State()
    send_contact = State()
    add_group = State()
    provider_title = State()
    provider_token = State()
    subs_type = State()
    get_paid = State()
    type_free = State()
    sub_type_add = State()
    price_add = State()
    add_price_confirm = State()