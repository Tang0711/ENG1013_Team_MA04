def tL_with_yellow_shiftbit(tLState):
    #bit follows green,yellow,red
    shiftBit = "000"

    if tLState == "r":
        #shiftBit = "100"
        shiftBit = "001"

    elif tLState == "g":
        #shiftBit = "001"
        shiftBit = "100"

    elif tLState == "y":
        shiftBit = "010"

    return shiftBit

def tL_without_yellow_shiftbit(tLState):
    #bit follows green,red
    shiftBit = "00"

    if tLState == "r":
        #shiftBit = "10"
        shiftBit = "01"

    elif tLState == "r0":
        shiftBit = "00"

    elif tLState == "g":
        #shiftBit = "01"
        shiftBit = "10"

    return shiftBit

def tL5_shiftbit(tLState):
    #bit follows solidgreen, yellow, red. Gives flashgreen
    shiftBit = "000"
    flash = 0

    if tLState == "r":
        #shiftBit = "100"
        shiftBit = "001"
        flash = 0

    elif tLState == "y":
        shiftBit = "010"
        flash = 0

    elif tLState == "solidg":
        #shiftBit = "001"
        shiftBit = "100"
        flash = 0

    elif tLState == "flashg":
        shiftBit = "000"
        flash = 1

    return shiftBit,flash
