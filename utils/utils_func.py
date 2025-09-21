from flask import redirect, url_for
from storage import data_storage
from app import POSTS


def check_data(posts, error_message):
    """
    Check if the data is valid, saves it to the database
    and redirect to the index page. Returns an error if saving fails
    """
    try:
        data_storage.save_data(posts, "data/data.json", indent=4)
    except Exception as e:
        return f"{error_message}: {e}", 500
    return redirect(url_for("index"))


def get_id():
    """Gets the maximum id in posts and generate a new one by adding 1"""
    return max((post["id"] for post in data_storage.POSTS), default=0) + 1


def fetch_post_by_id(post_id):
    """Fetches a post from the database"""
    for post in data_storage.POSTS:
        if post["id"] == post_id:
            return post
    return None
