from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, TextAreaField, FileField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')

class PostForm(FlaskForm):
    title = StringField("Title",[DataRequired()])
    content = TextAreaField("Content", [DataRequired() ])
    img = FileField() 