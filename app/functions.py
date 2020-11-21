import os
from flask import current_app as app
from PIL import Image

def formateImage(user, postID, imageName):
    imagePath = app.config["POST_UPLOADS"]+imageName
    #Resize image
    image =Image.open(imagePath)
    image.thumbnail((400,400))
    # Create new image name
    newImageName = user+str(postID)+imageName
    # Save new image
    image.save(app.config["POST_UPLOADS"]+newImageName)
    # Remove old image
    os.remove(imagePath)

    return newImageName
