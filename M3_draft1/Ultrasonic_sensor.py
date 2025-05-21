# A simple initialised Ultrasonic Module that only returns distance from it
# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1529
# version = '2.0'

import time

def read_ultrasonic(boardInput,triggerPin,echoPin):
    """

    Retrieves distance (cm) reading between object and sensor

    Parameter:
    - boardInput(pymata4.pymata4.Pymata4): board instance
    - triggerPin(int): digitalPin
    - echoPin(int): digitalPin

    Return:
    - avgDistance(int): averagedistance(cm) between object and sensor

    """

    readings = []
    for i in range(5):
        data = boardInput.sonar_read(triggerPin)
        distanceCM=data[0]
        if distanceCM != 0:
            readings.append(distanceCM)
        time.sleep(0.01)
    if readings:
        avgDistance = sum(readings) / len(readings)
        avgDistance = int(avgDistance+0.5)
    else:
        avgDistance = 0 
    
    return avgDistance

