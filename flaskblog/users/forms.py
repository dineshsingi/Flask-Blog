from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField, PasswordField,SubmitField, BooleanField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from flask_login import current_user
from flaskblog.models import User


# Accounts Related Started
# Registration Form
class RegistrationForm(FlaskForm):
    username            = StringField('Username', validators=[DataRequired(), Length(min=2, max=22)])
    email               = StringField('Email', validators=[DataRequired(), Email()])
    password            = PasswordField('Password', validators=[DataRequired()])
    confirm_password    = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])

    submit              = SubmitField("Sign In")

    # Validating User
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username Already Exists..!!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Already Exists..!!")


# Login Form
class LoginForm(FlaskForm):
    email               = StringField('Email', validators=[DataRequired(), Email()])
    password            = PasswordField('Password', validators=[DataRequired()])

    # Checking to weather the user to still remember to logged in (True or False)
    remember            = BooleanField('Remember Me')

    submit              = SubmitField('Login')

# Update Account Form
class UpdateAccountForm(FlaskForm):
    username            = StringField('Username', validators=[DataRequired(), Length(min=2, max=22)])
    email               = StringField('Email', validators=[DataRequired(), Email()])
    image               = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit              = SubmitField("Update")

    # Validating User
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username Already Exists..!!")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email Already Exists..!!")


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no Account with this email, Please register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit  = SubmitField('Rest Password')