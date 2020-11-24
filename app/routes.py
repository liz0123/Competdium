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
def index():
	form = PostForm()
	posts = None
	if  form.validate_on_submit():
		user_id = current_user.get_id()
		#user = User.query.filter_by(id=user_id).first()
		if form.img.data:
			img_name = secure_filename(form.img.data.filename)
			form.img.data.save(os.path.join(app.config['POST_UPLOADS'], img_name))
			post = Post(title=form.title.data, content=form.content.data, image_file=img_name, user_id=user_id)	
		else:
			post = Post(title=form.title.data, content=form.content.data, user_id=user_id)
		db.session.add(post)
		db.session.commit()

		# Standerize image 
		if form.img.data:
			post.image_file = formateImage(user=user_id, post=post, px=400, uploads="POST_UPLOADS" )
			db.session.commit()
		
		return redirect(url_for("index"))
	else:
		# get post form db
		posts = Post.query.order_by(Post.id.desc()).all()
	
	return render_template("public/home.html", posts=posts, form=form)

# ------ user -------
@app.route("/profile")
@login_required
def profile():
	user = User.query.filter_by(id=current_user.get_id()).first()
	posts = Post.query.filter_by(user_id=current_user.get_id()).all()

	return render_template("user/profile.html", user=user, posts=posts)

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
		pet = Pet(petType="DOG", user_id=current_user.get_id(), status="ADOPTION", gender=form.gender.data, name=form.name.data, age=form.age.data, description=form.description.data, image_file=form.img.data.filename, size=form.size.data)
		db.session.add(pet)
		db.session.commit()

		pet.image_file=formateImage(current_user.get_id(), pet, 200, uploads="PET_UPLOADS")
		db.session.commit()
		return redirect(url_for("searchPets"))

	pets = Pet.query.order_by(Pet.id.desc()).all()
	return render_template("public/searchPets.html", pets=pets, form=form)

@app.route("/addPet", methods = ["POST"])
def addPet():
	if request.method =='POST':
		print("adding pet")

	return render_template("public/adoptionPage.html")


