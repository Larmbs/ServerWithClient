from dataclasses import dataclass
from file_manager import FileManager

CONVERSE_FILE = "Server/db/conversations.txt"
    
@dataclass
class Conversation:
    user1:str
    user2:str
    lenDialogue:int = 0 
    
    def length(self):
        return self.lenDialogue
    
    def __str__(self):
        return f"{self.user1}:{self.user2}"
    

def createConversation(user1:str, user2:str):
    talk = Conversation(user1, user2)
    manager = FileManager(CONVERSE_FILE)
    manager.append_line(str(talk), "0")
    manager.save()
    
def getConversation(user1:str, user2:str) -> str:
    talk = Conversation(user1, user2)
    manager = FileManager(CONVERSE_FILE)
    index, line = manager.get_line_of_header(str(talk))
    return line

def getConversationLength(user1:str, user2:str) -> int:
    index, line = getConversation(user1, user2)
    length_header = len(user1+":"+user2) + 2
    length = int(line[length_header:])
    print(length)
    return length
    
    

    
    

    

    