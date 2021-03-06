from time import sleep
useZig = False
if not useZig:
    print("Caution! Zigbee is not turned on!")

import msvcrt
# import code that is used
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
from WriteGenome import *
from averageString import getAverage
from genomeprotocol import genome_protocol
if useZig:
    from Driving import *
#from Locations import *

locDict = {
"Lab" : [147, 1315],
"Funnel1" : [1403, 736],
"Funnel2" : [2130, 782],
"Funnel3" : [2735, 1401],
"Funnel4" : [2762, 2166],
"Funnel5" : [2030, 2669],
"Funnel6" : [1484, 2831],
"Funnel7" : [762, 2121],
"Funnel8" : [808, 1414],
"C01" : [2546, 262],
"C02" : [3275, 250],
"C03" : [3269, 964],
"C04" : [2250, 1270],
"C05" : [3256, 2553],
"C06" : [3244, 3242],
"C07" : [2547, 3250],
"C08" : [2250, 2250],
"C09" : [950, 3250],
"C10" : [250, 3250],
"C11" : [250, 2550],
"C12" : [1250, 2250],
"MiddleLabland" : [750, 750],
"MiddleEurope" : [2750, 750],
"MiddleAfrica" : [2750, 2750],
"MiddleAmerica" : [750, 2750]}

# Global variables/constants that can be accessed from all functions should be defined below

# set the simulator IP address
MEMESIM_IP_ADDR = "131.155.127.244"

# set the team number here
TEAM_NUMBER = 8

# create a MemeSimClient object that takes car of all TCP communication with the simulator
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)

# dictionary to hold a collection of memes
MY_MEMES = ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"]

sleep_length = 2.0

CityIDGen = []
CityID = []
city = 1

tr1 = "Lab"
tr2 = "Lab"

# the setup function is called once at startup
# you can put initialization code here
def setup():
    #    # create a collection of random memes
    #    for i in range(0, 10):
    #        mg = MemeGenome.random_meme_genome()
    #        mg[0] = 'A'
    #        mg[99] = mg[0]
    #        MY_MEMES['Meme'+str(i)] = mg

    # connect to the simulator
    MEMESIM_CLIENT.connect()


# the process_response function is called when a response is received from the simulator
def process_response(resp):
    if resp.cmdtype() == 'rq':
        if not resp.iserror():
            robot_id = int(float(resp.cmdargs()[1]))
            xpos = int(float(resp.cmdargs()[2]))
            ypos = int(float(resp.cmdargs()[3]))
            angle = int(float(resp.cmdargs()[4]))
            location_robot = [xpos, ypos, angle]
            print(location_robot)
    if resp.cmdtype() == 'pi':
        if not resp.iserror():
            global CityIDGen
            robot_id = int(float(resp.cmdargs()[1]))
            individualID_genome = resp.cmdargs()[2]
            individualID = individualID_genome[0]
            genome = individualID_genome[1]
            CityIDGen += [[city, individualID, genome]]
    if resp.cmdtype() == 'mq':
        if not resp.iserror():
            global CityID
            individualID = []
            robot_id = int(float(resp.cmdargs()[1]))
            group_size = int(float(resp.cmdargs()[2]))
            for i in range(group_size):
                if isinstance(resp.cmdargs()[i + 3], list):
                    individualID += [resp.cmdargs()[i + 3][0]]
                else:
                    individualID += [resp.cmdargs()[i + 3]]
                CityID += [[city, individualID[i]]]
                RQ1 = MemeSimCommand.IP(8, robot_id, individualID[i])
                MEMESIM_CLIENT.send_command(RQ1)
            print(CityID)
        #            print(CityIDGen)
    print("Received response: " + str(resp))


def genmeme(robotID, memename, protocol):
    global CityIDGen
    global CityID
    global city
    global MY_MEMES
    for i in range(len(CityID)):
        RQ1 = MemeSimCommand.PI(8, robotID, CityID[i][1])
        MEMESIM_CLIENT.send_command(RQ1)
    sleep(sleep_length)  # wait for responses
    RESPONSES = MEMESIM_CLIENT.new_responses()
    # process new responses
    for r in RESPONSES:
        process_response(r)
    genomes_to_send = []

    for i in range(len(CityIDGen)):
        if CityIDGen[i][0] == city:
            genomes_to_send += [CityIDGen[i][2]]
    #    print(genomes_to_send)
    averageGenome = getAverage(genomes_to_send)
    #    print(averageGenome)
    MY_MEMES += [[memename, genome_protocol(protocol, averageGenome)]]
    print(MY_MEMES)


def genmemes(robotID, memename):
    global CityIDGen
    global CityID
    global city
    global MY_MEMES
    for i in range(len(CityID)):
        RQ1 = MemeSimCommand.PI(8, robotID, CityID[i][1])
        MEMESIM_CLIENT.send_command(RQ1)
    sleep(sleep_length)  # wait for responses
    RESPONSES = MEMESIM_CLIENT.new_responses()
    # process new responses
    for r in RESPONSES:
        process_response(r)
    genomes_to_send = []

    for i in range(len(CityIDGen)):
        if CityIDGen[i][0] == city:
            genomes_to_send += [CityIDGen[i][2]]
    #    print(genomes_to_send)
    averageGenome = getAverage(genomes_to_send)
    #    print(averageGenome)
    for i in range(4):
        MY_MEMES += [[memename + str(i + 1), genome_protocol(i + 1, averageGenome)]]
    print(MY_MEMES)


