from passlib.apache import HtpasswdFile

FILE_NAME = "Server/db/user_passwords.txt"
    
def add_user(username, password):
    ht = HtpasswdFile(FILE_NAME)
    ht.set_password(username, password)
    ht.save()

def update_pass(username:str, password:str) -> None or str:
    ht = HtpasswdFile(FILE_NAME)
    if username in ht.users():
        ht.set_password(password)
        ht.save()
    return "Error: user does not exsist"
    
def check_password(username:str, entered_password:str) -> tuple[bool, str]: #Bool if it worked Str for error message
    ht = HtpasswdFile(FILE_NAME)
    if username in ht.users():
        return ht.check_password(username, entered_password)
    return False, "Error: user does not exsist"

def check_if_user_is_new(username):
    users = get_users()
    return username not in users

def user_exsists(username):
    users = get_users()
    return username in users
        
def get_users() -> list[str]:
    ht = HtpasswdFile(FILE_NAME)
    return ht.users()
    