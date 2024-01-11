import asyncio
import sqlite3
from pytz import timezone
import datetime
from settings import *

conn = sqlite3.connect('users_data.db', timeout=10, check_same_thread=False)
cur = conn.cursor()

# cur.execute("CREATE TABLE IF NOT EXISTS users_data "
#             "(user_id TEXT, watermark TEXT, position TEXT, opacity TEXT, width TEXT, rotate TEXT);")

# cur.execute("DROP TABLE adm_members;")
# cur.execute("DROP TABLE votes;")

# conn.commit()


async def db_new_watermark(user_id, num, watermark, position, opacity, width, rotate):
    cur.execute("CREATE TABLE IF NOT EXISTS users_data "
                "(user_id TEXT, num TEXT, watermark TEXT, position TEXT, opacity TEXT, width TEXT, rotate TEXT);")
    conn.commit()

    cur.execute("INSERT INTO users_data (user_id, num, watermark, position, opacity, width, rotate) VALUES('" + str(user_id) + "', '" + str(num) + "', '" + str(watermark) + "', '" + str(position) + "', '" +
                str(opacity) + "', '" + str(width) + "', '" + str(rotate) + "')")
    conn.commit()


async def db_show_all_table():
    cur.execute("select * from users_data")
    rows = cur.fetchall()
    return rows

# db_new_watermark(1234, None, None, None, None, None)