import cv2
import HandDetectionModule as htm

Wcam, Hcam = 980, 720  #Width and height of the camera

cap=cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)

detector=htm.HandDetector(detectionCon=0.6, maxHands=1)

while True:
    success, img=cap.read()
    detector.FindHands(img)
    lmList,bbox=detector.FindPosition(img, handDetectionID=100,draw=False)

    if len(lmList)!=0:
        print(type(lmList))
        fingers = []
        tipIds = [4, 8, 12, 16, 20]

        # for thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
            # for rest of 4 fingers
        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                    fingers.append(1)
            else:
                    fingers.append(0)
        Count=fingers.count(1)
        print("Count =", Count)
        cv2.putText(img, f'Count =:{int(Count)}', (300, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,255), 3)





    cv2.imshow("Image",img)
    cv2.waitKey(1)
    if cv2.waitKey(30) & 0xff == ord('E'):
        break
cap.release();
cv2.destroyAllWindows()
