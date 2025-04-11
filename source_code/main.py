# main entry point for executing milestone 2
# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1721
# version = '2.0'

# Reviewed by : Tang Wei Zhi (11/04/2025)

from pymata4 import pymata4
from ApproachHeight import approach_height_detection
from TunnelAve import tunnel_ave
from OverHeight import over_height_exit
from TunnelHeight import tunnel_height

if __name__ == "__main__":
    board1013 = pymata4.Pymata4()

    #bug: inital reading of ultrasonic sensor is 0cm (debug by adding condition heightCM != tunnel_height)

    tL1={"red":6,"green":7,"yellow":3}
    tL2={"red":4,"green":9,"yellow":10}
    tL3={"red":6,"green":7}
    tL4={"red":4,"green":9,"yellow":10}
    pL1={"red":6,"green":7}
    tL5={"red":6,"green":7,"yellow":3}
    ultrasonic = {"triggerPin":13,"echoPin":12}
    pushButton = 8
    #tunnelHeight(board1013,tL3,ultrasonic,100,20)
    #overHeight(board1013,tL5,ultrasonic,100,20)
    #approachHeightDetection(board1013,tL1,tL2,ultrasonic)
    #tunnelAve(board1013,tL4,pL1,pushButton)