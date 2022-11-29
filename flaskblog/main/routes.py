from flask import render_template, request, Blueprint
from flaskblog.models import BlogPost

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template(template_name_or_list='home.html', title='Home', posts=posts)

@main.route("/about")
def about():
    return render_template(template_name_or_list='about.html', title='About')


