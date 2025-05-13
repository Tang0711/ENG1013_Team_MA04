# This module contains the algorithms of a traffic system which integrates all subsystems
# Created By: Looi Yao Ren
# Created Date:: 05/05/2025 0400
# version = '1.0'

from pymata4 import pymata4
import time
from Ultrasonic_sensor import read_ultrasonic
from traffic_light_switch import tL_with_yellow_shiftbit,tL_without_yellow_shiftbit,tL5_shiftbit
from shift_register import set_tL_state

def us1_state(boardInput,trig,echo,tunnelHeight, threshold):
    """
        US1 determines whether subsystem 1 should execute responses

        Parameters:
            boardInput (pymata4.Pymata4): Arduino Board instance
            trig (int): pin number of US1 trigger pin
            echo (int): pin number of US1 echo pin
            tunnelHeight (int): Tunnel Height
            threshold (int): Maximum vehicle height allowed

        Returns:
            None
    """

    global us1 #ON/OFF state of US1
    global us1Detect #Overheight detection by US1
    global sub1Start #Start time of subsystem 1 response
    global us1Height #Height detected by US1
    global overCarExit #Has the overheight car from sub 1 exited?
    global tL1 #Light of TL1
    global tL2 #Light of TL2

    #Receives and process US1 readings
    us1Data = read_ultrasonic(boardInput,trig,echo)
    us1Height = tunnelHeight - us1Data

    if us1Height > threshold and 2<=us1Data<=60:
        us1Detect = True
        #Only if TL1 and TL2 is in inital state, execute response
        if tL1 == "g" and tL2 == "g":
            us1 = False
            overCarExit = False
            sub1Start = time.time()
            print(f"Alert: {us1Height}cm detected at {time.ctime()}")

    else:
        us1Detect = False

def us2_state(boardInput,trig,echo,tunnelHeight,threshold):
    """
        US2 determines whether subsystem 4 should execute responses

        Parameters:
            boardInput (pymata4.Pymata4): Arduino Board Instance
            trig (int): pin number of US2 trigger pin
            echo (int): pin number of US1 echo pin
            tunnelHeight (int): Tunnel Height
            threshold (int): Maximum vehicle height allowed
        
        Returns:
            None
    """

    global us2Detect #Overheight detection by US2
    global tL1
    global tL2
    global tL3 #Light of TL3
    global tL4 #Light of TL4
    global pB1 #ON/OFF state of PB1
    global pB1Pressed #Is PB1 pressed

    #Receives and process US2 readings
    us2Data = read_ultrasonic(boardInput,trig,echo)
    us2Height = tunnelHeight - us2Data

    if us2Height > threshold and 2<=us2Data<=60 :
        us2Detect = True

        #sets TL1, TL2 to red upon detection (Sub 4 I1)
        tL1 = "r"
        tL2 = "r"

        #sets TL3 to red upon detection (sub4 brief)
        tL3 = "r"

        #Sets TL4 to red upon detection (sub4 I2)
        tL4 = "r"
        
    else:
        us2Detect = False
        tL3 = "g"

        #If US2 does not detect overheight and PB1 is not pressed, always set TL4 to green
        if pB1Pressed == False:
            tL4 = "g"
    
def us3_state(boardInput,trig,echo,tunnelHeight,threshold):
    """
        US3 determines whether subsystem 3 should execute response

        Parameters:
            boardInput (int): Arduino Board Instance
            trig (int): pin number of US3 trigger pin
            echo (int): pin number of US3 echo pin
            tunnelHeight (int): Tunnel Height
            threshold (int): Maximum vehicle height allowed

        Returns:
            None
    """

    global us3 #ON/OFF state of US3
    global us3Detect #Overheight Detection of US3
    global overCarExit
    global sub3Start #Start time of subsystem 3 response
    global tL5 #Light of TL5
    global reloop #US3 has detected overheightcar

    #Receives and process US3 readings
    us3Data = read_ultrasonic(boardInput,trig,echo)
    us3Height = tunnelHeight - us3Data
    
    if us3Height > threshold and 2 <=us3Data<= 60:
        us3Detect = True
        overCarExit = False
        reloop = True #Without this boolean, we cannot know if the overheight car from sub1 has exited.

        #Only if TL5 is in initial state, executes response
        if tL5 == "r":
            us3 = False
            sub3Start = time.time()

        #if TL5 is already in solid or flashing green, continue flashing
        elif tL5 == "solidg" or tL5 == "flashg": #
            tL5 = "flashg"

    else:
        us3Detect = False
        tL5 = "r"
        
        #Only if US3 no longer detects the reached overheight car (from sub1), the car has exited.
        if reloop == True and overCarExit == False:
            overCarExit = True
            print(overCarExit)
            reloop = False

