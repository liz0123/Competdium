# Data Models
from flask.json import tojson_filter
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from . import db

liked_pet_table = db.Table(
    "liked_pets",
    db.Column("user_id", db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('pet_id', db.Integer, db.ForeignKey(
        'pet.id'), primary_key=True)
)
liked_post_table = db.Table(
    "liked_posts",
    db.Column("user_id", db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id'), primary_key=True)
)
saved_post_table = db.Table(
    "saved_posts",
    db.Column("user_id", db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id'), primary_key=True)
)
post_auther_table = db.Table(
    "post_auther",
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id'), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
)
reply_table = db.Table(
    "reply",
    db.Column('post_id', db.Integer, db.ForeignKey(
        'post.id'), primary_key=True),
    db.Column("comment_id", db.Integer, db.ForeignKey(
        'comment.id'), primary_key=True)
)
comment_auther_table = db.Table(
    "comment_auther",
    db.Column("comment_id", db.Integer, db.ForeignKey(
        'comment.id'), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
)
friendship = db.Table(
    'friendships',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey(
        'user.id'), primary_key=True)
)
#
'''
color = db.Table(
    'color',
    db.Column('pet_id', db.Integer, db.ForeignKey('pet.id')),
    db.Column("color", db.ARRAY(db.String))
)'''
# Create db model


class Pet(db.Model):
    __tablename__ = "pet"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(50))
    breed = db.Column(db.String(50))
    age = db.Column(db.String(50))
    size = db.Column(db.String(50))
    gender = db.Column(db.String(50))
    goodwith = db.Column(db.String(50))
    coat = db.Column(db.String(50))
    color = db.Column(db.String())
    care = db.Column(db.String(50))
    birth_date = db.Column(db.DateTime)
    description = db.Column(db.Text)
    image = db.Column(db.String(255), default="default.jpg")
    # location
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zip = db.Column(db.Integer)

    #color = db.relationship("color", secondary=color)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    # Create a function to return a string when pet is added
    def __repr__(self):
        return '<Name> %r' % self.id


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False, default="post")
    id_pet = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    image = db.Column(db.String(255), nullable=False, default="default.jpg")
    likes = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    writer = db.relationship("User", secondary=post_auther_table)
    comments = db.relationship("Comment", secondary=reply_table)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_created}' )"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    auther = db.relationship("User", secondary=comment_auther_table)


class Message(UserMixin, db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    sender_id = db.Column(db.Integer, nullable=False)
    reciever_id = db.Column(db.Integer, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bio = db.Column(db.Text)
    image = db.Column(db.String(255), nullable=False, default="default.jpg")
    confirmed = db.Column(db.Boolean, nullable=False, default=False)

    posts = db.relationship('Post', backref='auther', lazy=True)
    pets = db.relationship('Pet', backref='owner', lazy=True)
    liked_pets = db.relationship("Pet", secondary=liked_pet_table)
    liked_posts = db.relationship("Post", secondary=liked_post_table)
    saved_posts = db.relationship("Post", secondary=saved_post_table)

    friends = db.relationship('User',  # defining the relationship, User is left side entity
                              secondary=friendship,
                              primaryjoin=(friendship.c.user_id == id),
                              secondaryjoin=(friendship.c.friend_id == id),
                              backref=db.backref('user', lazy='dynamic'),
                              lazy='dynamic'
                              )

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"
