# ghostAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
import math

########################################################
# Imports specific to CPSC 481 project
import sys
import pacman
from searchAgents import mazeDirections, mazeDistance
from util import euclideanDistance
########################################################

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()


class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist


##################################################
# CPSC 481 - Blinky, Pinky, Inky, and Clyder
##################################################
class Blinky(GhostAgent):  # Blinky always targets PacMan's position
    def __init__(self, index):
        self.index = index
        self.color = [0.82, 0.01, 0.001]  # Red
        self.isColorSet = False

    def getDistribution(self, state):
        ghost_state = state.getGhostState(self.index)
        pos_x, pos_y = state.getGhostPosition(self.index)
        is_scared = ghost_state.scaredTimer > 0
        ghost_direction = ghost_state.configuration.direction
        walls = state.getWalls()
        top, right = walls.height - 2, walls.width - 2
        corners = ((1, 1), (1, top), (right, 1), (right, top))

        if ghost_direction == Directions.EAST or ghost_direction == Directions.NORTH:
            intpos = (int(math.ceil(pos_x)), int(math.ceil(pos_y)))
        else:
            intpos = (int(math.floor(pos_x)), int(math.floor(pos_y)))

        if is_scared:
            direction_list = []
        else:
            direction_list = mazeDirections(intpos, self.getTargetPosition(state), state, self.index)

        dist = util.Counter()
        if (float(pos_x)).is_integer() is False or (float(pos_y)).is_integer() is False:
            dist[ghost_direction] = 1  # If Ghost is in between tiles, continue previous direction
        else:
            if len(direction_list) == 0:
                dist[state.getLegalActions(self.index)[0]] = 1
            else:
                dist[direction_list[0]] = 1

        # This draws the path our ghost is planning on taking to get to his target..
        import __main__
        if '_display' in dir(__main__):
            if self.isColorSet is False and 'setGhostColor' in dir(__main__._display):
                __main__._display.setGhostColor(self.index, self.color)
                self.isColorSet = True
            if 'drawGhostPath' in dir(__main__._display) and __main__._drawPath:
                cell_list = []  # our list of directions converted into coordinates we then use to draw path
                for direction in direction_list:
                    successor = Actions.getSuccessor(intpos, direction)
                    cell_list.append(successor)
                    intpos = successor
                __main__._display.drawGhostPath(cell_list, self.color)
        dist.normalize()
        return dist

    def getTargetPosition(self, state):
        return state.getPacmanPosition()


class Pinky(GhostAgent):
    # Will be a modified Blinky which targets 4 legal positions ahead of PacMan's current vector.
    def __init__(self, index):
        self.index = index
        self.color = [.92, .51, .9]  # Pink
        self.isColorSet = False

    def getDistribution(self, state):
        ghost_state = state.getGhostState(self.index)
        pos_x, pos_y = state.getGhostPosition(self.index)
        is_scared = ghost_state.scaredTimer > 0
        ghost_direction = ghost_state.configuration.direction
        walls = state.getWalls()
        top, right = walls.height - 2, walls.width - 2
        corners = ((1, 1), (1, top), (right, 1), (right, top))

        if ghost_direction == Directions.EAST or ghost_direction == Directions.NORTH:
            intpos = (int(math.ceil(pos_x)), int(math.ceil(pos_y)))
        else:
            intpos = (int(math.floor(pos_x)), int(math.floor(pos_y)))

        if is_scared:
            direction_list = []
        else:
            direction_list = mazeDirections(intpos, self.getTargetPosition(state), state, self.index)

        dist = util.Counter()
        if (float(pos_x)).is_integer() is False or (float(pos_y)).is_integer() is False:
            if ghost_direction in state.getLegalActions(self.index):
                dist[ghost_direction] = 1  # If Ghost is in between tiles, continue previous direction #TODO: is this fixed?
            else:
                dist[state.getLegalActions(self.index)[0]] = 1
        else:
            if len(direction_list) == 0:
                dist[state.getLegalActions(self.index)[0]] = 1
            else:
                dist[direction_list[0]] = 1

        # This draws the path our ghost is planning on taking to get to his target..
        import __main__
        if '_display' in dir(__main__):
            if self.isColorSet is False and 'setGhostColor' in dir(__main__._display):
                __main__._display.setGhostColor(self.index, self.color)
                self.isColorSet = True
            if 'drawGhostPath' in dir(__main__._display) and __main__._drawPath:
                cell_list = []  # our list of directions converted into coordinates we then use to draw path
                for direction in direction_list:
                    successor = Actions.getSuccessor(intpos, direction)
                    cell_list.append(successor)
                    intpos = successor
                __main__._display.drawGhostPath(cell_list, self.color)
        dist.normalize()
        return dist

    def getTargetPosition(self, state):
        walls = state.getWalls()
        pacman_state = state.getPacmanState()
        pacman_direction = pacman_state.getDirection()
        pac_x, pac_y = state.getPacmanPosition()
        offset_x, offset_y = Actions.getSuccessor((pac_x, pac_y), pacman_direction)
        # changes target to a max of four tiles away from pac-man in the direction pac-man is currently moving
        for i in range(4):
            if pacman_direction == 'North' and not state.hasWall(int(offset_x), int(offset_y) + i):
                pac_y += 1
            elif pacman_direction == 'South' and not state.hasWall(int(offset_x), int(offset_y) - i):
                pac_y -= 1
            elif pacman_direction == 'East' and not state.hasWall(int(offset_x) + i, int(offset_y)):
                pac_x += 1
            elif pacman_direction == 'West' and not state.hasWall(int(offset_x) - i, int(offset_y)):
                pac_x -= 1
            else:
                break
        return pac_x, pac_y

        # Illegal ghost action East, ghostDirection: West, ghostIndex: 2, ghostPosition: (10.0, 5.0), pacmanPosition: (15, 5), pacmanDirection: West
        # Exception: Illegal ghost action East, ghostDirection: West, ghostIndex: 2, ghostPosition: (4.0, 16.0), pacmanPosition: (2, 16), pacmanDirection: East
        # for i in reversed(range(5)):
        #     if pacman_direction == 'North' and (pac_y+i < walls.height and not walls[pac_x][pac_y+i]):
        #         return pac_x, int(math.ceil(pac_y+i))
        #     elif pacman_direction == 'South' and (pac_y-i > 0 and not walls[pac_x][pac_y-i]):
        #         return pac_x, int(math.floor(pac_y-i))
        #     elif pacman_direction == 'East' and (pac_x+i < walls.width and not walls[pac_x+i][pac_y]):
        #         return int(math.ceil(pac_x+i)), pac_y
        #     elif pacman_direction == 'West' and (pac_x-i > 0 and not walls[pac_x-i][pac_y]):
        #         return int(math.floor(pac_x-i)), pac_y
        #     else:
        #         continue
        # return pac_x, pac_y

