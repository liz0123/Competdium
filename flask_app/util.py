from flask_mail import Message
from . import mail
from flask_app.forms import SearchPetForm
import os
from flask import current_app as app
from .models import db
from .models import Message as Msg
from sqlalchemy import or_
from PIL import Image
import os
import pusher
import cv2 as cv
from petpy import Petfinder
from datetime import datetime, timedelta
from itsdangerous import Serializer, URLSafeTimedSerializer

PROFILE_SIZE = (200, 200)
HEIGHT_PROFILE = (250, 200)
WIDTH_PROFILE = (200,250)
POST_SIZE = (400, 400)
PET_SIZE = (450, 400)
DAY = 1
MONTH = 30
TWO_MONTH = 60
YEAR_DAYS = 365
TWO_YEARS_DAYS = 730
MINUTE_IN_SECONDS = 60
TWO_MINUTE_IN_SECONDS = 120
HOUR_IN_SECONDS = 3600
TWO_HOUR_IN_SECONDS = 7200
DAY_IN_SECONDS = 86400


pusher_client = pusher.Pusher(
    app_id='1138510',
    key='c7fa9a824f00223cea96',
    secret='b315fc5f8cad057f8aed',
    cluster='us2',
    ssl=True
)

# Search Pet Finder
pf = Petfinder(key=app.config["KEY"], secret=app.config["SECRET"])


def searchPetFinder(form_data):
    # input form_data= { "type":type, "size": size, "age":age, "gender":gender, "city":city, "state":state }
    # list of pets with pet_id, name and image url
    location = form_data["city"]+", "+form_data["state"]

    animals = pf.animals(animal_type=form_data["type"], size=form_data["size"], age=form_data["age"], gender=form_data["gender"],
                         status='adoptable', location=location, distance=form_data["distance"], results_per_page=25)
    animal_ids = []
    for i in animals['animals']:
        animal_ids.append(i['id'])

    animal_data = pf.animals(animal_id=animal_ids)
    animals = []

    for animal in animal_data["animals"]:
        img = None
        for photo in animal["photos"]:
            img = photo["medium"]

        if img:
            animals.append({"id": animal["id"], "name": animal["name"],
                            "location": animals["location"], "image": img})

    return animals


def getPetFinder(petID):
    pet = {}
    pet_data = pf.animals(animal_id=petID)
    pet_data = pet_data["animals"]
    if pet_data:
        img = None
        for photo in pet_data["photos"]:
            img = photo["large"]
        pet = {"id": pet_data["id"], "name": pet_data["name"], "type": pet_data["type"], "age": pet_data["age"], "gender": pet_data["gender"],
               "description": pet_data["description"], "contact": pet_data["contact"], "url": pet_data["url"], "image": img}
    return pet

# Direct Messaging


def getMessages(currUser, otherUser):
    return db.session.query(Msg).filter(or_(Msg.sender_id == currUser.id, Msg.reciever_id == currUser.id)).filter(or_(Msg.sender_id == otherUser.id, Msg.reciever_id == otherUser.id)).all()


def formateMessages(currUser, otherUser):
    db_messages = getMessages(currUser, otherUser)
    list_messages = []
    for m in db_messages:
        message = {}
        message["message"] = m.message
        message["date"] = convertTime(m.date_created)

        message["sender"] = "your-message"
        message["img"] = ""
        if currUser.id is not m.sender_id:
            message["sender"] = "other-message"
            message["img"] = "../static/img/profiles/" + otherUser.image

        list_messages.insert(0, message)
    return list_messages


def getLastMessages(currUser, otherUser):
    db_messages = getMessages(currUser, otherUser)
    lastMessage = db_messages[-1]
    return {"message": lastMessage.message, "date": lastMessage.date_created}


def getFriendList(currUser):
    friends = currUser.friends
    friend_list = []
    for friend in friends:
        f = {}
        lastMessage = getLastMessages(currUser, friend)
        f["username"] = friend.username
        f["image_file"] = friend.image
        f["message"] = lastMessage["message"]
        f["date"] = convertTime(lastMessage["date"])
        friend_list.append(f)
    return friend_list

