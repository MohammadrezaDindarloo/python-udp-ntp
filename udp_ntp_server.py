import serial
import time
import struct
import threading
import time 
from src.utils import *

class udpNtpServer():
    '''A class that implements an NTP Server with serial interface. This has been tested with SiK serial radio modules'''
    
    def __init__(self, local_port = 5000):
        '''
        The constructor of the UDP NTP Server class. With this, the NTP server starts
        @param: port:
        The port number to which the server will listen
        '''
        self.link = wifiDataLink(None, None, local_port)
        self.running = True
        self.receiveTread = threading.Thread(target=self.receivingThread, args=())
        self.receiveTread.start()
        
    def receivingThread(self):
        while self.running:
            data, addr = self.link.getData(8)
            self.link.remote_ip = addr[0]
            self.link.remote_port = addr[1]
            if len(data) == 8:
                #record the time of the recpetion of the request
                self.stamp2 = time.time_ns();
                self.stamp1 = int(struct.unpack('Q', data)[0])
                self.link.transmitData([self.stamp1, self.stamp2, time.time_ns()], format = 'Q')
                
    def serverStop(self):
        self.running = False
        self.receiveTread.join()
        self.link.in_socket.close()
        self.link.out_socket.close()
        
server = udpNtpServer()