class Inky(GhostAgent):
    # Inky needs Pac-Man's current tile/orientation and Blinky's current tile to calculate his final target.
    def __init__(self, index):
        self.index = index
        self.color = [.274, .749, .933]  # Cyan
        self.isColorSet = False
        self.initialStateSet = False
        self.initialState = None

    def getDistribution(self, state):
        if self.initialStateSet is False:
            self.initialState = state.deepCopy()
            self.initialStateSet = True
        ghost_state = state.getGhostState(self.index)
        pos_x, pos_y = state.getGhostPosition(self.index)
        is_scared = ghost_state.scaredTimer > 0
        ghost_direction = ghost_state.configuration.direction
        walls = state.getWalls()
        top, right = walls.height - 2, walls.width - 2
        corners = ((1, 1), (1, top), (right, 1), (right, top))

        if ghost_direction == Directions.EAST or ghost_direction == Directions.NORTH:
            intpos = (int(math.ceil(pos_x)), int(math.ceil(pos_y)))
        else:
            intpos = (int(math.floor(pos_x)), int(math.floor(pos_y)))

        if self.initialState.getNumFood() - state.getNumFood() < 30:
            direction_list = []
        else:
            if is_scared:
                direction_list = mazeDirections(intpos, corners[1], state, self.index)
            else:
                direction_list = mazeDirections(intpos, self.getTargetPosition(state), state, self.index)

        dist = util.Counter()
        if (float(pos_x)).is_integer() is False or (float(pos_y)).is_integer() is False:
            dist[ghost_direction] = 1  # If Ghost is in between tiles, continue previous direction
        else:
            if len(direction_list) == 0:
                dist[state.getLegalActions(self.index)[0]] = 1
            else:
                dist[direction_list[0]] = 1

        # This draws the path our ghost is planning on taking to get to his target..
        import __main__
        if '_display' in dir(__main__):
            if self.isColorSet is False and 'setGhostColor' in dir(__main__._display):
                __main__._display.setGhostColor(self.index, self.color)
                self.isColorSet = True
            if 'drawGhostPath' in dir(__main__._display) and __main__._drawPath:
                cell_list = []  # our list of directions converted into coordinates we then use to draw path
                for direction in direction_list:
                    successor = Actions.getSuccessor(intpos, direction)
                    cell_list.append(successor)
                    intpos = successor
                __main__._display.drawGhostPath(cell_list, self.color)
        dist.normalize()
        return dist

    def getTargetPosition(self, state):
        walls = state.getWalls()
        height, width = walls.height, walls.width
        top, right = walls.height - 2, walls.width - 2
        pacman_state = state.getPacmanState()
        pacman_direction = pacman_state.getDirection()
        pac_x, pac_y = state.getPacmanPosition()
        b_x, b_y = state.getGhostPosition(1)
        offset_x, offset_y = Actions.getSuccessor((pac_x, pac_y), pacman_direction)

        # two tile offset from pac-man in the direction pac-man is currently moving
        for i in range(2):
            if pacman_direction == 'North' and not state.hasWall(int(offset_x), int(offset_y) + i):
                pac_y += 1
            elif pacman_direction == 'South' and not state.hasWall(int(offset_x), int(offset_y) - i):
                pac_y -= 1
            elif pacman_direction == 'East' and not state.hasWall(int(offset_x) + i, int(offset_y)):
                pac_x += 1
            elif pacman_direction == 'West' and not state.hasWall(int(offset_x) - i, int(offset_y)):
                pac_x -= 1
            else:
                break

        # throws illegal ghost action similar to pinky
        # for i in reversed(range(3)):
        #     if pacman_direction == 'North' and (pac_y + i < walls.height and not walls[pac_x][pac_y + i]):
        #         pac_y = int(math.ceil(pac_y+i))
        #         break
        #     elif pacman_direction == 'South' and (pac_y - i > 0 and not walls[pac_x][pac_y - i]):
        #         pac_y = int(math.floor(pac_y-i))
        #         break
        #     elif pacman_direction == 'East' and (pac_x + i < walls.width and not walls[pac_x + i][pac_y]):
        #         pac_x = int(math.ceil(pac_x+i))
        #         break
        #     elif pacman_direction == 'West' and (pac_x - i > 0 and not walls[pac_x - i][pac_y]):
        #         pac_x = int(math.floor(pac_x-i))
        #         break
        #     else:
        #         continue

        # mirrors blinky's current position around the two tile offset
        target_x = int(pac_x) + (int(pac_x) - int(b_x))
        target_y = int(pac_y) + (int(pac_y) - int(b_y))
        # out of bounds and illegal target control logic
        if (target_x, target_y) not in [(n, m) for n in range(width) for m in range(height)] \
                or state.hasWall(target_x, target_y):
            # reduces extreme targets to edge coordinates
            if target_x > right:
                target_x = right
            if target_y > top:
                target_y = top
            if target_x < 1:
                target_x = 1
            if target_y < 1:
                target_y = 1
            # finds next best target while target is a wall (always searches toward the center)
            while state.hasWall(target_x, target_y):
                if target_x < width/2 and target_y < height/2:
                    target_x += 2
                    target_y += 2
                elif target_x >= width/2 and target_y < height/2:
                    target_x -= 2
                    target_y += 2
                elif target_x < width/2 and target_y >= height/2:
                    target_x += 2
                    target_y -= 2
                elif target_x >= width/2 and target_y >= height/2:
                    target_x -= 2
        return target_x, target_y


