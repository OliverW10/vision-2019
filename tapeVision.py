import cv2
import numpy as np
import os
import math
import time

def findTape(img):
    minGreen = (60, 177, 177)
    maxGreen = (160, 255, 255)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, minGreen, maxGreen)
    mask=cv2.erode(mask, None, iterations=2)
    mask=cv2.dilate(mask, None, iterations=2)
    
    contours = cv2.findContours(mask, 1,2)[-2]
    if len(contours)>1:
        contours.sort(key=cv2.contourArea)
        removeUnder(10, contours)
        rects=[]
        boxes=[]
        for i in range(len(contours)):
            rects.append(cv2.minAreaRect(contours[i]))
        pairs=findPairs(rects)
        correctPairs=[]
        for i in range(len(pairs)):
            if checkOrien(pairs[i]) == True:
                correctPairs.append(pairs[i])
                
        for b in range(len(correctPairs)):
            boxes.append(cv2.boxPoints(correctPairs[b][0]))
            boxes.append(cv2.boxPoints(correctPairs[b][1]))
            
        boxes=np.int0(boxes)
        show=currentImg.copy()
        for i in range(len(boxes)):
            cv2.drawContours(show, [boxes[i]] ,0,  (0,0,255) ,2)
        cv2.imshow("mask", mask)
        cv2.imshow("img", show)
        
        return {"rects" : rects, "boxes" : boxes}

def removeUnder(under, contours):
    for c in range(len(contours)):
        if cv2.contourArea(contours[c])<under:
            del contours[c]
            removeUnder(under, contours)
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

def findPairs(rects):
    pairs=[]
    lower, upper = splitRemove(rects) #lower is pointing down left
    lower.sort(key = lambda x:x[0])
    upper.sort(key = lambda x:x[0])
    for l in range(len(lower)):
        for u in range(len(upper)):
            pairs.append([lower[l], upper[u]])
    return pairs

def splitRemove(rectList):
    at=-35 #below 35 in one list above in another
    miss=10
    list1, list2=[], []
    for i in range(len(rectList)):
        if (rectList[i][2]<-(15-miss) and rectList[i][2]>-(15+miss)) or (rectList[i][2]<-(75-miss) and rectList[i][2]>-(75+miss)):
            if rectList[i][2]<at:
                list1.append(rectList[i])
            else:
                list2.append(rectList[i])
    return list1, list2

def checkOrien(pair):
    pair.sort(key=lambda x:x[2])
    if pair[1][0][0]>pair[0][0][0]:
        return True
    else: return False
    
#( center (x,y), (width, height), angle of rotation ) min area rect things

files = os.listdir(".\images")
index = 0
currentImg = cv2.imread("./images/"+files[index], 1)

while True:
    tapes = findTape(currentImg)
    #mid = findMid(tapes["boxes"])
    #angle = findAngleToCamera(90, mid[2][0], currentImg.shape[0])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if cv2.waitKey(1) & 0xFF == ord('n'):
        index+=1
        currentImg = cv2.imread("./images/"+files[index], 1)
        print("next")

#cap.release()
cv2.destroyAllWindows()
quit()
