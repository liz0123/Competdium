
from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for, jsonify, make_response, request
from flask.json import tojson_filter
from sqlalchemy.sql.elements import False_
from sqlalchemy.sql.expression import update
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from .models import db, Post, Pet, User, Message
from .forms import PostForm
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
import json
@app.template_filter()
def isFavorite(id):
	pet_id = int(id)
	pet = Post.query.filter_by(id=pet_id).first()
	if pet in current_user.liked_pets:
		return True
	return False

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
	form = PostForm()
	posts = Post.query.filter_by(user_id=current_user.get_id()).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=current_user.get_id()).order_by(Pet.id.desc()).all()
	liked = current_user.liked_pets
	friend_list = getFriendList(current_user)

	return render_template("user/profile.html", user=current_user, posts=posts, pets=pets, liked=liked, friends=friend_list, form=form, datetime = datetime.utcnow())

@app.route("/myprofile/editPost", methods=["POST"])
@login_required
def editPost():
	post_id = int(request.form.get("post_id"))
	title = request.form.get("title")
	content = request.form.get("content")
	img = request.files["image"]
	post = Post.query.filter_by(id=post_id).first()
	if img:
		org_img = generateFileName([current_user.get_id(), post_id], "post")
		org_path = os.path.join(app.config["POST_UPLOADS"], org_img)
		img.save(org_path)
		post.image= org_img
	post.title = title
	post.content = content
	db.session.commit()	
	flash("Post was updated!")
	return redirect(url_for("my_profile"))
	#return make_response(jsonify({"update": "SAVED: About has been saved!"}), 200)

@app.route("/myprofile/removePost", methods=["POST"])
@login_required
def deletePost():
	post_id=int(request.form.get("post_id"))
	post = Post.query.filter_by(id=post_id).first()
	try:
		os.remove(os.path.join(app.config['POST_UPLOADS'], post.image))
	except:
		pass
	db.session.delete(post)
	db.session.commit()
	flash("Post removed")
	return redirect(url_for("my_profile"))

# -- profile/setting ---
#
@app.route("/myprofile/setting/updateProfileImg", methods=["POST"])
@login_required
def updateProfileImage():
	req = request.files['image']
	#user = User.query.filter_by(id=current_user.get_id()).first()
	org_img = current_user.image
	if "default" in org_img:
		org_img = generateFileName([current_user.get_id()], "profile")
		current_user.image = org_img
		db.session.commit()
	img_path = os.path.join(app.config["PROFILE_UPLOADS"], org_img)
	#resizeImage(img_path)
	req.save(img_path)
	return make_response(jsonify({"update":"SAVED! Image was saved!","img":org_img}), 200)


@app.route("/myprofile/setting/updateBio", methods=["POST"])
@login_required
def updateBio():
	req = request.form.get('bio')
	print("bio",req)
	user = User.query.filter_by(id=current_user.get_id()).first()
	user.bio = req
	db.session.commit()

	return make_response(jsonify({"update": "SAVED: About has been saved!","value":user.bio}), 200)

from sqlalchemy import func
@app.route("/myprofile/setting/updateUsername", methods=["POST","GET"])
@login_required
def updateUsername():
	req = request.form.get('username')
	print('username ', req)
	userWithname = User.query.filter(func.lower(User.username) == func.lower(req)).first()
	print("User ", userWithname)
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

@app.route("/searchPets/likedPet", methods=["POST"])
@login_required
def addLikedPet():
	update = ''
	res = request.get_json()
	pet_id = int(res['id'])
	pet = Pet.query.filter_by( id=pet_id).first()
	if pet in current_user.liked_pets:
		update = 'Pet was unliked'
		current_user.liked_pets.remove(pet)
	else:
		update = 'Pet was liked'
		current_user.liked_pets.append(pet)
	db.session.commit()
	return  make_response(jsonify({"update": update}), 200)

@app.route("/feed/likePost/", methods=["POST"])
@login_required
def likePost():
    update = ''
    res = request.get_json()
    post_id = int(res['id'])
    post = Post.query.filter_by(id=post_id).first()
    if post in current_user.liked_posts:
        update = 'UnLiked Post'
        post.likes = post.likes-1
        current_user.liked_posts.remove(post)
    else:
        update = 'liked Post'
        post.likes = post.likes+1
        current_user.liked_posts.append(post)
    db.session.commit()
    return make_response(jsonify({"update": update, "likes": post.likes}), 200)

@app.route("/feed/savePost", methods=["POST"])
@login_required
def savePost():
	update = ''
	res = request.get_json()
	post_id = int(res['id'])
	post = Post.query.filter_by(id=post_id).first()
	if post in current_user.saved_posts:
		update = 'Unsaved Post'
		current_user.saved_posts.remove(post)
	else:
		update = 'Post Saved'
		current_user.saved_posts.append(post)
	db.session.commit()
	return make_response(jsonify({"update": "Post is saved"}), 200)

@app.route("/profiles/user=<username>/")
def profile(username):
	user = User.query.filter_by(username=username).first()
	posts = Post.query.filter_by(user_id=user.id).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=user.id).order_by(Pet.id.desc()).all()
	if not user:
		flash("User not found")
		return redirect(url_for("searchPets"))

	return render_template("user/view_profile.html", user=user, posts=posts, pets=pets, datetime = datetime.utcnow())

