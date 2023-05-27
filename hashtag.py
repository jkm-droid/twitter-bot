from configs.twitter import create_api
from configs.database import create_db_connection
from logger import _logger
from services.hashtag_service import get_trends_by_location

if __name__ == "__main__":
    api = create_api()

    while True:
        try:
            conn = create_db_connection()
            get_trends_by_location(api, conn)
        except Exception as e:
            _logger().error(f'An error occurred getting hashtags {e}', exc_info=True)
