"""
bot.py

bot encapsulates the motors and provides several sensor daemons to
allow more intuitive high level use of the EV3's features

Author: H Paterson
Version: 3
Date: 12/03/18
"""


from ev3dev.ev3 import *
from helper import *
import threading
import time


# The objects used to control the motors.
leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')
motors = LargeMotorPair(OUTPUT_B, OUTPUT_C)


# These are speeds for the motors, in wheel rotations per second.
CRAWL_SPEED = 20
SLOW_SPEED = 50
INTERMEDIATE_SPEED = 100
NORMAL_SPEED = 200
HIGH_SPEED = 300
LIGHT_SPEED = 500
RIDICULOUS_SPEED = 700
LUDICROUS_SPEED = 900


# These are wheel angles required to turn the body a given angle.
NINETY_DEG = 180
QUARTER_TURN = NINETY_DEG
HALF_TURN = 2 * QUARTER_TURN
FULL_TURN = 2 * HALF_TURN
EIGHTH_TURN = QUARTER_TURN / 2


# These indicate turn directions. Their values are significant to some computations.
LEFT = 1
RIGHT = -1

# A small turn for until functions
TURN_QUANTUM = 5


"""
drive_forward drives the bot forward a specified distance (in wheel rotations)
If a speed is not specified, the default NORMAL_SPEED is used.

drive_forward blocks until the maneuver is finished. 

Usage:
drive_forward(some_distance)
drive_forward(some_distance, some_speed)
"""


def drive_forward(distance, speed=NORMAL_SPEED):
    motors.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    motors.wait_while('running')
    return


"""
drive_until drives the bot forward until a condition is met.

drive_until blocks until the maneuver is finishes (so the condition is true.)

Usage:

def aTest():
    if (some_conditions_are_met):
        return True
    else
        return False

drive_until(aTest)
drive_until(aTest, NORMAL_SPEED)
"""


def drive_until(predicate, distance=0, speed=NORMAL_SPEED):
    while not predicate():
        distance += TURN_QUANTUM
        motors.run_to_rel_pos(position_sp=TURN_QUANTUM, speed_sp=speed)
        motors.wait_while('running')
    return distance


"""
 drive_turning_until() drives forward in a turn until a condition is met
"""


def drive_turning_until(predicate, direction, speed=NORMAL_SPEED):
    turn_factor = 1.3
    if direction == LEFT:
        print("left")
        leftMotor.run_forever(speed_sp=speed)
        rightMotor.run_forever(speed_sp=turn_factor * speed)
    else:
        print("right")
        leftMotor.run_forever(speed_sp=turn_factor * speed)
        rightMotor.run_forever(speed_sp=speed)
    while not predicate():
        sleep(0.1)
    leftMotor.stop()
    rightMotor.stop()


"""
turn_left blocks while turning the bot 'distance' degrees left on the spot.

Usage:
turn_left(someDistance)
turn_left(someDistance, someSpeed)

"""


def turn_left(distance, speed=NORMAL_SPEED):
    leftMotor.run_to_rel_pos(position_sp=-distance, speed_sp=speed)
    rightMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    leftMotor.wait_while('running')
    rightMotor.wait_while('running')
    return


"""
turn_right blocks while turning the bot 'distance' degrees right on the spot.

Usage:
turn_right(someDistance)
turn_right(someDistance, someSpeed)

"""


def turn_right(distance, speed=NORMAL_SPEED):
    turn_left(-1 * distance, speed)
    return


"""
curve_left_until curve left until a condition is met, then returns how far 
the bot turned.
"""


def curve_left_until(predicate, distance_turned=0, speed=NORMAL_SPEED):
    while not predicate():
        distance_turned += TURN_QUANTUM
        curve_left(TURN_QUANTUM, speed)
    return distance_turned


"""
curve__right_until turns left until a condition is met, then returns how far 
the bot turned.
"""


def curve_right_until(predicate, distance_turned=0, speed=NORMAL_SPEED):
    while not predicate():
        distance_turned += TURN_QUANTUM
        curve_right(TURN_QUANTUM, speed)
    return distance_turned


"""
curve_right swings the body right without moving the light sensor backward
"""


def curve_right(distance, speed=NORMAL_SPEED):
    leftMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    leftMotor.wait_while('running')


"""
curve_right swings the body right without moving the light sensor backward
"""


def curve_left(distance, speed=NORMAL_SPEED):
    rightMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    rightMotor.wait_while('running')


