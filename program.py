import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import socket
from screeninfo import get_monitors
import numpy as np

# statics
screen = get_monitors().pop()
# webcam
cap = cv2.VideoCapture(0)
cap.set(3, screen.width)
cap.set(4, screen.height)

# hand detector
handdetect = HandDetector(maxHands=2, detectionCon=0.8)

# communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAdressPort = ('127.0.0.1', 5052)

ds = []
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = handdetect.findHands(img)
    # Landmark values - (x,y,z) * 21
    data = []
    imgContour = img.copy()
    if hands:
        for hand in hands:
            lmlist = hand['lmList']
            # find distamnce between hand and camera
            point1 = lmlist[5]
            cv2.circle(img, point1[:2], 7, (255, 0, 255), cv2.FILLED)
            point2 = lmlist[17]
            cv2.circle(img, point2[:2], 7, (255, 0, 255), cv2.FILLED)
            cv2.line(img, point1[:2], point2[:2], (0, 255, 0), 4)
            w, _ = handdetect.findDistance((point1[0], point1[1]), (point2[0], point2[1]))
            W = 7
            # find the focal
            # d = 40
            # f = (w*d) // W
            # ds.append(f)
            # print(f'{f}', sum(ds)//len(ds))

            # find distance
            f = 850
            dis = (W*f)/w
            cvzone.putTextRect(img, f'Depth: {int(dis)}cm', (lmlist[0][0]-80, lmlist[0][1]+50), scale=2)
            # collect data to will be send into server
            for lm in lmlist:
                data.extend([lm[0], screen.height - lm[1], int(dis)])
        sock.sendto(str.encode(str(data)), serverAdressPort)
    imgStack = cvzone.stackImages([img, imgContour], 2, 0.5)
    img = cv2.resize(img, (0, 0), None, 0.40, 0.40)
    cv2.imshow('win', img)
    cv2.waitKey(1)
