from flask import Flask, render_template, request, redirect, url_for
from storage import data_storage 


app = Flask(__name__)


def check_data(posts, error_message):
    """ 
    Check if the data is valid, saves it to the database
    and redirect to the index page. Returns an error if saving fails 
    """
    try:
        data_storage.save_data(posts, "data/data.json", indent=4)
    except Exception as e:
        return f"{error_message}: {e}", 500
    return redirect(url_for('index'))


def get_id():
    """ Gets the maximum id in posts and generate a new one by adding 1 """
    return max((post["id"] for post in data_storage.POSTS), default=0) +1


def fetch_post_by_id(post_id):
    """ Fetches a post from the database """
    for post in data_storage.POSTS:
        if post['id'] == post_id:
            return post
    return None


@app.route('/')
def index():
    """ Loads JSON data and renders template """
    return render_template('index.html', posts=data_storage.POSTS)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """ 
    Adds new post. 
    
    GET: Renders the add form.
    POST: Processes the form submission and adds it to the database.
    """
    if request.method == 'POST':
        # Gets all data
        post_id = get_id()
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        # Input 
        if not author or not title or not content:
            return render_template("add.html", error="Empty fields")
        
        # Appends new data to Json file
        data_storage.POSTS.append({"id": post_id, "author": author, "title": title, "content": content, "like": 0})
        
        # Check data
        return check_data(data_storage.POSTS, "Can't save post")
        
    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    """ Deletes a post from the database """
    # Find the blog post with the given id and remove it from the list
    for post in data_storage.POSTS:
        if post['id'] == post_id:
            data_storage.POSTS.remove(post)
            
            # Check data
            return check_data(data_storage.POSTS, "Can't delete post")
        
    return "Post not found", 404


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
        author = request.form.get("author", "").strip()
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        
        # Input Validation
        if not author or not title or not content:
            return render_template("update.html", post=post, error="Empty fields")
        
        # Appends new data to Json file  
        for post in data_storage.POSTS:    
            if post['id'] == post_id:
                post.update({"author": author, "title": title, "content": content})
                
                # Check data
                return check_data(data_storage.POSTS, "Can't update post")

    # GET request
    return render_template('update.html', post=post)


@app.route('/like/<int:id>', methods=['POST'])
def likes(id):
    """ Increments like count by 1 """
    for post in data_storage.POSTS:    
        if post['id'] == id:
            post['like'] = post.get('like', 0) + 1
            
            # Check data
            return check_data(data_storage.POSTS, "Can't update likes")

    return "Post not found", 404


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
    