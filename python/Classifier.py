import keras
from keras.utils import np_utils
from PIL import Image
import  numpy as np
import cv2 as cv
import os, sys


# ---- Gather Data ---
# Image to arrays
data = []
labels = []

path = "C:/Users/Work/Documents/gitHub/Dogs/DogImages/"
chi = os.listdir(path+"Chihuahua")
french = os.listdir(path+"French Bulldog")
german = os.listdir(path+"German Shepherd")

for dog in chi:
    img = cv.imread(path+"/Chihuahua/"+dog)
    img_to_arr = Image.fromarray(img,'RGB')
    resized_img = img_to_arr.resize((50,50))
    data.append(np.array(resized_img))
    labels.append(0)

for dog in french:
    img = cv.imread(path+"/French Bulldog/"+dog)
    img_to_arr = Image.fromarray(img,'RGB')
    resized_img = img_to_arr.resize((50,50))
    data.append(np.array(resized_img))
    labels.append(1)

for dog in german:
    img = cv.imread(path+"/German Shepherd/"+dog)
    img_to_arr = Image.fromarray(img,'RGB')
    resized_img = img_to_arr.resize((50,50))
    data.append(np.array(resized_img))
    labels.append(2)

# convert to numpy array
dogs = np.array(data)
labels = np.array(labels)

#save dog data
np.save("C:/Users/Work/Documents/gitHub/Dogs/DogImages/dogData", dogs)
np.save("C:/Users/Work/Documents/gitHub/Dogs/DogImages/dogLabels", labels)

# Shuffle data for train and test set
s = np.arange(dogs.shape[0])
np.random.shuffle(s)
dogs = dogs[s]
labels = labels[s]

# Set totale number of animal categories and data length
num_classes =(np.unique(labels))
data_length = len(dogs)

#--- Divide data into test and train ---
# divide data
(x_train,x_test)=dogs[(int)(0.1*data_length):],dogs[:(int)(0.1*data_length)]

x_train = x_train.astype('float32')/255
x_test = x_test.astype("float32")/255

train_length = len(x_train)
test_length = len(x_test)

# divide labels
(y_train,y_test)=labels[(int)(0.1*data_length):],labels[:(int)(0.1*data_length)]