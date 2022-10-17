import cv2
import time
import numpy as np
from HandTrackingModule import handDetector
import math
import alsaaudio

###############################################
wCam, hCam = 640, 480
###############################################


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# create a object from  class
detector = handDetector(detectionCon=0.7)


################## alsaaudio ###################
mixer = alsaaudio.Mixer()
minVol = 1
maxVol = 100
vol = 0
volBar = 400
volPer = 0
################################################

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    # false bc we already draw it
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])

        # create the circles of the points we want
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # get the center of the line between of that points
        cx, cy = (x1+ x2)// 2, (y1+y2)//2

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255, 0 , 255), 3)

        length = math.hypot(x2 - x1, y2 - y1)
        #print(f'leee{type(length)}')
        #print(length)

        ######## merge the volume and range of the finger points ########
        # Hand range 5 - 300
        # volume Range [0, 65536]

        vol = int(np.interp(length,[0,350], [minVol, maxVol]))
        volBar = int(np.interp(length, [0, 320], [400, 150]))
        volPer = int(np.interp(length, [0, 320], [0, 100]))
        print(f'vol {vol}')
        mixer.setvolume(vol)



        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    # bar
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, volBar), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f' {volPer} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 255, 0), 2)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow('Image', img)
    cv2.waitKey(10)