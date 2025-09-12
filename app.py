from flask import Flask, render_template, request, redirect, url_for
import json
import os


app = Flask(__name__)


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
    
    
def get_id():
    """ Gets the maximum id in posts and generate a new one by adding 1 """
    posts = load_data("data/data.json")
    if not posts:
        return 1
    ids = [id["id"] for id in posts]
    return max(ids) + 1


@app.route('/')
def index():
    blog_posts = load_data("data/data.json")
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Gets all data
        id = get_id()
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        
        # Appends new data to Json file
        posts = load_data("data/data.json")
        posts.append({"id": id, "author": author, "title": title, "content": content})
        save_data(posts, "data/data.json", indent=4)
        
        # Redirect to the home page
        return redirect(url_for('index'))
    
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)