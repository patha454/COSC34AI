#!/usr/bin/env python3
"""
phase_two.py
phase_two manages the second phase of the operation, approaching the tower.

phase_two can use and combination of the sensors available to locate the tower,
as well as dead reckoning - the tower (should) be seven large tiles directly
in front of the bot.

The sonar and bump sensors are suggested by the assessment specifications.

If you use the optical sensor to count tiles as you navigate, allow for the
bot's passage over the small (light and dark) tiles.

Author: Logan Griffin
Date: 07/03/2018
Version: 1
"""

from ev3dev.ev3 import *
import bot
from time import sleep

# creates ultrasonic sensor and puts sensor into distance mode
us = UltrasonicSensor()
us.mode = 'US-DIST-CM'

# reports 'cm' even though sensor measures in 'mm'
units = us.units

"""
approach_tower() drives the bot forward over seven large tiles, and searches for
the plastic tower.

approach_tower will return control when the bot is stopped, and in contact with 
the tower, ready for phase three to begin
"""

DISTANCE_BEFORE_CHECKING = bot.FULL_TURN

THRESHOLD_DISTANCE = 200


def approach_tower():
    # Move within sensor range (2m) of the tower
    bot.drive_forward(2.5 * bot.FULL_TURN, bot.LIGHT_SPEED)
    # points bot in right direction and sets distance to tower
    while not stopping_condition():
        bot.drive_forward(bot.FULL_TURN, bot.LIGHT_SPEED)
        if stopping_condition():
            break
        point_to_tower()
    point_to_tower()
    return


TURNS_TO_MAKE = 8
TOTAL_SCAN = 0.5 * bot.QUARTER_TURN
SMALL_DISTANCE = TOTAL_SCAN / TURNS_TO_MAKE
TURN_FACTOR = 6
MINIMUM_TURN = 2

t1 = TouchSensor('in1')
t2 = TouchSensor('in2')


"""
Stopping condition for phase two
"""


def stopping_condition():
    return us.value() < THRESHOLD_DISTANCE or t1.value() > 0 or t2.value() > 0


"""
Scans to each side and points the bot toward the minimum reading
"""


def point_to_tower():
    DISTANCE = 0
    ANGLE = 1
    left = scan(bot.LEFT)
    right = scan(bot.RIGHT)
    print("l", left[DISTANCE], "r", right[DISTANCE])
    if left[DISTANCE] < right[DISTANCE]:
        print("l", left[ANGLE])
        if (left[ANGLE]) < MINIMUM_TURN:
            return
        bot.turn_left(left[ANGLE]*TURN_FACTOR)
    else:
        print("r", right[ANGLE])
        if (right[ANGLE]) < MINIMUM_TURN:
            return
        bot.turn_right(right[ANGLE]*TURN_FACTOR)
    return


"""
scan() returns an ordered list containing the minimum value found, and 
the angle it was found at
"""


def scan(direction):
    smallest_dist = 3000
    correction_angle = 0
    for angle in range(TURNS_TO_MAKE):
        bot.turn_left(direction * SMALL_DISTANCE)
        sleep(0.05)
        reading = us.value()
        if reading < smallest_dist:
            smallest_dist = reading
            correction_angle = angle
    bot.turn_right(direction * TOTAL_SCAN)
    result = []
    result.append(smallest_dist)
    print("corr", correction_angle)
    result.append(correction_angle)
    return result


"""
__main()__ is provided for testing, so approach_tower() can be executed
independently of other functions by executing phase_one.py on the bot
"""
if __name__ == "__main__":
    approach_tower()
