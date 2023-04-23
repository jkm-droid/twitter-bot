# twitter-bot/helper.py

import random

from googletrans import Translator

from constants import constants
from services import database_service

translator = Translator()

"""read keywords randomly from a file"""
"""return two unique keywords"""


def get_unique_keyword_list(db_connection):
    db_keywords = database_service.get_item_from_db(db_connection, "keywords")

    keywords = random.sample(list(db_keywords), 2)
    formatted_keywords = ''
    for keyword in range(len(keywords)):
        my_keyword = keywords[keyword]
        my_keyword = translate_to_arabic(my_keyword)
        formatted_keywords += "#{key}\n".format(key=my_keyword)

    return formatted_keywords


"""get random subjects from a file"""
"""return the random subject"""


def get_unique_subject_list(db_connection):
    db_subjects = database_service.get_item_from_db(db_connection, "subjects")

    subjects = random.sample(list(db_subjects), 5)
    formatted_subjects = ''
    for subject in range(len(subjects)):
        my_subject = subjects[subject]
        my_subject = translate_to_arabic(my_subject)
        formatted_subjects += "#{sub}\n".format(sub=my_subject)

    return formatted_subjects


"""function to get random headings from a file"""
"""and return a random heading"""


def get_random_heading(db_connection):
    db_headings = database_service.get_item_from_db(db_connection, "headings")
    # open_file = open('headings.txt', encoding="utf-8").read().splitlines()
    heading = random.choice(db_headings)

    heading = translate_to_arabic(heading)

    return heading


def get_random_slogan(db_connection):
    db_slogans = database_service.get_item_from_db(db_connection, "slogans")
    slogan = random.choice(db_slogans)

    slogan = translate_to_arabic(slogan)

    return slogan


def get_random_hashtag(db_connection):
    db_hashtags = database_service.get_item_from_db(db_connection, "hashtags")
    hashtags = random.choice(db_hashtags)

    return hashtags


"""get random university"""
"""return a single university"""


def get_random_university(db_connection):
    db_universities = database_service.get_universities_from_db(db_connection)
    university = random.choice(db_universities)

    return university


"""generate a new tweet"""


def generate_tweet(db_connection):
    # get the generated heading 1
    heading = get_random_heading(db_connection)
    slogan = get_random_slogan(db_connection)

    hashtag = ''.join(char for char in get_random_hashtag(db_connection).replace(" ", "") if char.isalnum())

    hashtag1 = ''.join(char for char in get_random_hashtag(db_connection).replace(" ", "") if char.isalnum())

    university = ''.join(char for char in get_random_university(db_connection).replace(" ", "") if char.isalnum())

    # embed the keyword in the tweet message
    my_tweet = "{heading}\n{slogan}\n{subjects}{keywords}#{university}\n#{hashtag}\n#{hashtag1}\n{end}" \
        .format(
        heading=heading,
        slogan=slogan,
        subjects=get_unique_subject_list(db_connection),
        keywords=get_unique_keyword_list(db_connection),
        university=university,
        hashtag=hashtag,
        hashtag1=hashtag1,
        end=translate_to_arabic("KINDLY DM")
    )

    print(f"Before check:{len(my_tweet)}")
    if len(my_tweet) > 278:
        generate_tweet(db_connection)

    print(f"After check:{len(my_tweet)}")
    return my_tweet


def translate_to_arabic(message):
    if constants.translate:
        translated_message = translator.translate(message, dest=constants.language)

        return translated_message.text
    else:
        return message