""" 
waddle_until attempts drives in a shallow zig zag pattern.
This is an attempt to cancel out the course deviation in drive_until.

It is only mildly successful: Users will still need to use sensor 
data to guide the robot.
"""


def waddle_until(predicate, speed=NORMAL_SPEED):
    while not predicate():
        leftMotor.run_to_rel_pos(position_sp=50, speed_sp=speed)
        leftMotor.wait_while('running')
        rightMotor.run_to_rel_pos(position_sp=50, speed_sp=speed)
        rightMotor.wait_while('running')
    return


"""
zig_zag_until() is conceptually the same as waddle_until().

zig_zag_until, however, stops and turns in place.
"""


def zig_zag_until(predicate, speed=NORMAL_SPEED):
    turn_angle = QUARTER_TURN / 4
    facing = LEFT
    turn_left(turn_angle / 2)
    while not predicate():
        drive_forward(45, speed)
        if facing == LEFT:
            turn_right(turn_angle, speed)
            time.sleep(0.05)
            facing = RIGHT
        else:
            turn_left(turn_angle, speed)
            time.sleep(0.05)
            facing = LEFT
    # Time to straighten out
    if facing == LEFT:
        turn_right(turn_angle / 2)
    if facing == RIGHT:
        turn_left(turn_angle / 2)
    return


"""
LightIntensitySensor is a daemon wrapped around the EV3 ColorSensor

LightIntensitySensor takes the average of the 'SENSOR_PRECISION' readings
over the last 'SENSOR_PERIOD' seconds to filter noise from the tiles.

The values SENSOR_PERIOD and SENSOR_PRECISION can be tweaked if needed

Usage:
aSensor = LightIntensitySensor()
aSensor.value()
"""


class LightIntensitySensor:

    # The period of time the sensor averages data over (seconds)
    SENSOR_PERIOD = 0.2

    # The number of data points the sensor saves
    SENSOR_PRECISION = 5

    # Should the thread still run
    alive = True

    sensor = None
    data = []
    sensor_thread = None

    def __init__(self):
        self.sensor = ColorSensor()
        self.sensor.mode = 'COL-REFLECT'
        self.sensor_thread = threading.Thread(target=self.sensor_loop)
        self.sensor_thread.daemon = True
        self.sensor_thread.start()
        # Allow time for the sensor to populate itself with values
        sleep(self.SENSOR_PERIOD)
        return

    def sensor_loop(self):
        while self.alive:
            reading = self.sensor.value()
            if len(self.data) >= self.SENSOR_PRECISION:
                self.data.pop(0)
            self.data.append(reading)
            sleep(self.SENSOR_PERIOD / self.SENSOR_PRECISION)
        return

    """
    value() returns the average sensor reading over the last
    'SENSOR_PERIOD' seconds.
    """
    def value(self):
        average = 0
        for i in range(self.SENSOR_PRECISION):
            average += self.data[i]
        average /= self.SENSOR_PRECISION
        return average

    """
    Terminates the thread
    """
    def kill(self):
        self.alive = False


"""
Sonar is a class tha encapsulates the ultrasound device.

Sonar aims to remove noise by taking the average reading over time.

Sonar return the distance to the object in CM.
"""


class Sonar:

    # The period for the sonar to average, in seconds
    SENSOR_PERIOD = 0.1

    # The samples to take over SENSOR_PERIOD
    SENSOR_SAMPLES = 5

    # Recent readings
    data = []

    # When to kill the thread
    is_alive = True

    # The sonar daemon thread
    daemon = None

    # The device ultrasound sensor
    sensor = None

    def __init__(self):
        self.sensor = UltrasonicSensor()
        self.sensor.mode = 'US-DIST-CM'
        self.daemon = threading.Thread(target=self.sensor_loop)
        self.daemon.deamon = True
        self.daemon.start()
        sleep(self.SENSOR_PERIOD * 1.2)

    """
    sensor_loop: reads and averages the ultrasound range.
    """

    def sensor_loop(self):
        while self.is_alive:
            self.data.append(self.sensor.value())
            if len(self.data) > self.SENSOR_SAMPLES:
                self.data.pop(0)
        return


    """
    value: Returns the time average sonar reading, in cm
    """
    def value(self):
        average = 0
        for i in range(len(self.data)):
            average += self.data[i]
        average /= len(self.data)
        # The values the bot returns are actually mm
        average /= 10
        return average

    """
    kill the thread
    """
    def kill(self):
        self.is_alive = False
