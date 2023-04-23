import logging
import os
import time
from datetime import datetime

from dotenv import load_dotenv

from constants import constants
from helpers.helper import generate_tweet
from services import media_service, database_service

load_dotenv()

bot_id = os.environ.get('BOT_ID')
bot_name = os.environ.get('BOT_NAME')
bot_target_country = os.environ.get('BOT_TARGET_COUNTRY')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# function for sending the tweet
def send_tweet(api, db_connection):
    my_tweet = generate_tweet(db_connection)

    # send the tweet message
    logger.info("sending tweet...")
    image = media_service.attach_file_to_tweet()
    api.update_with_media(filename=image, status=my_tweet)
    logger.info("Tweet sent successfully")

    # save the tweets posted to a file
    logger.info("saving tweet...")
    current_data_time = datetime.now()
    date = current_data_time.strftime("%Y-%m-%d %H:%M")
    with open(f"{constants.bot_name}_logs.txt", 'a', encoding="utf-8") as f:
        f.write(f"\nPosted on {date} \n\n")
        f.write(my_tweet)
        f.write("\n************************************************************************************\n")
        f.close()

    logger.info("Tweet saved successfully")
    logger.info("sleeping...")
    logger.info("\n")

    # setting interval between tweets
    time.sleep(600)


def initialize_bot(db_connection):
    # first check the bot if bot exists
    cursor = db_connection.cursor()
    query = "SELECT * FROM bots WHERE id=%s"
    cursor.execute(query, [bot_id])
    bot_details = cursor.fetchone()
    cursor.close()
    if bot_details is not None:
        # check the bot initialization status
        init_status = bot_details[6]
        if init_status == 0:
            # check all associated tables  data
            result = check_all_bot_tables_for_data(db_connection)
            return result
        else:
            return {
                "initialized": 1,
                "errors": []
            }
    else:
        errors = [f"Bot not found. Invalid bot id {bot_id} set up in the env"]
        save_initialization_errors_to_file(errors)
        return {
            "initialized": 0,
            "errors": errors
        }


def check_all_bot_tables_for_data(db_conn):
    keywords = database_service.count_item_in_db(db_conn, "keywords")[0]
    subjects = database_service.count_item_in_db(db_conn, "subjects")[0]
    headings = database_service.count_item_in_db(db_conn, "headings")[0]
    slogans = database_service.count_item_in_db(db_conn, "slogans")[0]
    hashtags = database_service.count_item_in_db(db_conn, "hashtags")[0]
    errors = []
    if keywords <= 4:
        errors.append(f"insufficient keywords in db. add {5 - keywords} more keywords to proceed")

    if subjects <= 4:
        errors.append(f"insufficient subjects in db. add {5 - subjects} more subjects to proceed")

    if headings <= 4:
        errors.append(f"insufficient headings in db. add {5 - headings} more heading to proceed")

    if slogans <= 4:
        errors.append(f"insufficient slogans in db. add {5 - slogans} more slogans to proceed")

    if hashtags <= 4:
        errors.append(f"insufficient hashtags in db. add {5 - hashtags} more hashtags to proceed")

    if len(errors) > 0:
        save_initialization_errors_to_file(errors)
        return {
            "initialized": 0,
            "errors": errors
        }
    else:
        cursor = db_conn.cursor()
        query = "UPDATE bots SET is_initialized=%s WHERE bot_id=%s"
        cursor.execute(query, (1, bot_id))
        db_conn.commit()
        cursor.close()

        return {
            "initialized": 1,
            "errors": errors
        }


def save_initialization_errors_to_file(errors):
    current_data_time = datetime.now()
    date = current_data_time.strftime("%Y-%m-%d %H:%M")
    with open(f"{bot_name.replace('-', '_')}_initialization_errors", 'a', encoding="utf-8") as f:
        f.write(f"{bot_name} initialization errors on {date} \n")
        for error in errors:
            f.write(f"ERROR: {error}\n")
            f.write("\n")
        f.close()