class Clyde( GhostAgent ):
    # Will be a modified Blinky which targets PacMan's position until it is within 8 blocks away, then retreats
    def __init__( self, index):
        self.index = index
        self.color = [.858, .522, .11]  # Orange
        self.isColorSet = False
        self.initialStateSet = False
        self.inactiveCounter = 0

    def getDistribution(self, state):
        if self.initialStateSet is False:
            self.initialState = state.deepCopy()
            self.initialStateSet = True
        ghost_state = state.getGhostState(self.index)
        pos_x, pos_y = state.getGhostPosition(self.index)
        is_scared = ghost_state.scaredTimer > 0
        ghost_direction = ghost_state.configuration.direction
        walls = state.getWalls()
        top, right = walls.height - 2, walls.width - 2
        corners = ((1, 1), (1, top), (right, 1), (right, top))

        if ghost_direction == Directions.EAST or ghost_direction == Directions.NORTH:
            intpos = (int(math.ceil(pos_x)), int(math.ceil(pos_y)))
        else:
            intpos = (int(math.floor(pos_x)), int(math.floor(pos_y)))

        if float(self.initialState.getNumFood())/state.getNumFood() < 1.5 and self.inactiveCounter < 90:
            direction_list = []
            self.inactiveCounter += 1
        else:
            if is_scared:
                direction_list = mazeDirections(intpos, corners[0], state, self.index)
            else:
                direction_list = mazeDirections(intpos, self.getTargetPosition(state), state, self.index)

        dist = util.Counter()
        if (float(pos_x)).is_integer() is False or (float(pos_y)).is_integer() is False:
            dist[ghost_direction] = 1  # If Ghost is in between tiles, continue previous direction
        else:
            if len(direction_list) == 0:
                dist[state.getLegalActions(self.index)[0]] = 1
            else:
                dist[direction_list[0]] = 1

        # This draws the path our ghost is planning on taking to get to his target..
        import __main__
        if '_display' in dir(__main__):
            if self.isColorSet is False and 'setGhostColor' in dir(__main__._display):
                __main__._display.setGhostColor(self.index, self.color)
                self.isColorSet = True
            if 'drawGhostPath' in dir(__main__._display) and __main__._drawPath:
                cell_list = []  # our list of directions converted into coordinates we then use to draw path
                for direction in direction_list:
                    successor = Actions.getSuccessor(intpos, direction)
                    cell_list.append(successor)
                    intpos = successor
                __main__._display.drawGhostPath(cell_list, self.color)
        dist.normalize()
        return dist

    def getTargetPosition(self, state):
        pac_x, pac_y = state.getPacmanPosition()
        pos_x, pos_y = state.getGhostPosition(self.index)
        # list will point cylde home if less than 8 spaces away from pac-man
        if abs(int(pac_x) - pos_x) + abs(int(pac_y) - pos_y) < 8:
            return 1, 1
        else:
            return pac_x, pac_y
##################################################

