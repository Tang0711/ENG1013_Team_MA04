# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1725
# version = '1.0'

from Ultrasonic_sensor import ultrasonicSonar

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

    #Configure pins
    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)

    #Main Control loop
    while True:
        try:
            #Default states for all output pins
            boardInput.digital_pin_write(tL3Red,0)
            boardInput.digital_pin_write(tL3Green,1)
            
            while True:
                distanceCM = ultrasonicSonar(boardInput,trigPin,echoPin)

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
                board.digital_pin_write(pin, 0)
                
            boardInput.shutdown()


            

