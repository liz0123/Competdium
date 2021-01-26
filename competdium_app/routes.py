import os
from flask import flash, request, redirect, render_template, make_response, session, url_for, send_from_directory, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Post, Pet
from .functions import *
from . import mail



from flask_login import login_user, logout_user, login_required



# ------ user -------
@app.route("/profiles/user<username>/email",methods=["POST","GET"])
@login_required
def email(username):
	reciever = User.query.filter_by( username=username ).first()
	sender = User.query.filter_by(id=current_user.get_id()).first()
	if request.method =="POST":
		subject = "Hi "+reciever.username+"! You got a messaga from "+sender.username
		msg = Message(subject,sender=app.config["MAIL_USERNAME"], recipients=[reciever.email])
		msg.body = request.form.get("emailContect")
		print("email: ", request.form.get("emailContect"))
		mail.send(msg)
		flash("Email send!")
	return redirect(url_for("profile",username=username))
	

@app.route("/myprofile/delete:<UPLOAD>_<ID>")
@login_required
def delete(UPLOAD,ID):
	id = int(ID)
	print("upload ", UPLOAD)

	if UPLOAD == "POST_UPLOADS":
		original_image = Post.query.filter_by(id=id).first().original_image
		thumbnail = Post.query.filter_by(id=id).first().thumbnail
		Post.query.filter_by(id=id).delete()
		if "default.jpg" == original_image:
			db.session.commit()	
			return redirect(url_for("my_profile"))
	else:
		original_image = Pet.query.filter_by(id=id).first().original_image
		thumbnail = Pet.query.filter_by(id=id).first().thumbnail
		Pet.query.filter_by(id=ID).delete()

	if not (original_image == thumbnail):
		os.remove(app.config[UPLOAD]+thumbnail)
	os.remove( app.config[UPLOAD]+original_image)
	db.session.commit()	

	return redirect(url_for("my_profile"))

# ------ public -----
@app.route("/adoption")
def adoption():
	username = True if "username" in session else False
	return render_template("public/adoptionPage.html", username= username)








