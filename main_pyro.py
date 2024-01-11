import asyncio
import logging
import os
import re
from datetime import datetime
import functools
import pyrogram
from pyrogram import Client, types
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from db_worker import *
from watermark import File, Watermark, apply_watermark
import pathlib
import asyncio
from pyrogram import filters
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from watermark import File, Watermark, apply_watermark, Position
from tokens import *
import pyrostep
from keyboards import *

logging.basicConfig(filename='tg_bot.log', encoding='utf-8', level=logging.INFO)

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=pyro_tok)

pyrostep.listen(app, filters=~filters.command("cancel"))


async def menu_marker(org_file, message, position, opacity, width, rotate):
    #print(message)
    ext = str(pathlib.Path(org_file).suffix)
    file = File(org_file)
    wtm = Watermark(File("VK.png"), pos=position, opacity=opacity, width=width, rotate=rotate)
    out_file = apply_watermark(
        file, wtm, output_file='watered/' + str(message.from_user.id) + '_' + str(message.message.id) + ext)

    return str(out_file)


@app.on_message(filters.command("start"))
async def start(_, msg: types.Message):
    await msg.reply(
        'Hi Welcome!', reply_markup=main_menu)
    # await pyrostep.register_next_step(msg.from_user.id, functools.partial(text_answer))


@app.on_message(filters.photo | filters.video)
async def dump(client, message):
    if 'media' in str(message):
        print(message)
        if message.chat.id == 5976080333:
            org_file = await app.download_media(message)
            ext = str(pathlib.Path(org_file).suffix)
            file = File(org_file)
            wtm = Watermark(File("VK.png"), pos=Position.bottom_right)
            out_file = apply_watermark(
                file, wtm, output_file='watered/' + str(message.chat.id) + '_' + str(message.id) + ext)
            if 'PHOTO' in str(message.media):
                await app.send_photo(message.from_user.id, photo=out_file)
            if 'VIDEO' in str(message.media):
                print(out_file)
                await app.send_video(message.from_user.id, video=out_file,
                                     width=message.video.width,
                                     height=message.video.height)

            os.remove(org_file)
            os.remove(out_file)
    else:
        print(message)


@app.on_message(filters.regex('⚙️ Настроить водяной знак'))
async def text_answer(client, message):
    await app.send_message(chat_id=message.from_user.id, text='Настройка', reply_markup=mark_menu)


@app.on_callback_query()
async def create_mark(client, callback_query):
    if callback_query.data == 'create':
        marked_menu = await menu_marker('w_bg.png', callback_query, Position.bottom_right, '0.5', '0.6', '30')
        await app.delete_messages(chat_id=callback_query.from_user.id,
                                  message_ids=callback_query.message.id)
        await app.send_photo(chat_id=callback_query.from_user.id,
                             photo=marked_menu,
                             caption='Настройте водяной знак', reply_markup=settings_menu)
        os.remove(marked_menu)

        await db_new_watermark(callback_query.from_user.id, 1, None, None, None, None, None)
    if callback_query.data == 'w_bg':
        marked_menu = await menu_marker('w_bg.png', callback_query, Position.bottom_right, '0.5', '0.6', '30')
        await app.edit_message_media(chat_id=callback_query.from_user.id,
                                     message_id=callback_query.message.id,
                                     media=InputMediaPhoto(marked_menu, caption='Настройте водяной знак'),
                                     reply_markup=settings_menu)
        os.remove(marked_menu)
    if callback_query.data == 'd_bg':
        marked_menu = await menu_marker('d_bg.png', callback_query, Position.bottom_right, '0.5', '0.6', '30')
        await app.edit_message_media(chat_id=callback_query.from_user.id,
                                     message_id=callback_query.message.id,
                                     media=InputMediaPhoto(marked_menu, caption='Настройте водяной знак'),
                                     reply_markup=settings_menu)
        os.remove(marked_menu)


# app.add_handler(MessageHandler(dump))

async def main():
    await app.start()
    print("started")

    await pyrostep.safe_idle()
    await app.stop()


app.run(main())
