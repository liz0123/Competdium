
from flask import current_app as app
from flask import redirect, render_template, session, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from .models import db, Post
from .util import *
import os

#app.permanent_session_lifetime = timedelta(hours=1)
@app.route("/feed", methods=["POST","GET"])
def feed():
	posts = Post.query.order_by(Post.id.desc()).all()
	
	return render_template("public/feed.html", posts=posts)