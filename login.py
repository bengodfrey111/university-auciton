import sqlite3

def login(username, password): #will give true of false depending if user details are correct
    connection = sqlite3.connect("AuctionDB")
    cursor = connection.execute("SELECT * FROM Users WHERE username=:givenName AND password=:givenPassword", {"givenName": username, "givenPassword": password}) #sql parameters prevent sql injection attacks, learnt how to implement parametrs in python using https://docs.python.org/3/library/sqlite3.html
    for row in cursor:
        return True #this is if it returns anything, therefore an account exists with the same username and password where there can only be one since it won't allow two accounts with the exact same credentials or even the same username
    return False #returns if nothing found in sql server since account wouldn't exist or they typed the wrong password