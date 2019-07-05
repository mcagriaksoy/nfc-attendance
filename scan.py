# Requires Adafruit_Python_PN532

import binascii
import socket
import time
import signal
import sys

import Adafruit_PN532 as PN532

print('PN532 NFC RFID 13.56MHz Card Reading Attendance Software')
# PN532 configuration for a Raspberry Pi GPIO:
t = open("teaclist.txt")
s = open("studlist.txt")

# GPIO 18, pin 12
CS   = 18
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
    print(" last is " , last_uid , type(last_uid))
    print("read from txt" , t.read() , type(t.read()))
    if last_uid == t.read():
        print("Teacher recognized, beginning attendance")
        t_end = time.time()+30  #runs for 30 secs
        while time.time<t_end:
            uid_l= format(binascii.hexlify(pn532.read_passive_target()))
            if uid_l == s.read():
                print ("Student {0} recognized".uid_l)
            else:
                print("Student not recognized")
    else:
        print("Please scan a teacher's card to begin attendance")
    
#    # Authenticate and read block 4
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue

    time.sleep(DELAY)