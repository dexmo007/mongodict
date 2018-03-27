import json
import os


def load_dictionary(lang: str):
    filename = os.path.join(os.getcwd(), 'resources', f"{lang}.json")
    with open(filename, "r") as english_dictionary:
        valid_words = json.load(english_dictionary)
        return valid_words
