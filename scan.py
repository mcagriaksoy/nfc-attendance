# Requires Adafruit_Python_PN532
import mysql.connector
import binascii
import socket
import time
import signal
import sys
import Adafruit_PN532 as PN532

# Number of seconds to delay after reading data.
DELAY = 2

# LEDs GPIO pins
GREEN_LED = 17
YELLOW_LED = 27
RED_LED = 22

# GPIO setup
GPIO.setup(GREEN_LED, OUT)
GPIO.setup(YELLOW_LED, OUT)
GPIO.setup(RED_LED, OUT)

def green_on(x):
    ''' This function turns on the green LED for x seconds '''
    GPIO.output(GREEN_LED, GPIO.HIGH)
    time.sleep(x)
    GPIO.output(GREEN_LED, GPIO.LOW)

def yellow_on(x):
    ''' This function turns on the yellow LED for x seconds '''
    GPIO.output(YELLOW_LED, GPIO.HIGH)
    time.sleep(x)
    GPIO.output(YELLOW_LED, GPIO.LOW)

def red_on(x):
    ''' This function turns on the red LED for x seconds '''
    GPIO.output(RED_LED, GPIO.HIGH)
    time.sleep(x)
    GPIO.output(RED_LED, GPIO.LOW)

# initialize mysql server to connect to
mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="00An9M2NSl",
    passwd="rk85ywrVcY",
    database="00An9M2NSl"
)

yellow_on(500) #Yellow LED means system is on
mycursor = mydb.cursor()  # define cursor

def teacher_db():
    ''' This function returns the teacher's id from the database '''

    mycursor.execute("SELECT teacher_id FROM eem475")
    result = [x[0] for x in mycursor.fetchall()]
    return str(result[0])

def attending(id):
    ''' This function updates the database to show that the student is attending '''
    query = "UPDATE eem475 SET absence = '1' WHERE student_id = '{}'".format(id)
    print(query)
    mycursor.execute(query)
    green_on(500)

print('PN532 NFC RFID 13.56MHz Card Reading Attendance Software')
# PN532 configuration for a Raspberry Pi GPIO:
# GPIO 18, pin 12
CS = 18
# GPIO 23, pin 16
MOSI = 23
# GPIO 24, pin 18
MISO = 24
# GPIO 25, pin 22
SCLK = 25
# Configure the key to use for writing to the MiFare card.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Prefix, aka header from the card
HEADER = b'BG'

def close():
    ''' This function closes the program '''
    sys.exit(0)

signal.signal(signal.SIGINT, close)

# Create and initialize an instance of the PN532 class
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()
print('You may begin scanning.')

TEACHER_DETECTED = False
while not TEACHER_DETECTED:
    yellow_on(500)
    # Wait for a card to be available
    uid = pn532.read_passive_target()
    # Try again if no card found
    if uid is None:
        continue #no card or bad card detection results in looping
    # Found a card, now try to read block 4 to detect the block type
    last_uid = format(binascii.hexlify(uid))

    print(f'Card UID 0x{0}'.format(binascii.hexlify(uid)))
    #    # Authenticate and read block 4

    mycursor.execute("SELECT teacher_id FROM eem475")
    result = [x[0] for x in mycursor.fetchall()]
    result = str(result[0])
    if result == last_uid:
        print("Teacher's detected, beginning attendance")
        TEACHER_DETECTED = True
        yellow_on(500)
    else:
        print("Teacher's not detected, please scan a teacher's card")
        TEACHER_DETECTED = False
        red_on(500)

    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue

    time.sleep(DELAY)
print("Student Detection, time= ", time.ctime())
time_end = time.time() + 10
while time.time() < time_end: #begins timing
    yellow_on(500)
    uid = pn532.read_passive_target()
    if uid is None:
        continue  #no card or bad card detection results in looping

    student_uid = format(binascii.hexlify(uid))
    mycursor.execute("SELECT student_id FROM eem475")
    student_list = [x[0] for x in mycursor.fetchall()]

    if student_uid in student_list:
        print("here")
        green_on(500)
        student_uid = str(student_uid)
        attending(student_uid)

    else:
        print("absent")
        red_on(500)

    time.sleep(DELAY)
print("Time is out, no more attendance, time = ", time.ctime())
mydb.commit() #committing changes
mydb.close() #closing connection
