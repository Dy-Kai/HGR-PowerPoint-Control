import cv2
import time

import cvzone
import numpy as np
import math
import pyautogui
from cvzone.HandTrackingModule import HandDetector

width, height = 800, 600
gestureTreshold = 300
gestureCooldown = 1
timeTracked = time.time()

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=1)

x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57] # jarak sebenarnya antara titik 5 dan 17
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100] # jarak dalam sentimeter (CM)
coff = np.polyfit(x, y, 2) # Y = Ax^2 + Bx + C

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)

    cv2.line(img, (0, gestureTreshold), (width, gestureTreshold), (0, 255, 0), 5)

    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        x, y, w, h = hand['bbox']

        # mendapatkan posisi titik landmark 5 dan 17
        x1, y1 = lmList[5][:2]
        x2, y2 = lmList[17][:2]

        # mendapatkan jarak titik 5 dan 17 dalam satuan pixel
        lmDist = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        # mendnapatkan jarak yang telah dikonversi ke sentimeter (CM)
        A, B, C = coff
        distInCM = A * lmDist ** 2 + B * lmDist + C

        cvzone.putTextRect(img, f'{int(distInCM)} cm', (x + 5, y - 10))

        fingers = detector.fingersUp(hand)

        cx, cy = hand['center']

        if time.time() >= timeTracked + gestureCooldown and cy <= gestureTreshold:
            print(f'\nPosisi jari: {fingers}'
                  f'\nJarak (cm) : {distInCM}'
                  f'\nJarak (pixel) : {int(lmDist)}')

            if fingers == [1, 1, 0, 0, 0]:
                pyautogui.press('right')
                print(f'Pressing Right. Distance : {int(distInCM)} cm')

            elif fingers == [0, 0, 0, 0, 0]:
                pyautogui.press('left')
                print(f'Pressing Left. Distance : {int(distInCM)} cm')

            elif fingers == [1, 1, 1, 1, 1]:
                pyautogui.press('f5')
                print(f'Go to SlideShow. Distance : {int(distInCM)} cm')

            elif fingers == [1, 1, 1, 0, 0]:
                pyautogui.press('esc')
                print(f'Escape SlideShow. Distance : {int(distInCM)} cm')

            timeTracked = time.time()

    cv2.imshow("image", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
