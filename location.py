#nortontutors/location.py

import tweepy
import logging
import time
import random
# import geocoder
from config import create_api
from datetime import datetime

#logging logic
logging.basicConfig(level = logging.INFO)
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
		return(0)

def get_trends_by_location(location_id, api):
	logger.info('Getting latest trends...')
	try:
		trends = api.trends_place(location_id)
		with open('hashtags.txt', 'w', encoding="utf-8") as file:
			for tr in trends[0]['trends']:
				file.write(tr['name'])
				file.write("\n")

	except Exception as e:
		print('An Exception', e)
	logger.info("saved latest trends")
	logger.info("sleeping...")
	logger.info("\n")
	time.sleep(350)

if __name__ == "__main__":
	api = create_api()

	#saudi arabia - 23424938
	#usa - 23424977
	#israel - 23424852
	while True:
		get_trends_by_location(23424938, api)
