
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

from functools import wraps
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

@app.route("/resend/")
@login_required
def resend_confirmation():
	token = generate_confirmation_token(current_user.email)
	confirm_url = url_for('confirm_email', token=token, _external=True)
	html = render_template('user/activate.html', confirm_url=confirm_url)
	subject = "Please confirm your email"
	send_email(current_user.email, subject, html)
	flash('A new confirmation email has been sent.', 'success')
	
	return redirect(url_for('unconfirmed'))

@app.route("/myprofile/", methods=["POST","GET"])
@login_required
@check_confirmed
def my_profile():
	#user = User.query.filter_by(id=current_user.get_id()).first()
	posts = Post.query.filter_by(user_id=current_user.get_id()).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=current_user.get_id()).order_by(Pet.id.desc()).all()
	liked = current_user.liked_pets
	friend_list = getFriendList(current_user)

	return render_template("user/profile.html", user=current_user, posts=posts, pets=pets, liked=liked, friends=friend_list)


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
		return make_response(jsonify({"update": "INVAILED PASSWORD","error": "INVAILED PASSWORD" }),200)

	user.password = generate_password_hash(newPass, method='sha256') 
	db.session.commit()

	return make_response(jsonify({"update":"SAVED! Password has been saved!" }), 200)

@app.route("/myprofile/setting/updateProfileImg", methods=["PUT"])
@login_required
def updateProfileImage():
	req = request.files['img']

	user = User.query.filter_by(id=current_user.get_id()).first()
	org_img = user.original_image

	if "default" in org_img:
		org_img = generateFileName([current_user.get_id()], "profile")
		user.original_image = org_img
		db.session.commit()
	
	img_path = os.path.join(app.config["PROFILE_UPLOADS"], org_img)
	req.save(img_path)
	
	resizeImage(fromURL=img_path, toURL= img_path, size=(150,150))

	return make_response(jsonify({"update":"SAVED! Image was saved! Please give it some time.","img":img_path}), 200)

