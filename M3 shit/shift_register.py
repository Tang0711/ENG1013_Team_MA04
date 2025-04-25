def set_tL_state(board1013,shifterPin,byte):

    serialPin = shifterPin["serial"]
    clockPin = shifterPin["clock"]
    latchPin = shifterPin["latch"]
    clearPin = shifterPin["clear"]

    shiftByte = []

    for char in byte:
        shiftByte.append(int(char))

    board1013.digital_pin_write(clearPin,1)
    board1013.digital_pin_write(clearPin,0)

    #Sends data(bytes) to shift register (stays at serial pin)
    board1013.digital_pin_write(serialPin,shiftByte)

    #Accepts data(bytes) into shift register
    board1013.digital_pin_write(clockPin,1)
    board1013.digital_pin_write(clockPin,0)

    #Sends data(bytes) from shift register to storage registers (OUTPUT PINS) (Display)
    board1013.digital_pin_write(latchPin,1)
    board1013.digital_pin_write(latchPin,0)

    