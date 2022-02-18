import time
# import database
import sqlite3

# import PN532
import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI


def read_card():
    print('\n')
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="", flush=True)
    return uid


def uid_check(uid):
    uidstr = str(uid[0])+str(uid[1])
    conninuidc = sqlite3.connect('smartlocker.db')
    cursorinuidc = conninuidc.cursor()
    cursorinuidc.execute('select id from NFCInfo where uid =?', [uidstr])
    if cursorinuidc.fetchall():  # for list empty == False
        flaguc = True
    else:
        flaguc = False
    cursorinuidc.close()
    conninuidc.close()
    return flaguc

def write_card():
    print('new person? input 1 \nold person input 2\n')
    choose = input(int)
    conn = sqlite3.connect('smartlocker.db')
    cursor = conn.cursor()
    if choose == '1':
        print('input persoanl name')
        name = input()
        print('facila recon for 1\ncard for 2\nboth ok for 3')
        perferWay = input(int)
        print('input email')
        email = input()
        print('read new card')
        uid = read_card()
        cursor.execute('insert into ownerinfo(name,perferWay,email) values (?,?,?)', ([name],[perferWay],[email]))
        cursor.execute('select id from NFCInfo where name =?',[name])
        id = cursor.fetchone()
        cursor.execute('insert into nfcinfo(id,uid) values (?,?)',(id,uid))
    elif choose == '2':
        cursor.execute('select id,name from ownerinfo;')
        ownerinfo = cursor.fetchall()
        print('current user info')
        print(ownerinfo)
        print('\ninput choose user id\n')
        chooseid = input(int)
        cursor.execute('select id from NFCInfo where id =?', [chooseid])
        if cursor.fetchall() is not None:
            print('read new card')
            uid = read_card()
            cursor.execute('insert into nfcinfo(id,uid) values (?,?)', (chooseid, uid))
        else:
            print('wrong id!')
    else:
        print('wrong input!')
    cursor.close()
    conn.commit()
    conn.close()
    return

def wrong_card(uid):
    conn = sqlite3.connect('smartlocker.db')
    cursor = conn.cursor()
    cursor.execute('insert into failopen(uid) values (?)', [str(uid[0]) + str(uid[1])])
    cursor.close()
    conn.commit()
    conn.close()
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
print('read card function input \033[1;31m1\033[0m \nwrite card function input \033[1;31m2\033[0m')
choose = '0'
choose = input()
if choose == '1':
    while flag:
        flag = True
        uid = read_card()
        if uid is None:
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
            wrong_card(uid)
            time.sleep(1)
if choose == '2':
    write_card()
else
    print('wrong Input')

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