def pB1_state(boardInput,buttonPin):
    """
        PB1 determines whether subsystem 2 should execute response

        Parameters:
            boardInput (pymata4.Pymata4): Arduino Board Instance
            buttonPin (int): pin number of PB1
    """

    global pB1Pressed 
    global pB1 #ON/OFF state of PB1
    global sub2Start #Start time of subsystem 2 response

    #Read and process PB1 reading
    pB1Pressed = boardInput.digital_read(buttonPin)[0]

    #If PB1 is pressed, start the sequence and  turn off PB1
    if pB1Pressed:
        sub2Start = time.time()
        pB1 = False

def sub1_response():
    """
        Executes the response of subsystem 1

        Parameters:
            None
        
        Returns:
            None
    """

    global tL1
    global tL2
    global us1Detect
    global sub1Start
    global us1Height
    global us1

    #Records how long time has passed since the previous loop
    timePassed = time.time()-sub1Start

    if timePassed<=1:
        tL1 = "y"


    elif 1 <timePassed<= 2:
        tL1 = "r"
        tL2 = "y"

    elif timePassed> 2:
        tL1 = "r"
        tL2 = "r"
        us1 = True #Turn US1 back on once response is done

def sub2_response():
    """
        Executes the response of subsystem 2

        Parameters:
            None
        Returns:
            None
    """

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
        tL4 = "g"
        print("wait")

    elif timePassed >30:
        print("done")
        pB1 = True
    
def sub3_response():
    """
        Executes the response of subsystem 3

        Parameters:
            None

        Returns:
            None
    """

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
    """
        Determines when does TL1 and TL2 returns to initial state (green)

        Parameters:
            None
        Returns:
            None
    """

    global overCarExit
    global us1Detect
    global us2Detect
    global us3Detect
    global tL1
    global tL2

    #If an overheight car is detected at subsystem 1, only when that car has exited (US3) and US1 & US2 does not detect overheight,
    #TL1 and TL2 will turn back to green
    if overCarExit == True and us1Detect == False and us3Detect == False and us2Detect == False:
        tL1 = "g"
        tL2 = "g"
        overCarExit = None

    #If there is no overheight car and US2 no longer detects a car, TL1 and TL2 turns back to green
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

#initial traffic light states
tL1 = "g"
tL2 = "g"
tL3 = "g"
tL4 = "g"
pL1 = "r"
tL5 = "r"

#initial boolean states
us1 = True
us2 = True
us3 = True
pB1 = True
overCarExit = None
reloop = False

prevShiftBit = None  # To store last shift bit state
prevFlash = None # To store last flash state

#Main Loop
try:
    while True:
        tL1Light = tL_with_yellow_shiftbit(tL1)
        tL2Light = tL_with_yellow_shiftbit(tL2)
        tL3Light = tL_without_yellow_shiftbit(tL3)
        tL4Light = tL_with_yellow_shiftbit(tL4)
        pL1Light = tL_without_yellow_shiftbit(pL1)
        tL5Light,tL5flash = tL5_shiftbit(tL5)

        shiftBit = tL4Light + pL1Light + tL5Light + tL3Light + tL2Light + tL1Light

        if shiftBit != prevShiftBit: #update only if there are changes
            set_tL_state(board1013, shifterPin, shiftBit)
            prevShiftBit = shiftBit 

        if tL5flash != prevFlash: #update only if there are changes
            board1013.digital_pin_write(tL5FlashPin, tL5flash)
            prevFlash = tL5flash

        if us1:
            us1_state(board1013,us1Pin["trig"],us1Pin["echo"],tunnelHeight,threshold)

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
        
        #Since us2 overwrites almost all traffic light's state, it is placed at last
        if us2:
            us2_state(board1013,us2Pin["trig"],us2Pin["echo"],tunnelHeight,threshold)

        integration()

        #Let Arduino board wait for a while before executing next loop to prevent memory overuse
        time.sleep(0.05) 

except KeyboardInterrupt:
    print("board shutdown")
    shiftBit = "000000000000000000"
    set_tL_state(board1013, shifterPin, shiftBit)
    board1013.shutdown()

