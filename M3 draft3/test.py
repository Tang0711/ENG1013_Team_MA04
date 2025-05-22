from pymata4 import pymata4

from shift_register import set_tL_state
from Ultrasonic_sensor import read_ultrasonic
import time

us1Pin = {"trig":2,"echo":3}
us2Pin = {"trig":4,"echo":5}
us3Pin = {"trig":6,"echo":7}
# pB1Pin = 13
shifterPin2 = {"serial":8,"clock":10,"latch":9}
shifterPin1 = {"serial":11,"clock":13,"latch":12}

board1013 = pymata4.Pymata4()

# shifter setup
for pin in shifterPin1.values():
    board1013.set_pin_mode_digital_output(pin)

for pin in shifterPin2.values():
    board1013.set_pin_mode_digital_output(pin)


# board1013.set_pin_mode_digital_input(pB1Pin) #pushbutton
# board1013.set_pin_mode_digital_output(12) #TL5 green
#board1013.digital_pin_write(12,1)
count = True
shiftBit1 = "00010001"
shiftBit2 = "1111111111111111"
startTime = time.time()
prevShiftBit1 = None  # To store last shift bit state
prevShiftBit2 = None # To store last flash state

board1013.set_pin_mode_sonar(2,3,timeout=200000)
board1013.set_pin_mode_sonar(4,5,timeout=200000)
board1013.set_pin_mode_sonar(6,7,timeout=200000)
# board1013.set_pin_mode_digital_output(8)

board1013.set_pin_mode_analog_input(5)

try:
    while True:
        if shiftBit1 != prevShiftBit1: #update only if there are changes
            print(f"Updated ShiftBit1: {shiftBit1}")
            set_tL_state(board1013, shifterPin1, shiftBit1)
            prevShiftBit1 = shiftBit1  # Update stored value

        if shiftBit2 != prevShiftBit2: #update only if there are changes
            print(f"Updated ShiftBit2: {shiftBit2}")
            set_tL_state(board1013, shifterPin2, shiftBit2)
            prevShiftBit2 = shiftBit2  # Update stored value

        # if time.time()-startTime >5:
        #     print(shiftBit)
        #     shiftBit = "0000000000000000"
        #     board1013.digital_pin_write(5,0)
        # set_tL_state(board1013, shifterPin, "11111111")
        # print(board1013.digital_read(pB1Pin)[0])
        # print(read_ultrasonic(board1013,us1Pin["trig"],us1Pin["echo"]))
        # print(read_ultrasonic(board1013,us2Pin["trig"],us2Pin["echo"]))
        # print(read_ultrasonic(board1013,us3Pin["trig"],us3Pin["echo"]))
        
        # board1013.digital_pin_write(8,1)

        # print(board1013.analog_read(5)[0])
        # board1013.digital_pin_write(12,0)
        # set_tL_state(board1013, shifterPin, "1111111111000000")
        # set_tL_state(board1013, shifterPin2, "00000000")
        # board1013.digital_pin_write(7,1)
        time.sleep(0.1)
        # time.sleep(0.2)
except KeyboardInterrupt:
    # set_tL_state(board1013, shifterPin, "0000000000000000")
    set_tL_state(board1013, shifterPin1, "00000000")
    set_tL_state(board1013, shifterPin2, "0000000000000000")
    time.sleep(0.2)
    board1013.shutdown()