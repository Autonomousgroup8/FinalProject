''' Module for the MemeSimResponse class. '''

import re

class MemeSimResponse(object):

    ''' MemeSimResponse represents a response from the simulator '''

    # regular expression for a response
    # this may look cryptic, but it is quite convenient
    ResponseRegEx = re.compile(r'([^!@]+)(\!([^!@]+(\@[^!@]+)*))*')

    def __init__(self, responsestr):
        match = MemeSimResponse.ResponseRegEx.search(responsestr)
        if match is None:
            raise Exception('There is no response in the data.')
        
        lev1args = match.group(0).split('!')

        # get the command type and remove from the list
        self._cmdtype = lev1args[0]
        lev1args.pop(0)

        # parse the arguments
        self._cmdargs = [a.split('@') for a in lev1args]
        self._cmdargs = [l[0] if len(l) == 1 else l for l in self._cmdargs]

    def cmdtype(self):
        ''' returns the command type of the response '''
        return self._cmdtype

    def cmdargs(self):
        ''' returns the arguments of the response '''
        return self._cmdargs

    def iserror(self):
        ''' check if the response is an error response. '''
        # check if the last argument returned is 'err'
        # negative indices count backward from the end, so -1 returns the last element
        return  self._cmdargs[-1] == 'err'

    @staticmethod
    def extract_responses(inputdata):
        ''' Convert the input from the string input data into a list of separate responses. Returns a pair consisting of the list of responses and the remaining input data that could not be further processed.
        It may contain partial responses that will be completed with more incoming data. '''
        result = list()
        pos = inputdata.find('\n')
        while pos != -1:
            resp = inputdata[0:pos].strip()
            inputdata = inputdata[pos+1:]
            result.append(MemeSimResponse(resp))
            pos = inputdata.find('\n')
        return result, inputdata

    def asstring(self):
        ''' Return a representation of the resonse as a string. '''
        result = self._cmdtype+'!'
        args = ['@'.join(a) if isinstance(a, list) else a for a in self._cmdargs]
        result += '!'.join(args)
        return result

    # create a textual representation of the MemeGenome as a string
    def __repr__(self):
        return "Response({0})".format(self.asstring())

    # create a textual representation of the MemeGenome as a string
    def __str__(self):
        return self.__repr__()
