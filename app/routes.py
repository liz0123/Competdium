from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, User
@app.route("/logout")
def logout():
	session.pop("email")
	session.pop("username")
	session.pop("password")
	return redirect("/")

@app.route("/signing_in", methods=["POST"])
def signIn():
	if request.method =='POST':
		password = request.form.get("password")
		email = request.form.get("email")
		if email and password:
			existing_user = User.query.filter(User.email == email and User.password == password).first()
			return render_template("user/dashboard.html")

	return redirect(url_for("/login"))

@app.route("/addingUser", methods = ["POST"])
def addUser():
	print("adding user")
	if request.method =='POST':
		username = request.form.get("username")
		password = request.form.get("password")
		email = request.form.get("email")
		if username and email:
			existing_user = User.query.filter(User.username == username or User.email == email
        ).first()
			if existing_user:
				return make_response(f'{username} ({email}) already created!')
			new_user = User(username=username, password=password, email=email)
			db.session.add(new_user)
			db.session.commit()

			return render_template("user/dashboard.html")
	
	return redirect(url_for("/signup"))