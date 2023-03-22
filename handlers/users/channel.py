import sqlite3
import aiogram
import asyncio
from loader import dp, db, bot
from aiogram import types
from data.config import ADMINS
from states.state import Controls
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from keyboards.default.main import markup
from keyboards.inline.markup import confirm, add_group, show_channel
from filters import IsPrivate

@dp.message_handler(IsPrivate(), text="➕ Kanal qo'shish", user_id=ADMINS, state="*")
async def add_channel(message: types.Message):
    await message.answer(text="Kanalingiz linkini @ belgisi bilan yuboring. Namuna: @username", reply_markup=ReplyKeyboardRemove())
    await Controls.add_channel.set()


@dp.message_handler(IsPrivate(), state=Controls.add_channel, user_id=ADMINS)
async def get_channel_link(message: types.Message, state: FSMContext):
    channel_url = message.text
    try:
        channel = await message.bot.get_chat(channel_url)
        db.add_channel(user_id=message.from_user.id, channel_id=int(channel.id), title=channel.title, username=channel.username)
        await message.answer(text=f"{channel.title} bazaga muvaffaqiyatli qo'shildi.", reply_markup=markup)
    except sqlite3.Error as error:
        await message.answer(text=f"{channel.title} kanali oldin bazaga qo'shilgan.", reply_markup=markup)
    except aiogram.utils.exceptions.ChatNotFound:
        await message.answer(text="Bunday kanal telegramda mavjud emas.", reply_markup=markup)
    finally:
        await state.finish()

@dp.message_handler(text="➕ Guruh qo'shish", user_id=ADMINS, state="*")
async def add_group_to_db(message: types.Message):
    data = await bot.get_me()
    bot_username = data.username
    await message.answer(text="Botni guruhga qo'shish uchun pastdagi tugmani bosing.", reply_markup=add_group(bot_username))


@dp.message_handler(IsPrivate(), text="📕 Kanallar ro'yxati", user_id=ADMINS, state="*")
async def get_channel_list(message: types.Message, state: FSMContext):
    global channels
    channels = db.select_all_channels(user_id=message.from_user.id)
    # text = ""
    if channels == None:
        await message.answer(text="Siz hali kanal qo'shmagansiz")
    for channel in channels:
        text = f"<b>{channel[0]})</b>\n<i>ID: {channel[2]}\nTITLE: {channel[3]}</i>"
        if channel[4] != None:
            text += f"\n<i>USERNAME: {channel[4]}</i>"
            await message.answer(text=text, parse_mode="html", reply_markup=show_channel(channel[4]))
        else:
            await message.answer(text=text, parse_mode="html")

@dp.message_handler(text="📘 Guruhlar ro'yxati", user_id=ADMINS, state="*")
async def get_groups_list(message: types.Message):
    groups = db.select_all_groups(user_id=message.from_user.id)
    if groups == None:
        await message.answer(text="Siz hali guruh qo'shmagansiz")
    for group in groups:
        await message.answer(text=f"<b>{group[0]})</b>\n<i>ID: {group[1]}\nTITLE: {group[2]}</i>", parse_mode="html")

@dp.message_handler(text="🗣 Reklama", user_id=ADMINS, state="*")
async def get_ads(message: types.Message):
    await message.answer(text="Menga reklama uchun matn, rasm, stiker, hujjat yoki joylashuv jo'nating va men uni guruhlarga tarqataman.", reply_markup=ReplyKeyboardRemove())
    await Controls.ads.set()


@dp.message_handler(state=Controls.ads, user_id=ADMINS)
async def get_ads_content(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_xabari": message.text})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_text.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["photo"])
async def get_ads_photo(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_rasmi": message.photo[-1].file_id})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_photo.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["sticker"])
async def get_ads_sticker(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_stikeri": message.sticker.file_id})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_sticker.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["document"])
async def get_ads_document(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_hujjati": message.document.file_id})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_document.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["location"])
async def get_ads_location(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_joylashuv_kengligi": message.location.latitude, "reklama_joylashuv_uzunligi": message.location.longitude})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_location.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["audio"])
async def get_ads_document(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_audiosi": message.audio.file_id})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_audio.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["video"])
async def get_ads_document(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_videosi": message.video.file_id})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_video.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["voice"])
async def get_ads_document(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_voicesi": message.voice.file_id})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_voice.set()

@dp.message_handler(state=Controls.ads, user_id=ADMINS, content_types=["contact"])
async def get_ads_document(message: types.Message, state: FSMContext):
    await state.set_data(data={"reklama_kontakt_raqami": message.contact.phone_number, "reklama_kontakt_ismi": message.contact.first_name})
    await message.reply(text="Buni tarqatishga aminmisiz", reply_markup=confirm)
    await Controls.send_contact.set()

@dp.callback_query_handler(text="yes", state=Controls.send_text)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("reklama_xabari")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_message(chat_id=group[1], text=text)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_photo)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    photo = data.get("reklama_rasmi")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_photo(chat_id=group[1], photo=photo)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_sticker)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sticker = data.get("reklama_stikeri")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_sticker(chat_id=group[1], sticker=sticker)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_document)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    document = data.get("reklama_hujjati")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_document(chat_id=group[1], document=document)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_location)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    latitude = data.get("reklama_joylashuv_kengligi")
    longitude = data.get("reklama_joylashuv_uzunligi")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_location(chat_id=group[1], latitude=latitude, longitude=longitude)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_audio)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    audio = data.get("reklama_audiosi")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_audio(chat_id=group[1], audio=audio)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_video)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    video = data.get("reklama_videosi")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_video(chat_id=group[1], video=video)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_voice)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    voice = data.get("reklama_voicesi")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_voice(chat_id=group[1], voice=voice)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="yes", state=Controls.send_contact)
async def get_confirm_res(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    phone = data.get("reklama_kontakt_raqami")
    name = data.get("reklama_kontakt_ismi")
    try:
        groups = db.select_all_groups(user_id=call.from_user.id)
        for group in groups:
            await bot.send_contact(chat_id=group[1], phone_number=phone, first_name=name)
            await asyncio.sleep(0.05)
    except Exception as error:
        pass
    finally:
        await call.message.delete()
        await call.message.answer(text="✅ Xabar guruhlarga muvaffaqiyatli jo'natildi! ✅", reply_markup=markup)
        await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_text)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_photo)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_sticker)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_document)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_location)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_audio)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_video)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_voice)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()

@dp.callback_query_handler(text="no", state=Controls.send_contact)
async def res_confirm(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(text="❌ Reklama tarqatish bekor qilindi. ❌", reply_markup=markup)
    await state.finish()