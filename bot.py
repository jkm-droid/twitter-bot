# twitter-bot/bot.py

import logging
import time

from configs.config import create_api
from configs.database import create_db_connection
from constants import constants
from logger import log
from services import bot_service,media_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

"""function for creating the API"""
"""And sending the tweet"""


def main():
    log("connecting...please wait", constants.msg_info)
    api = create_api()
    if api:
        while True:
            try:
                db_connection = create_db_connection()
                result = bot_service.initialize_bot(db_connection)
                init_msg = result['initialized']
                if init_msg == 0:
                    log("Some errors occurred when initializing bot. See more details in the error logs file",
                        constants.msg_error)
                    break
                elif init_msg == 1:
                    bot_service.send_tweet(api, db_connection)
                else:
                    log("An error occurred when initializing bot", constants.msg_error)
            except Exception as e:
                log(f"An exception occurred {e}", constants.msg_error)
                time.sleep(100)
    else:
        log("Connection to the api could not be established", constants.msg_error)


if __name__ == "__main__":
    main()
