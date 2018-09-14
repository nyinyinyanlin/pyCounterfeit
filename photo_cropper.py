import cv2
import numpy as np
from os import walk
import os
import sys
from time import sleep

if(len(sys.argv)!=3):
    print("Argument Error. Exiting")
    exit()

def nothing(event):
    pass

def crop(img,width,height,x,y):
    return img[y:y+height,x:x+width]

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
    return (index,cv2.imread(os.path.join(path+"/"+files[index]),cv2.IMREAD_COLOR))

def save_img(img,path,filename):
    cv2.imwrite(os.path.join(path,("cropped-"+filename)),img)

def mouse_callback(event,x,y,flags,param):
    global img, showImg, cropImg, cx, cy
    if event == cv2.EVENT_LBUTTONDOWN:
        width = cv2.getTrackbarPos("Width","Cropper")
        height = cv2.getTrackbarPos("Height","Cropper")
        showImg = cv2.rectangle(showImg.copy(),(x,y),(x+width,y+height),(0,255,0),1)
        cropImg = crop(img,width,height,x,y)
        cx = x
        cy = y
    if event == cv2.EVENT_MOUSEMOVE:
        width = cv2.getTrackbarPos("Width","Cropper")
        height = cv2.getTrackbarPos("Height","Cropper")
        showImg = cv2.rectangle(img.copy(),(x,y),(x+width,y+height),(0,0,255),1)
cv2.namedWindow('Cropper')
cv2.createTrackbar("Width", "Cropper",0,2000,nothing)
cv2.createTrackbar("Height", "Cropper",0,2000,nothing)
cv2.setMouseCallback('Cropper',mouse_callback)

load_path = sys.argv[1]
save_path = sys.argv[2]
files = load_folder(load_path)
curIndex = 0
cx = 0
cy = 0
if len(files) == 0:
    print("No files loaded. Exiting now.")
    exit()
(curIndex, img) = get_img(curIndex,load_path,files)
showImg = img
cropImg = img
while(True):
    cv2.imshow("Cropper",showImg)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('n'):
        (curIndex, img) = get_img((curIndex+1),load_path,files)
        showImg = img
        cropImg = img
    elif key == ord('b'):
        (curIndex, img) = get_img((curIndex-1),load_path,files)
        showImg = img
        cropImg = img
    elif key == ord('a'):
        for i, x in enumerate(files):
            (curIndex, img) = get_img(i,load_path,files)
            showImg = img
            cropImg = img
            width = cv2.getTrackbarPos("Width","Cropper")
            height = cv2.getTrackbarPos("Height","Cropper")
            showImg = cv2.rectangle(showImg.copy(),(cx,cy),(cx+width,cy+height),(0,255,0),1)
            cropImg = crop(img,width,height,cx,cy)
            cv2.imshow("Cropper",showImg)
            save_img(cropImg,save_path,files[i])
            sleep(1)
    elif key == ord('s'):
        save_img(cropImg,save_path,files[curIndex])
cv2.destroyAllWindows()
