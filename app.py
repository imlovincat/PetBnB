from flask import Flask, render_template, request, session, redirect,url_for
from data_utils import *
from datetime import timedelta, datetime, date
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

@app.route("/viewaccount")
def petbnb_view_account():
    if session.get('user'): 
        data = view_account_data(session['user'])
        booking = view_booking_data(session['user'])
        email = session['user']
        return render_template(
            "viewaccount.html",
            the_title="Project - PetBnB",
            the_opening_title="View Account",
            data = data,
            email = email,
            booking = booking
        )  
    else:
        session['url'] = "viewaccount"
        return redirect('/login')
        
@app.route("/viewbooking/<data>",  methods=['GET'])
def petbnb_view_booking(data):
    bookingRef = data;
    data = view_booking_by_ref_data(bookingRef)
    print(data)
    return render_template(
        "viewbooking.html",
        the_title="Project - PetBnB",
        the_opening_title="View Booking",
        bookingRef = bookingRef,
        data = data,
    )



@app.route("/makebooking/<data>", methods=['GET'])
def petbnb_make_booking(data):
    if session.get('user'): 
        customerdata = customer_makebooking_data(session.get('user'))
    else: customerdata = ["","","","",""]
    data = view_petsitter_data(data)
    today = datetime.today().strftime('%Y-%m-%d')
    thisyear = int(today[0])*1000 +  int(today[1])*100 +  int(today[2])*10 +  int(today[3])
    nextyear = str(thisyear + 1) + today[4:]
    return render_template(
        "makebooking.html",
        the_title="Project - PetBnB",
        the_opening_title="Make Booking",
        customerdata = customerdata,
        data = data,
        today = today,
        nextyear = nextyear,
        service = str_to_list(data[0][11]),
        pettype = str_to_list(data[0][13]),
        petsize = str_to_list(data[0][14]),
    )

@app.route("/makebookingform/<petsitter>", methods=["POST","GET"])
def process_for_makebooking_form(petsitter):
    petsitter = view_petsitter_data(petsitter)
    data = request.form
    checkin = date(int(data['checkin'][0:4]),int(data['checkin'][5:7]),int(data['checkin'][8:10]))
    checkout = date(int(data['checkout'][0:4]),int(data['checkout'][5:7]),int(data['checkout'][8:10]))
    nights = (checkout - checkin).days
    if nights == 0: nights = 1
    price = int(petsitter[0][10]) * nights * int(data['numofpets'])
    if data.getlist('type[]'): pettype = format(data.getlist('type[]'))
    else: pettype = "[]"
    return render_template(
        "confirmbooking.html",
        the_title="Project - PetBnB",
        the_opening_title="Booking Payment",
        petsitter = petsitter,
        data = data,
        nights = nights,
        price = price,
        pettype = pettype,
    )  

@app.route("/confirmbookingform", methods=["POST"])
def process_for_confirmbooking_form():
    data = request.form
    petsitter = view_petsitter_data(data['petsitter'])
    pettype = str_to_list(data['type'])
    if session.get('user'):
        user = session['user']
    else: user = ""
    bookingRef = confirm_makebooking_data(user,data)
    return render_template(
        "completebooking.html",
        the_title="Project - PetBnB",
        the_opening_title="Booking completed",
        data = data,
        petsitter = petsitter,
        pettype = pettype,
        bookingRef = bookingRef
    )  


@app.route("/searchform", methods=["POST"])
def process_search_form():
    data = request.form
    return render_template(
        "searchresult.html",
        the_title="Project - PetBnB",
        the_opening_title="Search Result",
        data = search_petsitter_data(data),
        the_num = len(search_petsitter_data(data)),     
    )  
    
@app.route("/viewpetsitter/<data>", methods=['GET'])
def process_viewpetsitter_form(data):
    data = view_petsitter_data(data)
    
    return render_template(
        "viewpetsitter.html",
        the_title="Project - PetBnB",
        the_opening_title="View Pet Sitter Profile",
        data = data,
        service = str_to_list(data[0][11]),
        pettype = str_to_list(data[0][13]),
        petsize = str_to_list(data[0][14]),
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

@app.route("/signuppetsitterform", methods=["POST"])
def process_for_new_petsitter_signup_form():
    data = request.form
    petsitter_signup_data(session['user'],data)
    return redirect('/')

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
        
if __name__ == '__main__':
    app.run(debug=True)