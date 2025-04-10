# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1529
# version = '1.0'

import time

def ultrasonicSonar(boardInput,triggerPin,echoPin):
    """

    Retrieves distance (cm) reading between object and sensor

    Parameter:
    - boardInput(pymata4.pymata4.Pymata4)
    - triggerPin(int): digitalPin
    - echoPin(int): digitalPin

    Return:
    - distanceCM(int): distance(cm) between object and sensor

    """
    boardInput.set_pin_mode_sonar(triggerPin,echoPin)
    time.sleep(0.01)
    data = boardInput.sonar_read(triggerPin)
    distanceCM=data[0]
    return distanceCM

