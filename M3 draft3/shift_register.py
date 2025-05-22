import time
def set_tL_state(board1013,shifterPin,bits):

    serialPin = shifterPin["serial"]
    clockPin = shifterPin["clock"]
    latchPin = shifterPin["latch"]

    shiftBits = []

    for char in bits:
        shiftBits.append(int(char))

    for bit in shiftBits:
        # Sends data(bits) to shift register (stays at serial pin)
        board1013.digital_pin_write(serialPin,bit)
        # Accepts data(bits) into shift register
        board1013.digital_pin_write(clockPin,1)
        board1013.digital_pin_write(clockPin,0)

    # Sends data(bits) from shift register to storage registers (OUTPUT PINS) (Display)
    board1013.digital_pin_write(latchPin, 1)
    time.sleep(0.001)  # Slightly longer latch hold
    board1013.digital_pin_write(latchPin, 0)
