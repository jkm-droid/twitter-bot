# twitter-bot/services/hashtag_service.py
import logging
import time
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

bot_id = os.environ.get('BOT_ID')
bot_target_country_code = os.environ.get('BOT_TARGET_COUNTRY_CODE')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_woeid_of_place(country, api):
    try:
        trending = api.trends_available()
        for trend in trending:
            if (trend['name'].lower() == country.lower()):
                # print(trend['woeid'])
                return trend['woeid']

        print("location not found")

    except Exception as e:
        print('Exception', e)
        return (0)


def get_trends_by_location(api, db_connection):
    logger.info('Getting latest trends...')

    result = api.trends_place(bot_target_country_code)
    trends = result[0]['trends']
    if len(trends) > 0:
        delete_cursor = db_connection.cursor(buffered=True)
        delete_query = "DELETE FROM hashtags WHERE bot_id=%s"
        delete_cursor.execute(delete_query, [bot_id])
        db_connection.commit()
        delete_cursor.close()

        query = "INSERT INTO hashtags (bot_id, name, created_at,updated_at) VALUES (%s,%s,%s,%s)"
        hashtag_details = []
        for tr in trends:
            current_data_time = datetime.now()
            date = current_data_time.strftime("%Y-%m-%d %H:%M")
            details = (bot_id, tr['name'], date, date)
            hashtag_details.append(details)

        try:
            cursor = db_connection.cursor(buffered=True)
            cursor.executemany(query, hashtag_details)
            db_connection.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"An error occurred while saving hashtags {e}")

        logger.info("saved latest trends")
        logger.info("sleeping...")
        logger.info("\n")
        time.sleep(350)
