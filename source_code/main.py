# Created By : Looi_Yao_Ren(34471804)
# Created Date: 28/03/2025 1721
# version = '1.0'

from pymata4 import pymata4
from ApproachHeight import approachHeightDetection
from OverHeight import overHeight
from TunnelHeight import tunnelHeight
from TunnelAve import tunnelAve


board1013 = pymata4.Pymata4()

#bug: inital reading of ultrasonic sensor is 0cm (debug by adding condition heightCM != tunnel_height)

tL1={"red":6,"green":7,"yellow":3}
tL2={"red":4,"green":9,"yellow":10}
tL3={"red":6,"green":7}
tL4={"red":4,"green":9,"yellow":10}
pL1={"red":6,"green":7}
tL5={"red":6,"green":7,"yellow":3}
ultrasonic = {"triggerPin":13,"echoPin":12}
bP1 = 8
bP2 = 9
#tunnelHeight(board1013,tL3,ultrasonic,100,20)
#overHeight(board1013,tL5,ultrasonic,100,20)
#approachHeightDetection(board1013,tL1,tL2,ultrasonic,100,20)
#tunnelAve(board1013,tL4,pL1,bP1,bP2)