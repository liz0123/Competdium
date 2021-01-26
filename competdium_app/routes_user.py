
import re
from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for, jsonify, make_response, request
from flask.json import tojson_filter
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from .models import db, Post, Pet, User, Message
from datetime import datetime, date
from .functions import *

import pusher
import os

pusher_client = pusher.Pusher(
  app_id='1138510',
  key='c7fa9a824f00223cea96',
  secret='b315fc5f8cad057f8aed',
  cluster='us2',
  ssl=True
)


@app.route("/myprofile", methods=["POST","GET"])
@login_required
def my_profile():
	form = None
	user = User.query.filter_by(id=current_user.get_id()).first()
	posts = Post.query.filter_by(user_id=current_user.get_id()).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=current_user.get_id()).order_by(Pet.id.desc()).all()

	return render_template("user/profile.html", user=user, posts=posts, pets=pets,form=form)

# 
# --- profile/messages ---
#
def getMessages(currUser,otherUser):
	return db.session.query(Message).filter( or_(Message.sender_id==currUser.id, Message.reciever_id==currUser.id )).filter( or_(Message.sender_id==otherUser.id, Message.reciever_id==otherUser.id) ).all()
	
def formateMessages(currUser,otherUser):
	db_messages=getMessages(currUser,otherUser)
	list_messages=[]
	for m in db_messages:
		message = {}
		message["message"] = m.message
		message["date"] = convertTime(m.date_created)

		message["sender"] ="your-message"
		message["img"] = ""
		if currUser.id is not m.sender_id:
			message["sender"] = "other-message"
			message["img"] = "../static/img/"+ otherUser.image_file

		list_messages.insert(0, message)
	return list_messages

def getLastMessages(currUser, otherUser):
	db_messages = getMessages(currUser,otherUser)
	lastMessage = db_messages[-1]
	return { "message":lastMessage.message, "date":lastMessage.date_created}

def getFriendList(currUser):
	friends = currUser.friends
	friend_list = []
	for friend in friends:
		f ={}
		lastMessage=getLastMessages(currUser,friend)
		f["username"] = friend.username
		f["image_file"] = friend.image_file
		f["message"] = lastMessage["message"]
		f["date"] = convertTime(lastMessage["date"])
		friend_list.append(f)
	return friend_list


@app.route("/myprofile/messages")
@login_required
def chat():
	currUser = User.query.filter_by(id=current_user.get_id()).first()
	friend_list = getFriendList(currUser)

	return render_template("messages.html", user=currUser, friends=friend_list)

@app.route("/isPetPal", methods=["POST"])
@login_required
def isPetPal():
	reciever = User.query.filter_by(username=request.form.get("reciever")).first()
	currUser = User.query.filter_by(id=current_user.get_id()).first()

	if reciever is not currUser:
		currUser.friends.append(reciever)
		reciever.friends.append(currUser)
		db.session.commit()

	return  make_response(jsonify({"update": "Are pet pals"}), 200)

@app.route("/sendMessage", methods=["POST"])
@login_required
def sendMessage():
	msg = request.form.get("msg")
	if msg.isspace() or msg=="":
		return make_response(jsonify({"update": "Message was empty"}), 200)

	sender = User.query.filter_by(username=request.form.get("sender")).first()
	reciever  = User.query.filter_by(username=request.form.get("reciever")).first()
	img = sender.image_file
	
	message = Message(message=msg, sender_id=sender.id, reciever_id=reciever.id)
	db.session.add(message)
	db.session.commit()
	#get modify time
	dt = convertTime(message.date_created )

	pusher_client.trigger('chat-channel', 'new-message', {'message': msg, "date":dt, "sender":sender.username, "reciever":reciever.username,"img":img })

	return make_response(jsonify({"update": "Message was sent!"}), 200)

@app.route("/messages/getMessage", methods=["POST"])
@login_required
def Messages():
	req = request.get_json()
	currUser =  User.query.filter_by(username=req["currUser"]).first()
	otherUser =  User.query.filter_by(username=req["otherUser"]).first()
	if not otherUser:
		return make_response(jsonify({"update": "need other user", "messages":[] }), 200)	
	list_messages=formateMessages(currUser,otherUser )

	
	return make_response(jsonify({"update": "Got Messages","messages":list_messages}), 200)

# 
# -- profile/setting ---
#
@app.route("/myprofile/setting/updateBio", methods=["POST"])
@login_required
def updateBio():
	req = request.form.get('bio')
	user = User.query.filter_by(id=current_user.get_id()).first()
	user.bio = req
	db.session.commit()
	
	return make_response(jsonify({"update": "SAVED: About has been saved!","value":user.bio}), 200)

@app.route("/myprofile/setting/updateUsername", methods=["POST","GET"])
@login_required
def updateUsername():
	req = request.form.get('username')
	userWithname = User.query.filter_by(username=req).first()

	if userWithname:
		return make_response(jsonify( {"error": "USERNAME ALREADY IN USE!" } ), 200)

	user = User.query.filter_by(id=current_user.get_id()).first()
	user.username = req
	db.session.commit()
	res = make_response(jsonify({"update": "SAVED! Username has neen saved!", "value":user.username }), 200)
	
	return res

@app.route("/myprofile/setting/updateEmail", methods=["POST"])
@login_required
def updateEmail():
	email = request.form.get("email")
	password = request.form.get("password")
	userWithEmail = User.query.filter_by(email=email).first()

	if userWithEmail:
		return make_response(jsonify({ "error": "EMAIL ALREADY IN USE!" }), 200)

	user = User.query.filter_by(id=current_user.get_id()).first()

	if not (check_password_hash(user.password, password)):
		return make_response(jsonify({"error": "INVAILED PASSWORD" }),200)
	user.email = email
	db.session.commit()
	
	return make_response(jsonify({"update": "SAVED! Email has been saved!","value":user.email}),200)

@app.route("/myprofile/setting/updatePassword", methods=["POST"])
@login_required
def updatePassword():
	curPass = request.form.get("curPass")
	newPass = request.form.get("newPass")

	user = User.query.filter_by(id=current_user.get_id()).first()

	if not(check_password_hash(user.password, curPass)):
		return make_response(jsonify({"error": "INVAILED PASSWORD" }),200)

	user.password = generate_password_hash(newPass, method='sha256') 
	db.session.commit()

	return make_response(jsonify({"update":"SAVED! Password has been saved!" }), 200)

@app.route("/myprofile/setting/updateProfileImg", methods=["PUT"])
@login_required
def updateProfileImage():
	req = request.files['img']

	user = User.query.filter_by(id=current_user.get_id()).first()
	org_img = user.image_file

	if "default" in org_img:
		org_img = generateFileName([current_user.get_id()], "profile")
		user.image_file = org_img
		db.session.commit()
	
	img_path = os.path.join(app.config["PROFILE_UPLOADS"], org_img)
	req.save(img_path)
	
	resizeImage(fromURL=img_path, toURL= img_path, size=(150,150))

	return make_response(jsonify({"update":"SAVED! Image was saved!","img":img_path}), 200)
