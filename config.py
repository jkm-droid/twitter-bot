#nortontutors/config.py

import tweepy
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger()

def create_api():
	#getting the required keys and tokens from environment
	API_KEY = os.getenv('API_KEY')
	API_SECRET_KEY = os.getenv('API_SECRET_KEY')
	ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
	ACCESS_SECRET_TOKEN = os.getenv('ACCESS_SECRET_TOKEN')

	#Authenticating to twitter account
	auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)

	#creating API object
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	try:
		api.verify_credentials()
		username = api.me()
	except Exception as e:
		logger.error("Error creating API", exc_info=true)
		raise e

	logger.info("API created")
	logger.info(username.name)

	return api
