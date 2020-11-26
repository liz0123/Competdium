# Data Models
from . import db
from datetime import datetime
from flask_login import UserMixin

# Create db model
class Pet(db.Model):
	__tablename__ = "pet"
	id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.String(50))
	petType= db.Column(db.String(50))
	gender = db.Column(db.String(50))
	name = db.Column(db.String(50))
	weight = db.Column(db.String(50))
	age = db.Column(db.Integer)
	description =db.Column(db.Text)
	original_image= db.Column(db.String(255), default = "default.jpg")
	thumbnail = db.Column(db.String(255), default = "default.jpg")
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	# Create a function to return a string when pet is added
	def __repr__(self):
		return '<Name> %r' % self.id

class Post(db.Model):
	__tablename__ ="post"
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	content =db.Column(db.Text, nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)
	original_image = db.Column(db.String(255), nullable = False, default = "default.jpg")
	thumbnail = db.Column(db.String(255), nullable = False, default = "default.jpg")
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	 
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_created}' )"

class User(UserMixin, db.Model):
	__tablename__="user"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255), unique = True, nullable = False)
	email = db.Column(db.String(255), unique = True, nullable = False)
	password = db.Column(db.String(300), nullable =False)
	image_file = db.Column(db.String(255), nullable = False, default = "default_profile.png")
	post = db.relationship('Post', backref = 'auther', lazy = True)
	pet = db.relationship('Post', backref = 'owner', lazy = True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"
