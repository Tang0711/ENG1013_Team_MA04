# this module implements the tunnel height detection system
# Created By : Akram Abdullah Mohammed (34584714)
# Created Date: 13/04/2025 0855
# version = '2.0'

import time
from pymata4 import pymata4
from Ultrasonic_sensor import read_ultrasonic

def tunnel_height_detection(boardInput,tL3,ultrasonic,tunnel_height,threshold):
    """
        Executes the Tunnel Height Detection Subsystem

    Parameter:
    -boardInput(pymata4.pymata4.Pymata4):
    -tL3(dictionary):
        - red (int): digitalPin
        - green (int): digitalPin

    -ultrasonic(dictionary):
        - triggerPin (int): digitalPin
        - echoPin (int): digitalPin
    
    -threshold(int): maximum height allowed
    
    Return:
    None
    """

    #Pin assignments
    tL3Red = tL3["red"]
    tL3Green = tL3["green"]

    trigPin = ultrasonic["triggerPin"]
    echoPin = ultrasonic["echoPin"]

    outputPins = [tL3Red,tL3Green]

    #Configure output pins
    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)

    #Main Control loop
    while True:
        try:
            #Default states for all output pins: TL3 is green
            boardInput.digital_pin_write(tL3Red,0)
            boardInput.digital_pin_write(tL3Green,1)
            
            while True:
                distanceCM = read_ultrasonic(boardInput,trigPin,echoPin)

                #converts ultrasonic readings to vehicle height
                heightCM = tunnel_height - distanceCM

                #Upon detecting an overheight vehicle turns TL3 to red
                if heightCM > threshold and 2 <= distanceCM <=400 :
                    boardInput.digital_pin_write(tL3Green,0)
                    boardInput.digital_pin_write(tL3Red,1)

                #Resets to green if and only if there's no more overheight vehicle
                else:
                    break               

        except KeyboardInterrupt:
            print("Board Shutdown")
            
            #Turns off all pins
            for pin in outputPins:
                boardInput.digital_pin_write(pin, 0)
                
            boardInput.shutdown()

def main():
    """
    
    Uploads the subsystem to the Arduino board and executes the Tunnel Height Detection System

    Parameter:
    None

    Return:
    None

    
    """
    boardInput = pymata4.Pymata4()
    tL3={"red":6,"green":7}
    ultrasonic = {"triggerPin":13,"echoPin":12}
    tunnel_height = 100
    threshold = 20
    tunnel_height_detection(boardInput,tL3,ultrasonic,tunnel_height,threshold)


if __name__ == "__main__":
    main()
            
