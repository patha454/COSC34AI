### COSC34AI

##Task and notes on complications

Our bot must navigate the floor in the Department lobby, autonomously overcoming any problems.

Task:

#1. Travel 15 black tiles forward over the small black and white tiles.

Compilation: The while tiles are grey, dirty, and speckled. This noise will confuse the bot
Possible solution: Take an average sensor reading for the last (say) 0.2 seconds, not an instant value.
A demon thread will have to run to continually take sensor readings and compute the average for use.

Complication: The light levels in the lobby change throughout the day, and we can not use human intervention to help calberate the bot if we want full marks (we do.)
Possible solution: Firstly, look at change in light intensity, not the specif value to compute tiles passed.
Secondly, At the start of the task, the bot could 'creep' forward to calibrate its sensors before starting out.

#2. Turn right 90 degrease.

Compilation: Matching the exact body turn angle to a wheel turn angle.
Possible solution: Trail and error?

#3. Travel forward over seven *large* white tiles to reach a plastic tower.
Complication: Distinguishing the small and big white tiles: The specifications state the bot can't distinguish their colour reliably.
Possible solution: Use dead reckoning and the sonar for navigation? (How does the sonar work?)

#4. Push the plastic block off the square it's on, and "make a sound" to indicate it's finished? (Anyone want to give it a silly soundclip to play?)



