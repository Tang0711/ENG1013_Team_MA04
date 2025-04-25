def tL_switch(boardInput,tLState, lights):

    redLight = lights["red"]
    yellowLight = lights["yellow"]
    greenLight = lights["green"]


    if tLState == "r":
        boardInput.digital_pin_write(redLight,1)
        boardInput.digital_pin_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)

    if tLState == "g":
        boardInput.digital_pin_write(redLight,0)
        boardInput.digital_pin_write(greenLight,1)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)
    
    if tLState == "y":
        boardInput.digital_pin_write(redLight,0)
        boardInput.digital_pin_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,1)
    
    if tLState == "rr":
        boardInput.digital_pin_write(redLight,1)
        boardInput.pwm_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)

    if tLState == "gg":
        boardInput.digital_pin_write(redLight,0)
        boardInput.pwm_write(greenLight,250)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)
    
    if tLState == "ggg":
        boardInput.digital_pin_write(redLight,0)
        boardInput.pwm_write(greenLight,30)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)

def tL_with_yellow_shiftbyte(tLState):

    #byte follows red,yellow,green

    if tLState == "r":
        shiftbyte = "100"

    if tLState == "g":
        shiftbyte = "001"
    
    if tLState == "y":
        shiftbyte = "010"
    
    return shiftbyte

def tL_without_yellow_shiftbyte(tLState):

    #byte follows red,green

    if tLState == "r":
        shiftbyte = "10"

    if tLState == "g":
        shiftbyte = "01"

    return shiftbyte

def tL5_shiftbyte(tLState):

    #byte follows red,yellow

    if tLState == "rr":
        shiftbyte = "01"
        pwmGreen = 0

    if tLState == "gg":
        shiftbyte = "00"
        pwmGreen = 250
    
    if tLState == "ggg":
        shiftbyte = "00"
        pwmGreen = 30

    return shiftbyte,pwmGreen
