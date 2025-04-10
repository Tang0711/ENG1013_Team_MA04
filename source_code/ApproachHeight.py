# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1649
# version = '1.0'

from Ultrasonic_sensor import ultrasonicSonar
import time

def approachHeightDetection(boardInput,tL1,tL2,ultrasonic,tunnel_height,threshold):
    """

    Executes the Approach Height Detection Subsystem

    Parameter:
    -boardInput(pymata4.pymata4.Pymata4):
    -tL1(dictionary):
        - red (int): digitalPin
        - yellow (int): digitalPin
        - green (int): digitalPin
    
    -tL2(dictionary):
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

    #setPin
    tL1red = tL1["red"]
    tL1yellow = tL1["yellow"]
    tL1green = tL1["green"]

    tL2red = tL2["red"]
    tL2yellow = tL2["yellow"]
    tL2green = tL2["green"]

    trigPin = ultrasonic["triggerPin"]
    echoPin = ultrasonic["echoPin"]

    outputPins=[tL1red,tL1yellow,tL1green,tL2red,tL2yellow,tL2green,]
    #set digitalPinMode

    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)

    while True:
        try:
            #set initial state
            boardInput.digital_pin_write(tL1red,0)
            boardInput.digital_pin_write(tL1yellow,0)
            boardInput.digital_pin_write(tL1green,1)


            boardInput.digital_pin_write(tL2red,0)
            boardInput.digital_pin_write(tL2yellow,0)
            boardInput.digital_pin_write(tL2green,1)
            
            while True:
                
                distanceCM = ultrasonicSonar(boardInput,trigPin,echoPin)

                heightCM = tunnel_height - distanceCM

                if heightCM > threshold and heightCM !=tunnel_height:
                    print(f"Alert: {heightCM}cm detected at {time.time()}")
                    boardInput.digital_pin_write(tL1green,0)                    
                    boardInput.digital_pin_write(tL1yellow,1)
                    time.sleep(1)

                    boardInput.digital_pin_write(tL1red,1)
                    boardInput.digital_pin_write(tL1yellow,0)
                    boardInput.digital_pin_write(tL2green,0)
                    boardInput.digital_pin_write(tL2yellow,1)
                    time.sleep(1)

                    boardInput.digital_pin_write(tL2yellow,0)
                    boardInput.digital_pin_write(tL2red,1)
                    time.sleep(29)

                    boardInput.digital_pin_write(tL1red,0)
                    boardInput.digital_pin_write(tL1green,1)
                    time.sleep(1)
                    break

                else:
                    continue

        except KeyboardInterrupt:
            boardInput.shutdown()