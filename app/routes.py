import os
from flask import flash, request, redirect, render_template, make_response, session, url_for, send_from_directory
from flask import current_app as app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta 
from .forms import PostForm, PetForm
from .models import db, User, Post, Pet
from .functions import *

#app.permanent_session_lifetime = timedelta(hours=1)
@app.route("/", methods=["POST","GET"])
def feed():
	form = PostForm()
	posts = None
	if  form.validate_on_submit():
		user_id = current_user.get_id()
		#user = User.query.filter_by(id=user_id).first()
		if form.img.data:
			img_name = secure_filename(form.img.data.filename)
			form.img.data.save(os.path.join(app.config['POST_UPLOADS'], img_name))
			post = Post(title=form.title.data, content=form.content.data, original_image=img_name, user_id=user_id)	
		else:
			post = Post(title=form.title.data, content=form.content.data, user_id=user_id)
		db.session.add(post)
		db.session.commit()

		# Standerize image 
		if form.img.data:
			img_names = formateImage(user=user_id, post=post, px=400, uploads="POST_UPLOADS" )
			post.original_image = img_names[0]
			post.thumbnail = img_names[1]
			db.session.commit()
		
		return redirect(url_for("feed"))
	else:
		# get post form db
		posts = Post.query.order_by(Post.id.desc()).all()
	
	return render_template("public/feed.html", posts=posts, form=form)

# ------ user -------
@app.route("/profile_username=<username>")
@login_required
def usr(username):
	user = User.query.filter_by(username=username).first()
	if not user:
		flash("User not found")
		return redirect(url_for("feed"))
	posts = Post.query.filter_by(user_id=user.id).all()
	pets = Pet.query.filter_by(user_id=user.id).all()

	return render_template("user/profile.html", user=user, posts=posts, pets=pets)

@app.route("/profile")
@login_required
def profile():
	user = User.query.filter_by(id=current_user.get_id()).first()
	posts = Post.query.filter_by(user_id=current_user.get_id()).all()
	pets = Pet.query.filter_by(user_id=current_user.get_id()).all()

	return render_template("user/profile.html", user=user, posts=posts, pets=pets)

# ------ public -----
@app.route("/adoption")
def adoption():
	username = True if "username" in session else False

	return render_template("public/adoptionPage.html", username= username)

@app.route("/searchPets", methods=["POST","GET"])
def searchPets():
	form = PetForm()
	if form.validate_on_submit():
		# get image
		# casifly image
		# save image
		form.img.data.save(os.path.join(app.config['PET_UPLOADS'], form.img.data.filename))
		pet = Pet(petType="DOG", user_id=current_user.get_id(), status="ADOPTION", gender=form.gender.data, name=form.name.data, age=form.age.data, description=form.description.data, original_image=form.img.data.filename, weight=form.weight.data)
		db.session.add(pet)
		db.session.commit()

		img_names = formateImage(current_user.get_id(), pet, 200, uploads="PET_UPLOADS")
		pet.original_image = img_names[0]
		pet.thumbnail = img_names[1]
		db.session.commit()
		return redirect(url_for("searchPets"))

	pets = Pet.query.order_by(Pet.id.desc()).all()
	return render_template("public/searchPets.html", pets=pets, form=form)

@app.route("/searchPets/info_petID=<petID>")
def showPet(petID):
	pet = Pet.query.filter_by(id=petID).first()
	owner= User.query.filter_by(id=pet.user_id).first()

	return render_template("pet/pet_info.html", pet=pet, owner=owner.username)


@app.route("/addPet", methods = ["POST"])
def addPet():
	if request.method =='POST':
		print("adding pet")

	return render_template("public/adoptionPage.html")


