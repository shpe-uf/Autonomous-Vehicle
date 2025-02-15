#import GPIO library
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
import time
import os

# PINS
IR_SENSOR_LEFT_PIN = 10
IR_SENSOR_RIGHT_PIN = 22

SERVO_PIN = 12

MOTOR_A_EN = 9
MOTOR_A_IN1 = 14
MOTOR_A_IN2 = 4
MOTOR_B_EN = 11
MOTOR_B_IN1 = 25
MOTOR_B_IN2 = 1

#PUSH_BUTTON_PIN = 19

LED_GREEN = 13 
LED_RED = 20

ULTRASONIC_TRIG_LEFT = 21
ULTRASONIC_ECHO_LEFT = 6
ULTRASONIC_TRIG_RIGHT = 27
ULTRASONIC_ECHO_RIGHT = 17

# Initialize car state
car_running = False
# GPIO define input and output pins

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# IR SENSOR
GPIO.setup(IR_SENSOR_LEFT_PIN, GPIO.IN)
GPIO.setup(IR_SENSOR_RIGHT_PIN, GPIO.IN)

# ULTRASONIC SENSOR
ultrasonic_left = DistanceSensor(echo=ULTRASONIC_ECHO_LEFT, trigger=ULTRASONIC_TRIG_LEFT, threshold_distance=0.3)
ultrasonic_right = DistanceSensor(echo=ULTRASONIC_ECHO_RIGHT, trigger=ULTRASONIC_TRIG_RIGHT, threshold_distance=0.3)

# SERVO
GPIO.setup(SERVO_PIN, GPIO.OUT)

# DC MOTORS
GPIO.setup(MOTOR_A_EN, GPIO.OUT)
GPIO.setup(MOTOR_A_IN1, GPIO.OUT)
GPIO.setup(MOTOR_A_IN2, GPIO.OUT)
GPIO.setup(MOTOR_B_EN, GPIO.OUT)
GPIO.setup(MOTOR_B_IN1, GPIO.OUT)
GPIO.setup(MOTOR_B_IN2, GPIO.OUT)

#GPIO.output(MOTOR_A_EN, False)
GPIO.output(MOTOR_A_IN1, False)
GPIO.output(MOTOR_A_IN2, False)
#GPIO.output(MOTOR_B_EN, False)
GPIO.output(MOTOR_B_IN1, False)
GPIO.output(MOTOR_B_IN2, False)

b=GPIO.PWM(MOTOR_A_EN,100)
a=GPIO.PWM(MOTOR_B_EN,100)
a.start(0)
b.start(0)

normal_duty_cycle = 20

# PUSH BUTTON
#GPIO.setup(PUSH_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED INDICATORS
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.output(LED_GREEN, GPIO.LOW)
GPIO.setup(LED_RED, GPIO.OUT)
GPIO.output(LED_RED, GPIO.HIGH)

# Initialize servo motor
servo = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency for PWM
servo.start(0)  # Starts PWM with duty cycle 0 (straight position)


# function to set servo angle
def set_servo_angle(angle):
    duty = angle / 18 + 2  # Map angle to duty cycle for servo control
    GPIO.output(SERVO_PIN, True)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Adjust sleep time as needed for proper servo operation
    GPIO.output(SERVO_PIN, False)
    servo.ChangeDutyCycle(0)

def turn_left(angle1, dur):
    print("Turning left")
    a.ChangeDutyCycle(25)
    b.ChangeDutyCycle(25)
    set_servo_angle(angle1)  # Turn left
    time.sleep(0.5)
    #GPIO.output(MOTOR_A_EN, True)
    GPIO.output(MOTOR_A_IN1, True)
    GPIO.output(MOTOR_A_IN2, False)
    #GPIO.output(MOTOR_B_EN, True)
    GPIO.output(MOTOR_B_IN1, True)
    GPIO.output(MOTOR_B_IN2, False)

    time.sleep(dur)
    set_servo_angle(110)
    a.ChangeDutyCycle(normal_duty_cycle)
    b.ChangeDutyCycle(normal_duty_cycle)
    
     
