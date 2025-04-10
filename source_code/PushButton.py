import time

def pushButton(boardInput,buttonPin):
    """

    Retrieves button state (boolean)

    Parameter:
    - boardInput(pymata4.pymata4.Pymata4)
    - buttonPin(int): digitalPin

    Return:
    - buttonState(boolean): pushed (True) or not pushed (False) 

    """

    boardInput.set_pin_mode_digital_input(buttonPin)
    time.sleep(0.01)
    buttonData = boardInput.digital_read(buttonPin)
    buttonState = buttonData[0]


    return buttonState
