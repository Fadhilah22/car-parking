import cv2
import pickle
import pickle
import cvzone
import numpy as np
import os

seconds = 5

# Directory checking and fetching
currdir = os.getcwd()
directory = ""
for i in currdir:
    if i == '\\':
        directory += '/'
    else:
        directory += i
directory += '/TEST/'
parking_feed = directory + "test.mp4"

# Video feed
cap = cv2.VideoCapture(parking_feed)
cap.set(3, 1920)
cap.set(4, 1080)


# pickle preset
with open(directory + 'parkSlotPos_new', 'rb') as f:
            posList = pickle.load(f)

width, height = 58, 14

# for i in range(len(posList), 0):
#     posList[i][0] += 100
#     posList[i][1] += 100

def checkParkingSpace(img, img2):
    counter = 0
    for pos in posList:
        x,y = pos 
        x += 30
        y += 20
        imgCrop = img[y:y+height, x:x+width]
        cv2.imshow(str(x*y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        if count < 900:
            counter+=1
            color = (0, 255, 0)
            thickness = 2
        else:
            color = (0, 0, 255)
            thickness = 1
        cvzone.putTextRect(img2, str(count), (x, y+height-5), scale = 1.5, thickness = 2, offset = 0, colorR = color)
        cv2.rectangle(img2, (x,y), (x+ width, y+height), color, thickness)
    # Event().wait(seconds)
    # cvzone.putTextRect(img2, str(counter), (0, 30), scale = 2, thickness = 2, offset = 0, colorR = (0, 255, 0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imBlur = cv2.GaussianBlur(imGray, (3,3), 1)
    imAdaptive = cv2.adaptiveThreshold(imBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imMedian = cv2.medianBlur(imAdaptive, 5)
    
    kernel = np.ones((3,3), np.uint8)
    imDilate = cv2.dilate(imMedian, kernel, iterations=1)
    # rectangle
    checkParkingSpace(imAdaptive, img)
    
    cv2.imshow('Video', img)
    # cv2.imshow('VideoBlur', imBlur)
    cv2.imshow('VideoThresh', imAdaptive)
    # cv2.imshow('VideoThreshMedian', imMedian)
    cv2.imshow('VideoDilated', imDilate)

    cv2.waitKey(10)
