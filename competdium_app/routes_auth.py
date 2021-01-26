from flask import Flask, flash, request, render_template, redirect, url_for, request, flash, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from sqlalchemy import or_
from flask import current_app as app
from .models import db, User
from .functions import *


@app.route("/login", methods=["POST","GET"])
def login():
	if request.method =="POST":
		email = request.form.get("email")
		password = request.form.get("password")
		remember = True if request.form.get("remember") else False 
		user = db.session.query(User).filter( or_(User.email==email, User.username==email )).first()
		
		if user and check_password_hash(user.password, password):
			login_user(user, remember=remember)
			return redirect(url_for("searchPets"))
		
		flash('Please check your login details and try again.')
	return render_template("public/login.html")

@app.route('/register', methods=['POST', 'GET'])
def register():
	if request.method =="POST":
		username = request.form.get("username")
		email = request.form.get("email")
		password = request.form.get("password")
		#check database
		db_user = db.session.query(User).filter( or_(User.email==email, User.username==username)).first()
		print("user ", db_user)
		if db_user:
			flash("Account already exist. Try logging in.")
		else:
			new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)

			#create user avatar
			imgName= generateFileName([new_user.id], "profile")
			print("imgName ", imgName)
			resizeImage(app.config["PROFILE_UPLOADS"]+new_user.image_file, app.config["PROFILE_UPLOADS"]+imgName, PROFILE_SIZE)
			new_user.image_file = imgName
			db.session.commit()

			flash("Thanks for registering")
			return redirect(url_for("searchPets"))

	return render_template('public/signup.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("feed"))