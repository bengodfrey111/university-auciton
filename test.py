import sqlite3

connection = sqlite3.connect("AuctionDB.db")

connection.execute("INSERT INTO Bids (itemID, username, maxPrice) VALUES (:itemID, :username, :maxPrice);", {"maxPrice": "32", "itemID": 1, "username": "Ben"})
#connection.execute("SELECT * FROM Bids")
connection.commit()
connection.close()