from flask import Flask, render_template, request, redirect, url_for, session

import sqlite3

import re

from werkzeug.security import generate_password_hash, check_password_hash


# =========================
# FLASK APPLICATION
# =========================

app = Flask(__name__)


# Secret key for login sessions

app.secret_key = "admane_traders_secret_key"


# =========================
# DATABASE CONNECTION
# =========================

def get_db_connection():

    conn = sqlite3.connect("database.db")

    conn.row_factory = sqlite3.Row

    return conn


# =========================
# CREATE DATABASE TABLE
# =========================

def create_table():

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    conn.commit()

    conn.close()


# =========================
# HOME / LOGIN PAGE
# =========================

@app.route("/")
def home():

    message = session.pop("message", None)

    return render_template(
        "index.html",
        message=message
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]

    email = request.form["email"]

    password = request.form["password"]

    confirm_password = request.form["confirm_password"]


    # =========================
    # CHECK GMAIL FORMAT
    # =========================

    gmail_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"


    if not re.match(gmail_pattern, email):

        return render_template(
            "index.html",
            message="Please enter a valid Gmail address."
        )


    # =========================
    # CHECK PASSWORDS
    # =========================

    if password != confirm_password:

        return render_template(
            "index.html",
            message="Passwords do not match."
        )


    # =========================
    # CONNECT TO DATABASE
    # =========================

    conn = get_db_connection()


    # =========================
    # CHECK EXISTING EMAIL
    # =========================

    existing_user = conn.execute(

        "SELECT * FROM users WHERE email = ?",

        (email,)

    ).fetchone()


    if existing_user:

        conn.close()

        return render_template(
            "index.html",
            message="This email is already registered."
        )


    # =========================
    # HASH PASSWORD
    # =========================

    hashed_password = generate_password_hash(password)


    # =========================
    # INSERT USER
    # =========================

    conn.execute(

        """
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        """,

        (name, email, hashed_password)

    )


    # Save changes

    conn.commit()


    # Close database

    conn.close()


    # =========================
    # SUCCESS MESSAGE
    # =========================

    session["message"] = "Registration successful! Please login."


    return redirect(
        url_for("home")
    )


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    email = request.form["email"]

    password = request.form["password"]


    # Connect to database

    conn = get_db_connection()


    # Search for user

    user = conn.execute(

        "SELECT * FROM users WHERE email = ?",

        (email,)

    ).fetchone()


    conn.close()


    # =========================
    # CHECK LOGIN DETAILS
    # =========================

    if user and check_password_hash(
        user["password"],
        password
    ):

        # Store user name in session

        session["user_name"] = user["name"]


        # Open dashboard

        return redirect(
            url_for("dashboard")
        )


    # =========================
    # INVALID LOGIN
    # =========================

    return render_template(

        "index.html",

        message="Invalid email or password."

    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():


    # Check whether user is logged in

    if "user_name" not in session:

        return redirect(
            url_for("home")
        )


    return render_template(

        "dashboard.html",

        name=session["user_name"]

    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():


    # Remove session data

    session.clear()


    # Return to login page

    return redirect(
        url_for("home")
    )


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    # Create database table

    create_table()


    # Start Flask server

    app.run(debug=True)