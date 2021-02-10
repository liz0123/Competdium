import os
from PIL.Image import new
from flask import flash, request, redirect, render_template, make_response, session, url_for, send_from_directory, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from sqlalchemy_filters import apply_filters
from flask_mail import Message
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import PetForm, SearchPetForm
from .models import db, User, Post, Pet
from .util import *

@app.route("/", methods=["POST","GET"])
@app.route("/searchPets/", methods=["POST","GET"])
def searchPets():
	pets = db.session.query(Pet).order_by(Pet.id.desc())
	form = PetForm(request.form)
	searchForm = SearchPetForm(request.form)
	if request.method == 'POST':
		if form.validate():
			img =  request.files['image']
			name = request.form.get("name")
			type = request.form.get("type")
			gender = request.form.get("gender")
			size = request.form.get("size")
			age = request.form.get("age")
			month = int( request.form.get("month") )
			year = int( request.form.get("year") )
			desc = request.form.get("description")
			birthday = datetime(year, month, 1)
			# Create and save new pet
			newPet = Pet(type=type, name=name,age=age, gender=gender, size=size, birth_date=birthday, description=desc, user_id=current_user.get_id())
			db.session.add(newPet)
			db.session.commit()

			#create image names
			imageName =  generateFileName([current_user.get_id(),newPet.id], "pet")
			thumbName =  generateThumbName(imageName)
			#save images
			img.save(os.path.join(app.config["PET_UPLOADS"], imageName))
			resizeImage(os.path.join(app.config["PET_UPLOADS"], imageName), os.path.join(app.config["PET_UPLOADS"], thumbName), PET_SIZE)

			#save names to db
			newPet.original_image = imageName
			newPet.thumbnail = thumbName

			db.session.commit()
			searchForm = SearchPetForm()
			flash("Your pet was add!")

		else:
			type= request.form.get("type")
			size = request.form.get("size")
			age = request.form.get("age")
			gender = request.form.get("gender")

			form_data= { "type":type, "size": size, "age":age, "gender":gender }
			filter_spec=[]
			for key in form_data:
				if form_data[key] != "any":
					filter={}
					filter["field"] = key
					filter["op"] = "=="
					filter["value"] = form_data[key]
					filter_spec.append(filter)
			pets = apply_filters(pets, filter_spec)
			form = PetForm()

	pets = pets.all()
	likes =[]
	if current_user.get_id():
		currUser = User.query.filter_by(id=current_user.get_id()).first()
		likes=currUser.liked_pets
	return render_template("public/searchPets.html", pets=pets, likes=likes, form=form, searchForm=searchForm)

@app.route("/myprofile/pets/edit_<pet_id>/", methods=["POST","GET"])
@login_required
def viewEditPet(pet_id):
	pet = Pet.query.filter_by(user_id=current_user.get_id(), id=pet_id).first()
	if not pet:
		flash("Pet not found")
		return redirect(url_for("my_profile"))

	return render_template("pet/edit_pet.html", pet=pet)

@app.route("/myprofile/pets/updatePet/", methods=["POST"])
@login_required
def editPet():
	#img =  request.files['image']
	pet_id = int( request.form.get("pet_id") )
	month = int( request.form.get("month") )
	year = int( request.form.get("year") )

	currPet = Pet.query.filter_by(id=pet_id).first()
	if not currPet:
		return make_response(jsonify({"error": "Pet was not found"}), 400)
	currPet.name = request.form.get("name")
	currPet.type = request.form.get("type")
	currPet.gender = request.form.get("gender")
	currPet.size = request.form.get("size")
	currPet.description = request.form.get("description")
	currPet.birth_date = datetime(year, month, 1)
	db.session.commit()
	return make_response(jsonify({"update": "Pet was updated"}), 200)

@app.route("/myprofile/pets/updatePetImage/", methods=["POST"])
@login_required
def editPetImage():
	req = request.files['img']
	pet_id = request.form.get("pet_id")

	pet = Pet.query.filter_by(id=pet_id).first()
	# save input image
	img_path = os.path.join(app.config["PET_UPLOADS"], pet.original_image)
	req.save(img_path)
	#save thumbnail
	thum_path = os.path.join(app.config["PET_UPLOADS"],  pet.thumbnail)

	resizeImage(fromURL=img_path, toURL= thum_path, size=PET_SIZE)

	return make_response(jsonify({"update":"Pet Image was saved","img":img_path}), 200)

@app.route("/searchPets/addpet", methods=["POST","GET"])
@login_required
def addPet():
	print("add pet")
	form = PetForm(request.form)
	if request.method == 'POST' and form.validate():
		print("add pet")
		img =  request.files['file']
		name = request.form.get("name")
		type = request.form.get("type")
		gender = request.form.get("gender")
		size = request.form.get("size")
		month = int( request.form.get("month") )
		year = int( request.form.get("year") )
		desc = request.form.get("description")
		birthday = datetime(year, month, 1)
		# Create and save new pet
		newPet = Pet(type=type, name=name, gender=gender, size=size, birth_date=birthday, description=desc, user_id=current_user.get_id())
		db.session.add(newPet)
		db.session.commit()

		#create image names
		imageName =  generateFileName([current_user.get_id(),newPet.id], "pet")
		thumbName =  generateThumbName(imageName)
		#save images
		img.save(os.path.join(app.config["PET_UPLOADS"], imageName))
		resizeImage(os.path.join(app.config["PET_UPLOADS"], imageName), os.path.join(app.config["PET_UPLOADS"], thumbName), PET_SIZE)

		#save names to db
		newPet.original_image = imageName
		newPet.thumbnail = thumbName

		db.session.commit()
		flash("Your pet was add!")
	return redirect(url_for("searchPets",form=form))

@app.route("/searchPets/likedPet", methods=["POST"])
@login_required
def addLikedPet():
	currUser = User.query.filter_by(id=current_user.get_id()).first()
	pet = Pet.query.filter_by( id=request.form.get("pet_id") ).first()
	currUser.liked_pets.append(pet)
	db.session.commit()
	return  make_response(jsonify({"update": "Pet was liked!"}), 200)

@app.route("/searchPets/removeLikedPet", methods=["POST"])
@login_required
def removeLikedPet():
	currUser = User.query.filter_by(id=current_user.get_id()).first()
	pet = Pet.query.filter_by( id=request.form.get("pet_id") ).first()
	currUser.liked_pets.remove(pet)
	db.session.commit()
	return  make_response(jsonify({"update": "Pet was unliked!"}), 200)

#Delet Pet
@app.route("/myprofile/edit/deletePet_<pet_id>", methods=["POST"])
@login_required
def removePet(pet_id):
	pet = Pet.query.filter_by(user_id=current_user.get_id(), id=pet_id).delete()
	db.session.commit()
	flash("Pet was removed!")
	
	return redirect(url_for("my_profile"))
