import sqlite3

def newItem(itemName, description, username, image): #this will just allow the user to add a new item
    connection = sqlite3.connect("AuctionDB")
    cursor = connection.execute("INSERT INTO Items (name, description, username) VALUES (:newName, :newDescription, :newUsername)", {"newDescription": description, "newName": itemName, "newUsername": username})
    SecondCursor = connection.execute("SELECT last_insert_rowid()") #learn sql command in https://alvinalexander.com/android/sqlite-autoincrement-insert-value-primary-key/
    primaryID = 0
    for row in SecondCursor:
        primaryID = row[0]
    connection.commit()
    connection.close()
    image.save("itemImages/" + str(primaryID)) #image is going to be saved using the primary key