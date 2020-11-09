from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User


@app.route("/user/dashboard")
def dashboard():
	return render_template("user/dashboard.html")

@app.route("/user/profile")
def profile():
	return "<h1 style = 'color: red'>User profile</h1>"



