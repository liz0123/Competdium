import os
from flask import current_app as app
from PIL import Image
import os
import cv2 as cv
from datetime import datetime, timedelta
PROFILE_SIZE = (200,200)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def generateFileName(ids, uploadTo):
    #Input: ids is list conating user_id and post/pet ID, uploadTO is where img will be save to
    #Output: return a string name for the file
    user_id = ids[0]
    if "profile" is uploadTo:
        return "user_"+str(user_id)+"_avatar.jpg"

    obj_id = ids[1]

    if "post" is uploadTo:
        return "user_"+str(user_id)+"_post_"+str(obj_id)+"_original.jpg"
    
    return "user_"+str(user_id)+"_pet_"+str(obj_id)+"_original.jpg"


def generateThumbName(filename):
    #input: take a filename
    #output: returns string filename to thumbnail
    thmbnail = filename.replace("original","thumbnail")
    return thmbnail

def resizeImage(fromURL, toURL, size):
    img = cv.imread(fromURL, cv.IMREAD_UNCHANGED )
    height, width, channels = img.shape

    if height > size[0]:
        img= cv.resize(img, size, interpolation=cv.INTER_AREA)
    
    cv.imwrite(toURL, img)

def saveImage(pet_id, user_id, form_img, saveToFolder, size):
    # Set Image Names
    filename = form_img.data.filename
    org_name = "user_"+str(user_id)+"_pet_"+str(pet_id)+"_original_"+filename
    org_name = org_name[:-3]+"jpg"

    if "post" in saveToFolder:
        org_name = org_name.replace("pet","post")
    thmbnail = org_name.replace("original","thumbnail")

    # Save Image
    full_org_name = os.path.join(saveToFolder, org_name)
    full_thmbnail = os.path.join(saveToFolder, thmbnail)
    form_img.data.save (full_org_name)

    setThumbnail(full_org_name, full_thmbnail, size)
    
    return (org_name, thmbnail)

def setThumbnailPil(fromURL, toURl, size):
    image = Image.open(fromURL)
    width, height= image.size
    if height > size[0]:
        image.thumbnail(size)
    image.save(toURl)

def setThumbnail(fromURL, toURl, size):
    img = cv.imread(fromURL, cv.IMREAD_UNCHANGED )
    height, width, channels = img.shape

    if height > size[0]:
        img= cv.resize(img, size, interpolation=cv.INTER_AREA)
    
    cv.imwrite(toURl, img)

def formateImage(user, data, maxsize, uploads):
    #Get Image
    imgPath = app.config[uploads]+data.original_image
    # get pet type
    petType = classifyPet(imgPath)
    print("pet: ", petType)
    #
    img = cv.imread(imgPath, cv.IMREAD_UNCHANGED )
    height, width, channels = img.shape

    #Rename images
    original_image_name ="user_"+str(user)+"pet"+str(data.id)+"_original_"+data.original_image
    original_image_name = original_image_name[:-3]+"jpg"
    if uploads == "POST_UPLOADS":
        original_image_name = original_image_name.replace("pet","post")
    thumbnail_name = original_image_name

    if height > maxsize:
        thumbnail_name = original_image_name.replace("original", "px"+str(maxsize))
        thumbnail= cv.resize(img, (maxsize, maxsize), interpolation=cv.INTER_AREA)
        cv.imwrite(app.config[uploads]+thumbnail_name, thumbnail)
    cv.imwrite(app.config[uploads]+original_image_name, img)
    # Delect user image
    os.remove(imgPath)  
    return (original_image_name,thumbnail_name,petType)

def saveThumbnail(user, filename, maxsize, uploads):
    #Get Image
    imgPath = app.config[uploads]+filename
    img = cv.imread(imgPath, cv.IMREAD_UNCHANGED )
    height, width, channels = img.shape

    thumbnail_name ="user_"+str(user)+"profile_"+ filename
    if height > maxsize:
        thumbnail= cv.resize(img, (maxsize, maxsize), interpolation=cv.INTER_AREA)
    cv.imwrite(app.config[uploads]+thumbnail_name, thumbnail)

    os.remove(imgPath)  
    return thumbnail_name

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
DAY = 1
MONTH=30
TWO_MONTH = 60
YEAR_DAYS = 365
TWO_YEARS_DAYS = 730
MINUTE_IN_SECONDS = 60
TWO_MINUTE_IN_SECONDS = 120
HOUR_IN_SECONDS = 3600
TWO_HOUR_IN_SECONDS = 7200
DAY_IN_SECONDS = 86400


def convertTime(dt):
    time_dif =  datetime.utcnow()-dt

    if time_dif.days <0:
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
                return("%s months ago" %(int(time_dif.days/MONTH)) )
        else:
            if time_dif.days < TWO_YEARS_DAYS:
                return("1 year ago")
            else:
               return("%s/%s/%s" %(dt.month, dt.day, dt.year))
    else:
        if time_dif.seconds < MINUTE_IN_SECONDS:
            return("Now")
        elif time_dif.seconds < HOUR_IN_SECONDS:
            if time_dif.seconds < TWO_MINUTE_IN_SECONDS:
                return("1 min ago")
            else:
                return("%s mins ago" %(int(time_dif.seconds/MINUTE_IN_SECONDS)))
        elif time_dif.seconds < DAY_IN_SECONDS:
            if time_dif.seconds < TWO_HOUR_IN_SECONDS:
                return("1 hour ago")
            else:
                return("%s hours ago" %(int(time_dif.seconds/HOUR_IN_SECONDS)))


