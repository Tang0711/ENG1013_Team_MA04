# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1725
# version = '1.0'

from Ultrasonic_sensor import ultrasonicSonar

def tunnel_height(boardInput,tL3,ultrasonic,tunnel_height,threshold):
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

    tL3Red = tL3["red"]
    tL3Green = tL3["green"]

    trigPin = ultrasonic["triggerPin"]
    echoPin = ultrasonic["echoPin"]

    outputPins = [tL3Red,tL3Green]

    #Configure pins
    for pin in outputPins:
        boardInput.set_pin_mode_digital_output(pin)
    
    while True:
        try:
            boardInput.digital_pin_write(tL3Red,0)
            boardInput.digital_pin_write(tL3Green,1)
            
            while True:
                distanceCM = ultrasonicSonar(boardInput,trigPin,echoPin)
                
                heightCM = tunnel_height - distanceCM

                if heightCM > threshold and heightCM !=tunnel_height :
                    boardInput.digital_pin_write(tL3Green,0)
                    boardInput.digital_pin_write(tL3Red,1)

                else:
                    break               

        except KeyboardInterrupt:
            boardInput.shutdown()
            

