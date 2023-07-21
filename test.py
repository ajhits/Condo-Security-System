import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# TRIGGER
GPIO.setup(17, GPIO.OUT)

# ECHO
GPIO.setup(27, GPIO.IN)


# this code check if ultrasonic is working and check the distance by inches
while True:
    
    # TRIGGER
    GPIO.output(17,False)
    time.sleep(0.5)
    GPIO.output(17,True)
    time.sleep(0.00001)
    GPIO.output(17,False)
    
    # ECHO
    pulse_start,pulse_end = 0,0
    while GPIO.input(27) == 0:
        pulse_start = time.time()
        
    while GPIO.input(27) == 1:
        pulse_end = time.time()
        
    distance = (pulse_end-pulse_start) * 17150
    inches = round(distance / 2.54, 1)
    
    
    print("check distance of object detected: ",inches)
    