import datetime
from flask import Flask
from markupsafe import escape
from flask import request
from flask import make_response
from flask import render_template
from flask import session
import sqlite3
import time
from threading import Thread, Event

import login #my login code
import storeItems
import bid
import emailSend


def searchAndCloseItems(): #this is invloved in handling when the bid closes https://smirnov-am.github.io/background-jobs-with-flask/
    while True:
        time.sleep(10)
        closeItems = storeItems.dueClose()
        for i in range(0,len(closeItems)): #cycles through all the items that has been close
            log = bid.finalPrice(closeItems[i]["ID"])
            account = login.account(log["username"])
            emailSend.wonBid(closeItems[i], log["currentPrice"] ,account) #sends email to winner

    
thread = Thread(target=searchAndCloseItems)
thread.daemon = True
thread.start()


app = Flask(__name__)
app.secret_key = "zOGSyUx5ctSTf2UXwxBr" #just some random string to make the session key unpredictable

def stringDate(dateTime): #this simply makes the date time a string so that I can just stick it on a HTML page in a readable state
    return str(dateTime.day) + "/" + str(dateTime.month) + "/" + str(dateTime.year)

def htmlListItems(items): #this lists a bunch of items viewable in html
    html = ""
    for i in range(0,len(items)): #loops through all the items
        finalPrice = bid.finalPrice(items[i]["ID"])
        price = finalPrice["currentPrice"]
        if price % 1 == 0:
            price = str(int(finalPrice["currentPrice"]))
        else:
            price = str(finalPrice["currentPrice"]) + "0"
        html+= "<div id='" + str(i) +"'><a href='/item/" + str(items[i]["ID"]) + "'><h2>" + str(items[i]["name"]) + "</h2></a><br><img src='/static/itemImages/" + str(items[i]["ID"]) + "' width='100' height='100'/><br>" + "<p>£" + price + "</p><p>" + stringDate(items[i]["datetime"]) + "</p><br></div>"
    return html

def databaseCreation():
    try: #if database is not found then it will create a database instead with the right tables
        file = open("AuctionDB.db","r")
        file.close()
    except FileNotFoundError:
        file = open("AuctionDB.db","w") #create the file
        file.close()
        connection = sqlite3.connect("AuctionDB.db") #connects to the new database
        cursor = connection.cursor()
        tableCreate = open("databaseTableCreation.txt","r") #this file stores the sql commands to create the right tables
        tableCreate = tableCreate.readlines()
        string = ""
        for i in range(0,len(tableCreate)):
            string+= tableCreate[i] #makes the array representing each line into only one single string
        tableCreate = string
        cursor.executescript(tableCreate) #executes the sql script that will create the tables
        connection.close()
databaseCreation() #creates database if not created (needs to run on server startup)


@app.route("/logout")
def logout():
    session.pop("username", default=None)
    return "<script>window.location.replace('/');</script>" #just goes to index page after popping the session and therefore logging out


@app.route("/")
def index():
    html = "<!DOCTYPE html>"
    if session.get("username"): #if logged in send this html, else send another bit of html (login link)
        html+= "<button onclick=logout()>Logout</button><br><br> <script>function logout(){document.cookie=''; window.location.replace('/logout');}</script>"
        html+= '<button type="button" onclick="window.location.href=' + "'" + "/newItem" + "'" + '">Sell new item</button>' #display these when the user is logged in
        html+= '<button type="button" onclick="window.location.href=' + "'" + "/myItems" + "'" + '">My items</button>'
    else:
        html+= "<a href='/login'><small>login</small></a><br><br>" #display this when user isn't logged in

    items = storeItems.openItems() #gets all the items that are being sold and makes it presentable
    html+= htmlListItems(items) #list all items that user may want to buy

    return html

@app.route("/login", methods=["GET", "POST"])
def loginPage(validCredentials = ""):
    if request.method == "POST": #if tis handling the forms
        username = request.form["username"]
        password = request.form["password"] #gets inputed username and password
        if len(username) < 50 and len(password) < 50:
            if login.login(username, password): #if login credentials are valid then goes to right page, else goes back to log in so that they can put in valid credentials
                session["username"] = username
                return "<script>window.location.replace('/')</script>"
            else:
                return render_template("login.html", validUser="!") #send login page up with error message if login is invalid
    return render_template("login.html", validUser=validCredentials) #just displays the login page


