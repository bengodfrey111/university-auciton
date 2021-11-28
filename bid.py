import sqlite3

def existBid(itemID, username): #checks if user has done a bid with that specific item
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT * FROM Bids WHERE itemID=:itemID AND username=:username", {"itemID": itemID, "username": username})
    result = False
    for row in cursor:
        result = True
        break
    connection.close()
    return result

def newBid(itemID, username, maxPrice): #this will place a new bid the user makes
    bidExist = existBid(itemID, username)
    preBid = maxUserBid(itemID, username)
    currentPrice = finalPrice(itemID)
    maxPrice = int(float(maxPrice) * 10) / 10 #this will not allow single pences
    if maxPrice < float(currentPrice["currentPrice"]):
        return False
    end = True
    connection = sqlite3.connect("AuctionDB.db")
    try:
        if bidExist: #checks if user already made a bid and wants to make another bid, if bid already made just edit it, else make new record of the bid
            if float(preBid["maxBid"]) < maxPrice:
                connection.execute("UPDATE Bids SET maxPrice=:maxPrice WHERE itemID=:itemID AND username=:username", {"maxPrice": maxPrice * 10, "itemID": itemID, "username": username})
            else:
                end = False
        else:
            connection.execute("INSERT INTO Bids (maxPrice, itemID, username) VALUES (:maxPrice, :itemID, :username)", {"maxPrice": maxPrice * 10, "itemID": itemID, "username": username})
        connection.commit()
        connection.close()
        end = True
    except sqlite3.Error: #checks if bid is made
        connection.commit()
        connection.close()
        end = False
    return end
    

def maxUserBid(itemID, username): #this retreives the max bid of a specific user
    bidExist = existBid(itemID, username)
    if bidExist:
        connection = sqlite3.connect("AuctionDB.db")
        cursor = connection.execute("SELECT maxPrice, username, itemID FROM Bids WHERE itemID=:itemID AND username=:username", {"itemID": itemID, "username": username})
        for row in cursor:
            return {"maxBid": str(float(row[0]) / 10), "username": str(row[1]), "itemID": str(row[2])}
    else:
        return "None"

def maxBid(itemID): #max bid made for the entire bidding process
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT MAX(maxPrice), username, itemID FROM Bids WHERE itemID=:itemID", {"itemID": itemID})
    for row in cursor:
        if row[0] != None: #checks it exists
            return {"maxBid": str(float(row[0]) / 10), "username": str(row[1]), "itemID": str(row[2])}
    return {"maxBid": "0", "username": "", "itemID": ""}

def secondMaxBid(itemID): #this gets the second highest bid for the object, helps get the best cheapest price for the object (don't want someone buying an object for £2000 while the second highest bid was £10)
    max = maxBid(itemID)
    connection = sqlite3.connect("AuctionDB.db")
    cursor = connection.execute("SELECT MAX(maxPrice), username, itemID FROM Bids WHERE itemID=:itemID AND username!=:username", {"itemID": itemID, "username": max["username"]})
    for row in cursor:
        if row[0] != None:
            return {"maxBid": str(float(row[0]) / 10), "username": str(row[1]), "itemID": str(row[2])}
        return {"maxBid": "0", "username": "", "itemID": ""}

def finalPrice(itemID):
    max = maxBid(itemID)
    secondMax = secondMaxBid(itemID)
    if str(max["maxBid"]) != "None":
        if str(secondMax["maxBid"]) != "None": #this checks if the highest and second highest bid exists
            return {"currentPrice": float(secondMax["maxBid"]) + 0.1, "username": max["username"], "itemID": max["itemID"]} #makes current price 10p higher than second highest bid
        else:
            return {"currentPrice": float(max["maxBid"]), "username": max["username"], "itemID": max["itemID"]}
    else:
        return {"currentPrice": "0", "username": "", "itemID":""}


if __name__ == "__main__":
    print(maxBid(1))
    #print(secondMaxBid(1))
    print(finalPrice(1))