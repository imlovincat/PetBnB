from flask import Flask, flash,render_template, request, session, redirect,url_for, make_response, jsonify
from data_utils import *
from datetime import timedelta, datetime, date
import os.path
import os
from os import path

import time
import models
import paymentprocessing


from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.send_file_max_age_default = timedelta(seconds=1)

@app.route("/")
def display_homepage():
    session['url'] = ""
    pettype = list_pettype_data()
    return render_template(
        "index.html",
        the_title="Project - PetBnB",
        the_opening_title="Main Screen",
        pettype = pettype,

    )

@app.route("/error")
def petbnb_error_page():
    return render_template(
        "error.html",
        the_title="Project - PetBnB",
        the_opening_title="Error Screen",
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
    data = check_email_exists_data()
    return render_template(
        "signup.html",
        the_title="Project - PetBnB",
        the_opening_title="Sign Up Screen",
        data = data,
    )

@app.route("/signuppetsitter")
def petbnb_sign_up_petsitter():
    if session.get('user'): 
        session['url'] = None
        return render_template(
            "signuppetsitter.html",
            the_title="Project - PetBnB",
        )
    else :
        session['url'] = "signuppetsitter"
        return redirect('/login')

@app.route("/viewaccount")
def petbnb_view_account():
    if session.get('user'): 
        data = view_account_data(session['user'])
        petsitter_data = petsitter_signed_data(session['user'])
        signed_petsitter_num = len(petsitter_data)    
        booking = view_booking_data(session['user'])
        booking_num = len(booking)
        email = session['user']
        return render_template(
            "viewaccount.html",
            the_title="Project - PetBnB",
            the_opening_title="View Account",
            data = data,
            email = email,
            booking = booking,
            petsitter_data = petsitter_data,
            signed_petsitter_num = signed_petsitter_num,
            booking_num = booking_num,
        )  
    else:
        session['url'] = "viewaccount"
        return redirect('/login')
        
@app.route("/viewpetsitteraccount/<petsittername>", methods=['GET'])
def petbnb_view_petsitter_account(petsittername):
    if session.get('user'):
        petsitter_data = petsitter_signed_data(session['user'])
        email = session['user']
        signed_petsitter_num = len(petsitter_data) 
        data = manages_petsitter_account_data(petsittername,email)
        if len(data) == 0:
            return "Error"
        booking = petsitter_booking_data(petsittername)
        booking_num = len(booking)
        completed_booking = booking_quantity_data(petsittername,"Completed")
        pending_booking = booking_quantity_data(petsittername,"Pending")
        cancel_booking = booking_quantity_data(petsittername,"Canceled")
        
        return render_template(
            "viewpetsitteraccount.html",
            the_title="Project - PetBnB",
            the_opening_title="View Pet Sitter Account",
            data = data,
            email = email,
            petsitter_data = petsitter_data,
            signed_petsitter_num = signed_petsitter_num,
            booking = booking,
            booking_num = booking_num,
            completed_booking = completed_booking,
            pending_booking = pending_booking,
            cancel_booking = cancel_booking,
            
        )  
        
        
    else:
        return redirect('/login')
        
@app.route("/viewbooking/<data>",  methods=['GET'])
def petbnb_view_booking(data):
    bookingRef = data;
    data = view_booking_by_ref_data(bookingRef)
    petsittername = data[0][15]
    if session.get('user'):
        email = session['user']
    else: email = ""
    accessType = access_booking_data(bookingRef, email, petsittername)
    pettype = str_to_list(data[0][11])
    today = datetime.today().strftime('%Y-%m-%d')
    checkin = data[0][6].strftime('%Y-%m-%d')
    return render_template(
        "viewbooking.html",
        the_title="Project - PetBnB",
        the_opening_title="View Booking",
        bookingRef = bookingRef,
        data = data,
        accessType = accessType,
        pettype = pettype,
        today = today,
        checkin = checkin,
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
    
    if "Bank Credit/Debit Card" in data['payment']:
        return render_template(
            "bankcardpayment.html",
            the_title="Project - PetBnB",
            the_opening_title="Bank Credit/Debit Card Payment",
            data = data,
            petsitter = petsitter,
            pettype = pettype,
        )
    
    else:
        bookingRef = confirm_makebooking_data(user,data)
        newURL = "/viewbooking/" + bookingRef
        return redirect(newURL)

@app.route("/cancelbooking/<data>", methods=["GET"])
def process_for_canceledbooking_form(data):
    if session.get('user'):
        bookingRef = data
        data = view_booking_by_ref_data(bookingRef)
        email = session['user']
        petsittername = data[0][15]
        status = data[0][0]
        today = datetime.today().strftime('%Y-%m-%d')
        checkin = data[0][6].strftime('%Y-%m-%d')
        accessType = access_booking_data(bookingRef, email, petsittername)
        newstatus = "Canceled"
        if ("petsitter" in accessType) and ("Pending" in status or "Confirmed" in status):
            update_booking_data(bookingRef, accessType, newstatus)
        elif (checkin > today) and ("customer" in accessType) and ("Pending" in status or "Confirmed" in status):
            update_booking_data(bookingRef, accessType, newstatus)
        newUrl = "/viewbooking/" + bookingRef
        return redirect(newUrl)
            
            
@app.route("/confirmbooking/<data>", methods=["GET"])
def process_for_confirmedbooking_form(data):
    if session.get('user'):
        bookingRef = data
        data = view_booking_by_ref_data(bookingRef)
        email = session['user']
        petsittername = data[0][15]
        status = data[0][0]
        today = datetime.today().strftime('%Y-%m-%d')
        checkin = data[0][6].strftime('%Y-%m-%d')
        accessType = access_booking_data(bookingRef, email, petsittername)
        newstatus = "Confirmed"
        if (checkin >= today) and ("petsitter" in accessType or "customer" in accessType) and ("Pending" in status):
            update_booking_data(bookingRef, accessType, newstatus)
        newUrl = "/viewbooking/" + bookingRef
        return redirect(newUrl)        
    
@app.route("/completebooking/<data>", methods=["GET"])
def process_for_completedbooking_form(data):
    if session.get('user'):
        bookingRef = data
        data = view_booking_by_ref_data(bookingRef)
        email = session['user']
        petsittername = data[0][15]
        status = data[0][0]
        today = datetime.today().strftime('%Y-%m-%d')
        checkin = data[0][6].strftime('%Y-%m-%d')
        accessType = access_booking_data(bookingRef, email, petsittername)
        newstatus = "Completed"
        if (today >= checkin) and ("petsitter" in accessType or "customer" in accessType) and ("Confirmed" in status):
            update_booking_data(bookingRef, accessType, newstatus)
        newUrl = "/viewbooking/" + bookingRef
        return redirect(newUrl)   

@app.route("/searchform", methods=["POST"])
def process_search_form():
    data = request.form
    pettype = list_pettype_data()
    return render_template(
        "searchresult.html",
        the_title="Project - PetBnB",
        the_opening_title="Search Result",
        data = search_petsitter_data(data),
        the_num = len(search_petsitter_data(data)),
        pettype = pettype,
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
    email = data['email']
    if data['password'] != data['repeatpassword']:
        flash('password and repeat password can not match!')
        return render_template(
            "signup.html",
            the_title="Project - PetBnB | Customer Sign up",
            message2 = "not match!",
            data = data,
        )
    
    elif check_duplicated_email_data(email):

        customer_signup_data(data)
        session['user'] = data["email"]
        return redirect('/')
    else:
        flash('email is used!'),
        return render_template(
            "signup.html",
            the_title="Project - PetBnB | Customer Sign up",
            message1 = "Email is used!",
            data = data,
        )
    
    
    

@app.route("/signuppetsitterform", methods=["POST"])
def process_for_new_petsitter_signup_form():
    data = request.form
    petsittername = data['petsittername']
    if check_duplicate_petsitter_data(petsittername):
        petsitter_signup_data(session['user'],data)
        newURL = "/upload/" + petsittername
        return redirect(newURL)
    else: 
        return redirect('/signupetsitter')

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





@app.route("/payment", methods=["POST"])
def process_for_credit_card_payment(): 
    data = request.form
    amount = str("{:.2f}".format(float(int(data['price']))))
    card = models.CreditCard()
    card.number = data['number']
    card.expiration_date = data['expiration_date']
    card.code = data['code']
    response = paymentprocessing.charge_credit_card(card, amount)
    print(response.is_success)
    print(response.messages)
    
    if response.is_success:
        petsitter = view_petsitter_data(data['petsitter'])
        pettype = str_to_list(data['type'])
    
        if session.get('user'):
            user = session['user']
        else: user = ""
    
        transactionID = response.messages[0][-11:-1]
        bookingRef = confirm_makebooking_data(user,data)
        make_payment_data(transactionID, bookingRef)
        newURL = "/viewbooking/" + bookingRef
        
        return redirect(newURL)
        
    else:
        return "Error"
    
    
    
# for sandbox payment testing    
@app.route("/payment_testing")
def process_for_credit_card_payment_testing():    
    amount = "19.99"
    card = models.CreditCard()
    card.number = "4007000000027" # visa test number
    card.expiration_date = "2050-01" # any date in the future
    card.code = "123" # any 3 digit code

    response = paymentprocessing.charge_credit_card(card, amount)
    
    messages = "Sorry, the transaction is failed, please try again"
    if response.is_success: messages = str(response.messages)
    
    
    print(response.is_success)
    print(response.messages)
    
    return messages
    
@app.route('/editaccount') 
def modify_account_form():
    if session.get('user'):
        email = session['user']
        data = view_account_data(session['user'])
        return render_template(
            "modify_account.html",
            the_title="Project PetBnB | Modify Customer Account",
            email = email,
            data = data,
        )
    else: return redirect('/login')

@app.route("/update_account", methods=["POST"])
def process_update_account(): 
    if session.get('user'):
        data = request.form
        email = session['user']
        update_account_data(data,email)
        return redirect('/viewaccount')
    else: return redirect('/login')

@app.route('/editpetsitteraccount/<petsittername>', methods=['GET']) 
def modify_petsitter_account_form(petsittername):
    if session.get('user'):
        email = session['user']
        data = view_petsitter_data(petsittername)
        pettype = list_pettype_data()
        return render_template(
            "modify_petsitteraccount.html",
            the_title="Project PetBnB | Modify Pet Sitter Account",
            email = email,
            data = data,
            pettype = pettype,
        )
    else: return redirect('/login')

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/update_petsitter_account', methods=['POST'])
def process_update_petsitter_account():
    data = request.form
    if session.get('user'):
        email = session['user']
        petsittername = data['petsittername']
        newUrl = "/viewpetsitter/" + petsittername
        update_petsitter_account_data(data,email)
        data = view_petsitter_data(petsittername)
        petsitterID = data[0][0]

        basepath = os.path.dirname(__file__)
        if request.files['file1']:
            file1 = request.files['file1']
            if not (file1 and allowed_file(file1.filename)):
                return "only accept file types: png,PNG,jpg,JPG,bmp"
            file1.filename = str(petsitterID) + "a" + ".jpg"
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file1.filename))
            file1.save(upload_path)
            
        if request.files['file2']:
            file2 = request.files['file2']
            if not (file2 and allowed_file(file2.filename)):
                return "only accept file types: png,PNG,jpg,JPG,bmp"
            file2.filename = str(petsitterID) + "b" + ".jpg"
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file2.filename))
            file2.save(upload_path)
            
        if request.files['file3']:
            file3 = request.files['file3']
            if not (file3 and allowed_file(file3.filename)):
                return "only accept file types: png,PNG,jpg,JPG,bmp"
            file3.filename = str(petsitterID) + "c" + ".jpg"
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file3.filename))
            file3.save(upload_path)
        
        if request.files['file4']:
            file4 = request.files['file4']
            if not (file4 and allowed_file(file4.filename)):
                return "only accept file types: png,PNG,jpg,JPG,bmp"
            file4.filename = str(petsitterID) + "d" + ".jpg"
            upload_path = os.path.join(basepath, 'static/images', secure_filename(file4.filename))
            file4.save(upload_path) 
        return redirect(newUrl)
    else: return redirect('/login')

