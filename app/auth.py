from flask import Blueprint, render_template

auth= Blueprint('auth_routes', __name__ )
from flask import Blueprint, render_template, redirect, url_for

auth = Blueprint("auth", __name__)
# Database
@app.route("/login")
def login():
	return render_template("public/login.html")


@app.route("/signup")
def signup():
	return render_template("public/signup.html")

@app.route("/logout")
def logout():
	return render_template("public/home.html")