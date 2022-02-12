import time
# import database
import sqlite3

# import PN532
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI


def read_card():
    uid = pn532.read_passive_target(timeout=0.5)
    return uid


def uid_check(uid):
    uidstr = str(uid[0])+str(uid[1])
    conninuidc = sqlite3.connect('smartlocker.db')
    cursorinuidc = conninuidc.cursor()
    cursorinuidc.execute('select id from NFCInfo where uid =?', [uidstr])
    if cursorinuidc.fetchall():  # for list empty == False
        flag = True
    else:
        flag = False
    cursorinuidc.close()
    conninuidc.close()
    return flag

def write_card():

    return

def wrong_card():

    return

# initialize PN532
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)
ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))
pn532.SAM_configuration()

# temp UI
print('creat database input \033[1;31m1\033[0m to initialize database\notherwise input \033[1;31m0\033[0m')
choose = input()
if choose == '1':
    conn = sqlite3.connect('smartlocker.db')
    f = open(r'smartlockerinitialize.sql')
    cursor = conn.cursor()
    cursor.executescript(f.read())
    cursor.close()
    conn.commit()
    conn.close()
    print('datebase build')
# print('read card function input 1\nwrite card function input 2')
# choose = 0;
# choose = input(int)

# test data
print('create testdata input \033[1;31m1\033[0m to initialize database\notherwise input 0')
choose = input()
if choose == '1':
    conn = sqlite3.connect('smartlocker.db')
    f = open(r'testdata.sql')
    cursor = conn.cursor()
    cursor.executescript(f.read())
    cursor.close()
    conn.commit()
    conn.close()
flag = True
print("Waiting for RFID/NFC card...")
while flag:
    flag = True
    uid = read_card()
    if uid is None:
        print('.', end="", flush=True)
        continue
    if uid_check(uid):
        print('\ndoor open')
        conn = sqlite3.connect('smartlocker.db')
        cursor = conn.cursor()
        cursor.execute('insert into nfcopen(uid) values (?)', [str(uid[0]) + str(uid[1])])
        cursor.close()
        conn.commit()
        conn.close()
        flag = False
    else:
        print('\nfail authorisation\n')
        print("Waiting for RFID/NFC card...")
        wrong_card()
        time.sleep(1)