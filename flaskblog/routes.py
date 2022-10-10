import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from .forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    CreatePostForm,
    RequestResetForm,
    ResetPasswordForm
)
from . import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from .models import User, BlogPost


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(template_name_or_list='home.html', title='Home', posts=posts)

@app.route("/about")
def about():
    return render_template(template_name_or_list='about.html', title='About')


# RegistrationForm function view to the template
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #isntead of bytes use string password
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        #saving the info to the db
        db.session.add(user)
        db.session.commit()
        flash('Account Created!! Please login..', 'success')
        return redirect ('/login')

    return render_template(template_name_or_list='register.html', title='Register', form=form)


# LoginForm function view to the template
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please correct your details', 'danger')
    return render_template(template_name_or_list='login.html', title='Login', form=form)



# LogoutForm function view to the template
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))


# Account update form
def save_image(form_image):
    random_hex = secrets.token_hex(10)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/images', image_fn)

    #Image resizing
    output_size = (125,125)
    i = Image.open(form_image)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = save_image(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email  = form.email.data
        db.session.commit()
        flash('Your account is updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template(template_name_or_list='account.html', title='Account', image_file=image_file, form=form)


# Creating Route for Flask PostBlog

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post is Created..!!', 'success')
        return redirect(url_for('home'))

    return render_template(template_name_or_list='create_post.html', title='Create Post', form=form, legend='Create Post')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template(template_name_or_list='post.html', title=post.title, post=post)

# Update Post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form= CreatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post is updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(template_name_or_list='create_post.html', title='Update Post', form=form, legend='Update Post')

# Delete Post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post is deleted..!!', 'success')
    return redirect(url_for('home'))



# Only Particular User's posts
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author=user)\
        .order_by(BlogPost.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template(template_name_or_list='user_posts.html', posts=posts, user=user)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    return render_template(template_name_or_list='reset_request.html', title= 'Rest Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)















