import cv2

stop_sign = cv2.CascadeClassifier('cascade_stop_sign.xml')
turnleft = cv2.CascadeClassifier('cascade_turn_left8.xml')
turnright = cv2.CascadeClassifier('cascade_turn_right6.xml')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    _, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    stop_sign_scaled = stop_sign.detectMultiScale(gray, 1.6, 10)
    turnleft_scaled = turnleft.detectMultiScale(gray, 1.6, 10)
    turnright_scaled = turnright.detectMultiScale(gray, 1.6, 10)

    for (x, y, w, h) in stop_sign_scaled:
        stop_sign_rectangle = cv2.rectangle(img, (x,y),
                                            (x+w, y+h),
                                            (0, 255, 0), 3)
        stop_sign_text = cv2.putText(img=stop_sign_rectangle,
                                     text="Stop Sign",
                                     org=(x, y+h+30),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale=1, color=(0, 0, 255),
                                     thickness=2, lineType=cv2.LINE_4)

    for (x, y, w, h) in turnleft_scaled:
        turnleft_rectangle = cv2.rectangle(img, (x,y),
                                            (x+w, y+h),
                                            (0, 255, 0), 3)
        turnleft_text = cv2.putText(img=turnleft_rectangle,
                                     text="Turn Left Sign",
                                     org=(x, y+h+30),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale=1, color=(0, 0, 255),
                                     thickness=2, lineType=cv2.LINE_4)    

    for (x, y, w, h) in turnright_scaled:
        turnright_rectangle = cv2.rectangle(img, (x,y),
                                            (x+w, y+h),
                                            (0, 255, 0), 3)
        turnleft_text = cv2.putText(img=turnright_rectangle,
                                     text="Turn Right Sign",
                                     org=(x, y+h+30),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                     fontScale=1, color=(0, 0, 255),
                                     thickness=2, lineType=cv2.LINE_4)
    cv2.imshow("img", img)
    key = cv2.waitKey(30)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break