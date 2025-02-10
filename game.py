# game.py
#
# The top level loop that runs the world until it is clean.
#
# run this using:
#
# python3 game.py
#
# Written by: Simon Parsons
# Modified by: Helen Harman
# Last Modified: 01/02/24

from world import World
from vacuum  import Vacuum
from dirtyEnvironment import DirtyEnvironment
import random
import config
import utils
import time


# How we set the game up. Create a world, then connect player and
# display to it.
gameWorld = World()
player = Vacuum(gameWorld)
display = DirtyEnvironment(gameWorld)


# Show initial state
display.update()
time.sleep(1)

# Now run game...
while not(gameWorld.isEnded()):
    gameWorld.updateVacuum(player.makeMove())
    display.update()
    time.sleep(1)

