from pymata4 import pymata4
import time
from Ultrasonic_sensor2 import read_ultrasonic
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
            print(f"Alert: {us1Height}cm detected at {time.ctime()}")
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
        print("US2 detected overheight")
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
        print("US3 detected overheight")
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
            print("Car exited from overheight exit")
            reloop = False

def pB1_state(boardInput,buttonPin):
    
    global pB1Pressed
    global pB1
    global sub2Start

    pB1Raw = board1013.analog_read(0)[0]

    if pB1Raw <= 900:
        pB1Pressed = False
    else:
        pB1Pressed = True

    if pB1Pressed:
        print("Pedestrian push button PB1 is pressed.")
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
        pass
    
    elif 2 < timePassed <= 4:
        if us2Detect:
            tL4 = "r"
        else:
            tL4 = "y"

    elif 4 < timePassed <= 7:
        tL4 = "r"
        pL1 = "g"

    # elif 7 <timePassed <=9:
    #     pL1 = "r0"
    # elif 7.0 < timePassed <= 7.5:
    #     pL1 = "r"
    # elif 7.5 < timePassed <= 8.0:
    #     pL1 = "r0"
    # elif 8.0 < timePassed <= 8.5:
    #     pL1 = "r"
    # elif 8.5 < timePassed <= 9.0:
    #     pL1 = "r0"

    interval = 0.5
    if 7 < timePassed <= 9:
        pL1 = "r" if int((timePassed - 7) / interval) % 2 == 0 else "r0"

    elif 9 < timePassed <= 30:
        pL1 = "r"
        if us2Detect:
            tL4 = "r"
        else:
            tL4 = "g"
    
    elif timePassed >30:
        print("done")
        pB1 = True
    
def sub3_response(boardInput,trig,echo,tunnelHeight,threshold):
    global tL5
    global us3Detect
    global sub3Start
    global us3
    global us4Detect
    global overCarExit
    global reloop
    

    us4Data = read_ultrasonic(boardInput,trig,echo)
    us4Height = tunnelHeight - us4Data
    
    if us4Height > threshold and 2 <=us4Data<= 60:
        print("Car detected at overheight exit")
        us4Detect = True
        overCarExit = False
        reloop = True
    else:
        us4Detect = False
        
        if reloop == True and overCarExit == False:
            print("Car exited from overheight exit")
            overCarExit = True
            reloop = False

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
    global us4Detect
    global tL1
    global tL2

    if overCarExit == True and us1Detect == False and (us3Detect == False or us4Detect == False) and us2Detect == False:
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
pB1Pin = 0
shifterPin1 = {"serial":11,"clock":13,"latch":12}
shifterPin2 = {"serial":8,"clock":10,"latch":9}
# wl1=8
# tL5FlashPin = 12

#board setup
board1013 = pymata4.Pymata4()

#output pin setup

# board1013.set_pin_mode_digital_output(pB1Pin)

for pin in shifterPin1.values():
    board1013.set_pin_mode_digital_output(pin)

for pin in shifterPin2.values():
    board1013.set_pin_mode_digital_output(pin)

# board1013.set_pin_mode_digital_output(tL5FlashPin)
# board1013.set_pin_mode_digital_output(wl1)

board1013.set_pin_mode_sonar(us1Pin["trig"],us1Pin["echo"],timeout=200000)
board1013.set_pin_mode_sonar(us2Pin["trig"],us2Pin["echo"],timeout=200000)
board1013.set_pin_mode_sonar(us3Pin["trig"],us3Pin["echo"],timeout=200000)

# board1013.set_pin_mode_digital_input(pB1Pin)
board1013.set_pin_mode_analog_input(pB1Pin)
#constant values
tunnelHeight = 50
threshold = 30

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
prevShiftBit1 = None  # To store last shift bit state
prevShiftBit2 = None # To store last flash state
reloop = False
sub1Start = None
sub3Start = None
sub2Start = None
us4Detect = None


try:
    while True:
        tL1Light = tL_with_yellow_shiftbit(tL1)
        tL2Light = tL_with_yellow_shiftbit(tL2)
        tL3Light = tL_without_yellow_shiftbit(tL3)
        tL4Light = tL_with_yellow_shiftbit(tL4)
        pL1Light = tL_without_yellow_shiftbit(pL1)
        tL5Light,tL5flash = tL5_shiftbit(tL5)

        if tL2 != "g":
            wL1State = "1"
        else:
            wL1State = "0"

        #shiftBit = tL2Light + pL1Light + tL5Light + tL3Light + tL2Light + tL4Light
        #shiftBit1 unchained
        #shiftBit2 chained
        shiftBit1 = tL5Light + "0000"
        shiftBit2 = tL4Light  + wL1State + tL2Light + tL1Light + pL1Light + tL3Light + "00"



        if shiftBit1 != prevShiftBit1: #update only if there are changes
            print(f"Updated ShiftBit1: {shiftBit1}")
            set_tL_state(board1013, shifterPin1, shiftBit1)
            prevShiftBit1 = shiftBit1  # Update stored value
        
        time.sleep(0.01)
        if shiftBit2 != prevShiftBit2: #update only if there are changes
            print(f"Updated ShiftBit2: {shiftBit2}")
            set_tL_state(board1013, shifterPin2, shiftBit2)
            prevShiftBit2 = shiftBit2  # Update stored value

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
            sub3_response(board1013,us3Pin["trig"],us3Pin["echo"],tunnelHeight,threshold)
            
        integration()

        time.sleep(0.01)
        # small delay to avoid CPU hogging
        # start_time=time.time()
        # while((time.time()-start_time)<0.01):
        #     pass

except KeyboardInterrupt:
    set_tL_state(board1013, shifterPin1, "00000000")
    set_tL_state(board1013, shifterPin2, "0000000000000000")
    time.sleep(1)
    print("board shutdown")
    board1013.shutdown()
