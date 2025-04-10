# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1649
# version = '1.0'

from Ultrasonic_sensor import ultrasonicSonar
import time

def overHeight(boardInput,tL5,ultrasonic,tunnel_height,threshold):
    """

    Executes the Approach Height Detection Subsystem

    Parameter:
    -boardInput(pymata4.pymata4.Pymata4):
    -tL3(dictionary):
        - red (int): digitalPin
        - yellow (int): digitalPin
        - green (int): digitalPin

    -ultrasonic(dictionary):
        - triggerPin (int): digitalPin
        - echoPin (int): digitalPin
    
    -threshold(int): maximum height allowed
        
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
                distanceCM = ultrasonicSonar(boardInput,trigPin,echoPin)
                heightCM = tunnel_height - distanceCM

                if heightCM > threshold and heightCM !=tunnel_height:
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