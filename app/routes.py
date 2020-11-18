from flask import flash, request, redirect, render_template, make_response, session, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta 
from flask import current_app as app
from .models import db, User

#app.permanent_session_lifetime = timedelta(hours=1)

@app.route("/")
def index():
	return render_template("public/home.html")

# ------ user -------
@app.route("/user/dashboard")
def dashboard():
	if "username" not in session:
		flash("Please login")
		return redirect(url_for("login"))

	return render_template("user/dashboard.html", username=session["username"])

@app.route("/profile/<username>")
@login_required
def profile(username):
	user = User.query.filter_by(id=current_user.get_id()).first()
	
	return render_template("user/profile.html", username=user.username,email=user.email)

# ------ public -----

@app.route("/adoption")
def adoption():
	username = True if "username" in session else False

	return render_template("public/adoptionPage.html", username= username)

@app.route("/adoptPet")
def adoptPet():
	username = True if "username" in session else False
	# get images form folder as list and pass list to imageDisplay.html
	imagePaths ={'1': '1.png'}
	return render_template("public/imageDisplay.html", imagePaths=imagePaths, username=username)

@app.route("/addPet", methods = ["POST"])
def addPet():
	if request.method =='POST':
		print("adding pet")

	return render_template("public/adoptionPage.html")


