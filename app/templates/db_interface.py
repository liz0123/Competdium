from app import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

# Create db model
class pet(db.Model):
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