"""
bot.py

bot encapsulates the motors and provides several sensor daemons to
allow more intuitive high level use of the EV3's features

Author: H Paterson
Version: 2
Date: 11/03/18
"""


from ev3dev.ev3 import *
from helper import *
import threading


# These might be the wrong way around.
leftMotor = LargeMotor('outB')
rightMotor = LargeMotor('outC')
motors = LargeMotorPair(OUTPUT_B, OUTPUT_C)


# These are speeds for the motors, in wheel rotations per second
CRAWL_SPEED = 20
SLOW_SPEED = 50
INTERMEDIATE_SPEED = 100
NORMAL_SPEED = 200
HIGH_SPEED = 300
LIGHT_SPEED = 500
RIDICULOUS_SPEED = 700
LUDICROUS_SPEED = 900

# These are wheel angles required to turn the body a given angle
NINETY_DEG = 180
QUATER_TURN = NINETY_DEG
HALF_TURN = 2 * QUATER_TURN
FULL_TURN = 2 * HALF_TURN
EIGHTH_TURN = QUATER_TURN / 2


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


def drive_until(predicate, speed=NORMAL_SPEED):
    motors.run_forever(speed_sp = speed)
    # motors.run_to_rel_pos(position_sp = 10000, speed_sp = speed)
    while not predicate():
        continue
    motors.stop()
    return


"""
turn_left blocks while turning the bot 'distance' degrees left on the spot.

Usage:
turn_left(someDistance)
turn_left(someDistance, someSpeed)

"""


def turn_left(distance, speed=NORMAL_SPEED):
    leftMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    rightMotor.run_to_rel_pos(position_sp=-distance, speed_sp=speed)
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
    leftMotor.run_to_rel_pos(position_sp=-distance, speed_sp=speed)
    rightMotor.run_to_rel_pos(position_sp=distance, speed_sp=speed)
    leftMotor.wait_while('running')
    rightMotor.wait_while('running')
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
