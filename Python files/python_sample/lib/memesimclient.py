''' MemeSim Client takes care of TCP communication'''

import socket
from lib.memesimresponse import MemeSimResponse

class MemeSimClient(object):

    ''' MemeSimClient takes care of the TCP comunication to the simulator. '''

    MEMESIMPORTBASE = 7810

    EOL = '\r\n'

    # maximum input to buffer
    BufferSize = 2048

    def __init__(self, memesim_ipaddress, teamnumber):
        self._memesimip = memesim_ipaddress
        self._portnr = teamnumber + MemeSimClient.MEMESIMPORTBASE
        self._sock = None
        self._inputbuffer = ''

    def connect(self):
        ''' Connect to the server. '''
        # Create a TCP/IP socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        memesim_addr = (self._memesimip, self._portnr)
        print("MemSimClient is connecting to {0} port {1}".format(memesim_addr[0], memesim_addr[1]))
        self._sock.connect(memesim_addr)
        self._sock.setblocking(False)

    def _send(self, data):
        ''' Send data on the connection. '''

        if self._sock is None:
            raise Exception('Client is not connected.')

        self._sock.send(data.encode())

    def send_command(self, cmd):
        ''' Send data on the connection. '''

        self._send(cmd.asstring() + MemeSimClient.EOL)

    def _receive(self):

        if self._sock is None:
            raise Exception('Client is not connected.')

        # process new incoming data
        try:
            self._inputbuffer += self._sock.recv(MemeSimClient.BufferSize - len(self._inputbuffer)).decode('utf-8')
        except BlockingIOError:
            # there was no new data
            return


    def new_responses(self):
        ' Get the new responses in the input buffer '
        self._receive()
        res, self._inputbuffer = MemeSimResponse.extract_responses(self._inputbuffer)
        return res
