import DBcm

connection = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'petbnb'
}


def customer_signup_data(data):

    with DBcm.UseDatabase(connection) as cursor:
        SQL = """ INSERT INTO customer (email,password) VALUES (%s, %s) """
        cursor.execute(SQL, (data["email"], data["password"]),)


def customer_login_data(data):
    with DBcm.UseDatabase(connection) as cursor:
        SQL = """SELECT id, email FROM customer WHERE email = %s AND password = %s"""
        cursor.execute(SQL, (data["email"], data["password"]),)
        data = cursor.fetchall()
    return data
