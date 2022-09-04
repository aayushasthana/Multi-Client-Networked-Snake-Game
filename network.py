
import socket
import pickle
from gameconfiguration import *
from command import *


import globals


class Network:
    def __init__(self, sock, server, port):
        self.sock = sock
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)

        


    def connect(self):
        try:
            globals.debug_obj.info("Connecting to Server {}".format(SERVER))
            self.sock.connect(self.addr)
            globals.debug_obj.info("Connected to Server {}".format(SERVER))
        except socket.error as e:
            
            print(e)

    def close(self):
        self.sock.close()

    def send_text(self, s):
        try:
            
            self.sock.send(str.encode(s))
        except socket.error as e:
            
            print(e)
    
    def recv_text(self):
        try:
            
            return self.sock.recv(2048).decode()
        except socket.error as e:
            
            print(e)


    def send_cmd(self, cmd):
        try:
            
            
            self.send_data(pickle.dumps(cmd))
            
        except socket.error as e:
            
            print(e)

    def send_data(self,data):
        try:
            
            self.sock.send(data)
        except socket.error as e:
            
            print(e)


    def recv_cmd(self):
        try:
            
            data = self.sock.recv(2048*10)
            if not data:
                
                return Command(NO_DATA,b" ")
            cmd = pickle.loads(data)
            return Command(cmd.cmd, cmd.payload)
        except socket.error as e:
            
            print(e)


    

    
        
    





