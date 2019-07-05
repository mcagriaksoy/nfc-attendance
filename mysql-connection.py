import mysql.connector

mydb = mysql.connector.connect(
    host="192.168.173.112",
    user="root",
    passwd="R3juvenation",
    database="testdb"
)
NUM_TEACHERS = 1
mycursor = mydb.cursor()


def access_db(i):

    mycursor.execute("SELECT id FROM teachers")

    result_list = [x[i] for x in mycursor.fetchall()]
    return result_list[i]
