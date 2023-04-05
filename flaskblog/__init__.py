import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

# watch it for Config file https://www.youtube.com/watch?v=Wfx4YBzg16s&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=11&ab_channel=CoreySchafer
app.config['SECRET_KEY'] = '26eea4085b5ca875a5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER']  = 'smtp.googlemail.com'
app.config['MAIL_PORT']  = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL']  = True
app.config['MAIL_USERNAME']  = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD']  = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)


from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)