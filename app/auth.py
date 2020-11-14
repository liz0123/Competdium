from flask import Flask, flash, request, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask import current_app as app
from .models import db, User


@app.route("/login", methods=["POST","GET"])
def login():

	if request.method == "POST":
		email = request.form.get('email')
		password = request.form.get('password')
		remember = True if request.form.get('remember') else False

		user = User.query.filter_by(email=email).first()
		
		if not user and not check_password_hash(user.password, password):
			flash('Please check your login details and try again.')
			return redirect(url_for('login'))
		
		login_user(user, remember=remember)
		return redirect(url_for('profile'))
	
	return render_template("public/login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
	if request.method == "POST":
		email = request.form.get('email')
		name = request.form.get('username')
		password = request.form.get('password')
		
		user = User.query.filter_by(email=email).first()
		
		if user:
			flash('Email address already exists.')
			return redirect(url_for('signup'))
		
		new_user = User(email=email, username=name, password=generate_password_hash(password, method='sha256'))
		db.session.add(new_user)
		db.session.commit()
		return redirect(url_for('profile'))

	return render_template("public/signup.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))