# This module implements the Approach Height Detection Subsystem
# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1649
# version = '2.0'

from Ultrasonic_sensor import read_ultrasonic
import time
from pymata4 import pymata4

def over_height_exit(boardInput,tL5,ultrasonic,tunnelHeight,threshold):
    """

    Executes the Approach Height Detection Subsystem

    Parameter:
    -boardInput(pymata4.pymata4.Pymata4):
    -tL5(dictionary):
        - red (int): digitalPin
        - yellow (int): digitalPin
        - green (int): digitalPin

    -ultrasonic(dictionary):
        - triggerPin (int): digitalPin
        - echoPin (int): digitalPin

    -tunnelHeight(float): Tunnel height
    -threshold(float): maximum height allowed
        
    Return:
    None
    
    """

    #Pin assignments
    tL5Red = tL5["red"]
    tL5Yellow = tL5["yellow"]
    tL5Green = tL5["green"]

    trigPin = ultrasonic["triggerPin"]
    echoPin = ultrasonic["echoPin"]

    outputPins = [tL5Red,tL5Yellow, tL5Green]

    #Configure Output Pins
    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)

    #main control loop
    while True:
        try:
            #default state of all output pins: TL5 is red
            boardInput.digital_pin_write(tL5Red,1)
            boardInput.digital_pin_write(tL5Yellow,0)
            boardInput.digital_pin_write(tL5Green,0)

            while True:
                distanceCM = read_ultrasonic(boardInput,trigPin,echoPin)

                #Converts ultraosonic reading to vehicle height
                heightCM = tunnelHeight - distanceCM

                #upon detecting an overheight vehicle triggers response
                if heightCM > threshold and 2<=distanceCM<=400:

                    #TL5 turns yellow for 2 seconds
                    boardInput.digital_pin_write(tL5Red,0)
                    boardInput.digital_pin_write(tL5Yellow,1)
                    time.sleep(2)

                    #TL5 turns green for 5 seconds 
                    boardInput.digital_pin_write(tL5Yellow,0)
                    boardInput.digital_pin_write(tL5Green,1)
                    time.sleep(5)

                    #TL5 returns to initial state
                    break

                #Otherwise, keep checking
                else:
                    continue

        except KeyboardInterrupt:
            print("Board Shutdown")

            #Turn off all outputpins
            for pin in outputPins:
                board.digital_pin_write(pin, 0)
            
            boardInput.shutdown()

def main():
    """
    
    Uploads the subsystem to the Arduino board and executes the Approach Height Detection Subsystem

    Parameter:
    None
        
    Return:
    None
    
    """
    #Initialise board and digital pins
    boardInput = pymata4.Pymata4()
    tL5 = {'red':6,'yellow':7,'green':8}
    ultrasonic = {'triggerPin':4,'echoPin':5}

    #Set constant Tunnel height and overheight threshold
    tunnelHeight = 50
    threshold = 40

    #Call subsystem
    over_height_exit(boardInput,tL5,ultrasonic,tunnel_height,threshold)

if __name__ == "__main__":
    main()

    
    
