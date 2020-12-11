import os
from flask import current_app as app
from PIL import Image
import os
import cv2 as cv
import numpy as np
from tensorflow import keras

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

#------ Classification -------------
def convert_to_array(img):
    im = cv.imread(img)
    img = Image.fromarray(im, 'RGB')
    image = img.resize((50, 50))
    return np.array(image)

def get_breed(label):
    if label==0:
      return "DOG" 
    if label==1:
      return "CAT" 
    if label==2:
      return "BIRD"
    if label==3:
      return "RABBIT"

def classifyPet(filename):
    model = keras.models.load_model(app.config['PET_MODEL'])
    print("Predicting .................................")
    ar=convert_to_array(filename)
    ar=ar/255
    label=1
    a=[]
    a.append(ar)
    a=np.array(a)
    score=model.predict(a,verbose=1)
    print(score)
    label_index=np.argmax(score)
    print(label_index)
    acc=np.max(score)
    pet=get_breed(label_index)
    print(pet)
    print("The predicted Animal is a "+pet+" with accuracy =    "+str(acc))
    print()
    if acc <0.7:
        return "OTHER"
    return pet
