from pymata4 import pymata4
import time
from Ultrasonic_sensor import read_ultrasonic
from traffic_light_switch import tL_with_yellow_shiftbit,tL_without_yellow_shiftbit,tL5_shiftbit
from shift_register import set_tL_state

def us1_state(boardInput,trig,echo,tunnelHeight, threshold):
    global us1
    global us1Detect
    global sub1Start
    global us1Height
    global overCarExit
    global tL1
    global tL2

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
    global tL4
    global pB1
    global pB1Pressed

    us2Data = read_ultrasonic(boardInput,trig,echo)
    us2Height = tunnelHeight - us2Data

    if us2Height > threshold and 2<=us2Data<=60 :
        us2Detect = True
        tL1 = "r"
        tL2 = "r"
        tL3 = "r"
        tL4 = "r"
        
    else:
        us2Detect = False
        tL3 = "g"
        if pB1Pressed == False:
            tL4 = "g"
    
def us3_state(boardInput,trig,echo,tunnelHeight,threshold):
    global us3
    global us3Detect
    global overCarExit
    global sub3Start
    global tL5
    global reloop

    us3Data = read_ultrasonic(boardInput,trig,echo)
    us3Height = tunnelHeight - us3Data
    
    if us3Height > threshold and 2 <=us3Data<= 60:
        us3Detect = True
        overCarExit = False
        reloop = True

        if tL5 == "r":
            us3 = False
            sub3Start = time.time()

        elif tL5 == "solidg" or tL5 == "flashg": #
            tL5 = "flashg"

    else:
        us3Detect = False
        tL5 = "r"
        
        if reloop == True and overCarExit == False:
            overCarExit = True
            print(overCarExit)
            reloop = False

def pB1_state(boardInput,buttonPin):
    
    global pB1Pressed
    global pB1
    global sub2Start

    pB1Pressed = boardInput.digital_read(buttonPin)[0]

    if pB1Pressed:
        sub2Start = time.time()
        pB1 = False

def sub1_response():
    global tL1
    global tL2
    global us1Detect
    global sub1Start
    global us1Height
    global us1

    timePassed = time.time()-sub1Start

    if timePassed<=1:
        print(f"Alert: {us1Height}cm detected at {time.ctime()}")
        tL1 = "y"


    elif 1 <timePassed<= 2:
        tL1 = "r"
        tL2 = "y"

    elif timePassed> 2:
        tL1 = "r"
        tL2 = "r"
        us1 = True

def sub2_response():

    global pB1Pressed
    global pB1
    global sub2Start
    global tL4
    global pL1
    global us2Detect

    timePassed = time.time() - sub2Start

    if 0 < timePassed <= 2:
        print("Pedestrian push button PB1 is pressed.")
    
    elif 2 < timePassed <= 4:
        if us2Detect:
            tL4 = "r"
        else:
            tL4 = "y"

    elif 4 < timePassed <= 9:
        tL4 = "r"

    elif 9 < timePassed <= 12:
        pL1 = "g"
    
    elif 12 < timePassed <= 12.5:
        pL1 = "r"

    elif 12.5 < timePassed <= 13:
        pL1 = "r0"
    
    elif 13 < timePassed <= 13.5:
        pL1 = "r"

    elif 13.5 < timePassed <= 14:
        pL1 = "r0"

    elif 14 < timePassed <= 30:
        pL1 = "r"
        if us2Detect:
            tL4 = "r"
        else:
            tL4 = "g"
    
    elif timePassed >30:
        print("done")
        pB1 = True
    
def sub3_response():
    global tL5
    global us3Detect
    global sub3Start
    global us3

    timePassed = time.time()-sub3Start
    if timePassed <= 2:
        tL5 = "y"

    elif 2<timePassed <= 7:
        tL5 = "solidg"
    
    elif timePassed > 7:
        us3 = True

def integration():
    global overCarExit
    global us1Detect
    global us2Detect
    global us3Detect
    global tL1
    global tL2

    if overCarExit == True and us1Detect == False and us3Detect == False and us2Detect == False:
        tL1 = "g"
        tL2 = "g"
        overCarExit = None
    elif overCarExit == None and us2Detect == False:
        tL1 = "g"
        tL2 = "g"


#define pin
us1Pin = {"trig":2,"echo":3}
us2Pin = {"trig":4,"echo":5}
us3Pin = {"trig":6,"echo":7}
pB1Pin = 8
shifterPin = {"serial":11,"clock":9,"latch":10}

tL5FlashPin = 12

#board setup
board1013 = pymata4.Pymata4()

#output pin setup

board1013.set_pin_mode_digital_output(pB1Pin)

for pin in shifterPin.values():
    board1013.set_pin_mode_digital_output(pin)

board1013.set_pin_mode_digital_output(tL5FlashPin)

board1013.set_pin_mode_sonar(us1Pin["trig"],us1Pin["echo"],timeout=200000)
board1013.set_pin_mode_sonar(us2Pin["trig"],us2Pin["echo"],timeout=200000)
board1013.set_pin_mode_sonar(us3Pin["trig"],us3Pin["echo"],timeout=200000)

board1013.set_pin_mode_digital_input(pB1Pin)

#constant values
tunnelHeight = 50
threshold = 40

#initial states
tL1 = "g"
tL2 = "g"
tL3 = "g"
tL4 = "g"
pL1 = "r"
tL5 = "r"

us1 = True
us2 = True
us3 = True
overCarExit = None
pB1 = True
pB1Pressed = False
prevShiftBit = None  # To store last shift bit state
prevFlash = None # To store last flash state
reloop = False


try:
    while True:
        tL1Light = tL_with_yellow_shiftbit(tL1)
        tL2Light = tL_with_yellow_shiftbit(tL2)
        tL3Light = tL_without_yellow_shiftbit(tL3)
        tL4Light = tL_with_yellow_shiftbit(tL4)
        pL1Light = tL_without_yellow_shiftbit(pL1)
        tL5Light,tL5flash = tL5_shiftbit(tL5)

        shiftBit = tL4Light + pL1Light + tL5Light + tL3Light + tL1Light + tL2Light

        if shiftBit != prevShiftBit: #update only if there are changes
            set_tL_state(board1013, shifterPin, shiftBit)
            prevShiftBit = shiftBit  # Update stored value

        if tL5flash != prevFlash: #update only if there are changes
            board1013.digital_pin_write(tL5FlashPin, tL5flash)
            prevFlash = tL5flash

        if us1:
            us1_state(board1013,us1Pin["trig"],us1Pin["echo"],tunnelHeight,threshold)

        if us2:#
            us2_state(board1013,us2Pin["trig"],us2Pin["echo"],tunnelHeight,threshold)

        if us3:
            us3_state(board1013,us3Pin["trig"],us3Pin["echo"],tunnelHeight,threshold)

        if pB1:
            pB1_state(board1013,pB1Pin)

        if pB1Pressed:
            sub2_response()

        if us1Detect:
            sub1_response()

        if us3Detect:
            sub3_response()
            
        integration()
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("board shutdown")
    board1013.shutdown()

