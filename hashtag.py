# twitter-bot/hashtag.py

import logging

from configs.config import create_api
from configs.database import create_db_connection
from services.hashtag_service import get_trends_by_location

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

if __name__ == "__main__":
    api = create_api()

    while True:
        try:
            conn = create_db_connection()
            get_trends_by_location(api, conn)
        except Exception as e:
            logger.error('An error occurred getting hashtags', e)
