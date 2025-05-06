from pymata4 import pymata4
import time
from Ultrasonic_sensor import read_ultrasonic
from traffic_light_switch import tL_switch

def us1_state(boardInput,trig,echo,tunnelHeight, threshold):
    global us1
    global us1Detect
    global sub1Start
    global us1Height
    global overCarExit
    
    us1Data = read_ultrasonic(boardInput,trig,echo)
    us1Height = tunnelHeight - us1Data

    if us1Height > threshold and 2<=us1Data<=60:
        us1Detect = True
        if tL1 == "g" and tL2 == "g":
            us1 = False
            overCarExit = False
            sub1Start = time.time()

    else:
        us1Detect = False

def us2_state(boardInput,trig,echo,tunnelHeight,threshold):
    global us2Detect
    global tL1
    global tL2
    global tL3

    us2Data = read_ultrasonic(boardInput,trig,echo)
    us2Height = tunnelHeight - us2Data

    if us2Height > threshold and 2<=us2Data<=60 :
        us2Detect = True
        tL1 = "r"
        tL2 = "r"
        tL3 = "r"
        
    else:
        us2Detect = False
        tL3 = "g"
    
def us3_state(boardInput,trig,echo,tunnelHeight,threshold):
    global us3
    global us3Detect
    global overCarExit
    global sub3Start
    global tL5

    us3Data = read_ultrasonic(boardInput,trig,echo)
    us3Height = tunnelHeight - us3Data
    
    if us3Height > threshold and 2<=us3Data<=60:
        us3Detect = True
        overCarExit = False

        if tL5 == "rr":
            us3 = False
            sub3Start = time.time()

        elif tL5 == "gg" or tL5 == "ggg": #
            tL5 = "ggg"

    else:
        us3Detect = False
        tL5 = "rr"
        
        if overCarExit == False:
            overCarExit = True
    
def sub1_response():
    global tL1
    global tL2
    global us1Detect
    global sub1Start
    global us1Height
    global us1

    if us1Detect == True and (time.time()-sub1Start)<=1:
        print(f"Alert: {us1Height}cm detected at {time.ctime()}")
        tL1 = "y"

    if us1Detect == True and 1<(time.time()-sub1Start)<=2:
        tL1 = "r"
        tL2 = "y"

    if us1Detect == True and (time.time()-sub1Start)>2:
        tL1 = "r"
        tL2 = "r"
        us1 = True
    
def sub3_response():
    global tL5
    global us3Detect
    global sub3Start
    global us3

    if us3Detect == True and (time.time()-sub3Start)<=2:
        tL5 = "y"

    if us3Detect == True and 2<(time.time()-sub3Start)<=7:
        tL5 = "gg"
    
    if us3Detect == True and (time.time()-sub3Start)>7:
        us3 = True

def integration():
    global overCarExit
    global us1Detect
    global us2Detect
    global us3Detect
    global tL1
    global tL2

    if overCarExit == True and us1Detect == False and us3Detect == False:
        tL1 = "g"
        tL2 = "g"
        overCarExit = None
    elif overCarExit == None and us2Detect == False:
        tL1 = "g"
        tL2 = "g"

#define pin
tL1Pin = {"red":13,"yellow":0,"green":12}
tL2Pin = {"red":0,"yellow":0,"green":0}
tL3Pin = {"red":11,"yellow":0,"green":10}
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
#output pin setup
for pins in outputPins:
    board1013.set_pin_mode_digital_output(pins)

board1013.set_pin_mode_pwm_output(tL5Pin["green"])

#constant values
tunnelHeight = 50
threshold = 40

#initial states
tL1 = "g"
tL2 = "g"
tL3 = "g"
tL5 = "rr"
us1 = True
us2 = True
us3 = True
overCarExit = None

try:
    while True:
        tL1Light = tL_switch(board1013,tL1,tL1Pin)
        tL2Light = tL_switch(board1013,tL2,tL2Pin)
        tL3Light = tL_switch(board1013,tL3,tL3Pin)
        tL5Light = tL_switch(board1013,tL5,tL5Pin)

        if us1 == True:#
            us1_state(board1013,us1Pin["trig"],us1Pin["echo"],tunnelHeight,threshold)
        if us2 == True:#
            us2_state(board1013,us2Pin["trig"],us2Pin["echo"],tunnelHeight,threshold)
        if us3 == True:#
            us3_state(board1013,us3Pin["trig"],us3Pin["echo"],tunnelHeight,threshold)
        sub1_response()
        sub3_response()
        integration()
        time.sleep(0.05) #
except KeyboardInterrupt:
    print("board shutdown")
    board1013.shutdown()

