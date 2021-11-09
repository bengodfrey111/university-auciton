import sqlite3
import datetime

def newItem(itemName, description, username, image): #this will just allow the user to add a new item
    connection = sqlite3.connect("AuctionDB")
    cursor = connection.execute("INSERT INTO Items (name, description, username, datetime) VALUES (:newName, :newDescription, :newUsername, :cDateTime)", {"newDescription": description, "newName": itemName, "newUsername": username, "cDateTime": datetime.datetime.now()})
    SecondCursor = connection.execute("SELECT last_insert_rowid()") #learn sql command in https://alvinalexander.com/android/sqlite-autoincrement-insert-value-primary-key/
    primaryID = 0
    for row in SecondCursor:
        primaryID = row[0]
    connection.commit()
    connection.close()
    image.save("static/itemImages/" + str(primaryID)) #image is going to be saved using the primary key

def item(ID): #this will get all the information on a specific item
    connection = sqlite3.connect("AuctionDB")
    cursor = connection.execute("SELECT * FROM Items WHERE ID=:pID", {"pID": ID}) #gets all the attributes of an item that has a specific primary key (which there can only be one in existence)
    rawResult = []
    for row in cursor:
        rawResult = row
    connection.close()
    if rawResult != []:
        result = {"name": row[1], "description": row[2], "username": row[3], "datetime": datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')} #formats the attributes of the item so that it is easier to read
        return result
    return None

if __name__ == "__main__":
    print(item(2))