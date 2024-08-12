import cv2
import mediapipe as mp
import pyautogui as pag

import math
import time

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #changing the "0" to any positive integer will cycle through the cameras you have

#change these as per your wanted resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3000)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)

mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

#USED TO CALCULATE FRAMES PER SECOND
prevTime = 0
currTime = 0

#you may change def_x and def_y for the default coordinates of the mouse
def_x = 1250
def_y = 750
threshhold = 10 #You may change this. This is the minimum amount of pixels of movement before the cursor starts moving
pag.moveTo(def_x,def_y,0.5)


#change this as per your default index finger coordinates. This varies from the screen coordinates. Uncomment some of the print statements to understand your finger placement
x_change = 600
y_change = 335


#These are the x and y coordinates of the index finger, thumb, and middle finger
#They will be modified in the program shortly
x_index = 0
y_index = 0

x_thumb = 0
y_thumb = 0

x_middle = 0
y_middle = 0

while True:
    #Everytime the camera window is closed, it reopens due to this while loop
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            for id, lm in enumerate(handLandmarks.landmark):
                height, width, channels = img.shape
                cx, cy = int(lm.x*width), int(lm.y*height)
                #print(id, cx, cy)


                if id == 8: #8 is the id for the index finger
                    x_index, y_index = cx, cy
                if id == 4: #4 is the id for the thumb
                    x_thumb, y_thumb = cx, cy
                if id == 12: #12 is the id for the middle finger
                    x_middle, y_middle = cx, cy

                if id == 8 or id == 4 or id == 12:
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)

                    cv2.line(img, (x_thumb,y_thumb), (x_index, y_index),(255,0,255), 3)
                    cv2.line(img, (x_index, y_index), (x_middle, y_middle), (255,0,255), 3)

                    length_t = math.hypot(x_index-x_thumb, y_index-y_thumb)
                    print(f'Thumb: {length_t}')

                    length_m = math.hypot(x_index-x_middle, y_index-y_middle)
                    print(f'Middle: {length_m}')

                    if length_t < 160 and length_t > 100: #change this as you wish
                        pag.click()
                        pag.sleep(1)

                if id == 8:
                    cx_change = cx - x_change
                    cy_change = cy - y_change
                    #print(cx_change, cy_change)

                    #you can change the multipliers below
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