def turn_right(angle1, dur):
    print("Turning right")
    a.ChangeDutyCycle(25)
    b.ChangeDutyCycle(25)
    set_servo_angle(angle1)  # Turn right
    time.sleep(0.3)
    #GPIO.output(MOTOR_A_EN, True)
    GPIO.output(MOTOR_A_IN1, True)
    GPIO.output(MOTOR_A_IN2, False)
    #GPIO.output(MOTOR_B_EN, True)
    GPIO.output(MOTOR_B_IN1, True)
    GPIO.output(MOTOR_B_IN2, False)

    time.sleep(dur)
    set_servo_angle(110)
    a.ChangeDutyCycle(normal_duty_cycle)
    b.ChangeDutyCycle(normal_duty_cycle)

# function to control the motors based on sensor inputs
def control_motors():
    if GPIO.input(IR_SENSOR_LEFT_PIN) and GPIO.input(IR_SENSOR_RIGHT_PIN):
        # Both sensors detect line
        # Both sensors don't detect line
        print("Stopped. No black line detected")
        #GPIO.output(MOTOR_A_EN, True)
        GPIO.output(MOTOR_A_IN1, False)
        GPIO.output(MOTOR_A_IN2, False)
        #GPIO.output(MOTOR_B_EN, True)
        GPIO.output(MOTOR_B_IN1, False)
        GPIO.output(MOTOR_B_IN2, False)

    elif GPIO.input(IR_SENSOR_LEFT_PIN):
        # Left sensor detects line
        turn_right(115, 0.1)
        print("Turning right")

    elif GPIO.input(IR_SENSOR_RIGHT_PIN):
        # Right sensor detects line
        turn_left(105, 0.1)
        print("Turning left")
        
    else:
        # set_servo_angle(90)  # Straight
        print("Moving straight. Black lines on both sides.")
        #GPIO.output(MOTOR_A_EN, True)
        GPIO.output(MOTOR_A_IN1, True)
        GPIO.output(MOTOR_A_IN2, False)
        #GPIO.output(MOTOR_B_EN, True)
        GPIO.output(MOTOR_B_IN1, True)
        GPIO.output(MOTOR_B_IN2, False)


# function to stop the car
def stop_moving():
    global car_running, a, b
    car_running = False
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)
    GPIO.output(LED_RED, GPIO.HIGH)
    GPIO.output(LED_GREEN, GPIO.LOW)
    print(car_running)
    print("Car stopped")

def start_moving():
    global car_running, a, b
    car_running = True
    a.ChangeDutyCycle(normal_duty_cycle)
    b.ChangeDutyCycle(normal_duty_cycle)
    GPIO.output(LED_GREEN, GPIO.HIGH)
    GPIO.output(LED_RED, GPIO.LOW)
    print(car_running)
    print("Car started")

def stop_sign():
    global car_running, a, b
    car_running = False
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)
    GPIO.output(LED_RED, GPIO.HIGH)
    GPIO.output(LED_GREEN, GPIO.LOW)
    print(car_running)
    print("Car stopped")
    time.sleep(2)
    start_moving()

# function to start or stop the car based on button press
# def toggle_car(button_pin):
#     global car_running
#     if GPIO.input(button_pin) == GPIO.LOW:  # Button pressed
#         if car_running:
#             # Stop the car
#             stop_moving()
#         else:
#             # Start the car
#             start_moving()

# Function to perform car action
def perform_car_action():
    if os.path.exists("car_action.txt"):
        with open("car_action.txt", "r") as f:
            action = f.read().strip()
            if action == "STOP":
                stop_sign()
                print("Stop sign detected.")
            elif action == "LEFT":
                turn_left(95, 2)
                print("Left sign detected.")
            elif action == "RIGHT":
                turn_right(120, 2)
                print("Right sign detected.")
            elif action == "NONE":
                print("Normal motion")
                control_motors()
            else:
                control_motors()
        os.remove("car_action.txt")

# Add event detection for button press
# GPIO.add_event_detect(PUSH_BUTTON_PIN, GPIO.FALLING, callback=toggle_car, bouncetime=200)

# check for objects
ultrasonic_left.when_in_range = stop_moving
ultrasonic_right.when_in_range = stop_moving
ultrasonic_left.when_out_of_range = start_moving
ultrasonic_right.when_out_of_range = start_moving


try:
   # set_servo_angle(110)
    while True:
        if car_running:
            perform_car_action()
        time.sleep(0.1)
# If user press CTRL-C
except KeyboardInterrupt:
  # Reset GPIO settings
  GPIO.cleanup()
  print("GPIO Clean up")
