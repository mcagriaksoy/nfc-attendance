import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="R3juvenation",
  database="testdb"
)

mycursor= mydb.cursor()

# adding new lines
# sqlFormula = "INSERT INTO teachers (id, name) VALUES (%s, %s)"
#
# student1 = ("cbe27338", "Buğrahan")

mycursor.execute("SELECT id FROM teachers")

result_list = [x[0] for x in mycursor.fetchall()]
print(result_list[0])
if result_list[0] == 'cbe27338':
    print("match")
else:
    print("mismatch")
