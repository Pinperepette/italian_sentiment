#!/usr/bin/env python

from pkg_resources import resource_filename
import pickle

emoji_dict_path = resource_filename('italian_sentiment', 'files/emoji_dict.pkl')

with open(emoji_dict_path, 'rb') as f:
    emoji_dict = pickle.load(f)

def translate_emoji(text):
    for emoji, translation in emoji_dict.items():
        text = text.replace(emoji, translation)
    return text
