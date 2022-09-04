from copy import copy


import copy


class Command :
    def __init__(self, cmd, data):
        self.cmd = cmd  # command
        self.payload = copy.deepcopy(data) # data as bytes
        
    
