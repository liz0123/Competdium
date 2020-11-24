import os
from flask import current_app as app
from PIL import Image

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def formateImage(user, post, px, uploads):
    imagePath = app.config[uploads]+post.image_file
    #Resize image
    image =Image.open(imagePath)
    image.thumbnail((px,px))
    # Create new image name
    newImageName = str(user)+"_"+str(post.id)+"_"+post.image_file
    # Save new image
    image.save(app.config[uploads]+newImageName)
    # Remove old image
    os.remove(imagePath)

    return newImageName

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classifyImage(filename):
    imagePath = app.config["PET_UPLOADS"]+filename

    pass