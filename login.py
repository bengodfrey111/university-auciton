import sqlite3

def login(username, password): #will give true of false depending if user details are correct
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT * FROM Users WHERE username=:givenName AND password=:givenPassword", {"givenName": username, "givenPassword": password}) #sql parameters prevent sql injection attacks, learnt how to implement parametrs in python using https://docs.python.org/3/library/sqlite3.html
    result = False
    for row in cursor:
        result =  True #this is if it returns anything, therefore an account exists with the same username and password where there can only be one since it won't allow two accounts with the exact same credentials or even the same username
    connection.close()
    return result #will return result, if sql return anything then true but if sql returns nothing then false

def accountExists(username): #checks if an account with a username exists (similar to checking if login is the same with identical logic)
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT username FROM Users WHERE username=:givenName", {"givenName": username})
    result = False
    for row in cursor:
        result = True
    connection.close()
    return result

def newAccount(username, password):
    connection = sqlite3.connect("AuctionDB.db")
    accountExist = accountExists(username)
    if not(accountExist): #checks if the account exists or not before creating the account
        cursor = connection.execute("INSERT INTO Users (username, password) VALUES (:newUsername, :newPassword)", {"newUsername": username, "newPassword": password}) #adds the new account to the database
        connection.commit()
        connection.close()
    return accountExist #return if the account exists or not


if __name__ == "__main__":
    print(accountExists("Ben2"))
    #print(login("Ben2", "pass2"))