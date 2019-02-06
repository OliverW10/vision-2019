import cv2
import numpy

#1100 F for microsoft hd life cam

#Code for duel rects
def getDistance(rects):
    width = abs(rects[0][0] - rects[1][0])
    if width > 0:
        dist = (21 * 1200)/width
        #   width of object * F 
        return dist
    else:
        return None

#################


def rectDist(rect):
    width = max([rect[1][0], rect[1][1]])
    height = min([rect[1][0], rect[1][1]])
    if width > 0.001:
        dist = (21 * 1200)/width
        return dist
    else:
        return 0

def getRect(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (1, 180, 10), (15, 255, 254))
    cv2.imshow("img", img)
    cv2.imshow("mask", mask)
    contours = cv2.findContours(mask, 1, 2)[-2]
    distance = None
    if len(contours) >= 1:
        cnt = max(contours, key = cv2.contourArea)
        rect = cv2.minAreaRect(cnt)
        distance = rectDist(rect)
    return distance

testImg = cv2.imread("2.jpg")

cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    print(getDist(img))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows() 
        break