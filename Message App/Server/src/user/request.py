import src.user.actions as actions
from abc import ABC, abstractmethod

"""
The server takes request calls with a certain message fromat
The message is broken up by semi colons (;) and these semi colons determine what are the commands entered

FirstDIR;SECOUNDDIR;DATA

It is orginized in a directory setup and then finally at the end data so there is some orginization to it

Here are two special commands both user and client will share
i; will just ignore the message
p; ping back from server
"""

"""Available commands that the user can go through and activate in the udp domain"""
DIR_UDP = {
    "i": None, ##Ignore
    "p":actions.ping_back, ##Send a ping back
}

"""Available commands that the user can go through and activate in the udp domain"""
DIR_TCP = {  
    "info": None, ##Ignore Info on wrong message or other information
    "ping":actions.ping_back,
    "createUser":actions.create_user,
    "getUser":actions.get_user_names,
    "help":actions.help_info,
    "-h":actions.help_info,
    "gcd":actions
}

Address_Type = tuple[str, int]


def check_format(message:str, DIR:dict) -> tuple[bool, str]:
    if not message.endswith(";"):
        return False, "Wrong ; foramting: message must end with ;"
    split = message.split(";")
    if split[0] not in DIR.keys():
        return False, "Directroy does not exsist"
    return True, "success"

def clean_message(message:str):
    message = message.strip(" ")
    message = message.lower()
    if not message.endswith(";"):
        message += ";"
    return message
    
        
"""Request base class to handle client queries and return the appropriate server response"""
class Request(ABC):
    def __init__(self, message:str, addr:Address_Type):
        self.message:str = message
        self.addr:Address_Type = addr
        self.data = {}
    
    @abstractmethod
    def response(self) -> str:
        """Returns the response to the message"""

"""UDP version of request"""
class UDPRequest(Request):
    def response(self) -> str:
        split = self.message.split(";", 1)
        if type(split) != list:
            return "Invalid"
        value = DIR_UDP.get(split[0], None)
        
        if len(split) == 1:
            split.append("")
            
        if value is None:
            return "Invalid"
        return value(split[1], self.addr, self.data)

"""TCP version of request"""
class TCPRequest(Request):
    def response(self) -> str:
        message = clean_message(self.message)
        print(f"msg(ip:{self.addr[0]}, p:{self.addr[1]}): {message}")
        check = check_format(message, DIR_TCP)
        if check[0] == False:
            return check[1]
        
        split = message.split(";", 1)
        
        value = DIR_TCP.get(split[0], None)
        if len(split) == 1:
            split.append("")
        return value(split[1], self.addr)
    