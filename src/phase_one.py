#!/usr/bin/env python3
"""
phase_one.py
This is the script for the first phase of the bot's operation.
phase_one will drive the bot forward over black and white tiles, for a count of
15 black tiles.

After passing 15 black tiles, the bot will turn ninety degrease right and
return control to the caller, ready for the next phase.

This version uses a new algorithm, as the algorithm used up to V3 was found
Unreliable in testing.

Author: H Paterson
Date: 12/03/2018
Version: 4
"""


import bot
from time import sleep
import threading
from ev3dev.ev3 import *


# The number of black tiles to drive past
TILE_DISTANCE = 14


# The angle used for edge of track avoidance
CORRECTION_ANGLE = bot.QUARTER_TURN / 2


"""
drive_off() is the entry function in phaseOne.
Only drive_off() should be used by code outside the module phaseOne.
drive_off() will supervise the bot to drive forward 15 black tiles,
stop, and turn right.

drive_off() will also make a 'distinctive noise' each time a black 
tile is passed.
"""


def drive_off():
    tile_counter = TileReader()
    tiles_passed = 0
    while tiles_passed < TILE_DISTANCE:
        move_to_next_tile(tile_counter)
        tiles_passed += 1
        Sound.beep()
    bot.turn_right(bot.QUARTER_TURN)


"""
move_to_next_tile() advances the bot to the next black tile.

move_to_next_tile scans for possible course deviations, and computes
an acceptable course.

move_to_next_tile assumes the bot is located on a black tile when
the function is called.
"""


def move_to_next_tile(tile_counter):
    # Check for white to either side
    left_white = check_side(bot.LEFT, tile_counter)
    right_white = check_side(bot.RIGHT, tile_counter)
    # Compute a course correction
    if not left_white and not right_white:
        pass
    elif left_white and not right_white:
        bot.turn_right(CORRECTION_ANGLE / 2)
    elif right_white and not left_white:
        bot.turn_left(CORRECTION_ANGLE / 2)
    # drive forward
    tile_counter.reset()
    bot.drive_until(tile_counter.found_black)


"""
 Searches for white to either side of the tile.
 Returns the angle (relative to the start) where white was found.
"""


def check_side(direction, tile_counter):
    tile_counter.reset()
    bot.turn_left(direction * CORRECTION_ANGLE)
    sleep(tile_counter.colour_sensor.SENSOR_PERIOD)
    bot.turn_right(direction * CORRECTION_ANGLE)
    found_white = tile_counter.found_white
    tile_counter.reset()
    return found_white


class TileReader:

    # The previous optical sensor reading
    previous_colour = 0

    # The current optical sensor reading
    current_colour = 0

    # The light intensify threshold factor indicating going from black to white
    BLACK_THRESHOLD = 2

    # The object to read values from
    colour_sensor = None

    # The daemonic counter
    counter_thread = None

    # Should the thread be killed?
    alive = True

    # Have we found a target matching the parameters?
    found_black = False

    # Ditto
    found_white = False

    """
    scan_tiles() - Scans for new black or white tiles.

    scan_tiles looks at the change in light intensity over time.
    A sharp change upward must indicate we have passed from a black 
    tile onto a white tile; downwards, white to black.

    Absolute values are not used as the ambient light in the test
    environment (Owheo lobby) will change with a number of factors
    beyond our control.
    
    Values can be read from found_black and found_white, before 
    being reset with reset()
    """

    def scan_tiles(self):
        while self.alive:
                if self.current_colour > self.BLACK_THRESHOLD * self.previous_colour:
                    self.found_white = True
                else:
                    if self.current_colour < self.previous_colour / self.BLACK_THRESHOLD:
                        self.found_black = True
                self.previous_colour = self.current_colour
                self.current_colour = self.colour_sensor.value()
                sleep(self.colour_sensor.SENSOR_PERIOD * 1.2)
        return

    """
    Initialises the daemon thread.
    """

    def __init__(self):
        self.colour_sensor = bot.LightIntensitySensor()
        sleep(self.colour_sensor.SENSOR_PERIOD)
        self.previous_colour = self.colour_sensor.value()
        self.current_colour = self.previous_colour
        # Start the daemon
        self.counter_thread = threading.Thread(target=self.scan_tiles)
        self.counter_thread.daemon = True
        self.counter_thread.start()
        return

    """Shuts down the thread"""

    def kill(self):
        self.colour_sensor.kill()
        self.alive = False

    """
    Resets the black tile and white tile alerts
    """

    def reset(self):
        self.found_black = False
        self.found_white = False


"""
__main()__ is provided for testing, so drive_off() can be executed
independently of other functions by executing phaseOne.py on the bot
"""
if __name__ == "__main__":
    drive_off()
