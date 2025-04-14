# This module implements the Tunnel Avenue Control Subsystem
# Created By : Tang Wei Zhi(34894659)
# Created Date: 11/04/2025 1649
# version = '3.0'

import time
import pymata4.pymata4 as pymata4
# Constants for timing
systemWaitTime = 2.0 # second
yellowTLTime = 2.0  # seconds
redFlashingTime = 5.0 # seconds
greenPLTime = 3.0  # seconds
flashTimeInterval = 0.25  # seconds


def read_push_button(board, buttonPin)->bool:
    """
    Read the state of a push button with basic debouncing
    
    Parameters:
        board (pymata4.pymata4.Pymata4): board instance
        buttonPin (int): digital pin for the push button
        
    Returns:
        bool: True if button pressed, False otherwise
    """

    board.set_pin_mode_digital_input(buttonPin)
    button_state = board.digital_read(buttonPin)[0]
    
    if button_state == 1:
        return True
    else:
        return False

def tunnel_ave(board, trafficLight, pedestrianLight, pushButton)->None:
    """
        Executes the Tunnel Ave Control Subsystem, manage traffic lights' and pedestrian lights' behaviour when push button is pressed.

    Parameter:
        board (pymata4.pymata4.Pymata4): board instance
        
        trafficLight (dictionary): Traffic light pins configuration:
            - red (int): Digital pin for the red traffic light
            - yellow (int): Digital pin for the yellow traffic light
            - green (int): Digital pin for the green traffic light


        pedestrianLight (dictionary): Pedestrian light pins configuration:
            - red (int): Digital pin for the red pedestrian light
            - green (int): Digital pin for the green pedestrian light


        pushButton (int): Digital pin for pedestrian push button

    Return:
        None
    
    """

    # Extract pin assignments
    redTL = trafficLight["red"]
    yellowTL = trafficLight["yellow"]
    greenTL = trafficLight["green"]
    
    redPL = pedestrianLight["red"]
    greenPL = pedestrianLight["green"]
    
    outputPins=[redTL, yellowTL, greenTL, redPL, greenPL]
    
    # Configure output pins
    for pin in outputPins:
        board.set_pin_mode_digital_output(pin)

    # Configure button input
    board.set_pin_mode_digital_input(pushButton)

    try:
        # main control loop
        while True:
            # Default state: TL4 is green, PL1 is red
            board.digital_pin_write(redPL,1)
            board.digital_pin_write(greenPL,0)

            board.digital_pin_write(redTL,0)
            board.digital_pin_write(yellowTL,0)
            board.digital_pin_write(greenTL,1)

            if read_push_button(board, pushButton):                
                # print button pressed and wait for 2 second
                print("Pedestrian push button PB1 is pressed.")
                time.sleep(systemWaitTime)

                # TL4 turns yellow for 2 seconds
                board.digital_pin_write(greenTL,0)
                board.digital_pin_write(yellowTL,1)
                time.sleep(yellowTLTime)

                # TL4 turns red for 5 seconds
                board.digital_pin_write(redTL,1)
                board.digital_pin_write(yellowTL,0)

                # PL1 turns green for 3 seconds
                board.digital_pin_write(redPL,0)
                board.digital_pin_write(greenPL,1)
                time.sleep(greenPLTime)

                # Turn off PL1 green light
                board.digital_pin_write(greenPL,0)

                # PL1 flashing red 4 times over 2 seconds
                for sequence in range(4):
                    board.digital_pin_write(redPL, 1)
                    time.sleep(flashTimeInterval)
                    board.digital_pin_write(redPL, 0)
                    time.sleep(flashTimeInterval)

                # Reset to solid red for PL1
                board.digital_pin_write(redPL, 1)

                # TL4 turns back to green
                board.digital_pin_write(redTL, 0)
                board.digital_pin_write(greenTL, 1)

            # Small delay to prevent CPU overutilization
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Board Shuting down...")

        # Turn off all lights before shutdown
        for pin in outputPins:
            board.digital_pin_write(pin, 0)
                
        board.shutdown()

def main()->None:
    """
    main entry point to execute the Tunnel Ave Control Subsystem

    Parameter:
        None

    Return:
        None
    """
    # initialise board instance
    board=pymata4.Pymata4()
    #pin assignments
    tl4={"red":8,"yellow":9,"green":10}
    pl1={"red":6,"green":7}
    pb=4
    tunnel_ave(board,tl4,pl1,pb)

if __name__=="__main__":
    main()
