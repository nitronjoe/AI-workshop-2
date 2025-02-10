# world.py
#
# A file that represents the Vacuum World, keeping track of the
# position of all the objects and the agent, and
# moving them when necessary.
#
# Written by: Simon Parsons
# Modified by: Helen Harman
# Last Modified: 01/02/24

import random
import config
import utils
from utils import Pose
from utils import Actions
from utils import State

class World():

    def __init__(self):

        # Import boundaries of the world. because we index from 0,
        # these are one less than the number of rows and columns.
        self.maxX = config.worldLength - 1
        self.maxY = config.worldBreadth - 1

        # Keep a list of locations that have been used.
        self.locationList = []

        
        # Vacuum
        newLoc = utils.pickRandomPose(self.maxX, self.maxY) # utils.Pose(14, 9)
        self.vacuumLoc = newLoc
        self.locationList.append(newLoc)

        
        # Dirt
        self.dirtLoc = []
        for i in range(config.numberOfDirtyLocs):
            newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
            self.dirtLoc.append(newLoc)
            self.locationList.append(newLoc)


        # Walls
        self.wallLocations = []
        for i in range(config.numberOfWallLocations):
            newLoc = utils.pickUniquePose(self.maxX, self.maxY, self.locationList)
            self.wallLocations.append(newLoc)
            self.locationList.append(newLoc)
            

        # Game state
        self.status = State.PLAY

        
    #--------------------------------------------------
    # Access Methods
    #
    # These are the functions that should be used by Link to access
    # information about the world.

    # Where is the vacuum?
    def getVacuumLocation(self):
        return self.vacuumLoc

    # Where are the dirty locations?
    def getDirtLocations(self):
        return self.dirtLoc
        
    # Get a randomly selected dirty location
    def getAnyDirtyLocation(self):
        return random.choice(self.dirtLoc)

    def isVacuumAtDirtyLocation(self):
        for i in range(len(self.dirtLoc)):
            if utils.sameLocation(self.vacuumLoc, self.dirtLoc[i]):
                return True
        return False
 
    # can the vacuum enter the provided location?
    def isTraversable(self, loc):
        return ( (loc not in self.wallLocations) 
                   and (loc.x >= 0) and (loc.y >= 0) 
                    and (loc.x <= self.maxX) and (loc.y <= self.maxY) )
                    
    # can the vacuum enter the provided x,y position?
    def isXYTraversable(self, x, y):
        return self.isTraversable(utils.Pose(x, y))
 
    #
    # returns the actions that can be taken from the provided location
    def getActions(self, location):
        possibleMoves = []
        
        if self.isXYTraversable(location.x + 1, location.y):
            possibleMoves.append(  Actions.MOVE_RIGHT )
             
        if self.isXYTraversable(location.x - 1, location.y):
            possibleMoves.append( Actions.MOVE_LEFT )
        
        if self.isXYTraversable(location.x, location.y + 1):
            possibleMoves.append( Actions.MOVE_DOWN )
        
        if self.isXYTraversable(location.x, location.y - 1):
            possibleMoves.append( Actions.MOVE_UP )
            
        return possibleMoves
 
    #
    # Methods
    #
    # These are the functions that are used to update and report on
    # world information.

    # Has the game come to an end?
    def isEnded(self):
        if self.status == State.FINISHED:  
            print("Done!")
            return True
        return False
            
    #------------        
            
    # Implements the move 
    def updateVacuum(self, action):
        print("Executing action: ", action.name)
        
        if action == Actions.MOVE_LEFT:
            if self.vacuumLoc.x > 0:
                self.vacuumLoc.x = self.vacuumLoc.x - 1
                
        elif action == Actions.MOVE_RIGHT:
            if self.vacuumLoc.x < self.maxX:
                self.vacuumLoc.x = self.vacuumLoc.x + 1
                
        if action == Actions.MOVE_UP:
            if self.vacuumLoc.y > 0:
                self.vacuumLoc.y = self.vacuumLoc.y - 1
                
        elif action == Actions.MOVE_DOWN:
            if self.vacuumLoc.y < self.maxY:
                self.vacuumLoc.y = self.vacuumLoc.y + 1
                
        elif action == Actions.CLEAN: 
            index = -1
            for i in range(len(self.dirtLoc)):
                if utils.sameLocation(self.vacuumLoc, self.dirtLoc[i]):
                    self.dirtLoc.pop(i)
                    break

        elif action == Actions.STOP:            
            self.status = State.FINISHED
        else: # noops
            pass
            
            
        

        
            
