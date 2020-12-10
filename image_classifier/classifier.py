from PIL import Image
import os
import cv2 as cv
import numpy as np

cwd = os.getcwd()
print("dir: ", cwd)
# ---- Gather Data ---
# Load data
data = np.load("./image_classifier/sample_data/pet.npy")
labels = np.load("./image_classifier/sample_data/pet_labels.npy")
#data = np.load("dogData.npy")
#labels = np.load("dogLabels.npy")

# Shuffle data for train and test set
s = np.arange(data.shape[0])
np.random.shuffle(s)
data = data[s]
labels = labels[s]

# Set totale number of pet categories and data length
num_classes =len(np.unique(labels))
data_length = len(data)

#--- Divide data into test and train ---
# divide data
(x_train,x_test)=data[(int)(0.1*data_length):],data[:(int)(0.1*data_length)]

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

# --- Predicting single images ---
def convert_to_array(img):
    im = cv.imread(img)
    img = Image.fromarray(im, 'RGB')
    image = img.resize((50, 50))
    return np.array(image)

def get_breed(label):
    if label==0:
      return "dog" 

    if label==1:
      return "cat" 

    if label==2:
      return "bird"
    
    if label==3:
      return "rabbit"

def predict_pet(file):
    print("Predicting .................................")
    ar=convert_to_array(file)
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

predict_pet("./image_classifier/sample_data/cat.jpg")
model.save("./image_classifier/pet_model/")