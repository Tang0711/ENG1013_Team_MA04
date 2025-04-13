# This module implements the Approach Height Detection Subsystem
# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1649
# version = '1.0'

from Ultrasonic_sensor import read_ultrasonic
import time
from pymata4 import pymata4

def over_height_exit(boardInput,tL5,ultrasonic,tunnel_height,threshold):
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

    -tunnel_height(float): Tunnel height
    -threshold(float): maximum height allowed
        
    Return:
    None
    
    """


    tL5Red = tL5["red"]
    tL5Yellow = tL5["yellow"]
    tL5Green = tL5["green"]

    trigPin = ultrasonic["triggerPin"]
    echoPin = ultrasonic["echoPin"]

    outputPins = [tL5Red,tL5Yellow, tL5Green]

    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)
    
    while True:
        try:
            boardInput.digital_pin_write(tL5Red,1)
            boardInput.digital_pin_write(tL5Yellow,0)
            boardInput.digital_pin_write(tL5Green,0)

            while True:
                distanceCM = read_ultrasonic(boardInput,trigPin,echoPin)
                heightCM = tunnel_height - distanceCM

                if heightCM > threshold and 2<=distanceCM<=400:
                    boardInput.digital_pin_write(tL5Red,0)
                    boardInput.digital_pin_write(tL5Yellow,1)
                    time.sleep(2)

                    boardInput.digital_pin_write(tL5Yellow,0)
                    boardInput.digital_pin_write(tL5Green,1)
                    time.sleep(5)
                    break
                else:
                    continue

        except KeyboardInterrupt:
            print("Board Shutdown")
            boardInput.shutdown()

def main():
    """

    Uploads the subsystem to the Arduino board and executes the Approach Height Detection Subsystem

    Parameter:
    None
        
    Return:
    None
    
    """
    boardInput = pymata4.Pymata4()
    tL5 = {'red':6,'yellow':7,'green':8}
    ultrasonic = {'triggerPin':4,'echoPin':5}
    tunnel_height = 100
    threshold =70
    over_height_exit(boardInput,tL5,ultrasonic,tunnel_height,threshold)

if __name__ == "__main__":
    main()

    
    
