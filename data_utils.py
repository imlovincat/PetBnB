import DBcm

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

def petsitter_signup_data(user,data):
    try:
        with DBcm.UseDatabase(connection) as cursor:
            SQL = """SELECT id FROM customer WHERE email = %s"""
            cursor.execute(SQL,(user,),)
            return_data = cursor.fetchall()
            customerid = return_data[0][0]
            #customerid = ''.join(str(return_data[0]))
        
        if data.getlist('service[]'): petservice = format(data.getlist('service[]'))
        else: petservice = ""
        if data.getlist('type[]'): pettype = format(data.getlist('type[]'))
        else: pettype = ""
        if data.getlist('size[]'): petsize = format(data.getlist('size[]'))
        else: petsize = ""
        
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