from flask import current_app as app
from flask import flash, redirect, render_template, session, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import db, Post, Pet, User
from .functions import *
import os

@app.route("/", methods=["POST","GET"])
@app.route("/searchPets", methods=["POST","GET"])
def searchPets():
	pets = Pet.query.order_by(Pet.id.desc()).all()
	return render_template("public/searchPets.html", pets=pets)

@app.route("/searchPets/info_petID=<petID>")
def showPet(petID):
	pet = Pet.query.filter_by(id=petID).first()
	owner= User.query.filter_by(id=pet.user_id).first()
	return render_template("pet/pet_info.html", pet=pet, owner=owner.username)

@app.route("/profiles/user=<username>")
def profile(username):
	user = User.query.filter_by(username=username).first()
	posts = Post.query.filter_by(user_id=user.id).order_by(Post.id.desc()).all()
	pets = Pet.query.filter_by(user_id=user.id).order_by(Pet.id.desc()).all()
	if not user:
		flash("User not found")
		return redirect(url_for("searchPets"))
	
	return render_template("user/view_profile.html", user=user, posts=posts, pets=pets)
