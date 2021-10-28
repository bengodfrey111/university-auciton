from flask import Flask
from markupsafe import escape
from flask import request
from flask import make_response
from flask import render_template

import login #my login code

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html") #just displays the login page

@app.route("/logged_i")
def loggedIn():
    username = request.cookies.get('username') #gets the user credentials so that it knows that the user is logged in
    password = request.cookies.get('password')
    if login.login(username, password):
        return "logged in"
    else:
        return render_template("login.html")