from pymata4 import pymata4

def tL_switch(boardInput,tLstate, lights):


    redLight = lights["red"]
    yellowLight = lights["yellow"]
    greenLight = lights["green"]


    if tLstate == "r":
        boardInput.digital_pin_write(redLight,1)
        boardInput.digital_pin_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)

    if tLstate == "g":
        boardInput.digital_pin_write(redLight,0)
        boardInput.digital_pin_write(greenLight,1)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)
    
    if tLstate == "y":
        boardInput.digital_pin_write(redLight,0)
        boardInput.digital_pin_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,1)
    
    if tLstate == "rr":
        boardInput.digital_pin_write(redLight,1)
        boardInput.pwm_write(greenLight,0)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)

    if tLstate == "gg":
        boardInput.digital_pin_write(redLight,0)
        boardInput.pwm_write(greenLight,250)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)
    
    if tLstate == "ggg":
        boardInput.digital_pin_write(redLight,0)
        boardInput.pwm_write(greenLight,30)
        if yellowLight != 0:
            boardInput.digital_pin_write(yellowLight,0)