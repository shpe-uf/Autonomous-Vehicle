import cv2
from picamera2 import Picamera2

stop_sign = cv2.CascadeClassifier('cascade_stop_sign.xml')
turnleft = cv2.CascadeClassifier('cascade_turn_left8.xml')
turnright = cv2.CascadeClassifier('cascade_turn_right6.xml')
# turnleft = cv2.CascadeClassifier('TLXML3.xml')
# turnright = cv2.CascadeClassifier('TRXML3.xml')
print("Haar cascade import succesful")

# distance from camera to object(sign) measured 
# centimeter 
Known_distance = 25.5
#sign = 76.2

# width of sign in the real world or Object Plane 
# centimeter 
Known_width = 5.2

# Colors 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)

right_sign_count = 0
left_sign_count = 0

# focal length finder function 
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image): 
  
    # finding the focal length 
    focal_length = (width_in_rf_image * measured_distance) / real_width 
    return focal_length 
  
# distance estimation function 
def Distance_finder(Focal_Length, real_sign_width, sign_width_in_frame): 
  
    distance = (real_sign_width * Focal_Length)/sign_width_in_frame 
  
    # return the distance 
    return distance 

  
def sign_data(image, type): 
  
    sign_width = 0  # making sign width to zero 
  
    # converting color image to gray scale image 
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
  
    # detecting sign in the image 
    if (type == 'stop'):
        signs = stop_sign.detectMultiScale(gray_image, 1.3, 5)
    elif (type == 'left'):
        signs = turnleft.detectMultiScale(gray_image, 1.3, 3) 
    elif (type == 'right'):
        signs = turnright.detectMultiScale(gray_image, 1.3, 3) 
  
    # looping through the signs detect in the image 
    # getting coordinates x, y , width and height 
    for (x, y, h, w) in signs: 
  
        # draw the rectangle on the sign 
        cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2) 
  
        # getting sign width in the pixels 
        sign_width = w 
  
    # return the sign width in pixel 
    return sign_width 



# reading reference_image from directory 
ref_image = cv2.imread("Ref_image3.png") 

# find the sign width(pixels) in the reference_image 
ref_image_sign_width = sign_data(ref_image, 'stop') 
  
# get the focal by calling "Focal_Length_Finder" 
# sign width in reference(pixels), 
# Known_distance(centimeters), 
# known_width(centimeters) 
Focal_length_found = Focal_Length_Finder( 
    Known_distance, Known_width, ref_image_sign_width) 

cap = Picamera2()
config = cap.create_preview_configuration({'format': 'RGB888', "size": (640, 360)})
cap.configure(config)
cap.start()

print("Video capture succesful")

# Function to notify car action
def notify_car_action(action):
    with open("car_action.txt", "w") as f:
        f.write(action)

while True:
    frame = cap.capture_array()

    stop_sign_width_in_frame = sign_data(frame, 'stop')
    
    left_sign_width_in_frame = sign_data(frame, 'left')  

    right_sign_width_in_frame = sign_data(frame, 'right') 

    if stop_sign_width_in_frame != 0:
        Distance = Distance_finder(Focal_length_found, Known_width, stop_sign_width_in_frame)
        print(Distance)
        if Distance < 40:
            print("Stop Sign")
            notify_car_action("STOP")
        
    if left_sign_width_in_frame:
        Distance = Distance_finder(Focal_length_found, Known_width, left_sign_width_in_frame)
        left_sign_count += 1
        print(Distance)
        if Distance < 40 and left_sign_count > right_sign_count:
            print("Left Turn")
            notify_car_action("LEFT")    

    if right_sign_width_in_frame:
        Distance = Distance_finder(Focal_length_found, Known_width, right_sign_width_in_frame)
        right_sign_count += 1
        print(Distance)
        if Distance < 40 and right_sign_count > left_sign_count:
            print("Right Turn")
            notify_car_action("RIGHT")

    # If none of the signs are detected, notify car to continue normal control
    if stop_sign_width_in_frame == 0 and left_sign_width_in_frame ==0 and right_sign_width_in_frame ==0:
        left_sign_count = 0
        right_sign_count = 0
        notify_car_action("NONE")

    cv2.imshow("frame", frame)
    key = cv2.waitKey(30)
    if key == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

