from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for, jsonify, make_response, request
from flask.json import tojson_filter
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from .models import db, Post, Pet, User, Message
from datetime import datetime, date
from .util import *

import pusher
import os

pusher_client = pusher.Pusher(
  app_id='1138510',
  key='c7fa9a824f00223cea96',
  secret='b315fc5f8cad057f8aed',
  cluster='us2',
  ssl=True
)
# 
# --- profile/messages ---
#


@app.route("/myprofile/messages")
@login_required
def chat():
	currUser = User.query.filter_by(id=current_user.get_id()).first()
	friend_list = getFriendList(currUser)

	return render_template("messages.html", user=currUser, friends=friend_list)

@app.route("/isPetPal", methods=["POST"])
@login_required
def isPetPal():
	req = request.get_json()
	reciever = User.query.filter_by(username=req["reciever"]).first()

	if reciever is current_user:
		return  make_response(jsonify({"update": "Can't message yourself"}), 200)
	elif current_user in reciever.friends:
		return  make_response(jsonify({"update": "Already friends"}), 200)

	current_user.friends.append(reciever)
	reciever.friends.append(current_user) 
	db.session.commit()

	return  make_response(jsonify({"update": "Message link created"}), 200)

@app.route("/sendMessage", methods=["POST","GET"])
@login_required
def sendMessage():
	msg = request.form.get("msg")
	if msg.isspace() or msg=="":
		return make_response(jsonify({"update": "Message was empty. Please enter a message"}), 200)

	sender = User.query.filter_by(username=request.form.get("sender")).first()
	reciever  = User.query.filter_by(username=request.form.get("reciever")).first()
	img = sender.original_image
	
	message = Msg(message=msg, sender_id=sender.id, reciever_id=reciever.id)
	db.session.add(message)
	db.session.commit()
	#get modify time
	dt = convertTime(message.date_created )

	pusher_client.trigger('chat-channel', 'new-message', {'message': msg, "date":dt, "sender":sender.username, "reciever":reciever.username,"img":img })

	return make_response(jsonify({"update": "Message was Sent"}), 200)

@app.route("/messages/getMessage", methods=["POST"])
@login_required
def Messages():
	req = request.get_json()
	currUser =  User.query.filter_by(username=req["currUser"]).first()
	otherUser =  User.query.filter_by(username=req["otherUser"]).first()
	if not otherUser:
		return make_response(jsonify({"update": "need other user", "messages":[] }), 200)	
	list_messages=formateMessages(currUser,otherUser )
	list_friends= getFriendList(currUser)

	
	return make_response(jsonify({"update": "Got Messages","messages":list_messages, "friends":list_friends }), 200)

# 