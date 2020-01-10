import math as math
from time import sleep
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
from averageString import getAverage
#from zigbee import Zigbee
import Locations

angle_tolerance = 2
distance_tolerance = 10
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
#ZIGBEE = Zigbee('COM20', 9600)

def GetPosition(robotID):
    RQ = MemeSimCommand.RQ(8, robotID+14)
    MEMESIM_CLIENT.send_command(RQ)

    sleep(2.0)

    RESPONSES = MEMESIM_CLIENT.new_responses()

    for resp in RESPONSES:
        if resp.cmdtype() == 'rq':
            if not resp.iserror():
                xpos = int(float(resp.cmdargs()[2]))
                ypos = int(float(resp.cmdargs()[3]))
                angle = int(float(resp.cmdargs()[4]))
                return [xpos, ypos], angle
    return

def GetPos():
    global angle, pos

    angle = round(angle,1)

    if angle > 180:
        angle = angle-360

    return pos, angle

def GetInstruction(RobotID, target):
    try:
        #rob_pos, rob_angle = GetPos()
        rob_pos, rob_angle = GetPosition(RobotID)
    except:
        return "NULL"

    tar_angle = math.degrees(math.atan2(target[1] - rob_pos[1], target[0] - rob_pos[0])) - rob_angle
    tar_distance = math.sqrt((target[1] - rob_pos[1])**2 + (target[0] - rob_pos[0])**2)

    if tar_distance > distance_tolerance:
        if abs(tar_angle) > angle_tolerance:
            if tar_angle < 0:
                i = 0
                while angles[min(i+1,9)] <= abs(tar_angle) and i < 9:
                    i = i + 1
                return "R" + str(i)
            elif tar_angle > 0:
                i = 0
                while angles[min(i+1,9)] <= abs(tar_angle) and i < 9:
                    i = i + 1
                return "L" + str(i)
        elif tar_distance > distance_tolerance:
            i = 0
            while distances[min(i+1,9)] <= abs(tar_distance) and i < 9:
                i = i + 1
            return "F" + str(i)
    else:
        return "S"
    return "NULL"

def SendInstruction(RobotID, instruction):
    ReveiverID = [5, 6][RobotID-1]
    print("Send Instruction: " + "1" + str(ReveiverID) + instruction)
   # ZIGBEE.write(bytes("1" + str(ReveiverID) + instruction, 'utf-8'))

def GuideTo(RobotID, target):
    global angle, pos ### MOVE SIMULATOR PARAM ###

    time = 0
    endtime = 0
    instruction = " "

    while instruction[0] != "S":
        if endtime + 1 < time:
            print([round(pos[0], 1), round(pos[1], 1)], round(angle, 1))
            instruction = GetInstruction(RobotID, target)
            if instruction != "NULL":
                if instruction[0] == "F":
                    endtime = time + distances[int(instruction[-1:])] / 10
                elif instruction[0] != "S":
                    endtime = time + angles[int(instruction[-1:])] / 10
                SendInstruction(RobotID, instruction)
            else:
                print("Error retrieving instruction")

        ### MOVE SIMULATOR ###
        if endtime > time:
            if instruction[0] == "F":
                x = pos[0] + math.cos(math.radians(angle)) * speed
                y = pos[1] + math.sin(math.radians(angle)) * speed
                pos = [x, y]
            elif instruction[0] == "L":
                angle = angle + speed
                if angle > 180:
                    angle = angle - 360

            elif instruction[0] == "R":
                angle = angle - speed
                if angle < -180:
                    angle = angle + 360

        time = time + delta_t

# Init position
RobotID = 1
pos = [0, 0]
angle = 0

#target = [math.sqrt(0.5*1000**2) , math.sqrt(0.5*1000**2) ]
target = [1000, 200]

# try:
#     rob_pos, rob_angle = GetPosition(RobotID)
# except:
#     print("error")

#SendInstruction(1, "F0")

#GuideTo(RobotID, target)

print(Locations.Lab8)