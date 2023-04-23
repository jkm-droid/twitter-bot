import os
import random


def attach_file_to_tweet():
    media_list = []
    for dirpath, dirnames, files in os.walk("/home/jkmdroid/python-bots/twitter/nortontutors_v1/filenames"):
        for f in files:
            media_list.append(os.path.join(dirpath, f))
    image = random.choice(media_list)

    return image
