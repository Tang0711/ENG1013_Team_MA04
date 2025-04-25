from traffic_light_switch import tL_switch
from pymata4 import pymata4
from Ultrasonic_sensor import read_ultrasonic
import time

tL1Pin = {"red":13,"yellow":0,"green":12}
tL2Pin = {"red":11,"yellow":0,"green":10}
tL3Pin = {"red":9,"yellow":0,"green":8}
tL5Pin = {"red":8,"yellow":0,"green":9}
us1Pin = {"trig":7,"echo":6}
us2Pin = {"trig":5,"echo":4}
us3Pin = {"trig":3,"echo":2}

outputPins = [tL1Pin["red"],tL1Pin["yellow"],tL1Pin["green"],
              tL2Pin["red"],tL2Pin["yellow"],tL2Pin["green"],
              tL3Pin["red"],tL3Pin["green"],
              tL5Pin["red"],tL5Pin["yellow"]]

#board setup
board1013 = pymata4.Pymata4()

#outpin setup
for pins in outputPins:
    board1013.set_pin_mode_digital_output(pins)

board1013.set_pin_mode_pwm_output(tL5Pin["green"])

def us1_state(boardInput,trig,echo,tunnelHeight, threshold):
    global us1
    global us1Detect
    global sub1Start
    global us1Height
    
    us1Data = read_ultrasonic(boardInput,trig,echo)
    us1Height = tunnelHeight - us1Data

    if us1Height > threshold and 2<=us1Data<=60: #
        us1Detect = True
        if tL1 == "g" and tL2 == "g":
            us1 = False
            sub1Start = time.time()
    else:
        us1Detect = False

#constant values
tunnelHeight = 50
threshold = 40

#initial states
tL1 = "g"
tL2 = "g"
tL3 = "g"
tL5 = "r"
us1 = True
us2 = True
us3 = True
overCarExit = None

def sub1_response():
    global tL1
    global tL2
    global us1Detect
    global sub1Start
    global us1Height
    global us1

    if us1Detect == True and (time.time()-sub1Start)<=1:#
        print(f"Alert: {us1Height}cm detected at {time.time()}")
        tL1 = "y"

    if us1Detect == True and 1<(time.time()-sub1Start)<=2:
        tL1 = "r"
        tL2 = "y"

    if us1Detect == True and 2<(time.time()-sub1Start)<=7:
        tL2 = "r"

    if us1Detect == True and 7<(time.time()-sub1Start)<=8:
        tL1 = "g"

    if us1Detect == True and (time.time()-sub1Start)>=8:
        tL2 = "g"#
        us1 = True

try:
    while True:
        tL_switch(board1013,tL1,tL1Pin)
        tL_switch(board1013,tL2,tL2Pin)
        print(read_ultrasonic(board1013,us3Pin["trig"],us3Pin["echo"]))
except KeyboardInterrupt:
    board1013.shutdown()