# this function is called over and over again
def loop():
    repeatCmd = False
    global tr2
    global tr1
    global CityIDGen
    global CityID
    global city
    global MY_MEMES
    error = 0

    print("What do you want to do? (rq/mqip/genmeme/genmemes/tm/pc/lc/ca/db/rs/quit/print_ind/litt/save/read/dest)")
    command = input()
    if "*" in command:
        command = command.replace("*","")
        repeatCmd = True

    if command == "rq":
        print("location of which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        RQ1 = MemeSimCommand.RQ(8, robotID)

    elif command == "mq":  # need to store city number
        print("Query with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("For what group size?")
        group_size = int(input())
        RQ1 = MemeSimCommand.MQ(8, robotID, group_size)

    elif command == "ip":
        print("Interview person with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("Which person do you want to interview?")
        individualID = int(float(input()))
        RQ1 = MemeSimCommand.IP(8, robotID, individualID)

    elif command == "mqip":  # need to store city number
        print("Query and interview with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("For what group size?")
        group_size = int(input())
        print("In which city are you?")
        city = int(input())
        RQ1 = MemeSimCommand.MQ(8, robotID, group_size)

    elif command == "pi":  # need to store city number
        print("Process interview with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("Which person was interviewed?")
        individualID = input()
        RQ1 = MemeSimCommand.PI(8, robotID, individualID)

    elif command == 'genmeme':
        print("Process interview with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("For which city do you want to generate a meme?")
        city = int(input())
        print("What do you want to call the meme?")
        memename = input()
        print("What protocol do you want to use?")
        protocol = int(input())
        genmeme(robotID, memename, protocol)
        error = 1

    elif command == 'genmemes':
        print("Process interview with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("For which city do you want to generate a meme?")
        city = int(input())
        print("What do you want to call the meme?")
        memename = input()
        genmemes(robotID, memename)
        error = 1
    #
    #    elif command == 'gm':
    #        print("For which city do you want to generate a meme?")
    #        citynr = int(input())
    #        print("What do you want to call the meme?")
    #        memename = input()
    #        print("What protocol do you want to use?")
    #        protocol = int(input())
    #        genomes_to_send = []
    #        for i in range(len(CityIDGen)):
    #            if CityIDGen[i][0] == citynr:
    #                genomes_to_send += [CityIDGen[i][2]]
    #        print(genomes_to_send)
    #        averageGenome = getAverage(genomes_to_send)
    #        print(averageGenome)
    #        MY_MEMES += genome_protocol(protocol, averageGenome)
    #        error = 1 bla

    elif command == "tm":
        found = False
        print("Test meme with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("Which meme?")
        meme_name = input()
        print("Which person do you want to test on?")
        individualID = input()
        for i in range(len(MY_MEMES)):
            if MY_MEMES[i][0] == meme_name:
                meme_genome = MY_MEMES[i][1]
                found = True;
        if found == True:
            RQ1 = MemeSimCommand.TM(8, robotID, meme_genome, individualID)
        else:
            print("That meme does not excist")
            error = 1;
        found = False;

    elif command == "pc":
        print("Process campaign with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("Which meme?")
        meme_name = input()
        for i in range(len(MY_MEMES)):
            if MY_MEMES[i][0] == meme_name:
                meme_genome = MY_MEMES[i][1]
                found = true;
        if found == true:
            RQ1 = MemeSimCommand.PC(8, robotID, meme_name, meme_genome)
        else:
            print("That meme does not excist")
            error = 1;
        found = false;

    elif command == "lc":
        print("Launch campaign with which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("What meme do you want to launch?")  # optie voor later: print lijst met alle memes
        meme_name = input()
        print("What is the budget?")
        budget = input()
        RQ1 = MemeSimCommand.LC(8, robotID, meme_name, budget)

    elif command == "ca":
        RQ1 = MemeSimCommand.CA(8)

    elif command == "db":
        print("What do you want to do? money/reset")
        debug_command = input()
        RQ1 = MemeSimCommand.DB(8, debug_command)

    elif command == "rs":
        print("Set location of which robot? 1(henk)/2(ingrid)")
        robotID = int(input()) + 14
        print("At which x_position? (in mm)")
        x_pos = input()
        print("At which y_position? (in mm)")
        y_pos = input()
        print("At what angle?")
        angle = input()
        RQ1 = MemeSimCommand.RS(8, robotID, x_pos, y_pos, angle)

    elif command == "quit":
        exit()

    elif command == "print_ind":
        print(CityIDGen)
        error = 1
    elif command == "litt":
        print("Geef input")
        testcmd = input()
        exec(testcmd)
        error = 1
    elif command == "save":
        print("Saving meme genome")
        write_genome(CityIDGen)
        error = 1
    elif command == "dest":
        print("Input destination 1")
        testTr = input()
        print("Input destination 2")
        testTr = input()
        error = 1
    elif command == "read":
        print("Reading meme genome")
        read_genome(CityIDGen)
        error = 1
    else:
        print("error")
        error = 1

        # do something arbitray with the memes
    if error == 0:
        MEMESIM_CLIENT.send_command(RQ1)

    if repeatCmd:
        sleep(sleep_length)
        RESPONSES = MEMESIM_CLIENT.new_responses()
        # process new responses
        for r in RESPONSES:
            process_response(r)
        loop()

# call the setup function for initialization
setup()

while True:
    # get new responses
    RESPONSES = MEMESIM_CLIENT.new_responses()
    # process new responses
    for r in RESPONSES:
        process_response(r)

    # call the loop function

    if msvcrt.kbhit():
        loop()

    else:
        print(locDict[tr1])
        print(locDict[tr2])
        if useZig:
            GuideTo(1, locDict[tr1])
            GuideTo(2, locDict[tr2])

    # slow the loop down

    sleep(sleep_length)