from flask import Flask, render_template
import json


app = Flask(__name__)

def load_data(file_path):
    """ Loads a JSON file """
    with open(file_path, "r", encoding="utf-8") as handle:
        return json.load(handle)
    

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/')
def index():
    blog_posts = load_data("data/data.json")
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)