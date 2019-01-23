import cv2
import numpy as np
import os
import math
import time



def contourToPoints(contours): #contours should be two contours
    boxes=[]
    for contour in contours:
        box=[max(contour, key=lambda x:-x[0][0]+-x[0][1]), #top left
             max(contour, key=lambda x:-x[0][1]+x[0][0]), #bottom left
             max(contour, key=lambda x:x[0][0]+x[0][1]), #bottom right
             max(contour, key=lambda x:x[0][1]+-x[0][0])] #top right
        box=np.int0(box)
        boxes.append([box])
    box1 = np.average(boxes[0], axis=1)
    box2 = np.average(boxes[1], axis=1)
    if box1[0][0][0] > box2[0][0][0]: #box1 1 is right
        right = boxes[0].copy()
        left = boxes[1].copy()
    else:
        left = boxes[0].copy()
        right = boxes[1].copy()

    return left, right
    # [[top left], [bottom left], [bottom right], [top right]] for each contour





images=[cv2.imread("1.png", 1), cv2.imread("2.png", 1), cv2.imread("3.png", 1), cv2.imread("4.png", 1)]
def groundTape(img):
    grey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(grey, 60, 255)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("mask", mask)
    contours = cv2.findContours(mask, 1, 2)[-2]
    boxes=[]
    if len(contours)>=1:
        contours=sorted(contours, key = cv2.contourArea)
        cnt1=contours[0]
        cnt2=contours[1]
        cnt
            
            cv2.drawContours(img, left,0, (255, 0, 0),2)
            cv2.drawContours(img, right,0, (0, 255, 0),2)
        else:
            cv2.drawContours(img, boxes[0], 0, (0, 0, 255), 2)
        cv2.imshow("rects", img)
        
        return None

groundTape(images[1])
cv2.waitKey(0)