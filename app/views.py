from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User

@app.route("/")
def index():
	print(app.config["ENV"])

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

@app.route("/signup")
def signup():
	return render_template("user/signup.html")

@app.route("/login" )
def login():
	return render_template("user/login.html")
