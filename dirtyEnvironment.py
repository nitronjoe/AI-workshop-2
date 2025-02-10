# dirtyEnvironment.py
#
# Code to display information about the game in a window.
#
# Shouldn't need modifying --- only changes what gets shown, not what
# happens in the game.
#
# Written by: Simon Parsons. 
# Modified by: Helen Harman
# Last Modified: 01/02/24

from utils import Pose
from graphics import *
import config

class DirtyEnvironment():

    def __init__(self, dungeon):
        # Make a copy of the world an attribute, so that the graphics
        # have access.
        self.gameWorld = dungeon

        # How many pixels the grid if offset in the window
        self.offset = 10
        
        # How many pixels correspond to each coordinate.
        #
        # This works with the current images. any smaller and the
        # images will not fit in the grid.
        self.magnify = 40

        # How big to make "characters" when not using images
        self.cSize = 0.4

        # How big to make objects when not using images.
        self.oSize = 0.6

        # Setup window and draw objects
        self.pane = GraphWin("Vacuum World", ((2*self.offset)+((self.gameWorld.maxX+1)*self.magnify)), ((2*self.offset)+((self.gameWorld.maxY+1)*self.magnify)))
        self.pane.setBackground("white")
        self.drawBoundary()
        self.drawGrid()
        self.drawWalls()
        self.drawVacuum()
        self.drawDirt()

    #
    # Draw the world
    #
    
    # Put a box around the world
    def drawBoundary(self):
        rect = Rectangle(self.convert(0, 0), self.convert(self.gameWorld.maxX+1, self.gameWorld.maxY+1))
        rect.draw(self.pane)

    # Draw gridlines, to visualise the coordinates.
    def drawGrid(self):
        # Vertical lines
        vLines = []
        for i in range(self.gameWorld.maxX+1):
            vLines.append(Line(self.convert(i, 0), self.convert(i, self.gameWorld.maxY+1)))
        for line in vLines:
            line.draw(self.pane)
        # Horizontal lines
        hLines = []
        for i in range(self.gameWorld.maxY + 1):
            hLines.append(Line(self.convert(0, i), self.convert(self.gameWorld.maxX+1, i)))
        for line in hLines:
            line.draw(self.pane)

    #
    # Draw the agents
    #

    # 
    def drawVacuum(self):
        self.vacuum = Image(self.convert2(self.gameWorld.vacuumLoc.x, self.gameWorld.vacuumLoc.y), "images/robot.png")      
        self.vacuum.draw(self.pane)

 
    #
    # Draw the objects
    #
    
    # drawPits()
    #
    # The calculation for agents gives the centre of the
    # square. For a dirt and walls we need to move the x and y to either side of
    # this by 0.5*oSize*magnify.
    def drawDirt(self):
        self.dirt = []
        for i in range(len(self.gameWorld.dirtLoc)):
            centre = self.convert2(self.gameWorld.dirtLoc[i].x, self.gameWorld.dirtLoc[i].y)
            centreX = centre.getX()
            centreY = centre.getY()
            point1 = Point(centreX - 0.5*self.oSize*self.magnify, centreY - 0.5*self.oSize*self.magnify)
            point2 = Point(centreX + 0.5*self.oSize*self.magnify, centreY + 0.5*self.oSize*self.magnify)
            self.dirt.append(Rectangle(point1, point2))
            self.dirt[i].setFill('burlywood2')
        for i in range(len(self.gameWorld.dirtLoc)): 
            self.dirt[i].draw(self.pane)

    
    def drawWalls(self):
        self.dirt = []
        for i in range(len(self.gameWorld.wallLocations)):
            centre = self.convert2(self.gameWorld.wallLocations[i].x, self.gameWorld.wallLocations[i].y)
            centreX = centre.getX()
            centreY = centre.getY()
            point1 = Point(centreX - 0.8*self.oSize*self.magnify, centreY - 0.8*self.oSize*self.magnify)
            point2 = Point(centreX + 0.8*self.oSize*self.magnify, centreY + 0.8*self.oSize*self.magnify)
            self.dirt.append(Rectangle(point1, point2))
            self.dirt[i].setFill('black')
        for i in range(len(self.gameWorld.wallLocations)): 
            self.dirt[i].draw(self.pane)

    
    def update(self):
        for d in self.dirt: 
            d.undraw()
        self.drawDirt()
        self.vacuum.undraw()
        self.drawVacuum()

    # Take x and y coordinates and transform them for using offset and
    # magnify.
    #
    # This conversion works for the lines. 
    def convert(self, x, y):
        newX = self.offset + (x * self.magnify)
        newY = self.offset + (y * self.magnify)
        return Point(newX, newY)

    # Take x and y coordinates and transform them for using offset and
    # magnify.
    #
    # This conversion works for objects, returning the centre of the
    # relevant grid square.
    def convert2(self, x ,y):
        newX = (self.offset + 0.5*self.magnify) + (x * self.magnify)
        newY = (self.offset + 0.5*self.magnify) + (y * self.magnify)
        return Point(newX, newY)
