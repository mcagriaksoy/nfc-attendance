import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="R3juvenation",
    database="ogrdb"
)


def update_list(id):
    id1 = id
    query = "UPDATE eem475 SET absence = '1' WHERE student_id = '{}'".format(id)
    print(query)
    mycursor.execute(query)


mycursor = mydb.cursor()
mycursor.execute("SELECT teacher_id FROM eem475")
result = [x[0] for x in mycursor.fetchall()]
result = str(result[0])
mycursor.execute("SELECT teacher_id FROM eem475")
result = [x[0] for x in mycursor.fetchall()]
print(result)
result = str(result[0])
if result == '13f755df':
    mycursor.execute("SELECT student_id FROM eem475")
    student_list = [x[0] for x in mycursor.fetchall()]

    if "12345678" in student_list:
        print("found your guy")
        id = 12345678
        id=str(id)
        update_list(id)
        mycursor.execute("SELECT absence FROM eem475")
        absent = [x[0] for x in mycursor.fetchall()]
        print(absent)

    else:
        print("guy absent")
else:
    print("nah")
mydb.commit() #committing changes
mydb.close() #closing connection