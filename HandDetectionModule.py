import cv2
import mediapipe as mp
import math


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def FindHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)

        return img

    def FindPosition(self, img,handNo=0, handDetectionID=4,draw=True):
        self.lmList=[]
        xList = []
        yList = []
        boundBox = []
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    if(id==handDetectionID):
                        cv2.circle(img, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

            if draw:
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boundBox = xmin, ymin, xmax, ymax
                cv2.rectangle(img, (boundBox[0] - 20, boundBox[1] - 20), (boundBox[2] + 20, boundBox[3] + 20),
                                          (0, 255, 0), 2)
        return self.lmList, boundBox

    def FindDistance(self,p1,p2,img,draw=True):
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]  # Values of the 4th(p1) landmark which is Thumb pointer
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]  # Values of the 8th(p2) landmark which is Index finger pointer
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        Color_of_circles = (0, 255, 255)
        #drawing circles on the points
        cv2.circle(img, (x1, y1), 10, Color_of_circles, 3)
        cv2.circle(img, (x2, y2), 10, Color_of_circles, 3)
        # drawing a line between index tip and thumb tip
        cv2.line(img, (x1, y1), (x2, y2), Color_of_circles, 3)
        cv2.circle(img, (cx, cy), 10, Color_of_circles, cv2.FILLED)

        # Calculating the length of the line
        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1,y1,x2,y2,cx,cy]

    def FingersUp(self):
        fingers=[]
        self.tipIds=[4,8,12,16,20]

        # for thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # for rest of 4 fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    while True:
        success, img = cap.read()
        image = detector.FindHands(img)
        lmList,bbox=detector.FindPosition(image, handDetectionID=8)

        if len(lmList) != 0:
            print(lmList)



        cv2.imshow("Image", image)
        cv2.waitKey(1)
        if cv2.waitKey(30) & 0xff == ord('E'):
            break
    cap.release();
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
