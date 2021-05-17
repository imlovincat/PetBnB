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

def check_duplicate_petsitter_data(petsittername):
    try:
        with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT id FROM petsitter WHERE petsittername = %s"""
                cursor.execute(SQL,(petsittername,),)
                data  = cursor.fetchall()
                if len(data) == 0:
                    return True
                else: return False
    except:
        print("Error") 

def check_petsitter_access_data(petsittername,email):
    try:    
        with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT customer.id FROM customer
                         INNER JOIN petsitter ON (petsitter.customerid = customer.id)
                         WHERE petsitter.petsittername = %s AND customer.email = %s"""
                cursor.execute(SQL,(petsittername,email,),)
                data  = cursor.fetchall()
                if len(data) == 0:
                    return False
                else: return True
    except:
        print("Error") 
    
def confirm_makebooking_data(user,data):
    try:
        createdBy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        bookingRef = "PETBNB" + "00" + str(createdBy[0:4]) + str(createdBy[5:7]) + str(createdBy[8:10]) + str(createdBy[11:13]) + str(createdBy[14:16]) + str(createdBy[17:19]) + str(randint(0,9999))                    
        if user:
            with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT id FROM customer WHERE email = %s"""
                cursor.execute(SQL,(user,),)
                return_data = cursor.fetchall()
                customerid = return_data[0][0]
        else: customerid = 0
        with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT id FROM petsitter WHERE petsittername = %s"""
                cursor.execute(SQL,(data['petsitter'],),)
                return_data = cursor.fetchall()
                petsitterid = return_data[0][0]
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
                      paymentMethod,
                      petQunatity,
                      typeOfPet,
                      breed,
                      note,
                      createdBy,
                      deleteflag
                      ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0) """
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
                                data['payment'],
                                data['numofpets'],
                                data['type'],
                                breed,
                                note,
                                createdBy,
                                ),)

        
        return bookingRef
    except:
        print("Error")
        
def make_payment_data(transactionID, bookingRef):
    createdBy = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    try: 
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """INSERT INTO payment (
                    transactionID,
                    bookingRef,
                    createdBy,
                    canceled
                    ) VALUES (
                    %s,%s,%s,0 
                    )        
                    """
            cursor.execute(SQL, (transactionID, bookingRef, createdBy,),)
            return True
    except:
        print("Error")
    


def search_petsitter_data(data):
    try:
        SQL = """SELECT * FROM petsitter WHERE country = """
        SQL += "'" + data['country'] + "'"
        if data['location'] != '':
            SQL += " AND CONCAT(petsittername,city,town,address) LIKE '%" + data['location'] +"%' "
        if data['numofpet'] != '':
            SQL += "AND petnums >= " + data['numofpet']
        if data['pettype1'] != '':
            SQL += " AND pettype LIKE '%" + data['pettype1'] + "%' "
        if data['pettype2'] != '':
            SQL += " AND pettype LIKE '%" + data['pettype2'] + "%' "  
        if data['pettype3'] != '':
            SQL += " AND pettype LIKE '%" + data['pettype3'] + "%' "
        if data['pettype4'] != '':
            SQL += " AND pettype LIKE '%" + data['pettype4'] + "%' "
        with DBcm.UseDatabase(connection) as cursor:
                cursor.execute(SQL)
                return_data = cursor.fetchall()
                return return_data
    except:
        print("Error")
        
def view_petsitter_data(petsittername):
    with DBcm.UseDatabase(connection) as cursor:
        SQL = """SELECT * FROM petsitter
                WHERE petsittername = %s
                """
        cursor.execute(SQL, (petsittername,),)
        data = cursor.fetchall()
        return data

def petsitter_signed_data(email):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT petsitter.id, petsitter.petsittername FROM petsitter
                    INNER JOIN customer ON (petsitter.customerid = customer.id)
                    WHERE customer.email = %s
                    """
            cursor.execute(SQL, (email,),)
            data = cursor.fetchall()
            return data
    except:
        print("Error")
        
def manages_petsitter_account_data(petsittername,email):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT petsitter.* FROM petsitter
                    INNER JOIN customer ON (petsitter.customerid = customer.id)
                    WHERE petsitter.petsittername = %s AND customer.email = %s
                    """
            cursor.execute(SQL, (petsittername,email,),)
            data = cursor.fetchall()
            return data
    except:
        print("Error")

def petsitter_booking_data(petsittername):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT booking.* FROM booking
                     INNER JOIN petsitter ON (booking.petSitterID = petsitter.id)
                     WHERE petsitter.petsittername = %s AND booking.deleteflag = 0
                  """
            cursor.execute(SQL, (petsittername,),)
            data = cursor.fetchall()
            return data
        
    except:
        print("Error")

def booking_quantity_data(petsittername,status):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT COUNT(*) FROM booking
                     INNER JOIN petsitter ON (booking.petSitterID = petsitter.id)
                     WHERE petsitter.petsittername = %s AND booking.status = %s AND booking.deleteflag = 0
                  """
            cursor.execute(SQL, (petsittername,status,),)
            data = cursor.fetchall()
            return data
        
    except:
        print("Error")

def access_booking_data(bookingRef, email, petsittername):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT COUNT(*) FROM booking
                     INNER JOIN petsitter ON (booking.petSitterID = petsitter.id)
                     INNER JOIN customer ON (petsitter.customerid = customer.id)
                     WHERE booking.bookingRef = %s AND customer.email = %s AND petsitter.petsittername = %s AND booking.deleteflag = 0
                  """
            cursor.execute(SQL, (bookingRef,email,petsittername),)
            data = cursor.fetchall()
        if data[0][0] > 0:
            accessType = "petsitter"
        else:
            with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT COUNT(*) FROM booking
                         INNER JOIN customer ON (booking.customerID = customer.id)
                         WHERE booking.bookingRef = %s AND customer.email = %s AND booking.deleteflag= 0
                      """
                cursor.execute(SQL, (bookingRef,email, ),)
                data = cursor.fetchall()
            if data[0][0] > 0:
                accessType = "customer"
            else: accessType = "guest"    

        return accessType
        
    except:
        print("Error")

def update_booking_data(bookingRef, accessType, status):
    try:
        print("try")
        if "customer" in accessType or "petsitter" in accessType:
            with DBcm.UseDatabase(connection) as cursor:
                SQL = """UPDATE booking
                         SET status = %s
                         WHERE bookingRef = %s
                      """
                cursor.execute(SQL, (status,bookingRef,),)
        print("updated")
    except:
        print("Error")


def check_email_exists_data():
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT email FROM customer"""
            cursor.execute(SQL)
            data = cursor.fetchall()
            return data
    except:
        print("Error")


def list_pettype_data():
    try:
        with DBcm.UseDatabase(connection) as cursor:
                SQL = """SELECT DISTINCT pettype FROM petsitter"""
                cursor.execute(SQL)
                data  = cursor.fetchall()
                pettype = ['dog','cat']
                lastEle = ['other']
                newlist = []
                while len(data) > 0:
                    temp = data.pop()
                    templist = str_to_list(temp[0])
                    while len(templist) > 0:
                        tempElement = templist.pop()
                        if tempElement.lower() not in newlist and tempElement.lower() not in pettype and tempElement.lower() not in lastEle and tempElement != "":
                            newlist.append(tempElement.lower())
                newlist.sort()
                pettype.extend(newlist)
                pettype.extend(lastEle)
                return pettype
                    
    except:
        print("Error")


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