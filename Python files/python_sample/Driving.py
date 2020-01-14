import math as math
import time
from time import sleep
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
#zig from zigbee import Zigbee
import Locations
sign = lambda x: math.copysign(1, x)

angle_tolerance = 2
distance_tolerance = 50
angles = [2, 5, 10, 15, 20, 30, 45, 90, 135, 180]
distances = [20, 50, 100, 150, 200, 300, 400, 500, 750, 1000]


#MOVE SIM PARAM
delta_t = 0.001
speed = 10*delta_t

# Server connection setup
MEMESIM_IP_ADDR = "131.155.127.244"
TEAM_NUMBER = 8
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)
MEMESIM_CLIENT.connect()

# Connect Zigbee
#zig ZIGBEE = Zigbee('COM20', 9600)

def SetPosition(robotID, position):
    RQ = MemeSimCommand.RS(8, robotID+14 ,position[0] ,position[1] ,math.radians(position[2]))
    MEMESIM_CLIENT.send_command(RQ)

    sleep(1.0)

    RQ = MemeSimCommand.RQ(8, robotID+14)
    MEMESIM_CLIENT.send_command(RQ)

    sleep(1.0)

    RESPONSES = MEMESIM_CLIENT.new_responses()

    for resp in RESPONSES:
        if resp.cmdtype() == 'rs':
            if not resp.iserror():
                xpos = int(float(resp.cmdargs()[2]))
                ypos = int(float(resp.cmdargs()[3]))
                angle = round(math.degrees(float(resp.cmdargs()[4])))

                print(f"Set position of Robot {robotID}: {xpos}, {ypos}, {angle}")
    return

def simDriving(instruction):
    rob_pos, rob_angle = GetPosition(RobotID)

    if instruction[0] == "L":
        newAngle = rob_angle + angles[int(instruction[1])]
        SetPosition(2, [rob_pos[0], rob_pos[1], newAngle])
    elif instruction[0] == "R":
        newAngle = rob_angle - angles[int(instruction[1])]
        SetPosition(2, [rob_pos[0], rob_pos[1], newAngle])
    elif instruction[0] == "F":
        newPos = [rob_pos[0] + distances[int(instruction[1])]*math.cos(math.radians(rob_angle)), rob_pos[1] + distances[int(instruction[1])]*math.sin(math.radians(rob_angle))]
        SetPosition(2, [newPos[0], newPos[1], rob_angle])

def GetPosition(robotID):
    RQ = MemeSimCommand.RQ(8, robotID+14)
    MEMESIM_CLIENT.send_command(RQ)

    sleep(1.0)

    RESPONSES = MEMESIM_CLIENT.new_responses()

    for resp in RESPONSES:
        if resp.cmdtype() == 'rq':
            if not resp.iserror():
                xpos = int(float(resp.cmdargs()[2]))
                ypos = int(float(resp.cmdargs()[3]))
                angle = round(math.degrees(float(resp.cmdargs()[4])))

                return [xpos, ypos], angle
    return

def GetInstruction(RobotID, target):
    try:
        rob_pos, rob_angle = GetPosition(RobotID)
        print([round(rob_pos[0], 1), round(rob_pos[1], 1)], round(rob_angle, 1))
    except:
        return "ERROR: No Position"

    tar_angle = round(math.degrees(math.atan2(target[1] - rob_pos[1], target[0] - rob_pos[0]))) - rob_angle
    if abs(tar_angle) > 180:
        tar_angle = tar_angle - sign(tar_angle)*360

    tar_distance = math.sqrt((target[1] - rob_pos[1])**2 + (target[0] - rob_pos[0])**2)

    print(f"Target angle = {tar_angle}")
    print(f"Target distance = {tar_distance}")

    if tar_distance > distance_tolerance:
        if abs(tar_angle) > angle_tolerance:
            i = 0
            while angles[min(i + 1, 9)] <= abs(tar_angle) and i < 9:
                i = i + 1
            if tar_angle < 0:
                return "R" + str(i)
            elif tar_angle > 0:
                return "L" + str(i)
        elif tar_distance > distance_tolerance:
            i = 0
            while distances[min(i+1,9)] <= abs(tar_distance) and i < 9:
                i = i + 1
            return "F" + str(i)
    else:
        return "S"
    return "ERROR: No Instruction"

def SendInstruction(RobotID, instruction):
    ReveiverID = [5, 5][RobotID-1]
    print("Send Instruction: " + "1" + str(ReveiverID) + instruction)
    #zig ZIGBEE.write(bytes("1" + str(ReveiverID) + instruction, 'utf-8'))
    simDriving(instruction)

def GuideTo(RobotID, target):
    endtime = 0
    instruction = " "

    while instruction[0] != "S":
        Time = time.time()
        if endtime + 1 < Time:
            instruction = GetInstruction(RobotID, target)
            if instruction[0] in ["F", "L", "R", "S"]:
                if instruction[0] == "F":
                    endtime = Time + distances[int(instruction[-1:])] / 45
                elif instruction[0] != "S":
                    endtime = Time + angles[int(instruction[-1:])] / 25
                SendInstruction(RobotID, instruction)
            else:
                print(instruction)

# Init position
RobotID = 2
target = [0,500]

#print(GetPosition(RobotID))
SetPosition(RobotID, [500, 0, -90])
GuideTo(RobotID, target)
