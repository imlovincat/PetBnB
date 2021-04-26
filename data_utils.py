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
            SQL = """SELECT id, email FROM customer WHERE email = %s AND password = %s"""
            cursor.execute(SQL, (data["email"], data["password"]),)
            data = cursor.fetchall()
            return data
    except:
        print("Error")

def petsitter_signup_data(data):

    with DBcm.UseDatabase(connection) as cursor:
        SQL = """ INSERT INTO petsitter (email,password) VALUES (%s, %s) """
        cursor.execute(SQL, (data["email"], data["password"]),)