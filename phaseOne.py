#!/usr/bin/env python3
"""
phaseOne.py
This is the script for the first phase of the bot's operation.
phaseOne will drive the bot forward over black and white tiles, for a count of
15 black tiles.

After passing 15 black tiles, the bot will turn ninety degrease right and
return control to the caller, ready for the next phase.

Author: H Paterson
Date: 07/03/2018
Version: 1
"""


"""
driveOff() is the entry function in phaseOne.
Only driveOff() should be used by code outside the module phaseOne.
driveOff() will supervise the bot to drive forward 15 black tiles,
stop, and turn right.

driveOff() will also make a 'distinctive noise' each time a black 
tile is passed.
"""
def driveOff():
    return