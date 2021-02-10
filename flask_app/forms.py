from wtforms import Form, BooleanField, StringField, SelectField, IntegerField, PasswordField, validators, TextAreaField, FileField
from wtforms.validators import DataRequired
from datetime import datetime

class LoginForm(Form):
    username = StringField('Username or Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('remember me')

class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    #accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

class PostForm(Form):
    title = StringField("Title",[DataRequired()])
    content = TextAreaField("Content")
    img = FileField()
    # Catagory

class PetForm(Form):
    image = FileField("Select Image")
    name = StringField("Name", [DataRequired()])
    month = SelectField("Month", choices=[(1,"January"),(2,"February"),(3,"March"),(4,"April"),(5,"May"),(6,"June"),(7,"July"),(8,"August"),(9,"September"), (10,"October"), (11,"November"), (12,"December")])
    year = IntegerField("Year", [validators.NumberRange(min=1980, max=datetime.today().year, message='Invalid Year'), DataRequired()])
    type = SelectField("Type", choices=[('dog', 'Dog'),('cat', 'Cat'), ('bird', 'Bird'),('other', 'Other')])
    gender = SelectField("Gender", choices=[('female', 'Female'),('male', 'Male')])
    age = SelectField('Age ', choices=[("young","Young"), ("adult","Adult"), ("senior","Senior")])
    size = SelectField("Size", choices=[('small', 'Small'),('medium', 'Medium'), ('large', 'Large')])
    city = StringField("City", [DataRequired()] )
    state = SelectField("State", choices=[("al","AL"), ("ak","AK"), ("az","AZ"), ("ar","AR"), ("ca","CA"), ("co","CO"), ("ct","CT"), ("dc","DC"), ("de","DE"), ("fl","FL"), ("ga","GA"), ("hi","HI"), ("id","ID"), ("il","IL"), ("in","IN"), ("ia","IA"), ("ks","KS"), ("ky","KY"), ("la","LA"), ("me","ME"), ("md","MD"), ("ma","MA"), ("mi","MI"), ("mn","MN"), ("ms","MS"), ("mo","MO"), ("mt","MT"), ("ne","NE"), ("nv","NV"), ("nh","NH"), ("nj","NJ"), ("nm","NM"), ("ny","NY"), ("nc","NC"), ("nd","ND"), ("oh","OH"), ("ok","OK"), ("or","OR"), ("pa","PA"), ("ri","RI"), ("sc","SC"), ("sd","SD"), ("tn","TN"), ("tx","TX"), ("ut","UT"), ("vt","VT"), ("va","VA"), ("wa","WA"), ("wv","WV"), ("wi","WI"), ("wy","WY") ]) 
    zip = IntegerField("Zip",  [validators.NumberRange(min=501, max=99950, message="Invalid Zip Code"), DataRequired()])
    description= TextAreaField("Additional Information")
    

class SearchPetForm(Form):
    type = SelectField("Type", choices=[('any',"Any"),('dog', 'Dog'),('cat', 'Cat'), ('bird', 'Bird'),('other', 'Other')])
    breed = SelectField('Breed ', choices=["Chihuahua", "French Bulldog", "Labrador Retriever", "Standard Poodle", "Terrior Pet Mix"] )
    size = SelectField("Size", choices=[('any',"Any"),('small', 'Small'),('medium', 'Medium'), ('large', 'Large')])
    gender = SelectField("Gender", choices=[('any',"Any"),('female', 'Female'),('male', 'Male')])
    age = SelectField('Age ', choices=[('any',"Any"),("young","Young"), ("adult","Adult"), ("senior","Senior")])

class UserForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)] )
    email = StringField('Email Address', [validators.Length(min=6, max=35)] )
    password = PasswordField('New Password', [validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')
    bio = TextAreaField("BIO",)
    img = FileField("Select a profile image (400x400) ")
