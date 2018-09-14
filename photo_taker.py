from gpiozero import LED, Button
from time import sleep
import cv2
import numpy as np
import os
import datetime

lft_btn = Button(17)
rt_btn = Button(27)

red_led = LED(7)
yellow_led = LED(8)
green_led = LED(5)

uv_led = LED(23)
white_led = LED(24)

green_led.off()
uv_led.off()
red_led.off()
white_led.off()

cap = cv2.VideoCapture(0)
while(True):
        ret, frame = cap.read()
        now = datetime.datetime.utcnow()
        timestamp = now.isoformat()
        if lft_btn.is_pressed:
            green_led.on()
            uv_led.on()
            sleep(1)
            ret, frame = cap.read()
            cv2.imwrite(os.path.join("/home/pi/Desktop/Images/UV/",(timestamp+".jpeg")),frame)
            sleep(1)
            green_led.off()
            uv_led.off()
        if rt_btn.is_pressed:
            red_led.on()
            white_led.blink(0.1,0.5)
            sleep(1)
            rt, fr = cap.read()
            cv2.imwrite(os.path.join("/home/pi/Desktop/Images/White/",(timestamp+".jpeg")),fr)
            sleep(1)
            red_led.off()
            white_led.off()
        key = cv2.waitKey(1)
        if key == ord('q') & 0xFF:
            break
cap.release()
cv2.destroyAllWindows()
