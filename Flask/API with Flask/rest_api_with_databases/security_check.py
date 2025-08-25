from user import User

users = [User(1, 'Abhishek', 'mypassword'),
         User(2, 'Lucky', 'secret')] 

# dictionary comprehension, maps usernames to user objects
username_table = {u.username : u for u in users}    # {'Abhishek' : User(1, 'Abhishek', 'mypassword')}
userid_table = {u.id : u for u in users}

def authenticate(username, password):
    # Checks if any user is present with the provieded username
    # If yes, return the username

    user = username_table.get(username, None)   # If didn't get anything relevant, return None; username_table[username] would throw error if nothing relevant is found
    if user and password == user.password:
        return user
    return None
    
def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)