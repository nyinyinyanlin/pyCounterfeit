import cv2
import numpy as np
from os import walk
import os
import sys
from time import sleep
from sklearn.svm import SVC
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

if(len(sys.argv)<4):
    print("Argument Error. Exiting")
    exit()

def load_folder(path):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    return files

def get_img(index,path,files):
    if index < 0:
        index = 0
    if index > (len(files)-1):
        index = len(files)-1
    return (index,cv2.imread(os.path.join(path+"/"+files[index]),cv2.IMREAD_GRAYSCALE))

dataset = []
label_name = ["real","fake","1000"]
label = []
real_path = sys.argv[1]
fake_path = sys.argv[2]
k1_path = sys.argv[3]

print("Loading real dataset")
files = load_folder(real_path)
print(files)
for i, f in enumerate(files):
    index, img = get_img(i,real_path,files)
    dataset.append(img.ravel())
    label.append("real")

print("Loading fake dataset")
files = load_folder(fake_path)
print(files)
for i, f in enumerate(files):
    index, img = get_img(i,fake_path,files)
    dataset.append(img.ravel())
    label.append("fake")

print("Loading 1000ks dataset")
files = load_folder(k1_path)
print(files)
for i, f in enumerate(files):
    index, img = get_img(i,k1_path,files)
    dataset.append(img.ravel())
    label.append("1000")

print("Preprocessing data")
dataset_x = np.asarray(dataset)
dataset_x.flatten()
dataset_y = np.asarray(label)

print("Splitting train and test datasets")
x_train, x_test, y_train, y_test = train_test_split(dataset_x,dataset_y,test_size=0.10,random_state=0)

print("Training model")
clf = SVC(kernel='linear', C=1.0)
clf.fit(x_train,y_train)
print("Model trained")

print("Predicting with test dataset")
y_pred = clf.predict(x_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

if len(sys.argv) == 6:
    export_path = sys.argv[4]
    model_name = sys.argv[5]
    print("Exporting trained model")
    with open(os.path.join(export_path+"/"+model_name), 'wb') as file:
        pickle.dump(clf, file)
