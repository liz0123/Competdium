from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, PasswordField, TextAreaField, FileField, validators
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

class PetForm(FlaskForm):
    name = StringField("Name", [DataRequired()] )
    gender = SelectField("Gender", choices=[('female', 'Female'),('male', 'Male')])
    age = IntegerField("Age", [DataRequired()] )
    description= TextAreaField("Additional Information", [ ])
    weight = IntegerField("Weight", [DataRequired()] )
    img = FileField("Select Image", [DataRequired()]) 

