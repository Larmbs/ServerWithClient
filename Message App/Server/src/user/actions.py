from src.user.user import User, isValid, PASS_INFO, USER_INFO, user_exsists
import json
from src.dbHandler.passwords import get_users

"""Collection of responses to commands"""
def ping_back(data:str, addr:str) -> str:
    return "pr;pingback"

def create_user(data:str, addr:str) -> str:
    data =  data[:-1]
    user_data:dict = json.loads("{" + data + "}")
    new_user = User(*user_data.values())
    result = isValid(new_user)
    if result[0]:
        new_user.save()
    return "i;" + result[1]

def get_user_names(data:str, addr:str) -> str:
    users:list = get_users()
    if data == "":
        if len(users) > 0:
            return "i;" + str(users)
        return "i;no users"
    else:
        split = data.split(";")
        if split[0] == "msglen":
            return "5"
        elif split[0] == "exsists":
            return str(user_exsists(split[1]))
        else:
            return "what"

def help_info(data:str, addr:str) -> str:
    match data:
        case "pass;":
            return PASS_INFO
        case "newUser;":
            return USER_INFO
        case "all;":
            return "all help commands and syntax"
        case _:
            return "Help command does not exsist"
        
