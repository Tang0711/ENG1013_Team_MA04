from pymata4 import pymata4
import time
from Ultrasonic_sensor import read_ultrasonic
from traffic_light_switch import tL_with_yellow_shiftbyte,tL_without_yellow_shiftbyte,tL5_shiftbyte
from shift_register import set_tL_state

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

        if tL5 == "r":
            us3 = False
            sub3Start = time.time()

        elif tL5 == "solidg" or tL5 == "flashg": #
            tL5 = "flashg"

    else:
        us3Detect = False
        tL5 = "r"
        
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
        print(f"Alert: {us1Height}cm detected at {time.time()}")
        tL1 = "y"

    if us1Detect == True and 1<(time.time()-sub1Start)<=2:
        tL1 = "r"
        tL2 = "y"

    if us1Detect == True and (time.time()-sub1Start)>2:
        tL1 = "r"
        us1 = True
    
def sub3_response():
    global tL5
    global us3Detect
    global sub3Start
    global us3

    if us3Detect == True and (time.time()-sub3Start)<=2:
        tL5 = "y"

    if us3Detect == True and 2<(time.time()-sub3Start)<=7:
        tL5 = "solidg"
    
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
shifterPin = {"serial":8,"clock":9,"latch":10,"clear":11}
tL5GreenPin = 12
us1Pin = {"trig":7,"echo":6}
us2Pin = {"trig":5,"echo":4}
us3Pin = {"trig":3,"echo":2}

outputPins = [shifterPin["serial"],shifterPin["clock"],shifterPin["latch"],shifterPin["clear"]]

#board setup
board1013 = pymata4.Pymata4()

#output pin setup
for pins in outputPins:
    board1013.set_pin_mode_digital_output(pins)

#pwm pin setup
board1013.set_pin_mode_pwm_output(tL5GreenPin)

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

try:
    while True:
        tL1Light = tL_with_yellow_shiftbyte(tL1)
        tL2Light = tL_with_yellow_shiftbyte(tL2)
        tL3Light = tL_without_yellow_shiftbyte(tL3)
        tL5Light = tL5_shiftbyte(tL5)

        shift_byte = tL1Light + tL2Light + tL3Light + tL5Light

        set_tL_state(board1013,shifterPin,shift_byte)

        if us1 == True:#
            us1_state(board1013,us1Pin["trig"],us1Pin["echo"],tunnelHeight,threshold)
        if us2 == True:#
            us2_state(board1013,us2Pin["trig"],us2Pin["echo"],tunnelHeight,threshold)
        if us3 == True:#
            us3_state(board1013,us3Pin["trig"],us3Pin["echo"],tunnelHeight,threshold)

        sub1_response()
        sub3_response()
        integration()
        time.sleep(0.1) #
except KeyboardInterrupt:
    print("board shutdown")
    board1013.shutdown()

