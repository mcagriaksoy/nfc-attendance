# Requires Adafruit_Python_PN532
import mysql.connector
import binascii
import socket
import time
import signal
import sys
import Adafruit_PN532 as PN532

# initialize which server to connect to
mydb = mysql.connector.connect(
    host="192.168.173.112",
    user="root",
    passwd="R3juvenation",
    database="testdb"
)
mycursor = mydb.cursor()  # define cursor
i=0

def teacher_db():
    mycursor.execute("SELECT id FROM teachers")

    result_list = [x[0] for x in mycursor.fetchall()]
    return result_list[0]

def student_db():
    mycursor.execute("SELECT id FROM students")

    result_list = [x[0] for x in mycursor.fetchall()]
    return result_list[0]



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

# Configure the key to use for writing to the MiFare card.  You probably don't
# need to change this from the default below unless you know your card has a
# different key associated with it.
CARD_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Number of seconds to delay after reading data.
DELAY = 2

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
while True:
    # Wait for a card to be available
    uid = pn532.read_passive_target()
    # Try again if no card found
    if uid is None:
        continue
    # Found a card, now try to read block 4 to detect the block type
    last_uid = format(binascii.hexlify(uid))

    print('Card UID 0x{0}'.format(binascii.hexlify(uid)))
    #    # Authenticate and read block 4

    if last_uid == teacher_db(i):
        print("Teacher Recognized!")
        time_end=time.time()
        while time_end<time.time.time()+30:
            uid = pn532.read_passive_target()
            last_uid = format(binascii.hexlify(uid))
            if last_uid == student_db():
                print("Student detected ")
            else:
                print("Student not detected")
            
    else:
        print("Scan Teacher's ID to begin attendance system")



    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue

    time.sleep(DELAY)
