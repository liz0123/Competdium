from app import *

@app.route("/user/dashboard")
def dashboard():
	return render_template("user/dashboard.html")

@app.route("/user/profile")
def profile():
	return "<h1 style = 'color: red'>User profile</h1>"