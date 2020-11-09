from flask import flash, request, redirect, render_template, make_response, session, url_for
from datetime import datetime, timedelta 
from flask import current_app as app
from .models import db, User

#app.permanent_session_lifetime = timedelta(hours=1)

# Database
@app.route("/logout")
def logout():
	if 'username' in session:
		session.pop("username")
		flash("Loggout successful!", "info")
	return render_template("public/index.html")

@app.route("/login", methods=["POST","GET"])
def login():
	if request.method =='POST':
		password = request.form.get("password")
		email = request.form.get("email")
		if email and password:
			existing_user = User.query.filter(User.email == email and User.password == password).first()
			session["username"] = existing_user.username
			if request.form.get("keep_login"):
				session.permanent = True
			flash("Login Succesful!")
			return redirect(url_for("dashboard"))

	return render_template("user/login.html")

@app.route("/signup", methods = ["POST","GET"])
def signup():
	if request.method =='POST':
		username = request.form.get("username")
		password = request.form.get("password")
		email = request.form.get("email")
		if username and email:
			existing_user = User.query.filter(User.username == username or User.email == email
        ).first()
			if existing_user:
				flash("Email or username already exist")
				return redirect(url_for("signup"))
				
			new_user = User(username=username, password=password, email=email)
			db.session.add(new_user)
			db.session.commit() 

			session["username"] = new_user.username
			
			flash("Account was created")
			return redirect(url_for("dashboard"))
	
	return render_template("user/signup.html")

# ------ user -------
@app.route("/user/dashboard")
def dashboard():
	if "username" not in session:
		flash("Please login")
		return redirect(url_for("login"))

	return render_template("user/dashboard.html", username=session["username"])

@app.route("/user/profile")
def profile():
	return "<h1 style = 'color: red'>User profile</h1>"

# ------ public -----
@app.route("/")
def index():

	return render_template("public/index.html")

@app.route("/adoption")
def adoption():
	return render_template("public/adoptionPage.html")

@app.route("/adoptPet")
def adoptPet():
	# get images form folder as list and pass list to imageDisplay.html
	imagePaths ={'1': '1.png'}
	return render_template("public/imageDisplay.html", imagePaths=imagePaths)

@app.route("/addPet", methods = ["POST"])
def addPet():
	if request.method =='POST':
		print("adding pet")

	return render_template("public/adoptionPage.html")


