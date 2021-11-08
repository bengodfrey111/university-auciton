from flask import Flask
from markupsafe import escape
from flask import request
from flask import make_response
from flask import render_template
from flask import session

import login #my login code

app = Flask(__name__)


@app.route("/")
def index():
    return loginPage() #just displays the login page and allow python to dictate where to send the user after clicking submit (probably just leave it as a cosntant)

@app.route("/login")
def loginPage():
    return render_template("login.html", newPageLoc="/home") #just displays the login page and allow python to dictate where to send the user after clicking submit (probably just leave it as a cosntant)


@app.route("/newUser", methods=["GET", "POST"]) #this will allow a user to create a new account
def newUser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username)
        print(password)
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
        return loginPage()

@app.route("/newItem")
def newItem():
    username = request.cookies.get('username') #gets the user credentials so that it knows that the user is logged in
    password = request.cookies.get('password')
    if login.login(username, password):
        return render_template("newItem.html")
    else:
        return loginPage()