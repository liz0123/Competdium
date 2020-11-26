
from PIL import Image
import  numpy as np
import cv2 as cv
import os, sys

# ---- Gather Data ---
# Image to arrays
data = []
labels = []

#Load data
dogs = np.load("dogData.npy")
labels = np.load("dogLabels.npy")

# Shuffle data for train and test set
s = np.arange(dogs.shape[0])
np.random.shuffle(s)
dogs = dogs[s]
labels = labels[s]

# Set totale number of animal categories and data length
num_classes =len(np.unique(labels))
data_length = len(dogs)

#--- Divide data into test and train ---
# divide data
(x_train,x_test)=dogs[(int)(0.1*data_length):],dogs[:(int)(0.1*data_length)]

x_train = x_train.astype('float32')/255
x_test = x_test.astype('float32')/255

train_length=len(x_train)
test_length=len(x_test)

# divide labels
(y_train,y_test) = labels[(int)(0.1*data_length):],labels[:(int)(0.1*data_length)]


# Make labels into one hot encoding 
import keras
from keras.utils import np_utils
y_train = keras.utils.to_categorical(y_train,num_classes)
y_test = keras.utils.to_categorical(y_test,num_classes)


# ---- Make Keras model ---

from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dense,Flatten,Dropout

#make model
model=Sequential()

model.add(Conv2D(filters=16,kernel_size=2,padding="same",activation="relu",input_shape=(50,50,3)))

model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=32,kernel_size=2,padding="same",activation="relu"))

model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters=64,kernel_size=2,padding="same",activation="relu"))

model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(500,activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(num_classes,activation="softmax"))

model.summary()

# compile the model
model.compile(loss='categorical_crossentropy', optimizer='adam', 
                  metrics=['accuracy'])


# --- Train the model ---
model.fit(x_train,y_train,batch_size=50,epochs=100,verbose=1)

# --- Test model ---
score = model.evaluate(x_test, y_test, verbose=1)
print('\n', 'Test accuracy:', score[1])
