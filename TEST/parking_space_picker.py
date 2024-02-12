import cv2
import pickle
import os

# Directory checking and fetching
currdir = os.getcwd()
directory = ""
for i in currdir:
    if i == '\\':
        directory += '/'n
    else:
        directory += i
directory += '/'

directory += "TEST/"
 
parking_lot_img = directory +"Parking_lot.png"

print(parking_lot_img)
# image is static, wont change
read_img = cv2.imread(parking_lot_img)

width, height = 58, 14

overwrite = input("overwrite pos? Y/N >> ")

if overwrite.upper() == 'N':
    try:
        with open(directory + 'parkSlotPos_new', 'rb') as f:
            posList = pickle.load(f)
    except:
        posList = []
else:
    posList = []


    
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append([x, y])
        # print(x, y)
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            # print(x1)
            if (x1 < x < x1+width) and (y1 < y < y1+height):
                posList.pop(i)
    with open(directory + 'parkSlotPos_new', 'wb') as f:
        pickle.dump(posList, f)
    print(f"x= {x}  y= {y}")

while True:
    # cv2.rectangle(read_img, (50, 192), (157, 146), color=(255, 0, 255), thickness=2)
    read_img = cv2.imread(parking_lot_img)
    # detect mouse click
    for pos in posList:
        cv2.rectangle(read_img, pos, (pos[0]+ width, pos[1]+height), color=(255, 0, 255), thickness=2)
        
    cv2.imshow("Image", read_img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)