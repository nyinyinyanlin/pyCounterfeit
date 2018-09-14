import cv2
import numpy as np
from os import walk
import os
import sys
from sklearn.svm import SVC
import pickle
from sklearn.svm import SVC

if(len(sys.argv)<3):
    print("Argument Error. Exiting")
    exit()

def load_model(path):
    with open(path, 'rb') as file:
    	model = pickle.load(file)
        return model

def get_img(index,path,files):
    if index < 0:
        index = 0
    if index > (len(files)-1):
        index = len(files)-1
    return (index,cv2.imread(os.path.join(path+"/"+files[index]),cv2.IMREAD_GRAYSCALE))

def load_folder(path):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    return files

model_path = sys.argv[1]
folder_path = sys.argv[2]
files = load_folder(folder_path)
model = load_model(model_path)
for i, f in enumerate(files):
    index, img = get_img(i,folder_path,files)
    print(model.predict([img.ravel()]))
