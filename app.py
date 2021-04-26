from flask import Flask, render_template, request, session, redirect,url_for
from data_utils import *
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)

@app.route("/")
def display_homepage():
    session['url'] = ""
    return render_template(
        "index.html",
        the_title="Project - PetBnB",
        the_opening_title="Main Screen",

    )

@app.route("/loginpage")
def petbnb_login_page():
    session['url'] = ""
    return redirect('/login')
        

@app.route("/login")
def petbnb_login():  
    return render_template(
        "login.html",
        the_title="Project - PetBnB",
        the_opening_title="Login Screen",
    )

@app.route("/logout")
def petbnb_logout():
    session['user'] = None
    return redirect('/')


@app.route("/signup")
def petbnb_signup():
    return render_template(
        "signup.html",
        the_title="Project - PetBnB",
        the_opening_title="Sign Up Screen",
    )

@app.route("/signuppetsitter")
def petbnb_sign_up_petsitter():
    if session.get('user'): 
        session['url'] = None
        return render_template(
            "signuppetsitter.html",
            the_title="Project - PetBnB",
            the_opening_title="Sign up pet sitter Screen",
        )
    else :
        session['url'] = "signuppetsitter"
        return redirect('/login')

@app.route("/makebooking")
def petbnb_make_booking():
    return render_template(
        "makebooking.html",
        the_title="Project - PetBnB",
        the_opening_title="Make Booking Screen",
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

@app.route("/signuppetsitterform", methods=["GET","POST"])
def process_for_new_petsitter_signup_form():
    size = request.form.getlist('size[]')
    return format(size)

@app.route("/loginform", methods=["POST"])
def process_for_customer_login_form():
    data = request.form
    return_data = customer_login_data(data)

    if len(return_data) == 1:
        session['user'] = data["email"]
        session.permanent = True
        if session.get('url'):
            return redirect(session['url'])
        else: return redirect('/')
        
    else : 
        session['user'] = None
        return redirect('/login')