@app.route("/newUser", methods=["GET", "POST"]) #this will allow a user to create a new account
def newUser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        phoneNumber = request.form["phoneNumber"]
        if len(username) < 50 and len(password) < 50 and len(email) < 50 and len(phoneNumber) < 11:
            accountAlreadyExist = login.newAccount(username, password, email, phoneNumber) #inserts the data to create the account
            if accountAlreadyExist:
                return render_template("newLogin.html", validUser='!') #exclamation mark means not which means username is not valid
            return loginPage() #if login info valid, user will probably want to login so will go to login page
        else:
            return render_template("newLogin.html", validUser='!')
    return render_template("newLogin.html")


@app.route("/newItem", methods=["GET", "POST"])
def newItem():
    if session.get("username"): #checks if user is logged in:
        if request.method == "POST":
            description = request.form["description"] #obtains the image, description and item name the user puts in
            itemName = request.form["itemName"]
            if request.files: #checks if user is trying to upload a file (if not it would just display the new item page without doing anything)
                image = request.files["image"] #learnt how to handle images at https://pythonise.com/series/learning-flask/flask-uploading-files
                storeItems.newItem(itemName, description, session["username"], image) #filename is the primary key ID
                return index()
            

        return render_template("newItem.html")
    else:
        return loginPage("!")


@app.route("/item/<int:ID>")
def item(ID): #this simply displays the item using its unique ID
    itemAtr = storeItems.item(ID)
    if itemAtr != None: #checks if the item exists, if it exists then it will go to the normal page, if it doesn't then it will go to a page explaining that the item was not found 
        accountDetails = login.account(itemAtr["username"]) #gets user contact details
        auctionDone = ""
        if (itemAtr["datetime"] + datetime.timedelta(days=14)) >= datetime.datetime.now():
            auctionDone = ""
        else:
            auctionDone = "!"
        if session.get("username"): #checks if user is logged in
                return render_template("item.html", idImage=ID, user=itemAtr["username"], date=stringDate(itemAtr["datetime"]), login="", sold=auctionDone)
        else:
            return render_template("item.html", idImage=ID, user=itemAtr["username"], date=stringDate(itemAtr["datetime"]), login="!", sold=auctionDone)
    else:
        return render_template("noItem.html")


@app.route("/item/<int:itemID>/jsonPrice")
def JSONPrice(itemID): #this is the json file with the current price of the item
    firstBidding = bid.finalPrice(itemID)
    if firstBidding != None: #if there is a bid for the item
        return {"currentPrice": firstBidding["currentPrice"], "currency": "£"}
    else:
        return {"currentPrice": "0", "currency": "£"}

@app.route("/item/<int:ID>/json")
def JSON(ID): #this is the json file with all the attributes of item that I want public, I think it improves the readability of the code
    itemAtr = storeItems.item(ID)
    return {"name": itemAtr["name"], "description": itemAtr["description"], "datetime": itemAtr["datetime"].strftime('%Y-%m-%d %H:%M')}



@app.route("/item/<int:ID>/bid", methods=["GET", "POST"])
def bidPage(ID): #this will allow the user to make a bid
    itemAtr = storeItems.item(ID)
    accountDetails = login.account(itemAtr["username"])
    if session.get("username"):
        if itemAtr != None: #checks if item exists
            if (itemAtr["datetime"] + datetime.timedelta(days=14)) >= datetime.datetime.now(): #checks if bid is over
                if request.method == "POST": #handles the bid that the user makes
                    maxBid = request.form["maxBid"]
                    max = bid.maxBid(ID)
                    response = bid.newBid(ID, session["username"], maxBid) #creates the new bid
                    if response: #checks if bid was made
                        currentAccount = login.account(session["username"])
                        emailSend.bidSet(itemAtr, maxBid, currentAccount)
                        secondMax = bid.secondMaxBid(ID)
                        newMax = bid.maxBid(ID)
                        if max == secondMax: #this will send an email if someones bid was surpassed
                            surAccount = login.account(itemAtr["username"])
                            emailSend.surpassedBid(itemAtr, surAccount)
                        elif newMax["username"] != session["username"]:
                            surAccount = login.account(session["username"])
                            emailSend.surpassedBid(itemAtr, surAccount)
                    return item(ID)
            else:
                return "Bid is Over!!!" #shows when bidding is over to prevent new bids
            return render_template("bid.html", ID=ID)
        else:
            return render_template("noItem.html")
    else:
        return loginPage("!")

@app.route("/myItems")
def myItems():
    if session.get("username"): #checks if user is logged in
        items = storeItems.myItems(session["username"]) #gets all the items a specific user is selling
        html = "<!DOCTYPE html>"
        html+= htmlListItems(items)
        return html
    else:
        return loginPage("!")
