#nortontutors/helper.py

import random
import botconstants
from googletrans import Translator, constants

translator = Translator()

"""read keywords randomly from a file"""
"""return two unique keywords"""
def get_unique_keyword_list():
	open_file = open('keywords.txt').read().splitlines()
	keywords = random.sample(list(open_file), 2)
	formatted_keywords = ''
	for keyword in range(len(keywords)):
		my_keyword = keywords[keyword]
		my_keyword = translate_to_arabic(my_keyword)
		formatted_keywords += "#{key}\n".format(key=my_keyword)

	return formatted_keywords

"""get random subjects from a file"""
"""return the random subject"""
def get_unique_subject_list():
	open_file = open('subjects.txt').read().splitlines()
	subjects = random.sample(list(open_file), 5)
	formatted_subjects = ''
	for subject in range(len(subjects)):
		my_subject = subjects[subject]
		my_subject = translate_to_arabic(my_subject)
		formatted_subjects += "#{sub}\n".format(sub=my_subject)

	return formatted_subjects

"""function to get random headings from a file"""
"""and return a random heading"""
def get_random_heading():
	open_file = open('headings.txt').read().splitlines()
	heading = random.choice(open_file)

	heading = translate_to_arabic(heading)

	return heading

def get_random_slogan():
	open_file = open('slogan.txt').read().splitlines()
	slogan = random.choice(open_file)

	slogan = translate_to_arabic(slogan)

	return slogan

def get_random_hashtag():
	open_file = open('hashtags.txt', encoding="utf-8").read().splitlines()
	hashtags = random.choice(open_file)

	return hashtags

"""get random university"""
"""return a single university"""
def get_random_university():
	open_file = open('university.txt').read().splitlines()
	university = random.choice(open_file)

	return university

"""generate a new tweet"""
def generate_tweet():
	#get the generated heading 1
	heading = get_random_heading()
	slogan = get_random_slogan()

	hashtag = ''.join(char for char in get_random_hashtag().replace(" ", "") if char.isalnum())

	hashtag1 = ''.join(char for char in get_random_hashtag().replace(" ", "") if char.isalnum())

	university = ''.join(char for char in get_random_university().replace(" ", "") if char.isalnum())

	#embed the keyword in the tweet message
	my_tweet =  "{heading}\n{slogan}\n{subjects}{keywords}#{university}\n#{hashtag}\n#{hashtag1}\n{end}" \
		.format(
		heading=heading,
		slogan=slogan,
		subjects=get_unique_subject_list(),
		keywords=get_unique_keyword_list(),
		university=university,
		hashtag=hashtag,
		hashtag1=hashtag1,
		end=translate_to_arabic("KINDLY DM")
		)

	print(f"Before check:{len(my_tweet)}")
	if len(my_tweet) > 278:
		generate_tweet()

	print(f"After check:{len(my_tweet)}")
	return my_tweet

def translate_to_arabic(message):
	if botconstants.translate:
		translated_message = translator.translate(message,dest=botconstants.language)
		
		return translated_message.text
	else:
		return message