#!/usr/bin/env python3
"""
phase_one.py
This is the script for the first phase of the bot's operation.
phase_one will drive the bot forward over black and white tiles, for a count of
15 black tiles.

After passing 15 black tiles, the bot will turn ninety degrease right and
return control to the caller, ready for the next phase.

Author: H Paterson
Date: 07/03/2018
Version: 3
"""


import bot
from time import sleep
import threading
from ev3dev.ev3 import Sound


# The number of black tiles to drive past
TILE_DISTANCE = 14

"""
drive_off() is the entry function in phaseOne.
Only drive_off() should be used by code outside the module phaseOne.
drive_off() will supervise the bot to drive forward 15 black tiles,
stop, and turn right.

drive_off() will also make a 'distinctive noise' each time a black 
tile is passed.
"""


def drive_off():
    tile_counter = TileCounter()
    bot.zig_zag_until(lambda: tile_counter.tiles_passed >= TILE_DISTANCE, bot.NORMAL_SPEED)
    bot.turn_right(bot.QUATER_TURN)


class TileCounter:
    # The number of black tiles passed
    tiles_passed = 0

    # The previous optical sensor reading
    previous_colour = 0

    # The current optical sensor reading
    current_colour = 0

    # The minimum increase in light intensity from a black to white tile.
    BLACK_THRESHOLD = 2

    # The minimum increase in average light intensity onto a grey line
    GREY_THRESHOLD = 1.2

    # The object to read values from
    average_colour = None

    # The daemonic counter
    counter_thread = None

    # When to kill the thread
    alive = True

    """
    count_tiles() - Counts the number of black tiles passed.
    count_tiles is intended to be run in an independent thread.

    count_tiles looks at the change in light intensity over time.
    A sharp change upward must indicate we have passed from a black 
    tile onto a white tile.

    Absolute values are not used as the ambient light in the test
    environment (Owheo lobby) will change with a number of factors
    beyond our control.
    """

    def count_tiles(self):
        while self.alive:
            if self.current_colour > self.BLACK_THRESHOLD * self.previous_colour:
                Sound.beep()
                self.tiles_passed += 1
            self.previous_colour = self.current_colour
            self.current_colour = self.average_colour.value()
            sleep(self.average_colour.SENSOR_PERIOD * 1.2)
        return

    """
    Initialises the daemon thread.
    """

    def __init__(self):
        self.average_colour = bot.LightIntensitySensor()
        sleep(self.average_colour.SENSOR_PERIOD)
        self.previous_colour = self.average_colour.value()
        self.current_colour = self.previous_colour
        # Start the daemon
        self.counter_thread = threading.Thread(target=self.count_tiles)
        self.counter_thread.daemon = True
        self.counter_thread.start()
        return

    """Shuts down the thread"""

    def kill(self):
        self.average_colour.kill()
        self.alive = False


"""
__main()__ is provided for testing, so drive_off() can be executed
independently of other functions by executing phaseOne.py on the bot
"""
if __name__ == "__main__":
    drive_off()
