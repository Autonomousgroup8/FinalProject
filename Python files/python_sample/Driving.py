import math as math
from time import sleep
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
from averageString import getAverage

angle_tolerance = 2
distance_tolerance = 10
angles = [2, 5, 10, 15, 20, 30, 45, 90, 135, 180]
distances = [20, 50, 100, 150, 200, 300, 400, 500, 750, 1000]

#MOVE SIM PARAM
delta_t = 0.001
speed = 10*delta_t

# set the simulator IP address
MEMESIM_IP_ADDR = "131.155.127.244"

# set the team number here
TEAM_NUMBER = 8

# create a MemeSimClient object that takes car of all TCP communication with the simulator
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)

# connect to the simulator
MEMESIM_CLIENT.connect()

def GetPosition(robotID):
    RQ = MemeSimCommand.RQ(8, robotID+14)
    MEMESIM_CLIENT.send_command(RQ)

    sleep(2.0)

    resp = MEMESIM_CLIENT.new_responses()[0]

    if resp.cmdtype() == 'rq':
        if not resp.iserror():
            xpos = int(float(resp.cmdargs()[2]))
            ypos = int(float(resp.cmdargs()[3]))
            angle = int(float(resp.cmdargs()[4]))
            return [xpos, ypos], angle

    return "Error"

def GetPos():
    global angle, pos

    angle = round(angle,1)

    if angle > 180:
        angle = angle-360

    return pos, angle

def GetInstruction(RobotID, target):
    rob_pos, rob_angle = GetPos()
    #rob_pos, rob_angle = GetPosition(RobotID)

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
    print("Send Instruction: " + str(RobotID) + instruction)

def GuideTo(RobotID, target):
    global angle, pos ### MOVE SIMULATOR PARAM ###

    time = 0
    endtime = 0
    instruction = " "

    while instruction[0] != "S":
        if endtime + 1 < time:
            print([round(pos[0], 1), round(pos[1], 1)], round(angle, 1))
            instruction = GetInstruction(RobotID, target)
            if instruction[0] == "F":
                endtime = time + distances[int(instruction[-1:])] / 10
            elif instruction[0] != "S":
                endtime = time + angles[int(instruction[-1:])] / 10
            SendInstruction(RobotID, instruction)

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

print(GetPosition(1))

#GuideTo(RobotID, target)
