from djitellopy import Tello
import cv2
import numpy as np
import imutils

me = Tello()
me.connect()
print(me.get_battery())

me.streamoff()
me.streamon()
w, h = 360, 240

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

count = 0

me.takeoff()
me.move_up(80)

while True:
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #_, img = cap.read()
    #hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    low = np.array([0, 0, 0])
    high = np.array([250, 255, 35])

    mask = cv2.inRange(hsv, low, high)

    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        area = cv2.contourArea(c)
        if area > 5000:
            #cv2.drawContours(img, [c], -1, (0,255,0), 3)
            #cv2.rectangle(img, c, -1, (0,255,0), 3)
            M = cv2.moments(c)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            cv2.rectangle(img, (cx-50,cy-50), (cx+50,cy+50), (0, 255, 0), 3)
            cv2.circle(img, (cx,cy), 7, (255,255,255), -1)
            count = count + 1
            # Right now I set to 125 to help with the drone action timing, might need to alter
            if count == 100:
                print("Flip Now")
                #me.flip_back()
                count = 0
            cv2.putText(img, "Mask Detected", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 3)
    cv2.imshow("Frame", img)
    #cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break