from flask import Flask, flash, request, render_template, redirect, url_for, request, flash, make_response, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from flask import current_app as app
from .forms import RegisterForm, LoginForm
from .models import db, User
from .util import *



@app.route("/login/", methods=["POST","GET"])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		email = request.form.get("username").lower()
		password = request.form.get("password")
		remember = True if request.form.get("remember") else False
		user = db.session.query(User).filter( or_(User.email==email, User.username==email )).first()

		if user and check_password_hash(user.password, password):
			login_user(user, remember=remember)
			return redirect(url_for("unconfirmed"))

		flash('Please check your login details and try again.')
	return render_template("public/login.html", form=form)

@app.route('/register/', methods=['POST', 'GET'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		username = request.form.get("username")
		email = request.form.get("email").lower()
		password = request.form.get("password")
		#check database
		db_user = db.session.query(User).filter( or_(User.email==email, User.username==username)).first()
		if db_user:
			flash("Account already exist. Try logging in.")
		else:
			new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
			db.session.add(new_user)
			db.session.commit()

			#create user avatar
			imgName = generateFileName([new_user.id], "profile")
			relocateImage(app.config["PROFILE_UPLOADS"]+new_user.image, app.config["PROFILE_UPLOADS"]+imgName)
			#resizeImage(app.config["PROFILE_UPLOADS"]+imgName)
			new_user.image = imgName
			db.session.commit()
			session["username"]= new_user.username
			flash("Thanks for registering")

			# Email Confirmation
			token = generate_confirmation_token(new_user.email)
			confirm_url = url_for('confirm_email', token=token, _external=True)
			html = render_template('user/activate.html', confirm_url=confirm_url)
			subject = "Please confirm your email"
			send_email(new_user.email, subject, html)

			login_user(new_user)
			flash('A confirmation email has been sent via email.', 'success')

			return redirect(url_for("searchPets"))

	return render_template('public/signup.html', form=form)

@app.route("/reset/", methods=["POST","GET"])
def resetPassword():
	if request.method == "POST":
		user = User.query.filter_by(email= request.form.get("email")).first()
		if not user:
			flash("Email is not in our system")
			return render_template("public/reset_password.html")
		# Recover Account
		token = generate_confirmation_token(user.email)
		recover_url = url_for('reset_with_token', token=token, _external=True)
		html = render_template('user/activate_password.html', recover_url=recover_url)
		subject = "Password reset requested"
		send_email(user.email, subject, html)
		flash('Check you email for link!', "warning")

	return render_template("public/reset_password.html")

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
	try:
		email = confirm_token(token)
	except:
		flash('The confirmation link is invalid or has expired.', 'danger')

	if request.method == "POST":
		user = User.query.filter_by(email=email).first_or_404()
		new_password = request.form.get('password')
		user.password = generate_password_hash(new_password, method='sha256')

		db.session.add(user)
		db.session.commit()
		flash('Your password has been reset!', 'success')
		return redirect(url_for("login"))

	return render_template('user/recover.html', token=token)

@app.route("/confirm/<token>")
@login_required
def confirm_email(token):
	try:
		email = confirm_token(token)
	except:
		flash('The confirmation link is invalid or has expired.', 'danger')
	user = User.query.filter_by(email=email).first_or_404()
	if user.confirmed:
		flash('Account already confirmed. Please login.', 'success')
	else:
		user.confirmed = True
		db.session.add(user)
		db.session.commit()
		flash('You have confirmed your account. Thanks!', 'success')
	return redirect(url_for("unconfirmed"))

@app.route("/unconfirmed")
@login_required
def unconfirmed():
	if current_user.confirmed:
		return redirect("feed")
	flash('Please confirm your account!', "warning")
	return render_template('user/unconfirmed.html')

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash("Logout successful!")
	return redirect(url_for("searchPets"))

# Delete Account
@app.route("/myprofile/deleteAccount/", methods=["POST"])
@login_required
def deleteAccount():
	#currUser = User.query.filter_by(id=current_user.get_id()).first()
	for pet in current_user.pets:
		db.session.delete(pet)

	db.session.delete(current_user)
	db.session.commit()
	flash("Account was deleted")
	return render_template("public/signup.html")

