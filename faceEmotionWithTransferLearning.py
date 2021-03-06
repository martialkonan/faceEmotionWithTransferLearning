# -*- coding: utf-8 -*-
"""faceEmotion_Transfer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bsyMbhctfLJuGRT5Syhz42bWtKqsxepR
"""

import tensorflow as tf
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from zipfile import ZipFile
import tarfile
import random

my_tar = tarfile.open('archive.tar')
my_tar.extractall('') # specify which folder to extract to
my_tar.close()

img_array = cv2.imread("archive/train/0/Training_3908.jpg")
img_array.shape

img_size = 224
new_array = cv2.resize(img_array, (img_size, img_size))
#plt.imshow(cv2.cvtColor(new_array, cv2.COLOR_BGR2RGB))
#plt.show()

dataDirectory = "archive/train/" #training dataset
#classes = ['angry','disgust','fear','happy','neutral','sad',] # List of Foldder
classes = ['0','1','2','3','4','5','6',] # List of Foldder

for category in classes:
  path = os.path.join(dataDirectory, category) #//
  for img in os.listdir(path): 
    img_array = cv2.imread(os.path.join(path, img))
    plt.imshow(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)) 
    plt.show()
    break
  break

img_size = 224
new_array = cv2.resize(img_array, (img_size, img_size))
plt.imshow(cv2.cvtColor(new_array, cv2.COLOR_BGR2RGB))
plt.show()

new_array.shape

#read all the images and convertin them to array
path = dataDirectory #initialisation
training_Data = []
def create_training_Data():
  for category in classes:
    path = os.path.join(dataDirectory, category)
    class_num = classes.index(category)
    for img in os.listdir(path):
      try:
        img_array = cv2.imread(os.path.join(path, img))
        new_array = cv2.resize(img_array, (img_size, img_size))
        training_Data.append([new_array, class_num])
      except Exception as e:
        pass

create_training_Data()

print(len(training_Data))

temp = np.array(training_Data)
temp.shape

random.shuffle(training_Data)

X = []
Y = []
for features, label in training_Data:
  X.append(features)
  Y.append(label)

X = np.array(X).reshape(-1, img_size, img_size, 3)
# 3 is the channel for RGB

X.shape

X = X/255.0

Y = np.array(Y)

Y.shape

"""# **Model for training - transfer learning**"""

import tensorflow as tf
from keras import models
from tensorflow import keras
from tensorflow.keras import layers

model = tf.keras.applications.MobileNetV2() #Pre-trained model

model.summary()

base_input = model.layers[0].input

base_output = model.layers[-2].output

final_output = layers.Dense(128)(base_output)
final_output = layers.Activation('relu')(final_output)
final_output = layers.Dense(64)(final_output)
final_output = layers.Activation('relu')(final_output)
final_output = layers.Dense(7, activation='softmax')(final_output)

new_model = keras.Model(inputs = base_input, outputs = final_output)

new_model.summary()

new_model.compile(loss="sparse_categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

new_model.fit(X,Y, epochs = 25)

new_model.save('Final_model_95p07.h5')

new_model = tf.keras.models.load_model('Final_model_95p07.h5')

new_model.evaluate

img_test = cv2.imread('happy_boy_2.jfif')

img_test.shape

faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

gray = cv2.cvtColor(img_test, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(gray,1.1,4)
for (x, y, w, h) in faces :
    cv2.rectangle(img_test, (x, y), (x+w, y+h), (0, 255, 0),2)

faces = faceCascade.detectMultiScale(gray,1.1,4)
for x,y,w,h in faces:
   roi_gray = gray[y:y+h, x:x+w]
   roi_color = img_test[y:y+h, x:x+w]
   cv2.rectangle(img_test, (x,y), (x+w, y+h), (0, 255, 0), 2)
   facess = faceCascade.detectMultiScale(roi_gray)
   if len(facess) == 0:
      print("Face not detected")
   else:
        for (ex,ey,ew,eh) in facess:
            face_roi = roi_color[ey: ey+eh, ex:ex + ew]

plt.imshow(cv2.cvtColor(img_test, cv2.COLOR_BGR2RGB))

plt.imshow(cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB))

final_image = cv2.resize(face_roi,(224,224))
final_image = np.expand_dims(final_image,axis = 0)
final_image=final_image/255.0

predict = new_model.predict(final_image)

predict[0]

np.argmax(predict)
