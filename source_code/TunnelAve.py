from pymata4 import pymata4
from PushButton import pushButton
import time

def tunnelAve(boardInput,tL4, pL1, bP1,bP2):
    """
        Executes the Tunnel Ave Control Subsystem

    Parameter:
    -boardInput(pymata4.pymata4.Pymata4): board instance

    -tL4(dictionary):
        - red (int): digitalPin
        - yellow (int): digitalPin
        - green (int): digitalPin

    -PL1(dictionary):
        - red (int): digitalPin
        - green (int): digitalPin

    -bP1(int): digitalPin

    -bp2(int): digitalPin

    Return:
    None
    
    """

    tL4Red = tL4["red"]
    tL4Yellow = tL4["yellow"]
    tL4Green = tL4["green"]

    pL1Red = pL1["red"]
    pL1Green = pL1["green"]


    outputPins = [tL4Red,tL4Yellow,tL4Green,pL1Red,pL1Green]
    
    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)
    

    while True:
        try:
            boardInput.digital_pin_write(pL1Red,1)
            boardInput.digital_pin_write(pL1Green,0)

            boardInput.digital_pin_write(tL4Red,0)
            boardInput.digital_pin_write(tL4Yellow,0)
            boardInput.digital_pin_write(tL4Green,1)

            while True:
                buttonState1 = pushButton(boardInput,bP1)
                buttonState2 = pushButton(boardInput,bP2)

                if buttonState1 == 1 or buttonState2==1:
                    print("Pedestrian push button PB1 is pressed.")
                    time.sleep(2)

                    boardInput.digital_pin_write(tL4Green,0)
                    boardInput.digital_pin_write(tL4Yellow,1)
                    time.sleep(2)

                    boardInput.digital_pin_write(tL4Red,1)
                    boardInput.digital_pin_write(tL4Yellow,0)

                    boardInput.digital_pin_write(pL1Red,0)
                    boardInput.digital_pin_write(pL1Green,1)
                    time.sleep(3)

                    boardInput.digital_pin_write(pL1Green,0)
                    boardInput.digital_pin_write(pL1Red,1) #pL1 flash red for 2 seconds
                    time.sleep(0.5)
                    boardInput.digital_pin_write(pL1Red,0)
                    time.sleep(0.5)
                    boardInput.digital_pin_write(pL1Red,1)
                    time.sleep(0.5)
                    boardInput.digital_pin_write(pL1Red,0)
                    time.sleep(0.5)
                    break


        except KeyboardInterrupt:
            print("Board Shutdown")
            boardInput.shutdown()