''' Module for the MemeSimCommand class. '''

class MemeSimCommand(object):

    ''' MemeSimCommand represents a command to be sent to the simulator '''

    CommandList = ['rq', 'mq', 'ip', 'pi', 'tm', 'pc', 'lc', 'ca', 'db']

    def __init__(self, cmdtype, cmdargs):
        if not cmdtype in MemeSimCommand.CommandList:
            raise Exception('Not a valid command type.')
        self._cmdtype = cmdtype
        self._cmdargs = cmdargs

    def asstring(self):
        ''' Return a string for the command to be sent on the TCP connection to the simulator. '''
        # turn all arguments into strings
        strargs = [str(a) for a in self._cmdargs]
        # return the result
        return self._cmdtype+'!'+ '!'.join(strargs)
        
    @staticmethod
    
    #define all commands (rq/mq/ip/pi/tm/pc/lc/ca/db/rs)
    def RQ(team_id, robot_id):
        return MemeSimCommand('rq', [team_id, robot_id])
    
    def MQ(team_id, robot_id, group_size):
        return MemeSimCommand('mq', [team_id, robot_id, group_size])

    def IP(team_id, robot_id, individualID):
        return MemeSimCommand('ip', [team_id, robot_id, individualID])

    def PI(team_id, robot_id, individualID):
        return MemeSimCommand('pi', [team_id, robot_id, individualID])

    def TM(team_id, robot_id, meme_genome, individualID):
        return MemeSimCommand('tm', [team_id, robot_id, meme_genome, individualID])

    def PC(team_id, robot_id, meme_name, meme_genome):
        return MemeSimCommand('pc', [team_id, robot_id, meme_name, meme_genome])

    def LC(team_id, robot_id, meme_name, budget):
        return MemeSimCommand('lc', [team_id, robot_id, meme_name, budget])

    def DB(team_id, debug_command):
        return MemeSimCommand('db', [team_id, debug_command])
    
    def RS(team_id, robot_id, x_pos, y_pos, angle):
        return MemeSimCommand('rs', [team_id, robot_id, x_pos, y_pos, angle])

    def CA(team_id):
        return MemeSimCommand('ca', [team_id])    