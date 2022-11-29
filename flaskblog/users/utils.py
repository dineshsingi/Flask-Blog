import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flaskblog import app, mail

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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='dineshreddysingireddy15@gmail.com', recipients=[user.email])
    msg.body = f'''To Reset password, vising following link:
    {url_for('reset_token', token=token, _external=True)}
    Ignore if not you didn't make this request
    '''
    mail.send(msg)