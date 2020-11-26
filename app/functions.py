import os
from flask import current_app as app
from PIL import Image

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def formateImage(user, post, px, uploads):
    imagePath = app.config[uploads]+post.original_image
    #Rename orignal image
    image =Image.open(imagePath)
    og_name = str(user)+"_"+str(post.id)+"_original_"+post.original_image
    image.save(app.config[uploads]+og_name)
    
    #resize image 
    image.thumbnail((px,px))
    # Create new thumbnail name
    thnail_name = str(user)+"_"+str(post.id)+"_"+str(px)+"px_"+post.original_image
    # Save new image
    image.save(app.config[uploads]+thnail_name)

    # Remove old image
    os.remove(imagePath)    
    return (og_name, thnail_name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def classifyImage(filename):
    imagePath = app.config["PET_UPLOADS"]+filename

    pass