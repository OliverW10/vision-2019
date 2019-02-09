import cv2
import numpy
from cameraServer import getRetroPos
import os

files = os.listdir("images")
print(files)

#335 focal length

#Code for duel rects
def getDistance(rects):
    if len(rects) > 1:
        boxes = [cv2.boxPoints(rects[0]), cv2.boxPoints(rects[1])]
        Lpoint = max(boxes[0], key = lambda x:x[0])
        Rpoint = max(boxes[1], key = lambda x:-x[0])
        width = abs(Lpoint[0] - Rpoint[0])
        mid = (Rpoint[0]+Lpoint[0])/2
        mid = mid - 320/2
        offset = getOffset(width, mid)
        if width > 0:
            dist = (200 * 335)/width
            #   width of object * F 
            return dist, offset
        else:
            return None, offset

def getOffset(width, x):
    # if width = 20cm then what is x in cm
    offset = x / (width / 20)
    return -offset

#cap = cv2.VideoCapture(0)

#_, img = cap.read()
for img in files:
    testImg = cv2.imread("images/"+img)
    rects = getRetroPos(testImg, display = True)[4] #gives left rect, right rect

    dist = getDistance(rects)
    print(img+":   "+str(dist))