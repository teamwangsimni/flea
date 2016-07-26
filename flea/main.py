from __future__ import print_function
from RPi import GPIO


DC_TL = 16
DC_TR = 18
DC_BL = 22
DC_BR = 24


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(DC_TL, GPIO.OUT)
    GPIO.setup(DC_TR, GPIO.OUT)
    GPIO.setup(DC_BL, GPIO.OUT)
    GPIO.setup(DC_BR, GPIO.OUT)
