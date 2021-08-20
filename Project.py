import cv2
import time
from math import sqrt
import HandTrackingModule as htm
from pynput.mouse import Button, Controller
import pyautogui
import win32api,win32con
import mouse
import pydirectinput

pyautogui.FAILSAFE = False
# mouse = Controller()

cap = cv2.VideoCapture(0)
detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]
on=False

cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        if(totalFingers==0):
 
            if(on==False):
                on=True

            pyautogui.click() 
            '''
            if this statement is nested inside above if condition then click will be only once
            else the left mouse button will be pressed continuously
            
            '''
                
            
        elif(totalFingers==5):
            
            if(on==True):
                on=False

            x = int((lmList[9][1]+lmList[0][1])/2)
            y = int((lmList[9][2]+lmList[0][2])/2)

            x = 1920 - int(x*1920/640)
            y= int(y*1080/480)
            
            #Below are different ways to move the cursor, I chose win32api as it moved the cursor without any lag
            #mouse.position = (x,y)
            #pyautogui.moveTo(x,y)
            win32api.SetCursorPos((x,y))
            #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int((x-x1)/2), int((y-y1)/2))
            #mouse.move(x, y,absolute=True)
            #pydirectinput.moveTo(x, y)
            #pyautogui.dragTo(x,y)

    img = cv2.flip(img,1)
    if on:
        cv2.putText(img,"Shoot!",(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    else:
        cv2.putText(img,"Move Cursor!",(30,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if(key==27):
        break

cap.release()
cv2.destroyAllWindows()