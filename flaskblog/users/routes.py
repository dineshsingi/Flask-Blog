from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, BlogPost
from flaskblog.users.forms import (
            RegistrationForm,
            LoginForm,
            UpdateAccountForm,
            RequestResetForm,
            ResetPasswordForm
            )
from flaskblog.users.utils import save_image, send_reset_email


users = Blueprint("users", __name__)


# RegistrationForm function view to the template
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please correct your details', 'danger')
    return render_template(template_name_or_list='login.html', title='Login', form=form)



# LogoutForm function view to the template
@users.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template(template_name_or_list='account.html', title='Account', image_file=image_file, form=form)


# Only Particular User's posts
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = BlogPost.query.filter_by(author=user)\
        .order_by(BlogPost.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template(template_name_or_list='user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template(template_name_or_list='reset_request.html', title= 'Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid, Expired token", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #isntead of bytes use string password
        #saving the info to the db
        user.password = hashed_pw
        db.session.commit()
        flash('Your password updated!! Please login..', 'success')
        return redirect ('/login')
    return render_template(template_name_or_list='reset_token.html', title='Reset Password', form=form)