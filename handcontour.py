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


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = handdetect.findHands(img)
    # Landmark values - (x,y,z) * 21
    # data = []
    # if hands:
    #     for hand in hands:
    #         lmlist = hand['lmList']
    #         for lm in lmlist:
    #             data.extend([lm[0], screen.height - lm[1], lm[2]])
    #     sock.sendto(str.encode(str(data)), serverAdressPort)
    # img = cv2.resize(img, (0, 0), None, 0.5, 0.5)

    # define the upper and lower boundaries of the HSV pixel intensities
    # to be considered 'skin'
    imgContours = img.copy()
    hsvim = cv2.cvtColor(imgContours, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skinMask = cv2.inRange(hsvim, lower, upper)

    # blur the mask to help remove noise
    skinMask = cv2.blur(skinMask, (2, 2))

    # get threshold image
    ret, thresh = cv2.threshold(skinMask, 100, 255, cv2.THRESH_BINARY)

    # draw the contours on the empty image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = max(contours, key=lambda x: cv2.contourArea(x))
    cv2.drawContours(imgContours, [contours], -1, (255, 255, 0), 2)

    imgStack = cvzone.stackImages([img, imgContours, thresh], 2, 0.5)
    cv2.imshow('win', imgStack)
    cv2.waitKey(1)
