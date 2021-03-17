from wtforms import Form, BooleanField, StringField, SelectField, IntegerField, PasswordField, validators, TextAreaField, FileField, SelectMultipleField
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


class PetForm(Form):
    name = StringField("Name", [DataRequired()])
    #month = SelectField("Month", choices=[(1,"January"),(2,"February"),(3,"March"),(4,"April"),(5,"May"),(6,"June"),(7,"July"),(8,"August"),(9,"September"), (10,"October"), (11,"November"), (12,"December")])
    #year = IntegerField("Year", [validators.NumberRange(min=1980, max=datetime.today().year, message='Invalid Year'), DataRequired()])
    type = SelectField("Type", choices=[(None, "Any"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
        "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")])
    age = SelectField('Age ', choices=[("baby", "Baby"), (
        "young", "Young"), ("adult", "Adult"), ("senior", "Senior")])
    care = SelectMultipleField('Care & Behavior', choices=[(
        "housetrained", "House Trained"), ("specialneeds", "Special Needs")])
    size = SelectField("Size", choices=[(None, "Any"), ('small', 'Small'), (
        'medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')])
    gender = SelectField(
        "Gender", choices=[('female', 'Female'), ('male', 'Male')])
    goodwith = SelectMultipleField("Good With", choices=[(
        "kids", "Kids"), ("dogs", "Dogs"), ("cats", "Cats")])

    breed = SelectMultipleField(
        'Breed ', [DataRequired()], choices=[(None, "Any")])
    coat = SelectMultipleField('Coat Length ', [DataRequired()], choices=[
        (None, "Any"), ("short", "Short")])
    color = SelectMultipleField(
        'Color', choices=[(None, "Any"), ("black", "Black"), ("white", 'White')])

    name = StringField('Pet Name', [validators.Length(min=4, max=100)])
    size = SelectField("Size", choices=[(
        'small', 'Small'), ('medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')])
    city = StringField("City", [DataRequired()])
    state = SelectField("State", choices=[("al", "AL"), ("ak", "AK"), ("az", "AZ"), ("ar", "AR"), ("ca", "CA"), ("co", "CO"), ("ct", "CT"), ("dc", "DC"), ("de", "DE"), ("fl", "FL"), ("ga", "GA"), ("hi", "HI"), ("id", "ID"), ("il", "IL"), ("in", "IN"), ("ia", "IA"), ("ks", "KS"), ("ky", "KY"), ("la", "LA"), ("me", "ME"), ("md", "MD"), ("ma", "MA"), ("mi", "MI"), ("mn", "MN"), (
        "ms", "MS"), ("mo", "MO"), ("mt", "MT"), ("ne", "NE"), ("nv", "NV"), ("nh", "NH"), ("nj", "NJ"), ("nm", "NM"), ("ny", "NY"), ("nc", "NC"), ("nd", "ND"), ("oh", "OH"), ("ok", "OK"), ("or", "OR"), ("pa", "PA"), ("ri", "RI"), ("sc", "SC"), ("sd", "SD"), ("tn", "TN"), ("tx", "TX"), ("ut", "UT"), ("vt", "VT"), ("va", "VA"), ("wa", "WA"), ("wv", "WV"), ("wi", "WI"), ("wy", "WY")])
    zip = IntegerField("Zip",  [validators.NumberRange(
        min=501, max=99950, message="Invalid Zip Code"), DataRequired()])
    description = TextAreaField("Additional Information")


class SearchPetForm(Form):
    petfinder =BooleanField('Search PetFinder (recommended)')
    type = SelectField("Type",[DataRequired()] ,choices=[(None, "Any"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), (
        "horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")])
    species = SelectMultipleField('Species', choices=[])
    age = SelectMultipleField('Age ', choices=[("baby", "Baby"), (
        "young", "Young"), ("adult", "Adult"), ("senior", "Senior")])
    care = SelectMultipleField('Care & Behavior', choices=[(
        "housetrained", "House Trained"), ("specialneeds", "Special Needs")])
    days = SelectField('Days on Competdium', choices=[
                       (None, "Any"), ("1", "1"), ("5", "5"), ("15", "15"), ("30", "30+")])
    size = SelectMultipleField("Size", choices=[('small', 'Small'), (
        'medium', 'Medium'), ('large', 'Large'), ('xlarge', 'XLarge')])
    gender = SelectMultipleField(
        "Gender", choices=[('female', 'Female'), ('male', 'Male')])
    goodwith = SelectMultipleField("Good With", choices=[("kids", "Kids"), ("dogs", "Dogs"), ("cats", "Cats")])

    breed = SelectMultipleField('Breed ', choices=[])
    coat = SelectMultipleField('Coat Length ', choices=[])
    color = SelectMultipleField(
        'Color', choices=[("black", "Black"), ("white", 'White')])

    name = StringField('Pet Name', [validators.Length(min=4, max=100)])
    city = StringField("City", [DataRequired()] )
    state = SelectField("State", choices=[('', ''),("al","AL"), ("ak","AK"), ("az","AZ"), ("ar","AR"), ("ca","CA"), ("co","CO"), ("ct","CT"), ("dc","DC"), ("de","DE"), ("fl","FL"), ("ga","GA"), ("hi","HI"), ("id","ID"), ("il","IL"), ("in","IN"), ("ia","IA"), ("ks","KS"), ("ky","KY"), ("la","LA"), ("me","ME"), ("md","MD"), ("ma","MA"), ("mi","MI"), ("mn","MN"), ("ms","MS"), ("mo","MO"), ("mt","MT"), ("ne","NE"), ("nv","NV"), ("nh","NH"), ("nj","NJ"), ("nm","NM"), ("ny","NY"), ("nc","NC"), ("nd","ND"), ("oh","OH"), ("ok","OK"), ("or","OR"), ("pa","PA"), ("ri","RI"), ("sc","SC"), ("sd","SD"), ("tn","TN"), ("tx","TX"), ("ut","UT"), ("vt","VT"), ("va","VA"), ("wa","WA"), ("wv","WV"), ("wi","WI"), ("wy","WY") ])
    distance = SelectField('Distance ', choices=[("10","10"),("20","20"),("30","30"), ("40","40")])


class UserForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [validators.EqualTo(
        'confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    bio = TextAreaField("BIO")
    img = FileField("Select a profile image (400x400) ")


class PostForm(Form):
    #categories = SelectField("Categories", choices=[("post","Post"),("qna","Questions")] )
    title = StringField('Title', [DataRequired()])
    content = TextAreaField("Content")
    image = FileField("Select Image")
