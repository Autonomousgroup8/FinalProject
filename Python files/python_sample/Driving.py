import math as math
import time
from lib.memesimcommand import MemeSimCommand
from lib.memesimclient import MemeSimClient
from zigbee import Zigbee
import Locations
sign = lambda x: math.copysign(1, x)

angle_tolerance = 4
distance_tolerance = 80
angles = [2, 5, 10, 15, 20, 30, 45, 90, 135, 180]
distances = [20, 50, 100, 150, 200, 300, 400, 500, 750, 1000]
angle_endtime = [0.025, 0.05, 0.1, 0.15, 0.25, 0.35, 0.5, 1.0, 1.5, 2.0]
distance_endtime = [0.2, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 7.5, 10.0]

# Server connection setup
MEMESIM_IP_ADDR = "131.155.127.244"
TEAM_NUMBER = 8
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)
MEMESIM_CLIENT.connect()
print(" ")

# Connect Zigbee
ZIGBEE = Zigbee('COM20', 9600)

def GetPosition(robotID):
    RQ = MemeSimCommand.RQ(8, robotID+14)
    MEMESIM_CLIENT.send_command(RQ)

    time.sleep(1.0)

    RESPONSES = MEMESIM_CLIENT.new_responses()

    for resp in RESPONSES:
        if resp.cmdtype() == 'rq':
            if not resp.iserror():
                xpos = int(float(resp.cmdargs()[2]))
                ypos = int(float(resp.cmdargs()[3]))
                angle = round(math.degrees(float(resp.cmdargs()[4])))

                if abs(angle) > 180:
                    angle = angle - sign(angle) * 360

                return [xpos, ypos], angle
    return

def GetInstruction(RobotID, target):
    try:
        rob_pos, rob_angle = GetPosition(RobotID)
        print(f"Robot position: [{round(rob_pos[0], 1)}, {round(rob_pos[1], 1)}], {round(rob_angle, 1)}")
    except:
        return "ERROR: No Position"

    tar_angle = round(math.degrees(math.atan2(target[1] - rob_pos[1], target[0] - rob_pos[0]))) - rob_angle
    if abs(tar_angle) > 180:
        tar_angle = tar_angle - sign(tar_angle)*360

    tar_distance = math.sqrt((target[1] - rob_pos[1])**2 + (target[0] - rob_pos[0])**2)

    print(f"Target angle = {tar_angle}, Target distance = {tar_distance}")

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
    print(f"Send Instruction: 1{ReveiverID}{instruction}\n")
    #ZIGBEE.write(bytes(f"Send Instruction: 1{ReveiverID}{instruction}", 'utf-8'))
    ZIGBEE.write(bytes("1" + str(ReveiverID) + instruction, 'utf-8'))

def GuideTo(RobotID, target):
    endtime = 0
    instruction = " "

    while instruction[0] != "S":
        Time = time.time()
        if endtime + 1 < Time:
            instruction = GetInstruction(RobotID, target)
            if instruction[0] in ["F", "L", "R", "S"]:
                if instruction[0] == "F":
                    endtime = Time + distance_endtime[int(instruction[1])]
                elif instruction[0] != "S":
                    endtime = Time + angle_endtime[int(instruction[1])]*1.5
                SendInstruction(RobotID, instruction)
                SendInstruction(RobotID, instruction)
                SendInstruction(RobotID, instruction)
            elif instruction == "ERROR: No Position":
                SendInstruction(RobotID, "F2")
                print(f"{instruction}, Tunnel, forward 5 cm")
            else:
                print(instruction)

# Init position
RobotID = 2
target = Locations.Lab8

print(GetPosition(RobotID))

#GuideTo(RobotID, target)