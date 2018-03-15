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

Author: 
Date: 14/03/2018
Version: 1
"""

from ev3dev import ev3
import bot
from time import sleep


# The distance in front of the tower to stop (cm).
# This allows for some delay in the bot actually stopping.
PROXIMITY_THRESHOLD = 15


"""
approach_tower() drives the bot forward over seven large tiles, and searches for
the plastic tower.

approach_tower will return control when the bot is stopped, and in contact with 
the tower, ready for phase three to begin
"""


def approach_tower():
    bot.drive_forward(2 * bot.FULL_TURN)
    scan_approach(bot.NORMAL_SPEED)
    """
    bot.drive_turning_until(lambda: False, bot.LEFT)
    sonar = bot.Sonar()
    while True:
        sleep(sonar.SENSOR_PERIOD)
        print(sonar.value())
    """


"""
scan_approach() drives forward while homing on the minimum sonar value.

scan_approach assumes the tower is to the right of the robot
"""
### Currently overcorrecting near end
### TODO: special case or make chek more freqqunc

def scan_approach(speed):
    sonar_reader = SonarReader()
    direction = bot.RIGHT
    while sonar_reader.value() > PROXIMITY_THRESHOLD:
        print(sonar_reader.value())
        bot.drive_turning_until(sonar_reader.has_increased or sonar_reader.value() < PROXIMITY_THRESHOLD, direction, speed)
        # Reverse the direction
        print("Reversing")
        direction *= -1
    return


"""
SonarReader reads sonar values to tell if the value is increasing.

Depends upon calls to read. We may want to put this into a 
thread to check the sonar regularly
"""


class SonarReader:

    # The previous reading
    previous_reading = 256

    # The current reading
    current_reading = 256

    # The factor to recognise a change in values
    SONAR_THRESHOLD = 1.1

    # The sonar to use
    sonar = None

    def __init__(self):
        self.sonar = bot.Sonar()

    """
    has_increased() checks if the sonar reading has increased.
    """

    def has_increased(self):
        self.previous_reading = self.current_reading
        self.current_reading = self.sonar.value()
        if self.current_reading > self.SONAR_THRESHOLD * self.previous_reading:
            return True
        return False

    """
    Returns the current reading of the sonar
    """
    def value(self):
        self.previous_reading = self.current_reading
        self.current_reading = self.sonar.value()
        return self.current_reading


"""
__main()__ is provided for testing, so approach_tower() can be executed
independently of other functions by executing phase_one.py on the bot
"""
if __name__ == "__main__":
    approach_tower()

