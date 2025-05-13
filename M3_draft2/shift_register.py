# This module shifts the bits into shift registers
# Created By: Looi Yao Ren
# Created Date: 05/05/2025 06:00
# Version: "1.0"

import time
def set_tL_state(board1013,shifterPin,bits):
    """
        Sends the bits into the shift register and display out the output signals from shift registers
        
        Parameter:
            board1013 (pymata4.Pymata4): Arduino Board instance
            shifterPin (dictionary):
                serial (int): pin number of shift register serial pin
                clock (int): pin number of RCLK
                latch (int): pin number of SRCLK
            bits (string): contains string of bits 
        Returns:
            None
    """

    serialPin = shifterPin["serial"]
    clockPin = shifterPin["clock"]
    latchPin = shifterPin["latch"]

    for bit in bits:
    #Sends data(bits) to shift register (stays at serial pin)
        board1013.digital_pin_write(serialPin,int(bit))
        #Accepts data(bits) into shift register
        board1013.digital_pin_write(clockPin,1)
        board1013.digital_pin_write(clockPin,0)

    #Sends data(bits) from shift register to storage registers (OUTPUT PINS) (Display)
    board1013.digital_pin_write(latchPin,1)
    time.sleep(0.001)
    board1013.digital_pin_write(latchPin,0)
