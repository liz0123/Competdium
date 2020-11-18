from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, validators
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')