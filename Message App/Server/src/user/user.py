from dataclasses import dataclass
from src.dbHandler.passwords import add_user, check_if_user_is_new, user_exsists
from password_validator import PasswordValidator

USER_INFO = """
User info must be in the form of a json object
"name":username, "password":password"
remove curly brakets from dict to be accepted
"""

@dataclass    
class User:
    name:str
    password:str
    
    def save(self):
        add_user(self.name, self.password)


def isValid(user:User) -> tuple[bool, str]:
    comment = ''
    failed = False
    if not isValidPassword(user.password):
        comment += "Password must meet proper standars h;passFormat for info   "
        failed = True
    if not check_if_user_is_new(user.name):
        comment += "User name already taken h;userCreate"
        failed = True
    if not isValidUserName(user.name):
        comment += "User name does not follow criteria h;userFormat   "
        failed = True
        
    if failed:
        return (False, comment)
    return (True, "success")
    
PASS_INFO = """
Password must fall into this criteria
min len = 5
max len = 100
must have a upper case letter, lower case letter, a digit
must not have spaces
""" 

ValidUserNameChecker = PasswordValidator()
ValidUserNameChecker.min(5)\
    .max(100)\
    .has().no().spaces()
    
ValidPassChecker = PasswordValidator()
ValidPassChecker\
    .min(5)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().no().spaces()
    
def isValidPassword(password:str) -> bool:
    """Checks for proper password security"""
    return ValidPassChecker(password)

def isValidUserName(userName:str) -> bool:
    """Checks for proper username security"""
    return ValidUserNameChecker(userName)

def sendMessage(message:str, recipient:str) -> None:
    pass
   

    
    
    