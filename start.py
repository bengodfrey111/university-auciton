from flask import Flask
from markupsafe import escape
from flask import request
from flask import make_response
from flask import render_template
from flask import session
import datetime

import login #my login code
import storeItems

app = Flask(__name__)

def stringDate(dateTime): #this simply makes the date time a string so that I can just stick it on a HTML page in a readable state
    return str(dateTime.day) + "/" + str(dateTime.month) + "/" + str(dateTime.year)

def htmlListItems(items): #this lists a bunch of items viewable in html
    html = ""
    for i in range(0,len(items)): #loops through all the items
        html+= "<div id='" + str(i) +"'><a href='/item/" + str(items[i]["ID"]) + "'><h2>" + str(items[i]["name"]) + "</h2></a><br><img src='/static/itemImages/" + str(items[i]["ID"]) + "' width='100' height='100'/><br><p>" + stringDate(items[i]["datetime"]) + "</p><br></div>"
    return html


@app.route("/")
def index():
    html = "<!DOCTYPE html>"
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if login.login(username, password):
        html+= "<button onclick=logout()>Logout</button><br><br> <script>function logout(){document.cookie=''; window.location.replace('/');}</script>"
    else:
        html+= "<a href='/login'><small>login</small></a><br><br>"

    items = storeItems.allItems() #gets all the items that are being sold
    html+= htmlListItems(items)

    return html

@app.route("/login", methods=["GET", "POST"])
def loginPage(validCredentials = ""):
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login.login(username, password): #if login credentials are valid then goes to right page, else goes back to log in so that they can put in valid credentials
            return "<script>window.location.replace('/home')</script>"
        else:
            return render_template("login.html", validUser="!") #send login page up with error message if login is invalid
    return render_template("login.html", validUser=validCredentials) #just displays the login page


@app.route("/newUser", methods=["GET", "POST"]) #this will allow a user to create a new account
def newUser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        accountAlreadyExist = login.newAccount(username, password)
        if accountAlreadyExist:
            return render_template("newLogin.html", validUser='!') #exclamation mark means not which means username is not valid
        return loginPage() #if login info valid, user will probably want to login so will go to login page
    return render_template("newLogin.html")


@app.route("/home")
def home():
    username = request.cookies.get('username') #gets the user credentials so that it knows that the user is logged in
    password = request.cookies.get('password')
    if login.login(username, password): #if login credentials are valid then goes to right page, else goes back to log in so that they can put in valid credentials
        return render_template("home.html")
    else:
        return loginPage("!")


@app.route("/newItem", methods=["GET", "POST"])
def newItem():
    username = request.cookies.get('username') #gets the user credentials so that it knows that the user is logged in
    password = request.cookies.get('password')
    if login.login(username, password):
        if request.method == "POST":
            description = request.form["description"] #obtains the image, description and item name the user puts in
            itemName = request.form["itemName"]
            if request.files: #checks if user is trying to upload a file (if not it would just display the new item page without doing anything)
                image = request.files["image"] #learnt how to handle images at https://pythonise.com/series/learning-flask/flask-uploading-files
                storeItems.newItem(itemName, description, username, image) #filename is the primary key ID
                return home()
            

        return render_template("newItem.html")
    else:
        return loginPage("!")


@app.route("/item/<int:ID>")
def item(ID): #this simply displays the item using its unique ID
    itemAtr = storeItems.item(ID)
    if itemAtr != None: #checks if the item exists, if it exists then it will go to the normal page, if it doesn't then it will go to a page explaining that the item was not found
        username = request.cookies.get('username')
        password = request.cookies.get('password')
        if login.login(username, password):
            return render_template("item.html", idImage=ID, name=itemAtr["name"], user=itemAtr["username"], description=itemAtr["description"], dateTime=stringDate(itemAtr["datetime"]), login="")
        else:
            return render_template("item.html", idImage=ID, name=itemAtr["name"], user=itemAtr["username"], description=itemAtr["description"], dateTime=stringDate(itemAtr["datetime"]), login="!")
    else:
        return render_template("noItem.html")


@app.route("/myItems")
def myItems():
    username = request.cookies.get('username')
    password = request.cookies.get('password')
    if login.login(username, password): #checks if user is logged in
        items = storeItems.myItems(username) #gets all the items a specific user is selling
        html = "<!DOCTYPE html>"
        html+= htmlListItems(items)
        return html
    else:
        return loginPage("!")