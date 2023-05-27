# twitter-bot/services/database_service.py
import os

from dotenv import load_dotenv

load_dotenv()

bot_id = os.environ.get('BOT_ID')
bot_target_country = os.environ.get('BOT_TARGET_COUNTRY')


def get_item_from_db(db_connection, item_table):
    cursor = db_connection.cursor(buffered=True)
    query = f"SELECT name FROM {item_table} WHERE bot_id=%s"
    cursor.execute(query, [bot_id])
    result = cursor.fetchall()
    items = []
    for item in result:
        items.append(item[0])

    return items


def get_universities_from_db(db_connection):
    cursor = db_connection.cursor(buffered=True, dictionary=True)
    query = "SELECT name FROM universities WHERE (bot_id=%s AND country=%s)"
    cursor.execute(query, (bot_id, bot_target_country))
    result = cursor.fetchall()
    universities = []
    for item in result:
        universities.append(item[0])

    return universities


def count_item_in_db(db_conn, item_table):
    cursor = db_conn.cursor(buffered=True)
    query = f"SELECT COUNT(*) FROM {item_table} WHERE bot_id=%s"
    cursor.execute(query, [bot_id])

    return cursor.fetchone()
