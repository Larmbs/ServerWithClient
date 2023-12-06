#import funcs
from abc import ABC, abstractmethod

"""
message
"""

"""Available commands that the user can go through and activate in the udp domain"""
DIR_UDP = {
}

"""Available commands that the user can go through and activate in the udp domain"""
DIR_TCP = {  
}

Address_Type = tuple[str, int]

"""Request base class handles server requests"""
class Request(ABC):
    def __init__(self, message, addr, data):
        self.message:str = message
        self.addr:Address_Type = addr
        self.data = data
    
    @abstractmethod
    def response(self):
        """Returns the response to the message"""

"""UDP version of request"""
class UDPRequest(Request):
    def response(self):
        split = self.message.split(";", 1)
        value = DIR_UDP.get(split[0], None)
        if value is None:
            return "Invalid"
        return value(split[1], self.addr, self.data)

"""TCP version of request"""
class TCPRequest(Request):
    def response(self):
        split = self.message.split(";", 1)
        value = DIR_TCP.get(split[0], None)
        if value is None:
            return "Invalid"
        return value(split[1], self.addr, self.data)
    