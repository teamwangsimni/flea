from __future__ import print_function
from RPi import GPIO
from .utils import directions
from .motor import setup_motors, drive


MOTORS = {
    directions.TL: 16,
    directions.TR: 22,
    directions.BL: 18,
    directions.BR: 24,
}



if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    setup_motors(MOTORS)

    # TODO: NOT IMPLEMENTED YET
