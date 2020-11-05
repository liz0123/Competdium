from app import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

# Create db model
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255), unique = True, nullable = False)
	email = db.Column(db.String(255), unique = True, nullable = False)
	password = db.Column(db.String(60), nullable =False)
	image_file = db.Column(db.String(255), nullable = False, default = "default.jpg")
	post = db.Column('Post', backref = 'author', lazy = True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	content =db.Column(db.Text, nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)	

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_created}' )"
	
		

class Pet(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	status = db.Column(db.String(50))
	petType= db.Column(db.String(50))
	breed = db.Column(db.String(50))
	gender = db.Column(db.String(50))
	name = db.Column(db.String(50))
	age = db.Column(db.Integer)
	email = db.Column(db.String(50))
	location = db.Column(db.String(50))
	description =db.Column(db.Text)
	image = db.Column(db.String(255))
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	# Create a function to return a string when pet is added
	def __repr__(self):
		return '<Name> %r' % self.id