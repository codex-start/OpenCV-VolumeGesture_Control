import cv2
import time
import HandTrackingModule as htm
import numpy as np
import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

####################################################################
wCam , hCam = 640 ,480

####################################################################
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.9)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol= volRange[0]
maxVol= volRange[1]




while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img , draw = False)
    if len(lmList) != 0:
      #  print(lmList[4] , lmList[8])

        x1 , y1  =  lmList[4][1] , lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx , cy = (x1+x2)//2 , (y1 +y2)//2



        cv2.circle(img , (x1 , y1) ,7 , (255,0,255),cv2.FILLED)
        cv2.circle(img, (x2, y2), 7, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1,y1),(x2,y2),(255,0,255),2)
        cv2.circle(img, (cx, cy), 7, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1 , y2 - y1)


        vol = np.interp(length , [30 ,150] , [minVol , maxVol])
        print(length , vol)

        volume.SetMasterVolumeLevel(vol, None)


        if length<30:
            cv2.circle(img, (cx, cy), 7, (0, 255, 0), cv2.FILLED)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img,f'FPS: {int(fps)}' , (40,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3 )


    cv2.imshow("Capture" , img)
    cv2.waitKey(1)
