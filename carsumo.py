import RPi.GPIO as GPIO
from time import sleep
from gpiozero import DistanceSensor
ultrasonic = DistanceSensor(echo=17,trigger=3)
#ultrasonic.distance for distance
#to do, change the ir to be used for edge detection, 3 points detect white = walk straight


in1 = 23
in2 = 24
en = 25
in3 = 6
in4 = 5
enb = 26
temp1=1

l = 4
c = 14
r = 15

status = [1,1,1]



GPIO.setmode(GPIO.BCM)
GPIO.setup([in1,in2,en,in3,in4,enb],GPIO.OUT)
GPIO.setup([l,c,r],GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.output([in1,in2,in3,in4],GPIO.LOW)
p=GPIO.PWM(en,1000)
g=GPIO.PWM(enb, 1000)
p.start(100)
g.start(100)

def set_stat(index):
    status[index] = 0
def reset_stat(index):
    status[index] = 1

def button_pressed_R(channel):
    set_stat(2)

def button_pressed_L(channel):
    set_stat(0)

def button_pressed_C(channel):
    set_stat(1)

def update_status():
    status[0]= 1- GPIO.input(l)
    status[1]= 1- GPIO.input(c)
    status[2]= 1- GPIO.input(r)

def set_speed(left, right):
    p.ChangeDutyCycle(left)
    g.ChangeDutyCycle(right)

def move_forward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
def turn_left():
    GPIO.output([in1,in4],GPIO.LOW)
    GPIO.output([in2,in3],GPIO.HIGH)
def turn_right():
    GPIO.output([in1,in4],GPIO.HIGH)
    GPIO.output([in2,in3],GPIO.LOW)
def move_backward():
    GPIO.output([in1,in3],GPIO.HIGH)
    GPIO.output([in2,in4],GPIO.LOW)
def checkstat():
    if not all(status):
        GPIO.output([in1,in2,in3,in4], GPIO.LOW)
        return True
    return False

GPIO.add_event_detect(l, GPIO.FALLING, callback=button_pressed_L, bouncetime = 100)
GPIO.add_event_detect(r, GPIO.FALLING, callback=button_pressed_R, bouncetime = 100)
GPIO.add_event_detect(c, GPIO.FALLING, callback=button_pressed_C, bouncetime = 100)
try:
    set_speed(100,100)
    #sleep(2)
    while(1):
        update_status()
        print(status)
        if GPIO.input(l) and GPIO.input(c) and GPIO.input(r):
            GPIO.output([in1,in2,in3,in4],GPIO.LOW)
            print("ended")
            break
        elif GPIO.input(c):
            print("center")
            set_speed(70,70)
            move_forward()
        elif GPIO.input(r):
            print("right")
            set_speed(0,100)
            turn_right()
        elif GPIO.input(l):
            print("left")
            set_speed(100,0)
            turn_left()
        #sleep(.1)
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.output([in1,in2,in3,in4],GPIO.LOW)
    GPIO.cleanup()
