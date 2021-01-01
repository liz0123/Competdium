import os
from flask import flash, request, redirect, render_template, make_response, session, url_for, send_from_directory, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from .forms import PostForm, PetForm, SearchPetForm, UserForm
from .models import db, User, Post, Pet
from .functions import *
from . import mail

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
			img_names = formateImage(user_id, post, 400,"POST_UPLOADS" )
			post.original_image = img_names[0]
			post.thumbnail = img_names[1]
			db.session.commit()
		
		return redirect(url_for("feed"))
	else:
		# get post form db
		posts = Post.query.order_by(Post.id.desc()).all()
	
	return render_template("public/feed.html", posts=posts, form=form)

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
	
@app.route("/profiles/user=<username>")
def profile(username):
	user = User.query.filter_by(username=username).first()
	posts = Post.query.filter_by(user_id=user.id).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=user.id).order_by(Pet.id.desc()).all()
	if not user:
		flash("User not found")
		return redirect(url_for("searchPets"))
	
	return render_template("user/view_profile.html", user=user, posts=posts, pets=pets)

@app.route("/myprofile", methods=["POST","GET"])
@login_required
def my_profile():
	form = UserForm()
	user = User.query.filter_by(id=current_user.get_id()).first()
	posts = Post.query.filter_by(user_id=current_user.get_id()).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=current_user.get_id()).order_by(Pet.id.desc()).all()

	if form.validate_on_submit():
		user.username = form.username.data
		user.email = form.email.data
		user.bio = form.bio.data
		if not (form.img.data.filename =="" or "default" in form.img.data.filename):
			img_name = secure_filename(form.img.data.filename)
			form.img.data.save(os.path.join(app.config['PROFILE_UPLOADS'], img_name))
			img_names = saveThumbnail(user.id, form.img.data.filename, 100,"PROFILE_UPLOADS" )
			user.image_file = img_names
		db.session.commit()
		return jsonify({"results":'Success'})

	return render_template("user/profile.html", user=user, posts=posts, pets=pets,form=form)


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

@app.route("/searchPets", methods=["POST","GET"])
def searchPets():
	form = PetForm()
	searchForm = SearchPetForm()
	if form.validate_on_submit():
		path = form.img.data.save(os.path.join(app.config['PET_UPLOADS'], form.img.data.filename))
		birth = datetime(int(form.year.data), int(form.month.data),1)
		
		pet = Pet(petType="OTHER", user_id=current_user.get_id(), status="ADOPTION", gender=form.gender.data, name=form.name.data,birth =birth, description=form.description.data, original_image=form.img.data.filename, weight=form.weight.data)
		db.session.add(pet)
		db.session.commit()

		#update pet info
		img_names = formateImage(current_user.get_id(), pet, 200, uploads="PET_UPLOADS")
		pet.petType = img_names[2]
		pet.original_image = img_names[0]
		pet.thumbnail = img_names[1]
		db.session.commit()
		return redirect(url_for("searchPets"))

	pets = Pet.query.order_by(Pet.id.desc()).all()
	return render_template("public/searchPets.html", pets=pets, form=form, searchForm=searchForm)

@app.route("/searchPets/info_petID=<petID>")
def showPet(petID):
	pet = Pet.query.filter_by(id=petID).first()
	owner= User.query.filter_by(id=pet.user_id).first()
#date="2018-01-01 00:00:00"    
#tdate= datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
#print(tdate.minute)        


	return render_template("pet/pet_info.html", pet=pet, owner=owner.username)






