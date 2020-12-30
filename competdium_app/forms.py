from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, BooleanField, PasswordField, TextAreaField, FileField, validators
from wtforms.validators import DataRequired,NumberRange
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)] )
    email = StringField('Email Address', [validators.Length(min=6, max=35)] )
    password = PasswordField('New Password', [ validators.DataRequired(), validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')

class PostForm(FlaskForm):
    title = StringField("Title",[DataRequired()])
    content = TextAreaField("Content")
    img = FileField()
    # Catagory

class PetForm(FlaskForm):
    today = datetime.today()
    name = StringField("Name", [DataRequired()] )
    gender = SelectField("Gender", choices=[('female', 'Female'),('male', 'Male')])
    month = SelectField("Month", choices=[(1,"January"),(2,"February"),(3,"March"),(4,"April"),(5,"May"),(6,"June"),(7,"July"),(8,"August"),(9,"September"), (10,"October"), (11,"November"), (12,"December")])
    year = IntegerField("Year", [DataRequired(), NumberRange(min=1900, max=today.year, message='Please check the year submitted')])
    description= TextAreaField("Additional Information",)
    weight = IntegerField("Weight", [DataRequired()] )
    img = FileField("Select Image", [DataRequired()])

class SearchPetForm(FlaskForm):
    breed = SelectField('Breed ', choices=["Chihuahua", "French Bulldog", "Labrador Retriever", "Standard Poodle", "Terrior Pet Mix"] )
    age = SelectField('Age ', choices=["Young", "Adult", "Senior"])
    size = SelectField('Size ', choices=["S", " M", "L","XL"])
    img = FileField("Select ideal pet ") 

class UserForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)] )
    email = StringField('Email Address', [validators.Length(min=6, max=35)] )
    password = PasswordField('New Password', [validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')
    bio = TextAreaField("BIO",)
    img = FileField("Select a profile image( 200x200 px ideal)")
