from RPi import GPIO
from ..utils import directions
from .. import config


# =======================
# Module Level Attributes
# =======================

# pwm cache
__pwms__ = {}


# ===
# API
# ===

def setup_motors(motors):
    for _, p in motors.items():
        GPIO.setup(p, GPIO.OUT)


def cleanup_motors(motors):
    for p in motors.values():
        stop_motor(p)
    GPIO.cleanup()


def drive(motors, direction, speed=1):
    assert(0 <= speed and speed <= 1), 'Speed should be between 0 and 1'

    # COMPOSITE DIRECTION
    if direction.is_composite:
        p1 = motors[direction.vertical + direction.horizontal]
        p2 = motors[direction.vertical - direction.horizontal]
        drive_motor(p1, config.CMP_DIR_HORIZONTAL_WEIGHT * speed)
        drive_motor(p2, config.CMP_DIR_HORIZONTAL_OPPOSITE_WEIGHT * speed)
        stop_motors_except_for(motors, (p1, p2))
    # ELEMENTARY DIRECTION (VERTICAL)
    elif direction.is_vertical:
        p1 = motors[direction + directions.LEFT]
        p2 = motors[direction - directions.RIGHT]
        drive_motor(p1, speed)
        drive_motor(p2, speed)
        stop_motors_except_for(motors, (p1, p2))
    # ELEMENTARY DIRECTION (HORIZONTAL)
    elif direction.is_horizontal:
        p1 = motors[direction + directions.TOP]
        drive_motor(p1, speed)
        stop_motors_except_for(motors, (p1,))
    # STOP MOTORS IF NO DIRECTION GIVEN
    else:
        stop_motors_except_for(motors, ())


def drive_motor(motor, dutycycle):
    pwm = _get_pwm(motor)

    # change dutycycle if the motor is already running
    if _is_motor_running(motor):
        pwm.ChangeDutyCycle(dutycycle)
    # start pwm if motor is not running currently
    else: 
        pwm.start(dutycycle)
        pwm.running = True


def stop_motor(motor):
    if _is_motor_running(motor):
        pwm = _get_pwm(motor)
        pwm.stop()
        pwm.running = False


def stop_motors_except_for(motors, excepts):
    for p in motors:
        if p not in excepts:
            stop_motor(p)


# ============
# Internal API
# ============

def _get_pwm(motor):
    try:
        return __pwms__[motor]
    except KeyError:
        pwm = GPIO.PWM(motor, config.PWM_DEFAULT_FREQUENCY)
        __pwms__[motor] = pwm
        return pwm


def _is_motor_running(motor):
    pwm = _get_pwm(motor)
    return getattr(pwm, 'running', False)
