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


def fetch_post_by_id(post_id):
    """ Fetches a post from the database """
    posts = load_data("data/data.json")
    for post in posts:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    """ Loads JSON data and renders template """
    blog_posts = load_data("data/data.json")
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """ 
    Adds new post. 
    
    GET: Renders the add form.
    POST: Processes the form submission and adds it to the database.
    """
    if request.method == 'POST':
        # Gets all data
        id = get_id()
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        
        # Appends new data to Json file
        posts = load_data("data/data.json")
        posts.append({"id": id, "author": author, "title": title, "content": content, "like": 0})
        save_data(posts, "data/data.json", indent=4)
        
        # Redirect to the home page
        return redirect(url_for('index'))
    
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """ Deletes a post from the database """
    # Find the blog post with the given id and remove it from the list
    posts = load_data("data/data.json")
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            
            save_data(posts, "data/data.json", indent=4)
            # Redirect back to the home page
            return redirect(url_for('index'))

        
@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """ 
    Handle updating a post with the given post_id.
    
    GET: Render the update form for specified post.
    POST: Process the form submission and update the post in the database.
    """
    # Fetch the blog posts from the JSON file
    post = fetch_post_by_id(post_id) 
    if post is None:
        # Post not found
        return "Post not found", 404
    
    if request.method == 'POST':
        # Update the post in the JSON file
        id = request.form.get("id")
        author = request.form.get("author")
        title = request.form.get("title")
        content = request.form.get("content")
        
        # Appends new data to Json file
        posts = load_data("data/data.json")
       
        for post in posts:    
            if post['id'] == post_id:
                post.update({"author": author, "title": title, "content": content})
                save_data(posts, "data/data.json", indent=4)
        
                # Redirect to the home page
                return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post)


@app.route('/like/<int:id>', methods=['POST'])
def likes(id):
    """ Increments like count by 1 """
    posts = load_data("data/data.json")
    for post in posts:    
        if post['id'] == id:
            post['like'] = post.get('like', 0) + 1
            
    save_data(posts, "data/data.json", indent=4)

    # Redirect to the home page
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    