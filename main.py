import io
import os
from multiprocessing import Process

from apscheduler.jobstores.redis import RedisJobStore
from watermark import File, Watermark, apply_watermark, Position
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from tokens import *
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, executor
import logging
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from sqlalchemy import create_engine
import psycopg2

# https://github.com/aahnik/telewater
# https://pypi.org/project/watermark.py/

engine = create_engine('postgresql://localhost:5432/sega')

loop = asyncio.get_event_loop()

storage = RedisStorage2()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_tok)
dp = Dispatcher(bot, storage=storage)

# job_stores = {
#     "default": SQLAlchemyJobStore(engine=engine)}

job_stores = {
    "default": RedisJobStore(
        jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running",
    )
}

scheduler = AsyncIOScheduler(jobstores=job_stores)
scheduler.start()


async def marker(file, media_type, chat_id):
    final_file = File(file)
    #watermark = Watermark(File("watermark.png"), pos=Position.bottom_centre)
    watermark = Watermark(File("Logo 1.png"), pos=Position.centre)
    final_media = apply_watermark(final_file, watermark)
    os.remove(file)
    print(final_media)
    if media_type == 'photo':
        await bot.send_photo(chat_id=chat_id, photo=open(final_media, 'rb'))
        os.remove(final_media)
    if media_type == 'video':
        await bot.send_video(chat_id=chat_id, video=open(final_media, 'rb'))
        os.remove(final_media)

@dp.message_handler(content_types=['photo'])
async def media_handler(message: types.Message):
    file_name = str(message.from_user.id) + '_' + str(message.message_id) + '.jpg'
    await message.photo[-1].download(destination_file=file_name, make_dirs=True)
    scheduler.add_job(marker, args=(file_name, 'photo', message.from_user.id,),
                      next_run_time=datetime.now(),
                      timezone='Asia/Yekaterinburg')


@dp.message_handler(content_types=['video'])
async def media_handler(message: types.Message):
    file_name = str(message.from_user.id) + '_' + str(message.message_id) + '.mp4'
    await message.video.download(destination_file=file_name, make_dirs=True)
    scheduler.add_job(marker, args=(file_name, 'video', message.from_user.id,),
                      next_run_time=datetime.now(),
                      timezone='Asia/Yekaterinburg')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
