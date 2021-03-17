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



@app.template_filter()
def searchOption(form, type):
    if type == "dog":
        form.type.choices = [('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), ("horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.age.choices = [("baby", "Puppy"),("young", "Young"), ("adult", "Adult"), ("senior", "Senior")]
        form.breed.choices = [("labrador-retriever", "Labrador Retriever"), ('golden-retriever', "Golden Retriever"), ('german-shepherd', 'German Shepherd')]
     
    elif type == "cat":
        form.type.choices = [('cat', 'Cat'), ('dog', 'Dog'), ("barnyard", "Barnyard"), ('bird', 'Bird'), ("horse", "Horse"), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.age.choices = [("baby", "Kitten"),("young", "Young"), ("adult", "Adult"), ("senior", "Senior")]
        form.breed.choices = [('american-bobtail', 'American Bobtail'), ("persian", "Persian"), ("maine-Coon", "Maine Coon"),("bengal", "Bengal"), ('british-shorthair', 'British Shorthair'), ('persian-cat', 'Persian Cat')]
        form.coat.choices = [('small', 'Small'), ('long', 'Long')]
        form.color.choices = [('agouti', 'Agouti'), ('black', 'Black'), ('blue-gray', 'Blue/Gray'), ('brown-chocolate', 'Brown/Chocolate'), ('cream', 'Cream'), ('lilac', 'Lilac'), ('orange-red', 'Orange/Red'), ('sable', 'Sable'), ('silvermarten', "Silver Marten"), ('tan', 'Tan'), ('tortoiseshell', 'Tortoiseshell'), ('white', 'White')]
    
    elif type == 'rabbit':
        form.type.choices = [('rabbit', 'Rabbit'), ('cat', 'Cat'), ('dog', 'Dog'), ("barnyard", "Barnyard"), ('bird', 'Bird'), ("horse", "Horse"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.breed.choices = [('american', 'American'), ('american-sable', 'American Sable'),('angora-rabbit', 'Angora Rabbit'), ('belgian-hare', 'Belgian Hare')]
        form.coat.choices = [('small', 'Small'), ('long', 'Long')]

    elif type == 'small-furry':
        form.type.choices = [("small-furry", "Small-Furry"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), ("horse", "Horse"), ("rabbit", "Rabbit"), ("scales-fins-other", "Scales-Fins-Other")]
        form.breed.choices = [('abyssinian', 'Abyssinian'), ('chinchilla', 'Chinchilla'), ('degu', 'Degu'), ('dwarf-hamster', 'Dwarf Hamster'), ('ferret', 'Ferret'), ('gerbil', 'Gerbil'), ('guinea-pig', 'Guinea Pig'), ('hamster', 'Hamster'), ('hedgehog', 'Hedgehog'), ('mouse', 'Mouse'), ('peruvian', 'Peruvian'), ('prairie-dog', 'Prairie Dog'), ('rat', 'Rat'),('rex', 'Rex'), ('short-haired', 'Short-Haired'), ('silkie-sheltie', 'Silkie/Sheltie'), ('skunk', 'Skunk'), ('sugar-glider', 'Sugar Glider'), ('teddy', 'Teddy')]
        form.species.choices = [('chinchilla', 'Chinchilla'), ('degu', 'Degu'), ('ferret', 'Ferret'), ('gerbil', 'Gerbil'), ('guinea-pig', 'Guinea Pig'), ('hamster', 'Hamster'), ('hedgehog', 'Hedgehog'), ('mouse', 'Mouse'), ('prairie-dog', 'Prairie Dog'), ('rat', 'Rat'), ('skunk', 'Skunk'), ('sugar-glider', 'Sugar Glider')]
        form.coat.choices = [('hairless', 'Hairless'),('small', 'Small'), ('long', 'Long')]
        form.color.choices = [('agouti', 'Agouti'), ('albino', 'Albino'), ('black', 'Black'), ('black-sable', 'Black Sable'), ('blue-gray','Blue/Gray'), ('brown-chocolate', 'Brown/Chocolate'), ('calico', 'Calico'), ('cinnamon', 'Cinnamon'), ('cream', 'Cream'), ('orange-red', 'Orange/Red'), ('sable', 'Sable'), ('tan', 'Tan'), ('tortoiseshell', 'Tortoiseshell'), ('white', 'White'), ('white-dark-eyed', 'White (Dark-Eyed')]
    
    elif type == 'horse':
        form.type.choices = [("horse", "Horse"), ('dog', 'Dog'), ('cat', 'Cat'), ("barnyard", "Barnyard"), ('bird', 'Bird'), ("rabbit", "Rabbit"), ("small-furry", "Small-Furry"), ("scales-fins-other", "Scales-Fins-Other")]
        form.species.choices = [('donkey', 'Donkey'), ('horse', 'Horse'), ('miniature-horse', 'Miniature Horse'), ('mule', 'Mule'), ('pony', 'Pony')]
        form.breed.choices = [('appaloose', 'Appaloosa'), ('arabian', 'Arabian'), ('belgian', 'Belgian'), ('clydesdale','Clydesdale'), ('connemara', 'Connemara'), ('curly-horse', 'Curly Horse'), ('donkey', 'Donkey'), ('draft', 'Draft')]
     
    return form


def createPost(pet_id, category):
    pet = Pet.query.filter_by(id=int(pet_id)).first()
    compedium = User.query.filter_by(email="competdium@gmail.com").first()
    pet_id = None
    if category == "adopted":
        title = "Congratulations to "+pet.name.capitalize()
        content = " Another furry friend has found their forever home! We wish them all the best with their new family and that they recieve all the love and attention they deserve."
    elif category == "newpet":
        pet_id = pet.id
        title = "Meet "+pet.name.capitalize()
        content = pet.name.capitalize()+" is a "+pet.type
    newPost = Post(category=category, title=title,
                   content=content, user_id=compedium.id, id_pet=pet_id)
    newPost.writer.append(compedium)
    db.session.add(newPost)
    db.session.commit()

    imageName = generateFileName([compedium.id, newPost.id], "post")
    newPost.image = imageName

    fromURL = os.path.join(app.config["PET_UPLOADS"], pet.image)
    toURL = os.path.join(app.config["POST_UPLOADS"], imageName)
    relocateImage(fromURL, toURL)
    db.session.commit()
    return True


def daysInFilter(days, pets):
    # Days on Competdium
    for pet in pets[:]:
        numDays = (datetime.utcnow()-pet.date_created).days
        bool = int(days) < numDays
    if bool:
        pets.remove(pet)
    return pets


def toJsonFriendly(pets):
    petsDic = []
    for pet in pets:
        p = {'id': pet.id, 'name': pet.name,
             'breed': pet.breed.replace('-'," "), 'age': pet.age,
             'size': pet.size, "city": pet.city,
             "state": pet.state, "image": pet.image}
        try:
            if pet in current_user.liked_pets:
                p['liked'] =True
        except:
            p['liked'] = False
        petsDic.append(p)
    return petsDic

def applyFilters(request):
    type = request.form.get("type")
    days = request.form.get("days")
    name = request.form.get("name").lower()
    breed = request.form.getlist("breed")
    age = request.form.getlist("age")
    size = request.form.getlist("size")
    gender = request.form.getlist("gender")
    goodwith = request.form.getlist("goodwith")
    coat = request.form.getlist("coat")
    care = request.form.getlist("care")
    color = request.form.getlist("color")
    #
    city = request.form.get("city").lower()
    state = request.form.get("state")
    # Create filter
    pets = db.session.query(Pet).order_by(Pet.id.desc())
    filter_spec = []
    form_data = {'type': type, 'name': name, 'city':city, 'state':state}
    for key in form_data:
        if (form_data[key] != 'None') and (form_data[key]) and not (form_data[key].isspace()):
            filter = {'field': key, 'op': '==', 'value': form_data[key]}
            filter_spec.append(filter)

    pets = apply_filters(pets, filter_spec)
    form_data_list = {"breed": breed, "age": age, "size": size, "gender": gender, "goodwith": goodwith,
                      "coat": coat, "color": color, "care": care}
    filter_spec = []
    filter_or = {}
    for key in form_data_list:
        for value in form_data_list[key]:
            filter = {'field': key, 'op': 'like', 'value': '%'+value+'%'}
            filter_spec.append(filter)
        if form_data_list[key]:
            filter_or["or"] = filter_spec
            filter_1 = []
            filter_1.append(filter_or)
            pets = apply_filters(pets, filter_1)
            filter_spec = []
    # Apply Filter
    pets = daysInFilter(days, pets) if days != 'None' else pets
    return pets.all()


@app.route("/searchPets/filters", methods=["POST", "GET"])
def filters():
    pets = applyFilters(request)
    output = toJsonFriendly(pets)
    return make_response({"update": "Update", "pets": output}, 200)

@app.route("/", methods=["POST", "GET"])
@app.route("/searchPets/", methods=["POST", "GET"])
def searchPets():
    pets = db.session.query(Pet).order_by(Pet.id.desc()).all()
    petForm = PetForm()
    searchForm = SearchPetForm(request.form)
    if request.method == 'POST':
        type = request.form.get("type")
        searchForm = searchOption(searchForm, type)
        pets = applyFilters(request)
        
    finder_pets = None
    return render_template("public/searchPets.html", pets=pets, form=petForm, searchForm=searchForm, finder_pets=finder_pets, datetime=datetime.utcnow())


def convertToString(org_list, seperator=' '):
    return seperator.join(org_list)


@app.route("/searchPets/addPet", methods=["POST", "GET"])
@login_required
def addPet():
    type = request.form.get("type")
    print("type ", type)
    if type != 'None':
        try:
            img = request.files['image']
            name = request.form.get("name").lower()
            age = request.form.get("age")
            size = request.form.get("size")
            gender = request.form.get("gender")
            breed = convertToString(request.form.getlist("breed"))
            goodwith = convertToString(request.form.getlist("goodwith"))
            coat = convertToString(request.form.getlist('coat'))
            color = convertToString(request.form.getlist('color'))
            care = convertToString(request.form.getlist('care'))

            city = request.form.get("city").lower()
            state = request.form.get("state")
            zip = request.form.get("zip")
            desc = request.form.get("description")
            # Create and save new pet
            newPet = Pet(type=type, name=name, age=age, gender=gender, size=size, breed=breed, goodwith=goodwith, coat=coat, color=color, care=care,
                        description=desc, city=city, state=state, zip=zip, user_id=current_user.get_id())
            db.session.add(newPet)
            db.session.commit()
            # create image name
            imageName = generateFileName([current_user.get_id(), newPet.id], "pet")
            # save images
            img.save(os.path.join(app.config["PET_UPLOADS"], imageName))
            # save names to db
            newPet.image = imageName
            # Create Post
            createPost(newPet.id, "newpet")
            db.session.commit()
            flash("Your pet was add!")
            return redirect(url_for("searchPets"))
        except:
            flash("Unable to add pet")
            return redirect(url_for("searchPets"))
    flash("Please select type of pet")
    return redirect(url_for("searchPets"))


@ app.route("/searchPets/viewPetFinder=<petID>/")
def viewPetFinder(petID):
    pet = getPetFinder(petID)
    return render_template("pet/view_petfinder.html", pet=pet, datetime=datetime.utcnow())


@ app.route("/myprofile/pets/edit_<pet_id>/", methods=["POST", "GET"])
@ login_required
def viewEditPet(pet_id):
    pet = Pet.query.filter_by(
        user_id=current_user.get_id(), id=pet_id).first()
    if not pet:
        flash("Pet not found")
        return redirect(url_for("my_profile"))
    return render_template("pet/edit_pet.html", pet=pet, datetime=datetime.utcnow())


@ app.route("/searchPets/viewPet=<pet_id>/")
def viewPet(pet_id):
    pet = Pet.query.filter_by(id=pet_id).first()
    owner = User.query.filter_by(id=pet.user_id).first()
    liked = False
    if current_user.is_authenticated:
        if pet in current_user.liked_pets:
            liked = True
    return render_template("pet/pet_info.html", pet=pet, owner=owner.username, liked=liked, datetime=datetime.utcnow())


@ app.route("/myprofile/pets/updatePet/", methods=["POST"])
@ login_required
def editPet():
    # img =  request.files['image']
    pet_id = int(request.form.get("pet_id"))
    currPet = Pet.query.filter_by(id=pet_id).first()
    if not currPet:
        return make_response(jsonify({"error": "Pet was not found"}), 400)
    currPet.name = request.form.get("name")
    currPet.type = request.form.get("type")
    currPet.gender = request.form.get("gender")
    currPet.size = request.form.get("size")
    currPet.description = request.form.get("description")
    db.session.commit()
    return make_response(jsonify({"update": "Pet was updated"}), 200)


@ app.route("/myprofile/pets/updatePetImage/", methods=["POST"])
@ login_required
def editPetImage():
    req = request.files['img']
    pet_id = request.form.get("pet_id")
    pet = Pet.query.filter_by(id=pet_id).first()
    # save input image
    img_path = os.path.join(app.config["PET_UPLOADS"], pet.image)
    req.save(img_path)
    return make_response(jsonify({"update": "Pet Image was saved", "img": img_path}), 200)

# Delet Pet
@ app.route("/myprofile/edit/deletePet_<pet_id>/", methods=["POST"])
@ login_required
def removePet(pet_id):
    Pet.query.filter_by(user_id=current_user.get_id(), id=pet_id).delete()
    db.session.commit()
    flash("Pet was removed!")

    return redirect(url_for("my_profile"))


@ app.route("/myprofile/pet/adopted<pet_id>", methods=["POST", "GET"])
@ login_required
def adoptedPet(pet_id):
    createPost(pet_id, "adopted")
    # delete post
    Pet.query.filter_by(user_id=current_user.get_id(), id=pet_id).delete()
    db.session.commit()
    flash("Pet was removed")
    return redirect(url_for("my_profile"))
