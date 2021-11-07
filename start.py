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
    return render_template("login.html", newPageLoc="/home") #just displays the login page and allow python to dictate where to send the user after clicking submit (probably just leave it as a cosntant)

@app.route("/home")
def home():
    username = request.cookies.get('username') #gets the user credentials so that it knows that the user is logged in
    password = request.cookies.get('password')
    if login.login(username, password): #if login credentials are valid then goes to right page, else goes back to log in so that they can put in valid credentials
        return render_template("home.html")
    else:
        return render_template("login.html", newPageLoc="/home")

@app.route("/newItem")
def newItem():
    username = request.cookies.get('username') #gets the user credentials so that it knows that the user is logged in
    password = request.cookies.get('password')
    if login.login(username, password):
        return render_template("newItem.html")
    else:
        return render_template("login.html", newPageLoc="/home")