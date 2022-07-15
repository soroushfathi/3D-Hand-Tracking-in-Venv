import cv2
from cvzone.HandTrackingModule import HandDetector
import socket
from screeninfo import get_monitors


# statics
screen = get_monitors().pop()
# webcam
cap = cv2.VideoCapture(0)
cap.set(3, screen.width)
cap.set(4, screen.height)

# hand detector
handdetect = HandDetector(maxHands=1, detectionCon=0.8)

# communication
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAdressPort = ('127.0.0.1', 5052)


while True:
    success, img = cap.read()
    hands, img = handdetect.findHands(img)
    # Landmark values - (x,y,z) * 21
    data = []
    if hands:
        hand = hands[0]
        lmlist = hand['lmList']
        # data = [x for lm in lmlist for x in lm]
        for lm in lmlist:
            data.extend([lm[0], screen.height - lm[1], lm[2]])
        sock.sendto(str.encode(str(data)), serverAdressPort)
    img = cv2.resize(img, (0, 0), None, 0.5, 0.5)
    cv2.imshow('win', img)
    cv2.waitKey(1)