# Email Confirmation


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)

# Image Manipulation


def generateFileName(ids, uploadTo):
    # Input: ids is list conating user_id and post/pet ID, uploadTO is where img will be save to
    # Output: return a string name for the file
    user_id = ids[0]
    if "profile" is uploadTo:
        return "user_"+str(user_id)+"_avatar.jpg"

    obj_id = ids[1]

    if "post" is uploadTo:
        return "user_"+str(user_id)+"_post_"+str(obj_id)+"_original.jpg"

    return "user_"+str(user_id)+"_pet_"+str(obj_id)+"_original.jpg"


def generateThumbName(filename):
    # input: take a filename
    # output: returns string filename to thumbnail
    thmbnail = filename.replace("original", "thumbnail")
    return thmbnail


def relocateImage(fromURL, toURL):
    img = cv.imread(fromURL, cv.IMREAD_UNCHANGED)
    cv.imwrite(toURL, img)

def resizeImage(url):
    img = cv.imread(url, cv.IMREAD_UNCHANGED)
    height, width, channels = img.shape
    #if height > PROFILE_SIZE[1]:
    newImg = cv.resize(img, (500, 200), interpolation=cv.INTER_AREA)
    cv.imwrite(url, newImg)

@app.template_filter()
def convertTime(dt):
    time_dif = datetime.utcnow()-dt

    if time_dif.days < 0:
        return("Time created is in the futuer.")

    if time_dif.days > 0:
        if time_dif.days < MONTH:
            if time_dif.days == DAY:
                return("1 day ago")
            else:
                return("%s days ago" % (time_dif.days))
        elif time_dif.days < YEAR_DAYS:
            if time_dif.days < TWO_MONTH:
                return("1 month ago")
            else:
                return("%s months ago" % (int(time_dif.days/MONTH)))
        else:
            if time_dif.days < TWO_YEARS_DAYS:
                return("1 year ago")
            else:
                return("%s/%s/%s" % (dt.month, dt.day, dt.year))
    else:
        if time_dif.seconds < MINUTE_IN_SECONDS:
            return("Now")
        elif time_dif.seconds < HOUR_IN_SECONDS:
            if time_dif.seconds < TWO_MINUTE_IN_SECONDS:
                return("1 min ago")
            else:
                return("%s mins ago" % (int(time_dif.seconds/MINUTE_IN_SECONDS)))
        elif time_dif.seconds < DAY_IN_SECONDS:
            if time_dif.seconds < TWO_HOUR_IN_SECONDS:
                return("1 hour ago")
            else:
                return("%s hours ago" % (int(time_dif.seconds/HOUR_IN_SECONDS)))


@app.template_filter()
def convertTime2(dt):
    time_dif = datetime.utcnow()-dt

    if time_dif.days < 0:
        return("Time created is in the futuer.")

    if time_dif.days > 0:
        if time_dif.days < MONTH:
            if time_dif.days == DAY:
                return("1 day ago")
            else:
                return("%s days ago" % (time_dif.days))
        elif time_dif.days < YEAR_DAYS:
            if time_dif.days < TWO_MONTH:
                return("1 month ago")
            else:
                return("%s months ago" % (int(time_dif.days/MONTH)))
        else:
            if time_dif.days < TWO_YEARS_DAYS:
                return("1 year ago")
            else:
                return("%s/%s/%s" % (dt.month, dt.day, dt.year))
    else:
        if time_dif.seconds < MINUTE_IN_SECONDS:
            return("Now")
        elif time_dif.seconds < HOUR_IN_SECONDS:
            if time_dif.seconds < TWO_MINUTE_IN_SECONDS:
                return("1 min ago")
            else:
                return("%s mins ago" % (int(time_dif.seconds/MINUTE_IN_SECONDS)))
        elif time_dif.seconds < DAY_IN_SECONDS:
            if time_dif.seconds < TWO_HOUR_IN_SECONDS:
                return("1 hour ago")
            else:
                return("%s hours ago" % (int(time_dif.seconds/HOUR_IN_SECONDS)))