@app.route('/picture/<data>', methods=['GET']) 
def petsitter_picture_form(data):
    if session.get('user'):
        email = session['user']
        petsittername = data
        if check_petsitter_access_data(petsittername,email):
            return render_template(
            "upload.html",
            the_title="Project - PetBnB",
            the_opening_title="Pet Sitter Picture Upload",
            petsittername = data,
            )
        else: return redirect('/login') 
    else: return redirect('/login')   


@app.route('/upload/<data>', methods=['POST', 'GET']) 
def upload(data):
    petsittername = data
    data = view_petsitter_data(petsittername)
    petsitterID = data[0][0]
    basepath = os.path.dirname(__file__)
    
    if request.files['file1']:
        file1 = request.files['file1']
        if not (file1 and allowed_file(file1.filename)):
            return "only accept file types: png,PNG,jpg,JPG,bmp"
        file1.filename = str(petsitterID) + "a" + ".jpg"
        upload_path = os.path.join(basepath, 'static/images', secure_filename(file1.filename))
        file1.save(upload_path)
        
    if request.files['file2']:
        file2 = request.files['file2']
        if not (file2 and allowed_file(file2.filename)):
            return "only accept file types: png,PNG,jpg,JPG,bmp"
        file2.filename = str(petsitterID) + "b" + ".jpg"
        upload_path = os.path.join(basepath, 'static/images', secure_filename(file2.filename))
        file2.save(upload_path)
        
    if request.files['file3']:
        file3 = request.files['file3']
        if not (file3 and allowed_file(file3.filename)):
            return "only accept file types: png,PNG,jpg,JPG,bmp"
        file3.filename = str(petsitterID) + "c" + ".jpg"
        upload_path = os.path.join(basepath, 'static/images', secure_filename(file3.filename))
        file3.save(upload_path)
    
    if request.files['file4']:
        file4 = request.files['file4']
        if not (file4 and allowed_file(file4.filename)):
            return "only accept file types: png,PNG,jpg,JPG,bmp"
        file4.filename = str(petsitterID) + "d" + ".jpg"
        upload_path = os.path.join(basepath, 'static/images', secure_filename(file4.filename))
        file4.save(upload_path)
    
    newURL = "/viewpetsitteraccount/" + petsittername
    return redirect(newURL)