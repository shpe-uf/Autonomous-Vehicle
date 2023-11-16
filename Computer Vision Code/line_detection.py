## No longer necessary, in posession of 2 IR sensors

import cv2 as cv

cap = cv.VideoCapture(0)
cap.set(3,160)
cap.set(4,120)

while(True):

    ret, frame = cap.read()
    crop_img = frame[60:120, 0:160]
    gray = cv.cvtColor(crop_img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray,(5,5),0)
    ret,thresh = cv.threshold(blur,60,255,cv.THRESH_BINARY_INV)
    contours,hierarchy = cv.findContours(thresh.copy(), 1, cv.CHAIN_APPROX_NONE)

    if len(contours) > 0:
        c = max(contours, key=cv.contourArea)
        M = cv.moments(c)

        cx = int(M['m10']/(M['m00']+1))
        cy = int(M['m01']/(M['m00']+1))

        cv.line(crop_img, (cx,0),(cx,720),(255,0,0),1)
        cv.line(crop_img, (0, cy),(1280,cy),(255,0,0),1)

        if cx >= 120: 
            print("Turn Left")
        if cx < 120 and cx > 50:
            print("On Track")
        if cx <= 50:
            print("Turn Right")

    else:
        print("I cant see the line")

    cv.imshow('frame', crop_img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break