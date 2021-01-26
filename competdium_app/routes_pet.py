import os
from flask import flash, request, redirect, render_template, make_response, session, url_for, send_from_directory, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User, Post, Pet
from .functions import *


@app.route("/myprofile/pets/edit=<petName>_<petID>", methods=["POST","GET"])
@login_required
def editPet(petName, petID):
	pet = Pet.query.filter_by(user_id=current_user.get_id(), id=petID).first()
	if not pet:
		flash("Pet not found")
		return redirect(url_for("my_profile"))

	return render_template("pet/edit_pet.html", pet=pet)

@app.route("/searchPets/search", methods=["POST"])
def search():
	petType = request.form.get("type")
	petSize = request.form.get("size")
	petAge = request.form.get("age")
	distance = request.form.get("distance")
	pets = Pets.query.order_by( type=petType, size=petSize, age=petAge ).first()