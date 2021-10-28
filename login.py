def login(username, password):
    usernames = ["Ben"] #just temporary, will be changed so that it is in sql and also passwords will be more secured
    passwords = ["pass"]
    for i in range(0,len(usernames)):
        if username == usernames[i] and password == passwords[i]:
            return True

    return False