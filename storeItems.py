import sqlite3
import datetime

def newItem(itemName, description, username, image): #this will just allow the user to add a new item
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("INSERT INTO Items (name, description, username, datetime, finished) VALUES (:newName, :newDescription, :newUsername, :cDateTime, 0)", {"newDescription": description, "newName": itemName, "newUsername": username, "cDateTime": datetime.datetime.now()})
    SecondCursor = connection.execute("SELECT last_insert_rowid()") #learn sql command in https://alvinalexander.com/android/sqlite-autoincrement-insert-value-primary-key/
    primaryID = 0
    for row in SecondCursor:
        primaryID = row[0] #gets the primary key of the newly inserted item
    connection.commit()
    connection.close()
    image.save("static/itemImages/" + str(primaryID)) #image is going to be saved using the primary key

def item(ID): #this will get all the information on a specific item
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT * FROM Items WHERE ID=:pID", {"pID": ID}) #gets all the attributes of an item that has a specific primary key (which there can only be one in existence)
    rawResult = []
    for row in cursor:
        rawResult = row
    connection.close()
    if rawResult != []:
        result = {"ID": row[0],"name": row[1], "description": row[2], "username": row[3], "datetime": datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')} #formats the attributes of the item so that it is easier to read
        return result
    return None

def myItems(username): #this will retreive the items that a specific user is selling
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT * FROM Items WHERE username=:name", {"name": username}) #getting all items a specific username is selling
    result = []
    for row in cursor:
        result.append({"ID": row[0], "name": row[1], "description": row[2], "username": row[3], "datetime": datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')}) #this will store all the atributes of the objects returned
    connection.close()
    return result

def allItems(): #retreiving all the items that are being sold
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT * FROM Items")
    result = []
    for row in cursor:
        result.append({"ID": row[0], "name": row[1], "description": row[2], "username": row[3], "datetime": datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')}) #this will store all the atributes of the objects returned
    connection.close()
    return result

def openItems(): #retreiving all the items that are being sold
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT * FROM Items WHERE finished != 1")
    result = []
    for row in cursor:
        result.append({"ID": row[0], "name": row[1], "description": row[2], "username": row[3], "datetime": datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')}) #this will store all the atributes of the objects returned
    connection.close()
    return result

def closeItem(itemID): #this will just allow the user to add a new item
    connection = sqlite3.connect("AuctionDB.db")
    connection.execute("UPDATE Items SET finished=1 WHERE ID=:itemID", {"itemID": itemID})
    connection.commit()
    connection.close()

def dueClose(): #finds the bids that needs to be closed
    openI = openItems()
    now = datetime.datetime.now()
    array = []
    for i in range(0,len(openI)):
        if openI[i]["datetime"] + datetime.timedelta(days=14) < now: #add 14 days since there is a hard set time period where auctions last 2 weeks
            closeItem(openI[i]["ID"])
            array.append(openI[i])
    return array


if __name__ == "__main__":
    print(openItems()) #testing functions