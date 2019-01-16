import cv2
import numpy as np
import os
import math
import time


def findTape(img, display):
    minGreen = (60, 177, 177)  # colors to mask with
    maxGreen = (150, 255, 255)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, minGreen, maxGreen)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours = cv2.findContours(mask, 1, 2)[-2]
    if len(contours) > 1:
        #contours.sort(key=cv2.contourArea) 
        removeUnder(10, contours)   #sort contours by area and then remove them if they're under a certen size
        rects = []  # all rects
        boxes = []
        allBoxes = []
        for i in range(len(contours)):
            rects.append(cv2.minAreaRect(contours[i]))
        pairs = findPairs(rects)
        correctPairs = []
        for i in range(len(pairs)):
            if checkOrien(pairs[i]) == True:
                correctPairs.append(pairs[i])

        for o in range(len(correctPairs)):
            breaker = False
            for i in range(len(correctPairs)):
                if i != o and correctPairs[o][0] == correctPairs[i][0]:
                    if xdist(
                        correctPairs[i][0][0][0], correctPairs[i][1][0][0]
                    ) < xdist(correctPairs[o][0][0][0], correctPairs[o][1][0][0]):
                        del correctPairs[o]
                        breaker = True
                        break
                    else:
                        del correctPairs[i]
                        breaker = True
                        break
            if breaker == True:
                break

        if display==True:
            for i in range(len(rects)):
                allBoxes.append(cv2.boxPoints(rects[i]))

        for b in range(len(correctPairs)):
            boxes.append(cv2.boxPoints(correctPairs[b][0]))
            boxes.append(cv2.boxPoints(correctPairs[b][1]))

        boxes = np.int0(boxes)
        if display==True:
            allBoxes = np.int0(allBoxes)
            show = img.copy()
            for i in range(len(allBoxes)):
                cv2.drawContours(show, [allBoxes[i]], 0, (0, 0, 255), 2)

            for i in range(len(boxes)):
                cv2.drawContours(show, [boxes[i]], 0, (0, 255, 0), 2)
            cv2.imshow("mask", mask)
            cv2.imshow("img", show)

        return {"rects": rects, "boxes": boxes, "hatches": correctPairs}
        # rects is all found tape and boxes is all correct found tape (as box) and hatches is


def removeUnder(under, contours):
    for c in range(len(contours)):
        if cv2.contourArea(contours[c]) < under:
            del contours[c]
            removeUnder(under, contours)
            break


def findMid(boxes):
    mid1 = (boxes[0][0][0], boxes[0][0][1])
    mid2 = (boxes[1][0][0], boxes[1][0][1])
    bothMid = [(mid1[0] + mid2[0]) / 2, (mid1[1] + mid2[1]) / 2]

    return (np.int0(mid1), np.int0(mid2), np.int0(bothMid))
    #   center of 1rst, center of 2nd, center of both


def findAngleToCamera(FOV, X, W):
    perc = X / W
    angFromL = perc * FOV
    return angFromL - FOV / 2


def findPairs(rects):
    pairs = []
    lower, upper = splitRemove(rects)  # lower is pointing down left
    lower.sort(key=lambda x: x[0])
    upper.sort(key=lambda x: x[0])
    for l in range(len(lower)):
        for u in range(len(upper)):
            pairs.append([lower[l], upper[u]])
    return pairs


def splitRemove(
    rectList
):  ############### change this to make it able to spot skewed hatches
    at = -35  # below 35 in one list above in another
    miss = 15
    list1, list2 = [], []
    for i in range(len(rectList)):
        if (rectList[i][2] < -(15 - miss) and rectList[i][2] > -(15 + miss)) or (
            rectList[i][2] < -(75 - miss) and rectList[i][2] > -(75 + miss)
        ):
            if rectList[i][2] < at:
                list1.append(rectList[i])
            else:
                list2.append(rectList[i])
    return list1, list2


def checkOrien(pair):
    pair.sort(key=lambda x: x[2])
    if pair[1][0][0] > pair[0][0][0]:
        return True
    else:
        return False


def closer(X1, X23):
    dist = [X1 - X23[0], X1 - X23[1]]
    if abs(dist[0]) > abs(dist[1]):
        return 0
    else:
        return 1


def xdist(x1, x2):
    return abs(x1 - x2)


# ( center (x,y), (width, height), angle of rotation ) min area rect things

files = os.listdir(".\images")
index = 0
testImg = cv2.imread("./images/" + files[index], 1)
def process(currentImg, display):
    hatches = currentImg.copy()
    tapes = findTape(currentImg, display)
    if display==True:
        mids=[]
        if len(hatches) > 1:
            for i in range(len(tapes["hatches"])):
                mids.append(findMid([tapes["hatches"][i][0], tapes["hatches"][i][1]])[2])
                mid = findMid([tapes["hatches"][i][0], tapes["hatches"][i][1]])
                cv2.ellipse(
                    hatches,
                    (mid[2][0], mid[2][1]),
                    (mid[2][0] - mid[0][0], mid[2][0] - mid[0][0]),
                    0,
                    0,
                    360,
                    (0, 255, 255),
                    3,
                )
            cv2.imshow("hatches", hatches)
        return mids
    else:
        mids=[]
        if len(hatches) > 1:
            for i in range(len(tapes["hatches"])):
                mids.append(findMid([tapes["hatches"][i][0], tapes["hatches"][i][1]])[2])
        return mids

if __name__=="__main__":
    while True:
        print(process(testImg, False)) #true is weather or not to display the stuff
        cv2.imshow("the image", testImg)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        if cv2.waitKey(1) & 0xFF == ord("n"):
            index += 1
            testImg = cv2.imread("./images/" + files[index], 1)
            print("next")
cv2.destroyAllWindows()
quit()
