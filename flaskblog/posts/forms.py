from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

# Creating forms for BlogPost

class CreatePostForm(FlaskForm):
    title               = StringField('Title', validators=[DataRequired(), Length(min=2, max=120)])
    content             = TextAreaField('Content', validators=[DataRequired()])

    submit              = SubmitField('Post')
