#!/usr/bin/env python3
"""
phase_three.py
phase_three manages the third phase, moving a block off the tile.

The bot should push the block forward until it leaves the tile
the block was located on, stop, and emit a sound.

Author:
Date: 07/03/2018
Version: 1
"""
import bot
from ev3dev.ev3 import *
from time import sleep

"""
push_tower() pushes the tower block off the square it's currently in.

push_tower() assumes that the robot is already in contact with the tower block.
push_tower() will emit a sound after the block is off the square and the bot
has stopped, to indicate completion of the task.
"""


def push_tower():
    bot.drive_forward(-0.5 * bot.FULL_TURN)
    bot.drive_forward(3 * bot.FULL_TURN, bot.LUDICROUS_SPEED)
    Sound.play("src/fin.wav").wait()
    Sound.beep()
    sleep(1)
    Sound.beep()
    return


"""
__main()__ is provided for testing, so push_tower() can be executed
independently of other functions by executing phase_three.py on the bot
"""
if __name__ == "__main__":
    push_tower()
