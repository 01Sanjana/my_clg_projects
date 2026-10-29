
import os
import re
import sqlite3

from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

# =========================
# FLASK APPLICATION
# =========================

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev-only-change-this"
)

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
    name = request.form["name"].strip()
    email = request.form["email"].strip()
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # Validate Gmail address
    gmail_pattern = r"^[a-zA-Z0-9._%+-]+@gmail\.com$"

    if not re.match(gmail_pattern, email):
        return render_template(
            "index.html",
            message="Please enter a valid Gmail address."
        )

    # Check password confirmation
    if password != confirm_password:
        return render_template(
            "index.html",
            message="Passwords do not match."
        )

    conn = get_db_connection()

    # Check whether email is already registered
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

    # Hash password before storing it
    hashed_password = generate_password_hash(password)

    try:
        conn.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, hashed_password)
        )

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()

        return render_template(
            "index.html",
            message="This email is already registered."
        )

    conn.close()

    # Show success message after registration
    session["message"] = "Registration successful! Please login."

    return redirect(url_for("home"))


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"].strip()
    password = request.form["password"]

    conn = get_db_connection()

    user = conn.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    conn.close()

    # Verify email and password
    if user and check_password_hash(
        user["password"],
        password
    ):
        session["user_name"] = user["name"]

        return redirect(url_for("dashboard"))

    return render_template(
        "index.html",
        message="Invalid email or password."
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():
    if "user_name" not in session:
        return redirect(url_for("home"))

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# =========================
# CREATE TABLE ON STARTUP
# =========================

create_table()


# =========================
# START APPLICATION LOCALLY
# =========================

if __name__ == "__main__":
    app.run(debug=True)
