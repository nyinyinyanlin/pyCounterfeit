#!/usr/bin/env python

import cv2
import numpy as np
from os import walk
import os
import sys
from sklearn.svm import SVC
from gpiozero import LED, Button
from time import sleep
import pickle

if(len(sys.argv)>1):
    print("Argument Error. Exiting")
    exit()

def load_model(path):
    with open(path, 'rb') as file:
    	model = pickle.load(file)
        return model

lft_btn = Button(17)
rt_btn = Button(27)

red_led = LED(7)
yellow_led = LED(5)
green_led = LED(8)

uv_led = LED(23)
white_led = LED(24)

green_led.off()
uv_led.off()
red_led.off()
white_led.off()
yellow_led.off()

cap = cv2.VideoCapture(0)
model_path = "/home/pi/Desktop/uv_trained.pkl"
model = load_model(model_path)
sleep(1)
ret,frame = cap.read()
while True:
    ret, frame = cap.read()
    if rt_btn.is_pressed:
        green_led.off()
        red_led.off()
        yellow_led.off()
        uv_led.off()
        white_led.off()
    if lft_btn.is_pressed:
        green_led.off()
        red_led.off()
        yellow_led.off()
        white_led.off()
        uv_led.on()
        sleep(1)
        ret, frame = cap.read()
        img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        img = img[132:132+210,82:82+440]
        result = model.predict([img.ravel()])
        sleep(1)
        uv_led.off()
        print(result)
        if result[0] == "real":
            green_led.blink(0.5,0.5)
        if result[0] == "fake":
            red_led.blink(0.5,0.5)
        if result[0] == "1000":
            green_led.blink(0.5,0.5)
            yellow_led.blink(0.5,0.5)
    key = cv2.waitKey(1)
    if key == ord('q') & 0xFF:
        break
cap.release()
cv2.destroyAllWindows()
