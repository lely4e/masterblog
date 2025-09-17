import json
import os


def load_data(file_path):
    """ Loads a JSON file """
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as handle:
        try:
            return json.load(handle)
        except json.JSONDecodeError:
            return []


def save_data(data, file_path, indent=4):
    """ Saves new post in JSON file """
    with open(file_path, "w", encoding="utf-8") as handle:
        return json.dump(data, handle, indent=indent)
    

POSTS = load_data("data/data.json")