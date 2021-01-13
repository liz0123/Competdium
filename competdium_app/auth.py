from flask import Flask, flash, request, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask import current_app as app
from .models import db, User
from .forms import LoginForm, RegisterForm


@app.route("/login", methods=["POST","GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		remember = True if form.remember.data else False
		user = User.query.filter_by(username=username).first()
		
		if user and check_password_hash(user.password, password):
			login_user(user, remember=remember)
			return redirect(url_for("feed"))
		
		flash('Please check your login details and try again.')
	return render_template("public/login.html",form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
	reg = RegisterForm()
	if reg.validate_on_submit():
		email = reg.email.data
		username = reg.username.data
		user_email = User.query.filter_by(email=email).first()
		user_name = User.query.filter_by(username=username).first()

		if user_email and user_name:
			flash("Account already exist. Try logging in.")

		elif user_email:
			flash("Email already exist!")

		elif user_name:
			flash("Username already exist!")

		else:
			flash('Thanks for registering')
			new_user = User(email=email, username=username, password=generate_password_hash(reg.password.data, method='sha256'))
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user)
			return redirect(url_for("feed",username=username))

	return render_template('public/signup.html', form=reg)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("feed"))