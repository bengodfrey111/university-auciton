import sqlite3

def login(username, password): #will give true of false depending if user details are correct
    connection = sqlite3.connect("AuctionDB")
    cursor = connection.execute("SELECT * FROM Users WHERE username=:givenName AND password=:givenPassword", {"givenName": username, "givenPassword": password}) #sql parameters prevent sql injection attacks, learnt how to implement parametrs in python using https://docs.python.org/3/library/sqlite3.html
    for row in cursor:
        return True
    return False