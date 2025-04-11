# This module implements the Tunnel Avenue Control Subsystem
# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1649
# version = '2.0'

# Reviewed by : Tang Wei Zhi (11/04/2025)

from Ultrasonic_sensor import read_ultrasonic
import time

# Constants for timing and measurements
yellowTLTime = 1.0  # seconds
redTLTime = 30.0  # seconds
tl2DelayTime = 1.0  # seconds
threshold = 20  # cm
tunnelHeight = 100 # cm

def approach_height_detection(board,trafficLight1,trafficLight2, ultrasonic, )->None:
    """

    Executes the Approach Height Detection Subsystem, manage traffic lights' speaker system's and warning lights' behaviour when detecting vehicle height using ultrasonic sensor. 

    Parameter:
        board (pymata4.pymata4.Pymata4): board instance

        trafficLight1 (dictionary): Traffic light 1 pins configuration:
            - red (int): Digital pin for the red traffic light
            - yellow (int): Digital pin for the yellow traffic light
            - green (int): Digital pin for the green traffic light

        trafficLight2 (dictionary): Traffic light 2 pins configuration:
            - red (int): Digital pin for the red traffic light
            - yellow (int): Digital pin for the yellow traffic light
            - green (int): Digital pin for the green traffic light
                    
        ultrasonic (dictionary): ultrasonic pin configuration:
            - triggerPin (int): Digital pin for the trigger pin
            - echoPin (int): Digital pin for the echo pin
    
        threshold(int): maximum height allowed
        
    Return:
        None

    """

    # Extract pin assignments
    redTL1 = trafficLight1["red"]
    yellowTL1 = trafficLight1["yellow"]
    greenTL1 = trafficLight1["green"]

    redTL2 = trafficLight2["red"]
    yellowTL2 = trafficLight2["yellow"]
    greenTL2 = trafficLight2["green"]

    trigPin = ultrasonic["triggerPin"]
    echoPin = ultrasonic["echoPin"]

    outputPins=[redTL1, yellowTL1, greenTL1, redTL2, yellowTL2, greenTL2]

    # Configure output pins
    for pin in outputPins:
        board.set_pin_mode_digital_output(pin)

    try:
        # main control loop
        while True:
            # default state: TL1 and TL2 are green
            board.digital_pin_write(redTL1,0)
            board.digital_pin_write(yellowTL1,0)
            board.digital_pin_write(greenTL1,1)


            board.digital_pin_write(redTL2,0)
            board.digital_pin_write(yellowTL2,0)
            board.digital_pin_write(greenTL2,1)
            
            # read ultrasonic sensor input    
            distanceCM = read_ultrasonic(board,trigPin,echoPin)

            # convert deected value to height
            heightCM = tunnelHeight - distanceCM

            if heightCM > threshold:
                # print an alert
                print(f"Alert: {heightCM}cm detected at {time.time()}")
                
                # TL1 switch to yellow for 1 second
                board.digital_pin_write(greenTL1,0)                    
                board.digital_pin_write(yellowTL1,1)
                time.sleep(yellowTLTime)

                # TL1 switch to red
                board.digital_pin_write(redTL1,1)
                board.digital_pin_write(yellowTL1,0)

                # TL2 switch to yellow for 1 second                
                board.digital_pin_write(greenTL2,0)
                board.digital_pin_write(yellowTL2,1)
                time.sleep(tl2DelayTime)

                # TL2 switch to red
                board.digital_pin_write(yellowTL2,0)
                board.digital_pin_write(redTL2,1)

                # remain the traffic light status for 29 seconds
                time.sleep(redTLTime-tl2DelayTime)

                # TL1 switch to green
                board.digital_pin_write(redTL1,0)
                board.digital_pin_write(greenTL1,1)

                
                # TL2 switch to green after 1 second
                time.sleep(tl2DelayTime)
                board.digital_pin_write(redTL2,0)
                board.digital_pin_write(greenTL2,1)

               

    except KeyboardInterrupt:
        print("Board Shutting down...")
        
        # Turn off all lights and speaker before shutdown
        for pin in outputPins:
            board.digital_pin_write(pin, 0)
            
        board.shutdown()