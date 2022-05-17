import cv2
import numpy as np
import HandDetectionModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

Wcam, Hcam = 980, 720  #Width and height of the camera

cap=cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,Hcam)

detector=htm.HandDetector(detectionCon=0.7, maxHands=1)

#Code from Pycaw library

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
VolRange=volume.GetVolumeRange()
minVol=VolRange[0]
maxVol=VolRange[1]
print(minVol,maxVol)


while True:
    success, img=cap.read()
    detector.FindHands(img)
    lmList,bbox=detector.FindPosition(img, handDetectionID=100,draw=True)

    if len(lmList) != 0:
        print(lmList[4],lmList[8])

        # Filter the box, based on size
        area=((bbox[2]-bbox[0]) * (bbox[3]-bbox[1]))//100
        print("area =", area)
        if 250 < area < 1100 :
            print("IN THE RANGE")
            # Find the distance between index and thumb
            length,img,Lineinfo=detector.FindDistance(4,8,img)
            print(length)
            # convert volume
            # vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])

            # Reduce the resolution to make it smoother
            smoothness=10
            volPer=smoothness * round(volPer/smoothness)
            # Check fingers up
            fingres=detector.FingersUp()
            print(fingres)
            #code for counting the fingres
            # Count=fingres.count(1)
            # print("total fingres=",Count)

            # IF pinky is down set volume
            if fingres[2]==False:
                volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                cv2.circle(img, (Lineinfo[4], Lineinfo[5]), 15, (255, 0, 255), cv2.FILLED)
                volColor=(255,0,255)
            else:
                volColor=(255,255,255)

            # Hand range = 50 to 300
            # Volume range= 0 to -65



            if length<50:
                cv2.circle(img, (Lineinfo[4], Lineinfo[5]), 10, (0,0,255), cv2.FILLED)
            cv2.rectangle(img, (50,150),(85,400),(0,0,0),3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}%',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),3)
            cVol = int(volume.GetMasterVolumeLevelScalar() * 100)
            cv2.putText(img, f'Vol set to :{int(cVol)}', (300, 40), cv2.FONT_HERSHEY_COMPLEX, 1, volColor, 3)



    cv2.imshow("Image",img)
    cv2.waitKey(1)
    if cv2.waitKey(30) & 0xff == ord('E'):
        break
cap.release();
cv2.destroyAllWindows()
