#nortontutors/tweet.py

import tweepy
import logging
import time
import random

import botconstants
from helper import generate_tweet
from config import create_api
from datetime import datetime
from location import get_trends_by_location
import os

#logging logic
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger()

"""function for sending the tweet"""
def send_tweet(api):
	my_tweet = generate_tweet()

	#send the tweet message
	logger.info("sending tweet...")

	media_list = []
	for dirpath, dirnames, files in os.walk("/home/jkmdroid/python-bots/twitter/nortontutors_v1/filenames"):
	    for f in files:
	        media_list.append(os.path.join(dirpath, f))
	image = random.choice(media_list)

	api.update_with_media(filename=image, status=my_tweet)

	logger.info("Tweet sent successfully")

	#save the tweets posted to a file
	logger.info("saving tweet...")

	current_data_time = datetime.now()
	date = current_data_time.strftime("%Y-%m-%d %H:%M")

	with open(f"{botconstants.bot_name}_logs.txt", 'a', encoding="utf-8") as f:
		f.write(f"\nPosted on {date} \n\n")
		f.write(my_tweet)
		f.write("\n************************************************************************************\n")
		f.close()

	logger.info("Tweet saved successfully")

	logger.info("sleeping...")
	logger.info("\n")

	#setting interval between tweets
	time.sleep(600)

"""function for creating the API"""
"""And sending the tweet"""
def main():
	api = create_api()
	while True:
		send_tweet(api)
		
if __name__ == "__main__":
	main()