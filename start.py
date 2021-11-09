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

def stringDateTime(dateTime): #this simply makes the date time a string so that I can just stick it on a HTML page in a readable state
    return str(dateTime.day) + "/" + str(dateTime.month) + "/" + str(dateTime.year) + " " + str(dateTime.hour) + ":" + str(dateTime.minute)

@app.route("/")
def index():
    return loginPage() #just displays the login page and allow python to dictate where to send the user after clicking submit (probably just leave it as a cosntant)

@app.route("/login")
def loginPage(validCredentials = ""):
    return render_template("login.html", newPageLoc="/home", validUser=validCredentials) #just displays the login page and allow python to dictate where to send the user after clicking submit (probably just leave it as a cosntant)


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
        return render_template("item.html", idImage=ID, name=itemAtr["name"], user=itemAtr["username"], description=itemAtr["description"], dateTime=stringDateTime(itemAtr["datetime"]))
    else:
        return render_template("noItem.html")
