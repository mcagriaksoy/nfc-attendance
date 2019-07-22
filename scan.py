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

# LEDs GPIO pins,
ledGreen = 17
ledYellow = 27
ledRed = 22

GPIO.setup(ledGreen,OUT)
GPIO.setup(ledYellow,OUT)
GPIO.setup(ledRed,OUT)


def GreenOn(x):
    GPIO.output(ledGreen, GPIO.HIGH)
    time.sleep(x)
    GPIO.output(ledGreen, GPIO.LOW)
def YellowOn():
    GPIO.output(ledYellow, GPIO.HIGH)
    time.sleep(x)
    GPIO.output(ledYellow, GPIO.LOW)
def RedOn(x):
    GPIO.output(ledRed, GPIO.HIGH)
    time.sleep(x)
    GPIO.output(ledRed, GPIO.LOW)

# initialize mysql server to connect to
mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="00An9M2NSl",
    passwd="rk85ywrVcY",
    database="00An9M2NSl"
)
YellowOn(500) #Yellow LED means system is on


mycursor = mydb.cursor()  # define cursor


def teacher_db():

    mycursor.execute("SELECT teacher_id FROM eem475")
    result = [x[0] for x in mycursor.fetchall()]
    return str(result[0])


def attending(id):
    query = "UPDATE eem475 SET absence = '1' WHERE student_id = '{}'".format(id)
    print(query)
    mycursor.execute(query)
    GreenOn(500)


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


def close(signal, frame):
    sys.exit(0)


signal.signal(signal.SIGINT, close)

# Create and initialize an instance of the PN532 class
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()
print('You may begin scanning.')

teacher_detected = False
while not teacher_detected:
    YellowOn(500)
    # Wait for a card to be available
    uid = pn532.read_passive_target()
    # Try again if no card found
    if uid is None:
        continue #no card or bad card detection results in looping
    # Found a card, now try to read block 4 to detect the block type
    last_uid = format(binascii.hexlify(uid))

    print('Card UID 0x{0}'.format(binascii.hexlify(uid)))
    #    # Authenticate and read block 4

    mycursor.execute("SELECT teacher_id FROM eem475")
    result = [x[0] for x in mycursor.fetchall()]
    result = str(result[0])
    if result == last_uid:
        print("Teacher's detected, beginning attendance")
        teacher_detected = True
        YellowOn(500)
    else:
        print("Teacher's not detected, please scan a teacher's card")
        teacher_detected = False
        RedOn(500)

    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue

    time.sleep(DELAY)
print("Student Detection, time= ", time.ctime())
time_end = time.time() + 10
while time.time() < time_end: #begins timing
    YellowOn(500)
    uid = pn532.read_passive_target()
    if uid is None:
        continue  #no card or bad card detection results in looping

    student_uid = format(binascii.hexlify(uid))
    mycursor.execute("SELECT student_id FROM eem475")
    student_list = [x[0] for x in mycursor.fetchall()]

    if student_uid in student_list:
        print("here")
        GreenOn(500)
        student_uid=str(student_uid)
        attending(student_uid)

    else:
        print("absent")
        RedOn(500)

    time.sleep(DELAY)
print("Time is out, no more attendance, time = ", time.ctime())
mydb.commit() #committing changes
mydb.close() #closing connection
