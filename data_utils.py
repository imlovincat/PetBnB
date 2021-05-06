import DBcm
from datetime import datetime,date
from random import seed
from random import randint

connection = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'petbnb'
}


def customer_signup_data(data):
    try: 
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """ INSERT INTO customer (email,password) VALUES (%s, %s) """
            cursor.execute(SQL, (data["email"], data["password"]),)
    except:
        print("Error")


def customer_login_data(data):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT email FROM customer WHERE email = %s AND password = %s"""
            cursor.execute(SQL, (data["email"], data["password"]),)
            data = cursor.fetchall()
            return data
    except:
        print("Error")

def view_account_data(user):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT fname, sname, title, dateOfBirth, address, contactNumber FROM customer
                    WHERE email = %s
                    """
            cursor.execute(SQL, (user,),)
            data = cursor.fetchall()
        return data
    except:
        print("Error")   

def view_booking_data(user):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT id FROM customer WHERE email = %s"""
            cursor.execute(SQL,(user,),)
            return_data = cursor.fetchall()
            customerid = int(return_data[0][0])
            
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT 
                     booking.bookingRef,
                     booking.petsitterID,
                     booking.status,
                     booking.title,
                     booking.fname,
                     booking.sname,
                     booking.phone,
                     booking.email,
                     booking.startDate,
                     booking.endDate,
                     booking.totalPrice,
                     booking.petQunatity,
                     booking.typeOfPet,
                     booking.breed,
                     booking.note,
                     booking.createdBy,
                     petsitter.petsittername,
                     petsitter.country,
                     petsitter.city,
                     petsitter.town,
                     petsitter.address
                     FROM booking
                     INNER JOIN petsitter ON (booking.petsitterID = petsitter.id)
                     WHERE booking.customerID = %s
                     ORDER BY booking.createdBy DESC"""
            cursor.execute(SQL, (customerid,),)
            data = cursor.fetchall()
        return data
    except:
        print("Error") 

def view_booking_by_ref_data(ref):
    try:    
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT 
                     booking.status,
                     booking.title,
                     booking.fname,
                     booking.sname,
                     booking.phone,
                     booking.email,
                     booking.startDate,
                     booking.endDate,
                     booking.totalPrice,
                     booking.paymentMethod,
                     booking.petQunatity,
                     booking.typeOfPet,
                     booking.breed,
                     booking.note,
                     booking.createdBy,
                     petsitter.petsittername,
                     petsitter.email,
                     petsitter.phone,
                     petsitter.country,
                     petsitter.city,
                     petsitter.town,
                     petsitter.address
                     FROM booking
                     INNER JOIN petsitter ON (booking.petsitterID = petsitter.id)
                     WHERE booking.bookingRef = %s LIMIT 1"""
            cursor.execute(SQL, (ref,),)
            data = cursor.fetchall()
        return data
    except:
        print("Error") 

def customer_makebooking_data(email):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT email, fname, sname, title, contactNumber FROM customer WHERE email = %s"""
            cursor.execute(SQL, (email,),)
            data = cursor.fetchall()
            return data
    except:
        print("Error")

def petsitter_signup_data(user,data):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT id FROM customer WHERE email = %s"""
            cursor.execute(SQL,(user,),)
            return_data = cursor.fetchall()
            customerid = return_data[0][0]
            #customerid = ''.join(str(return_data[0]))
        
        if data.getlist('service[]'): petservice = format(data.getlist('service[]'))
        else: petservice = "[]"
        if data.getlist('type[]'): pettype = format(data.getlist('type[]'))
        else: pettype = "[]"
        if data.getlist('size[]'): petsize = format(data.getlist('size[]'))
        else: petsize = "[]"
        
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """ INSERT INTO petsitter (
                      customerid,
                      petsittername,
                      email,
                      phone,
                      country,
                      city,
                      town,
                      address,
                      description,
                      price,
                      petservice,
                      petnums,
                      pettype,
                      petsize,
                      housetype,
                      outdoor,
                      transport,
                      deleteflag
                      ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0) """
            cursor.execute(SQL, (customerid,data['petsittername'],data["email"],data["phone"],data['country'],data['city'],data['town'],data['street'],data['description'],data['price'],petservice,data['numofpet'],pettype,petsize,data['house'],data['outdoor'],data['transport']),)    

    except:
        print("Error")  

def confirm_makebooking_data(user,data):
    try:
        if user != "":
            with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT id FROM customer WHERE email = %s"""
                cursor.execute(SQL,(user,),)
                return_data = cursor.fetchall()
                customerid = return_data[0][0]
        else: customerid = ""
        with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT id FROM petsitter WHERE petsittername = %s"""
                cursor.execute(SQL,(data['petsitter'],),)
                return_data = cursor.fetchall()
                petsitterid = return_data[0][0]
        createdBy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        bookingRef = "PETBNB" + "00" + str(createdBy[0:4]) + str(createdBy[5:7]) + str(createdBy[8:10]) + str(createdBy[11:13]) + str(createdBy[14:16]) + str(createdBy[17:19]) + str(randint(0,9999))
        status = "Pending"
        if data.get('phone'): phone = data['phone']
        else: phone = ""
        if data.get('breed'): breed = data['breed']
        else: breed = ""
        if data.get('optional'): note = data['optional']
        else: note = ""
        
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """ INSERT INTO booking (
                      bookingRef,
                      petSitterID,
                      customerID,
                      status,
                      title,
                      fname,
                      sname,
                      phone,
                      email,
                      startDate,
                      endDate,
                      totalPrice,
                      petQunatity,
                      typeOfPet,
                      breed,
                      note,
                      createdBy,
                      deleteflag
                      ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0) """
            cursor.execute(SQL, (
                                bookingRef,
                                petsitterid,
                                customerid,
                                status,
                                data['title'],
                                data['fname'],
                                data['sname'],
                                phone,
                                data['email'],
                                data['checkin'],
                                data['checkout'],
                                data['price'],
                                data['numofpets'],
                                data['type'],
                                breed,
                                note,
                                createdBy,
                                ),)
        
        print(bookingRef)
        print(petsitterid)
        print(customerid)
        print(status)
        print(data['title'])
        print(data['fname'])
        print(data['sname'])
        print(phone)
        print(data['email'])
        print(data['checkin'])
        print(data['checkout'])
        print(data['price'])
        print(data['numofpets'])
        print(data['type'])
        print(breed)
        print(note)
        print(createdBy)                    
        return bookingRef
    except:
        return "Error"
        
    
    
    
    
def search_petsitter_data(data):
    with DBcm.UseDatabase(connection) as cursor:
        SQL = """SELECT * FROM petsitter
                WHERE CONCAT(petsittername,country,city,town,address) LIKE %s
                """
        cursor.execute(SQL, (('%' + data['location'] + '%'),),)
        return_data = cursor.fetchall()
        return return_data
        
def view_petsitter_data(petsittername):
    with DBcm.UseDatabase(connection) as cursor:
        SQL = """SELECT * FROM petsitter
                WHERE petsittername = %s
                """
        cursor.execute(SQL, (petsittername,),)
        data = cursor.fetchall()
        return data

def str_to_list(data):
    i = 2
    newlist = [] 
    newstring =""
    while i != len(data):
        if i == len(data)-2:
            newlist.append(newstring)
        elif data[i] == "'" and data[i+1] == "," and data[i+2] == " " and data[i+3] == "'":
            newlist.append(newstring)
            newstring = ""
            i = i+3
        else:
            newstring += data[i]
        i = i+1
    return newlist