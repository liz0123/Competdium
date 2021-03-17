
from flask import current_app as app
from flask import flash, redirect, render_template, session, make_response, jsonify, url_for
from flask.globals import request
from flask.wrappers import Response
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from wtforms import form
from .models import db, Post, Comment, User
from .forms import PostForm
from .util import *
import os


def getRecentPost():
    return Post.query.order_by(Post.id.desc()).all()

def getCategoryPost(category):
    return Post.query.filter_by(category=category).order_by(Post.id.desc()).all()

def getLikePost():
    return Post.query.order_by(Post.likes.desc()).all()

#app.permanent_session_lifetime = timedelta(hours=1)

@app.route("/feed/", methods=["POST", "GET"])
def feed():
    return redirect(url_for('feedTabs', tab='recent'))

@app.route("/feed/<tab>", methods=["POST", "GET"])
def feedTabs(tab):
    print("get")
    print("tab ", tab)
    form = PostForm()
    if tab == "adopted" or tab == "newpet":
        posts = getCategoryPost(tab)
    elif tab == "mostliked":
        posts = getLikePost()
    else:
        posts = getRecentPost()
    return render_template("public/feed.html", posts=posts, form=form, datetime=datetime.utcnow(), tab=tab)

@app.route("/feed/addPost/", methods=["POST", "GET"])
@login_required
def addPost():
    title = request.form.get("title")
    content = request.form.get("content")
    newPost = Post(title=title, content=content, user_id=current_user.get_id())
    newPost.writer.append(current_user)
    db.session.add(newPost)
    db.session.commit()
    # add Image
    if request.files["image"].filename != "":
        imageName = generateFileName(
            [current_user.get_id(), newPost.id], "post")
        # save images
        inputImage = request.files["image"]
        inputImage.save(os.path.join(app.config["POST_UPLOADS"], imageName))
        #
        newPost.image = imageName
        db.session.commit()
    return redirect(url_for("feed"))

@app.route("/feed/addComment/", methods=["POST"])
@app.route("/community/addComment", methods=["POST"])
@login_required
def addComment():
    req = request.get_json()
    comment = req["comment"]
    if comment.isspace() or comment == "":
        return make_response(jsonify({"update": "Commpent was empty"}), 200)

    user_id = int(req["from_id"])
    post_id = int(req["post_id"])

    newComment = Comment(content=comment)
    db.session.add(newComment)
    db.session.commit()

    user = User.query.filter_by(id=user_id).first()
    newComment.auther.append(user)
    post = Post.query.filter_by(id=post_id).first()
    post.comments.append(newComment)
    db.session.commit()

    pusher_client.trigger('comment-channel', 'new-comment', {"img": user.image, "username": user.username, "date": convertTime(
        newComment.date_created), 'comment': comment, "post_id": post_id})

    return make_response(jsonify({"update": "comment was added!"}), 200)


@app.route("/community/post=<post_id>")
def viewPost(post_id):
    post = Post.query.filter_by(id=post_id).first()
    return render_template("public/post.html", post=post)
