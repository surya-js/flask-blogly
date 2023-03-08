"""Blogly application."""

from flask import Flask, request, render_template,  redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    """Show only 5 recent list of posts, most_recent first"""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template('home-page.html', posts = posts)

#User Routes

@app.route('/users')
def list_users():
    """Shows list of all users in db"""

    users = User.query.all()
    return render_template('list.html', users = users)

@app.route('/users/new')
def add_user_form():
    """Shows add user form"""

    return render_template('add-user.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """Adds new user to DB and redirects to users list"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['url']
    image_url = url if url else None

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about the given user"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user = user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """Shows the edit page for a user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user = user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edits user's details in DB and redirects to users list"""

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    url = request.form['url']
    image_url = url if url else DEFAULT_IMAGE_URL

    user = User.query.get_or_404(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete the User"""
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# Post Routes

@app.route('/users/<int:user_id>/posts/new')
def add_post_form(user_id):
    """Shows add post form for a specific user"""

    user = User.query.get_or_404(user_id)
    return render_template('post-add.html', user = user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Adds post to DB for a specific user and
       redirects to the user detail page"""
    
    title = request.form['title']
    content = request.form['content']

    user = User.query.get_or_404(user_id)

    new_post = Post(title=title, content=content, user_id=user.id)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Shows a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Shows form to edit a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post-edit.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' edited.")

    return redirect(f'/users/{post.user_id}')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete the specific post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    flash(f"Post Deleted!")
    return redirect(f'/users/{post.user_id}')

