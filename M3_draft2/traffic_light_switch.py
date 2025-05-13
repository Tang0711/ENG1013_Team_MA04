# This module contains functions that sets the bits for a traffic light
# Created By: Looi Yao Ren
# Created Date: 05/05/2025 0600
# Version: '1.0'

def tL_with_yellow_shiftbit(tLState):
    """
        Determines the bits for traffic lights that has yellow light

        Parameter:
            tLState (string): light of the traffic light
        Returns:
            shiftBit (String): a string of bits that sets which led to 0 and 1
    """

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
    """
        Determines the bits for traffic lights that has no yellow light

        Parameter:
            tLState (string): light of the traffic light
        Returns:
            shiftBit (String): a string of bits that sets which led to 0 and 1
    """
    
    #bit follows red,green
    shiftBit = "00"

    if tLState == "r":
        shiftBit = "10"

    elif tLState == "r0": #r0 means turn all lights off
        shiftBit = "00"

    elif tLState == "g":
        shiftBit = "01"

    return shiftBit

def tL5_shiftbit(tLState):
    """
        Determines the bits for TL5 that that green LED can turn solid or blink

        Parameter:
            tLState (string): Light of the traffic light

        Returns:
            shiftBit (string): a string of bits that sets which led to 0 and 1
    """
    
    #bit follows red,yellow,solidgreen,flashgreen
    shiftBit = "000"
    flash = 0

    if tLState == "r":
        shiftBit = "100"
        flash = 0

    elif tLState == "y":
        shiftBit = "010"
        flash = 0

    #if solid green, use shift register output signal
    elif tLState == "solidg":
        shiftBit = "001"
        flash = 0

    #if flash greem, use arduino board pin output signal
    elif tLState == "flashg":
        shiftBit = "000"
        flash = 1

    return shiftBit,flash