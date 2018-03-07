#!/usr/bin/env python3


"""
OTAGO COSC343 Group 2, Assignment 1.
This is the entry point for out bot.
The this code will sequentially execute each of the task's parts and any
exceptions to the screen when they occure.

Author: H Paterson, based on Craig Atkinson's (343 Demonstrator) provided code.
Date: 07/03/108
Version: 1
"""


from ev3dev.ev3 import *
import sys


""" 
main() is the 'entry point' for the robot.
main() will execute driveOff() [task 1], approachTower() [task 2], and
moveTower() [task 3] in sequence.

main() assumes each of the function tasks will block untill the task and the
bot is idle, ready to begin the next phase.
"""
def main():
    # remove the following line and replace with your code
    raise ValueError('A very specific bad thing happened.')


"""
__main__() is the bot's real entry point into the script.
__main__() executes the bot script main(), and catches exceptions for printing
to the console.
"""
try:
    btn = Button()
    main()
except:
    import traceback
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stdout)
    while not btn.any():
        pass
