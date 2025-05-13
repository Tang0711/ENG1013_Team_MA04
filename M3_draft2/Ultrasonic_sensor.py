# A simple initialised Ultrasonic Module that only returns distance from it
# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1529
# version = '1.0'

import time

def read_ultrasonic(boardInput,triggerPin,echoPin):
    """

    Retrieves distance (cm) reading between object and sensor

    Parameter:
    - boardInput(pymata4.pymata4.Pymata4): board instance
    - triggerPin(int): digitalPin
    - echoPin(int): digitalPin

    Return:
    - distanceCM(int): distance(cm) between object and sensor

    """
    time.sleep(0.01)
    data = boardInput.sonar_read(triggerPin)
    distanceCM=data[0]
    return distanceCM

