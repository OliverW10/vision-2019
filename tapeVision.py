import cv2
import numpy as np
import os
import math


def findTape(img):
    minGreen = (70, 10, 50)
    maxGreen = (120, 255, 253)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, minGreen, maxGreen)
    
    contours = cv2.findContours(mask, 1,2)[-2]
    removeUnder(10)
    if len(contours)>1:
        contours.sort(key=cv2.contourArea)
        rects = (cv2.minAreaRect(contours[-1]), cv2.minAreaRect(contours[-2]))
        boxes = (cv2.boxPoints(rects[-1]), cv2.boxPoints(rects[-2]))

    boxes=np.int0(boxes)
    show=currentImg.copy()
    cv2.drawContours(show, [boxes[0]] ,0,  (0,0,255) ,2)
    cv2.drawContours(show, [boxes[1]] ,0,  (0,0,255) ,2)
    cv2.imshow("mask", mask)
    cv2.imshow("img", show)
        
    return {"rects" : rects, "boxes" : boxes}

def removeUnder(under):
    for c in range(len(contours)):
        if contours[c].contoursArea<under:
            del contours[c]
            removeUnder(under)
            break
        
def findMid(box):
    mid1=np.average(box[0], axis=0)
    mid2=np.average(box[1], axis=0)
    bothMid=[(mid1[0]+mid2[0])/2, (mid1[1]+mid2[1])/2]

    return (mid1, mid2, bothMid)
    #   center of 1rst, center of 2nd, center of both
    
def findAngleToCamera(FOV, X, W):
    perc=X/W
    angFromL=perc*FOV
    return angFromL-FOV/2

def rotCheck(boxs):
    boxs[1].sort(key=lambda a : a[1])


files = os.listdir(".\images")
index = 0
currentImg = cv2.imread("./images/"+files[index], 1)

while True:
    tapes = findTape(currentImg)
    mid = findMid(tapes["boxes"])
    angle = findAngleToCamera(90, mid[2][0], currentImg.shape[0])
    #print(angle)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if cv2.waitKey(1) & 0xFF == ord('n'):
        index+=1
        currentImg = cv2.imread("./images/"+files[index], 1)
        print("swapped")

#cap.release()
cv2.destroyAllWindows()
quit()


