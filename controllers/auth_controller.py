from models.user import check_user

def login(username, password):
    return check_user(username, password)