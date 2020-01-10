from time import sleep

# import code that is used
from lib.memegenome import MemeGenome
from lib.memesimcommand import MemeSimCommand
from lib.memesimresponse import MemeSimResponse
from lib.memesimclient import MemeSimClient
from averageString import getAverage
# Global variables/constants that can be accessed from all functions should be defined below

# set the simulator IP address
MEMESIM_IP_ADDR = "131.155.127.244"

# set the team number here
TEAM_NUMBER = 8

# create a MemeSimClient object that takes car of all TCP communication with the simulator
MEMESIM_CLIENT = MemeSimClient(MEMESIM_IP_ADDR, TEAM_NUMBER)

# dictionary to hold a collection of memes
MY_MEMES = dict()

sleep_length = 2.0

CityIDGen = [[1, '1199037', 'GCTGGTCTCTGTAATTAGCGTTATTCGTTTAACCCGTTTGAAATATCGGTGGCAAGATAGAGCCCCTGAGGGGGAGACCAATGCGCACTAAACCCGCCAA'], [1, '1199287', 'GCTTTAATGAGAGAGGTGCGTAACTCTGCAAGGGGTTCAAAATCCTTGGTGCTATTAGATCAGCTAGAAAAGGGGGTCAAAAACCCAAAGCGCACCTCAT']]

city = 1

# the setup function is called once at startup
# you can put initialization code here
def setup():

    # create a collection of random memes
    for i in range(0, 10):
        mg = MemeGenome.random_meme_genome()
        mg[0] = 'A'
        mg[99] = mg[0]
        MY_MEMES['Meme'+str(i)] = mg


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
#            print(CityIDGen)   
    print("Received response: " + str(resp))

# this function is called over and over again
def loop():
    global CityIDGen
    global city
    error = 0
    print("What do you want to do? (rq/mq/ip/pi/tm/pc/lc/ca/db/rs/q/print_ind)")
    command = input()
    if command == "rq":
        print("location of which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14   
        RQ1 = MemeSimCommand.RQ(8, robotID)        
    elif command == "mq": # need to store city number
        print("Query with which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14   
        print("For what group size?")
        group_size = int(input())
        RQ1 = MemeSimCommand.MQ(8, robotID, group_size)
    elif command == "ip":
        print("Interview person with which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14   
        print("Which person do you want to interview?")
        individualID = int(float(input()))
        RQ1 = MemeSimCommand.IP(8, robotID, individualID)                   
    elif command == "pi": # need to store city number
        print("Process interview with which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14   
        print("Which person was interviewed?")
        individualID = input()
        RQ1 = MemeSimCommand.PI(8, robotID, individualID)                    
    elif command == "tm":
        print("Test meme with which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14   
        print("What is the genome of the meme you want to test?")
        meme_genome = input()        
        print("Which person do you want to test on?")
        individualID = input()        
        RQ1 = MemeSimCommand.TM(8, robotID, meme_genome, individualID)                   
    elif command == "pc":
        print("Process campaign with which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14   
        print("What do you want to call the meme?")
        meme_name = input()
        print("What is the genome of the meme?")
        meme_genome = input()         
        RQ1 = MemeSimCommand.PC(8, robotID, meme_name, meme_genome)
    elif command == "lc":
        print("Launch campain with which robot? 1(henk)/2(ingrid)")
        robotID = int(input())+14
        print("What meme do you want to launch?") #optie voor later: print lijst met alle memes
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
        robotID = int(input())+14
        print("At which x_position? (in mm)")
        x_pos = input()
        print("At which y_position? (in mm)")
        y_pos = input()
        print("At what angle?")
        angle = input()
        RQ1 = MemeSimCommand.RS(8,robotID,x_pos,y_pos,angle)
    elif command == "q":
        exit()
    elif command == "print_ind":
        print(CityIDGen)
        error = 1
    elif command == "litt":
        print("Geef input")
        testcmd = input()
        exec(testcmd)
        error = 1
    elif command == "dump":
        print("Printing meme genome")
        error = 1

    elif command == "avg":
        print("Welke stad?")
        citynr = int(input())
        genomes_to_send = []
        for i in range(len(CityIDGen)):
            if CityIDGen[i][0] == citynr:
                genomes_to_send += [CityIDGen[i][2]]
        print(genomes_to_send)
        averageGenome = getAverage(genomes_to_send)
        print(averageGenome)
        error = 1
    else:
        print("error")
        error = 1                
    
    # do something arbitray with the memes
    if error == 0:
        MEMESIM_CLIENT.send_command(RQ1)


# call the setup function for initialization
setup()

while True:
    # get new responses
    RESPONSES = MEMESIM_CLIENT.new_responses()
    # process new responses
    for r in RESPONSES:
        process_response(r)

    # call the loop function
    loop()
    # slow the loop down

    sleep(sleep_length)
