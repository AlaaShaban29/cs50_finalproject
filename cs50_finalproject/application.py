import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology

# Configure application - Copied from Problem set 8
app = Flask(__name__)

# Ensure templates are auto-reloaded - Copied from Problem set 8
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached - Copied from Problem set 8


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies) - Copied from Problem set 8
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///appeople.db")

# Register - Copied from Problem set 8
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Render register page
    if request.method == "GET":
        print("0")
        return render_template("register.html")

    # Checking if user provided all the required fields correctly and if the username is taken
    elif request.method == "POST":
        print("teste 1")
        if not request.form.get("username"):
            print("teste 2")
            return apology ("You must provide a username.")
            print("0")
        print("1")

        if not request.form.get("email"):
            return apology ("You must provide a valid email.")
        print("2")
        if not request.form.get("password"):
            return apology ("You must provide a password.")

        if not request.form.get("confirmation"):
            return  apology("You must confirm your password.")

        if request.form.get("password") != request.form.get("confirmation"):
            return apology ("Your passwords don't match! Try typing again.")

        if not db.execute("SELECT username FROM users WHERE username = :username", username=request.form.get("username")):
            hashword = generate_password_hash(request.form.get("password"))
            users = db.execute("INSERT INTO users (username, hashword) VALUES(:username, :hash)",
                               username=request.form.get("username"), hash=hashword)
            return apology ("success!")

        else:
            return apology ("Username was already taken!")

    return redirect("/")

@app.route("/")
def index():
    #session["user_id"]
    return render_template("index.html")

@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    username = request.args.get("username")
    rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    # If inputed username does not have at least 1 character and is not taken
    if len(username) > 1 and not rows:
        return jsonify(True)

    else:
        return jsonify(False)