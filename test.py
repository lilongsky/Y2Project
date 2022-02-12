import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi,cs_pin,debug=False)
ic, ver, rev, support = pn532.firmware_version
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
pn532.SAM_configuration()
while True:
    uid = pn532.read_passive_target(timeout=0.5)
    print('.', end="", flush=True)
    if uid is None:
        continue
    else:
        print('Found card with UID:', [i for i in uid])
        print((str(uid[0]) + str(uid[1])))
        break

