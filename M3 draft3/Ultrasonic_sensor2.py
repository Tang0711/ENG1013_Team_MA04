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
    
    # create an empty array to store the reading of the ultrasonic sensor
    readings = []

    # loop for 5 input reading and take the average as the filtered data
    for i in range(5):
        data = boardInput.sonar_read(triggerPin)
        distanceCM=data[0]
        if distanceCM != 0:
            readings.append(distanceCM)

        time.sleep(0.01)
        # small delay for more consistant reading
        # start_time=time.time()
        # while(time.time()-start_time<0.01):
        #     pass

    # if readings array not empty, return average sum
    if readings:
        avgDistance = sum(readings) / len(readings)
        # rounding without using module
        avgDistance = int(avgDistance+0.5)
        return avgDistance


    # else return 0
    else:
        return 0