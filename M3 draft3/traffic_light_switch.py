def tL_switch(boardInput,tLState, lights):

    redLight = lights["red"]
    yellowLight = lights["yellow"]
    greenLight = lights["green"]


    if tLState == "r":
        boardInput.digital_pin_write(redLight,1)
        boardInput.digital_pin_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)
    
    if tLState == "r0":
        boardInput.digital_pin_write(redLight,0)
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



def tL_with_yellow_shiftbit(tLState):

    #bit follows red,yellow,green
    shiftBit = "000"

    if tLState == "r":
        shiftBit = "100"

    elif tLState == "g":
        shiftBit = "001"

    elif tLState == "y":
        shiftBit = "010"

    return shiftBit

def tL_without_yellow_shiftbit(tLState):

    #bit follows red,green
    shiftBit = "00"

    if tLState == "r":
        shiftBit = "10"

    elif tLState == "r0":
        shiftBit = "00"

    elif tLState == "g":
        shiftBit = "01"

    return shiftBit

def tL5_shiftbit(tLState):

    #bit follows red,yellow,solidgreen,flashgreen
    shiftBit = "0000"
    flash = 0

    if tLState == "r":
        shiftBit = "1000"
        flash = 0

    elif tLState == "y":
        shiftBit = "0100"
        flash = 0

    elif tLState == "solidg":
        shiftBit = "0010"
        # shiftBit = "100"
        flash = 0

    elif tLState == "flashg":
        shiftBit = "0001"
        flash = 1

    return shiftBit,flash