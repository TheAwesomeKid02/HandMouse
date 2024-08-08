import cv2
import mediapipe as mp
import pyautogui as pag

import math
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

def_x = 1250
def_y = 750
threshhold = 10
pag.moveTo(def_x,def_y,0.5)

x_change = 600
y_change = 335

x_index = 0
y_index = 0

x_thumb = 0
y_thumb = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):
                height, width, channels = img.shape
                cx, cy = int(lm.x*width), int(lm.y*height)
                #print(id, cx, cy)


                if id == 8:
                    x_index, y_index = cx, cy
                if id == 4:
                    x_thumb, y_thumb = cx, cy

                if id == 8 or id == 4:
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)

                    cv2.line(img, (x_thumb,y_thumb), (x_index, y_index),(255,0,255), 3)

                    length = math.hypot(x_index-x_thumb, y_index-y_thumb)
                    print(length)

                    if length < 160 and length > 100:
                        pag.click()
                        pag.sleep(1)

                if id == 8:
                    cx_change = cx - x_change
                    cy_change = cy - y_change
                    #print(cx_change, cy_change)

                    if abs(cx_change) > threshhold:
                        pag.moveTo(def_x - 1.5*cx_change, def_y + 1.9*cy_change, 0.1)
                    if abs(cy_change) > threshhold:
                        pag.moveTo(def_x - 1.5*cx_change, def_y + 1.9*cy_change, 0.1)

                    #print(x_change, y_change)

            mpDraw.draw_landmarks(img, handLandmarks, mpHands.HAND_CONNECTIONS)

    currTime = time.time()
    fps = 1/(currTime-prevTime)
    prevTime = currTime

    cv2.putText(img, f'FPS: {str(int(fps))}', (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,0), 3)


    cv2.imshow("Image", img)
    cv2.waitKey(1)