import cv2
import mediapipe as mp
import HandDetectionModule as htm

cap = cv2.VideoCapture(0)
detector = htm.HandDetector()

while True:
    success, img = cap.read()
    image = detector.FindHands(img)
    lmList = detector.FindPosition(image, handDetectionID=6)
    if len(lmList) != 0:
        print(lmList[6])
    cv2.imshow("Image", image)
    cv2.waitKey(1)
    if cv2.waitKey(30) & 0xff == ord('E'):
        break
cap.release();
cv2.destroyAllWindows()
