import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

GPIO_ECHO = 17
GPIO_TRIGGER = 3

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


GPIO.setup([in1,in2,en,in3,in4,enb],GPIO.OUT)
GPIO.setup([l,c,r],GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.output([in1,in2,in3,in4],GPIO.LOW)
p=GPIO.PWM(en,1000)
g=GPIO.PWM(enb, 1000)
p.start(100)
g.start(100)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartTime = time.time()
    StopTime = time.time()
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    return distance


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

try:
    set_speed(100,100)
    while(1):
        time.sleep(.5)
        dist = distance()
        print(dist)
        if not GPIO.input(l):
            turn_right()
            print('turning right')
        elif not GPIO.input(r):
            turn_left()
            print('turning left')
        elif dist <= 30:
            move_forward()
            print('found enemy')
        else:
            turn_left()
            print('spin')
    GPIO.cleanup()
except KeyboardInterrupt:
    GPIO.output([in1,in2,in3,in4],GPIO.LOW)
    GPIO.cleanup()
