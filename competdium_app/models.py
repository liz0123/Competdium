# Data Models
from flask.json import tojson_filter
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
	birth = db.Column(db.DateTime)
	description = db.Column(db.Text)
	original_image= db.Column(db.String(255), default = "default.jpg")
	thumbnail = db.Column(db.String(255), default = "default.jpg")
	date_created = db.Column(db.DateTime, default = datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

	# Create a function to return a string when pet is added
	def __repr__(self):
		return '<Name> %r' % self.id

class Post(db.Model):
	__tablename__ ="post"
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), nullable = False)
	content = db.Column(db.Text, nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)
	original_image = db.Column(db.String(255), nullable = False, default = "default.jpg")
	thumbnail = db.Column(db.String(255), nullable = False, default = "default.jpg")
	user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	 
	def __repr__(self):
		return f"Post('{self.title}', '{self.date_created}' )"

class Message(UserMixin, db.Model):
	__tablename__ ="message"
	id = db.Column(db.Integer, primary_key = True)
	message =  db.Column(db.Text, nullable = False)
	date_created = db.Column(db.DateTime, default = datetime.utcnow)

	sender_id = db.Column(db.Integer, nullable = False)
	reciever_id = db.Column(db.Integer, nullable = False)



friendship = db.Table(
	'friendships',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('friend_id', db.Integer, db.ForeignKey('user.id'),primary_key=True)
)

class User(UserMixin, db.Model):
	__tablename__="user"
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(255), unique = True, nullable = False)
	email = db.Column(db.String(255), unique = True, nullable = False)
	password = db.Column(db.String(300), nullable =False)
	bio = db.Column(db.Text)
	image_file = db.Column(db.String(255), nullable = False, default = "default_profile.png")


	post = db.relationship('Post', backref = 'auther', lazy = True)
	pet = db.relationship('Pet', backref = 'owner', lazy = True)


	friends = db.relationship('User', #defining the relationship, User is left side entity
        secondary = friendship, 
        primaryjoin = (friendship.c.user_id == id), 
        secondaryjoin = (friendship.c.friend_id == id),
        backref=db.backref('user', lazy='dynamic'),
        lazy='dynamic'
    ) 


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# friendship_union = select( [friendship.c.friend_id] ).union( select( [friendship.c.friend_id,friendship.c.user_id] ) ).alias()

#User.all_friends = relationship('User', secondary=friendship_union, primaryjoin=User.id==friendship_union.c.user_id, secondaryjoin=User.id==friendship_union.c.friend_id, viewonly=True)