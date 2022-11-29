from flask import (render_template, url_for, flash, redirect,
                   request,abort,Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import BlogPost
from flaskblog.posts.forms import CreatePostForm


posts = Blueprint("posts", __name__)


# Creating Route for Flask PostBlog

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your Post is Created..!!', 'success')
        return redirect(url_for('main.home'))

    return render_template(template_name_or_list='create_post.html', title='Create Post', form=form, legend='Create Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template(template_name_or_list='post.html', title=post.title, post=post)

# Update Post
@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template(template_name_or_list='create_post.html', title='Update Post', form=form, legend='Update Post')

# Delete Post
@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post is deleted..!!', 'success')
    return redirect(url_for('main.home'))