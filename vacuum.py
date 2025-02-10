


# vacuum.py
#
# The code that defines the behaviour of the vacuum. 
#
# Written by: Simon Parsons
# Modified by: Helen Harman
# Last Modified: 01/02/24

import world
import random
import utils
from utils import Actions
from utils import Location
from utils import LocState

from node import Node

import world
import random
import utils
from utils import Actions
from utils import Location
from utils import LocState
from collections import deque
from node import Node


class Vacuum():

    def __init__(self, dirtyEnvironment):
        self.gameWorld = dirtyEnvironment
        self.moves = [Actions.MOVE_LEFT, Actions.MOVE_RIGHT, Actions.MOVE_UP, Actions.MOVE_DOWN, Actions.CLEAN]

        self.path = []
        self.path_index = 0

    def makeMove(self):
        if not self.path:
            vacuumLoc = self.gameWorld.getVacuumLocation()
            dirtyLoc = self.gameWorld.getAnyDirtyLocation()

            # Call Depth-Limited Search with depth limit 10
            self.path = self.depthLimitedSearch(vacuumLoc, dirtyLoc,)

        if self.path_index == len(self.path) and not self.gameWorld.isVacuumAtDirtyLocation():
            return Actions.STOP

        if self.path_index == len(self.path):
            return Actions.CLEAN

        self.path_index = self.path_index + 1
        return self.path[self.path_index - 1]

    def depthFirstSearch(self, start, goal):
        node = Node(start, None, None, 0)
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []

        frontiers = [node]
        explored = set()

        while frontiers:
            node = frontiers.pop()
            explored.add(node)

            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action, node.depth + 1)
                if child not in explored and child not in frontiers:
                    if child.isGoal(goal):
                        print("Found goal")
                        return self.recoverPlan(child)
                    frontiers.append(child)

        print("Failed to find a path")
        return []

    def breadthFirstSearch(self, start, goal):
        node = Node(start, None, None, 0)
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []

        frontiers = deque([node])
        explored = set()

        while frontiers:
            node = frontiers.popleft()
            explored.add(node)

            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action, node.depth + 1)
                if child not in explored and child not in frontiers:
                    if child.isGoal(goal):
                        print("Found goal")
                        return self.recoverPlan(child)
                    frontiers.append(child)

        print("Failed to find a path")
        return []

    def depthLimitedSearch(self, start, goal, limit):
        node = Node(start, None, None, 0)
        if node.isGoal(goal):
            print("Start and end locations are the same")
            return []

        frontiers = [node]
        explored = set()

        while frontiers:
            node = frontiers.pop()
            explored.add(node)

            if node.depth > limit:
                print("cutoff")
                continue

            for action in self.gameWorld.getActions(node.location):
                child = self.createChildNode(node, action, node.depth + 1)

                if child not in explored and child not in frontiers:
                    if child.isGoal(goal):
                        print("Found goal")
                        return self.recoverPlan(child)
                    frontiers.append(child)

        print("Failed to find a path")
        return []

    def createChildNode(self, parent, action, depth):
        if action == Actions.MOVE_RIGHT:
            return Node(utils.Pose(parent.location.x + 1, parent.location.y), parent, action, depth)
        if action == Actions.MOVE_LEFT:
            return Node(utils.Pose(parent.location.x - 1, parent.location.y), parent, action, depth)
        if action == Actions.MOVE_DOWN:
            return Node(utils.Pose(parent.location.x, parent.location.y + 1), parent, action, depth)
        if action == Actions.MOVE_UP:
            return Node(utils.Pose(parent.location.x, parent.location.y - 1), parent, action, depth)

    def recoverPlan(self, child):
        plan = []
        self.recoverPlanRecursive(child, plan)
        return plan

    def recoverPlanRecursive(self, node, plan):
        if node.parent:
            self.recoverPlanRecursive(node.parent, plan)
            plan.append(node.action)
