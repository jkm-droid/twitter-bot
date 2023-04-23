import os
import random


def attach_file_to_tweet():
    path = f"{os.getcwd()}/filenames"
    media_list = []
    for dirpath, dirnames, files in os.walk(path):
        for f in files:
            media_list.append(os.path.join(dirpath, f))
    image = random.choice(media_list)

    return image
