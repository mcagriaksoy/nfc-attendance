import mysql.connector


mydb = mysql.connector.connect(
  host="192.168.173.112",
  user="root",
  passwd="R3juvenation",
  database="testdb"
)

mycursor= mydb.cursor()


mycursor.execute("SELECT id FROM teachers")

result_list = [x[0] for x in mycursor.fetchall()]
print(result_list[0])
if result_list[0] == 'cbe27338':
    print("match")
else:
    print("mismatch")
