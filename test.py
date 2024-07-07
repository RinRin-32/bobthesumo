from gpiozero import DistanceSensor
ultrasonic = DistanceSensor(echo=17, trigger = 3)

while True:
    print(ultrasonic.distance)
