from app import *
#from flask import render_template, redirect, request, url_for


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
