# Farkle-AI

**Farkle,** also known as Henry's Ambition, is a dice game in Kingdom Come: Deliverance that can be played in almost every tavern. 
And the purpose of this project is mainly to simulate the process of player and AI battles.

### Game Rules ###
 - At the beginning of each turn, the player throws all the dice at once.
 - The goal is to be the first one to reach a certain number of points
 - After each throw, one or more scoring dice must be set aside (see sections on scoring below).
 - The player may then either end their turn and bank the score accumulated so far, or continue to throw the remaining dice.
 - If the player has scored all six dice, they have "hot dice" and may continue their turn with a new throw of all six dice, adding to the score they have already accumulated. There is no limit to the number of "hot dice" a player may roll in one turn.
 - If none of the dice score in any given throw, the player has "farkled" and all points for that turn are lost.
 - At the end of the player's turn, the dice are handed to the next player in succession (usually in clockwise rotation), and they have their turn.
 
 https://en.wikipedia.org/wiki/Farkle
 
 ### How to play ###
 Run the src/run.py file with python **version 3.9 (or higher)**
 
 ## To do: ##
 Method ai_strategy(next_states) in the run.py, we need to help the AI determine the actions to execute
