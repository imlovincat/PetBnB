from flask import Flask, render_template, request, session
from data_utils import *
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

@app.route("/")
def display_homepage():
    return render_template(
        "index.html",
        the_title="Project - PetBnB",
        the_opening_title="Main Screen",
    )

@app.route("/login")
def petbnb_login():
    return render_template(
        "login.html",
        the_title="Project - PetBnB",
        the_opening_title="Login Screen",
    )

@app.route("/signup")
def petbnb_signup():
    return render_template(
        "signup.html",
        the_title="Project - PetBnB",
        the_opening_title="Sign Up Screen",
    )

@app.route("/bepetsitter")
def petbnb_be_a_petsitter():
    return render_template(
        "bepetsitter.html",
        the_title="Project - PetBnB",
        the_opening_title="Sign up pet sitter Screen",
    )

@app.route("/signupform", methods=["POST"])
def process_for_new_customer_signup_form():
    data = request.form
    customer_signup_data(data)
    return render_template(
        "signupcomplete.html",
        the_title="Project - PetBnB",
        the_opening_title="Thanks for sign up",
        the_email=data["email"],
    )

@app.route("/loginform", methods=["POST"])
def process_for_customer_login_form():
    data = request.form
    return_data = customer_login_data(data)

    if len(return_data) == 1:
        session['user'] = data["email"]
        session.permanent = True
        command = "Login Sucess"
        
    else : 
        command = "Login Failed"
        session['user'] = False

    return render_template(
        "logincomplete.html",
        the_title="Project - PetBnB",
        the_opening_title="Login complete",
        the_command = command,
    )