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

# creates ultrasonic sensor and puts sensor into distance mode
ultraS = UltrasonicSensor()
ultraS.mode = 'US-DIST-CM'

# reports 'cm' even though sensor measures in 'mm'
units = us.units

"""
approach_tower() drives the bot forward over seven large tiles, and searches for
the plastic tower.

approach_tower will return control when the bot is stopped, and in contact with 
the tower, ready for phase three to begin
"""

DISTANCE_BEFORE_CHECKING = bot.FULL_TURN

def approach_tower():
    # points bot in right direction and sets distance to tower
    distance = point_to_tower()

    # drives bot forward a distance and then points bot in right direction until distance = 0
    while (distance > 0) {
        bot.drive_forward(DISTANCE_BEFORE_CHECKING)
        distance = point_to_tower()   	
    }

    return

""" 
Scans slightly left and right and infront and finds the smallest distance to an 
item infront of it, stops the bot in the position with the sensor in the position
closest to item.
"""

SMALL_DISTANCE = 1
TURNS_TO_MAKE = 20

def point_to_tower(): 
    smallest_distance = us.value()
    found_angle = 0

    # scans left to try find a smaller distance
    for x in range(0, TURNS_TO_MAKE):   
        bot.turn_left(SMALL_DISTANCEi, bot.SLOW_SPEED)
        if (us.value() < smallest_distance) {
	    smallest_distance = us.value()
            found_angle = -(x)
	}
    
    # returns bot to start position
    bot.turn_right(SMALL_DISTANCE * TURNS_TO_MAKE, bot.SLOW_SPEED)

    # scans right to try find a smaller distance
     for y in range(0, TURNS_TO_MAKE):
          bot.turn_right(SMALL_DISTANCE, bot.SLOW_SPEED)
          if (us.value() < smallest_distance) {
              smallest_distance = us.value()
	      found_angle = x
          }

     # returns bot to start position
     bot.turn_left(SMALL_DISTANCE * TURNS_TO_MAKE, bot.SLOW_SPEED)

     if (x < 0) {
     	bot.turn_left(SMALL_DISTANCE * abs(x), bot.SLOW_SPEED)
     } else if (x > 0) {
        bot.turn_right(SMALL_DISTANCE * x, bot.SLOW_SPEED)
     }
    
     return smallest_distance	

"""
__main()__ is provided for testing, so approach_tower() can be executed
independently of other functions by executing phase_one.py on the bot
"""
if __name__ == "__main__":
    approach_tower()
