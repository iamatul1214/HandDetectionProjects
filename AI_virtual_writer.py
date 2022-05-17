import cv2
import HandDetectionModule as htm
import os
import numpy as np

##variable declaration
pen_thickness=10
xp,yp=0,0
eraser_thickness=100
canvas_image=np.zeros((720,1280,3),np.uint8)
#################
cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.HandDetector(detectionCon=0.85)
while True:
    success, img=cap.read()
    img=cv2.flip(img,1)  #to flip the image hence, right side will appear right and left will left.
#detecting the hand
    img=detector.FindHands(img)

#detecting the hand marks
    lmlist,bbox=detector.FindPosition(img,draw=False)
    if(len(lmlist)!=0):
        # print(lmlist)


#taking the tip values of index and thumb.
         x1,y1=lmlist[8][1:]  #reading the list values from 1 to 2 but not the 0th as 0 will be hand mark code
         x2,y2=lmlist[12][1:]
# tracking the fingers up/down
         fingers_up=detector.FingersUp()
        # print(fingers_up)
#The deletion method which works when index, middle and ring fingers are up
         if fingers_up[1] and fingers_up[2] and fingers_up[3]:
            xp,yp=x1,y1
            cv2.line(img,(xp,yp),(x1,y1),(0,0,0),eraser_thickness)
            cv2.line(canvas_image, (xp, yp), (x1, y1), (0,0,0), eraser_thickness)
            xp, yp = x1, y1
# If selection mode is on, means index and middle fingers are up
         if fingers_up[1] and fingers_up[2]:
            xp,yp=0,0       #To have flawless line drawing
            cv2.rectangle(img,(x1,y1 -15),(x2,y2 +25),(0,0,0),cv2.FILLED)
            # if xp==0 and yp==0:
            xp,yp=x1,y1   #To start erasing from the point where the index and middle fingers are
            # cv2.line(img,(xp,yp),(x1,y1),(0,0,0),eraser_thickness)
            # cv2.line(canvas_image, (xp, yp), (x1, y1), (0,0,0), eraser_thickness) # Since we saw that we cannot draw on a live image/video, hence let's create a black canvas.
            xp,yp=x1,y1
            print("selection mode is on")
# The writing mode is on, only index finger is up
         if fingers_up[1] and fingers_up[2]==False:
            cv2.circle(img,(x1,y1),20,(255,0,255),cv2.FILLED)
            print("writing mode is on")
            if xp==0 and yp==0:
                xp,yp=x1,y1   #To start drawing from the point where the index finger is
            cv2.line(img,(xp,yp),(x1,y1),(255,0,255),pen_thickness)
            cv2.line(canvas_image, (xp, yp), (x1, y1), (255, 0, 255), pen_thickness) # Since we saw that we cannot draw on a live image/video, hence let's create a black canvas.
            xp,yp=x1,y1       #To continue drawing the line by tracking x1,y1

    imgGray=cv2.cvtColor(canvas_image,cv2.COLOR_BGR2GRAY)
    _, imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,canvas_image)


    cv2.imshow("Image",img)
    cv2.imshow("canvas_image",canvas_image)
    cv2.waitKey(1)
    if cv2.waitKey(30) & 0xff == ord('E'):
        break
cap.release();
cv2.destroyAllWindows()
