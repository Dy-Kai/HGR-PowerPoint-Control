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
gest = ''
timeTracked = time.time()

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(detectionCon=0.8, maxHands=2)

# x = [280, 112, 75, 49, 54, 42, 37, 34] # jarak sebenarnya antara titik 5 dan 17
# y = [25, 50, 75, 100, 125, 150, 175, 200] # jarak dalam sentimeter (CM)

# x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57, 53, 50, 48, 46, 44, 41, 38, 36, 34, 32, 31, 30, 29, 28, 27, 26, 25, 25, 24, 24] # jarak sebenarnya antara titik 5 dan 17
# y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200] # jarak dalam sentimeter (CM)

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
        x1, y1, z1 = lmList[5]
        x2, y2, z2 = lmList[17]

        # mendapatkan jarak titik 5 dan 17 dalam satuan pixel
        lmDist = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)

        # mendapatkan jarak yang telah dikonversi ke sentimeter (CM)
        A, B, C = coff
        distInCM = A * lmDist ** 2 + B * lmDist + C

        # cvzone.putTextRect(img, f'{int(distInCM)} cm', (x + 5, y - 10))
        cv2.putText(img, gest, (x - 15, y - 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        fingers = detector.fingersUp(hand)

        cx, cy = hand['center']

        if time.time() >= timeTracked + gestureCooldown:
            print(f'\nPosisi jari: {fingers}'
                  f'\nJarak (pixel) : {int(lmDist)}'
                  f'\nJarak (Z value) : {z1}'
                  f'\nJarak (cm) : {distInCM}')

            if fingers == [1, 1, 0, 0, 0]:
                if cy <= gestureTreshold:
                    pyautogui.press('right')
                print(f'Pressing Right. Distance : {int(distInCM)} cm')
                gest = 'Next'

            elif fingers == [0, 0, 0, 0, 0]:
                if cy <= gestureTreshold:
                    pyautogui.press('left')
                print(f'Pressing Left. Distance : {int(distInCM)} cm')
                gest = 'Previous'

            elif fingers == [1, 1, 1, 1, 1]:
                if cy <= gestureTreshold:
                    pyautogui.press('f5')
                print(f'Go to SlideShow. Distance : {int(distInCM)} cm')
                gest = 'Fullscreen'

            elif fingers == [1, 1, 1, 0, 0]:
                if cy <= gestureTreshold:
                    pyautogui.press('esc')
                print(f'Escape SlideShow. Distance : {int(distInCM)} cm')
                gest = 'Exit Fullscreen'

            else:
                gest = ''

            timeTracked = time.time()

    cv2.imshow("image", img)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break