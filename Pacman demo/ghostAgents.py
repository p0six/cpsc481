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
# CPSC 481 - Blinky, Pinky, Inky, and Clyde
##################################################
class Blinky(GhostAgent):
    # Blinky always targets PacMan's position, currently using BFS
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector(a, speed) for a in legalActions]
        newPositions = [(pos[0]+a[0], pos[1]+a[1]) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        pos_x, pos_y = pos
        intpos = (int(pos_x), int(pos_y))  # pos returns floats, but we need ints.

        # returns a list of directions like... North, South, South, East, etc..
        direction_list = mazeDirections(intpos, pacmanPosition, state)

        # Select best action for Blinky given the state
        distancesToPacman = [euclideanDistance (pos, pacmanPosition) for pos in newPositions ]
        dist = util.Counter()
        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
            bestActions = [action for action, distance in zip(legalActions, distancesToPacman) if distance == bestScore]

            # Construct distribution
            for a in bestActions: dist[a] = bestProb / len(bestActions)
            for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        else:
            if direction_list[0] in legalActions:  # action is legal.. proceed
                dist[direction_list[0]] = 1
            else:  # select the first action from list of legal actions, update direction list to indicate new path
                successor = Actions.getSuccessor(intpos, legalActions[0])  # an (x,y) tuple representing new location
                pos_x, pos_y = successor
                intpos = (int(pos_x), int(pos_y))
                direction_list = mazeDirections(intpos, pacmanPosition, state)
                dist[legalActions[0]] = 1

        # cell_list is the list of directions converted into grid coordinates for use with our draw function..
        cell_list = []
        for direction in direction_list:
            successor = Actions.getSuccessor(intpos, direction)
            cell_list.append(successor)
            intpos = successor

        # This draws the path our ghost is planning on taking to get to his target..
        import __main__
        if '_display' in dir(__main__):
            if 'drawExpandedCells' in dir(__main__._display):
                __main__._display.drawExpandedCells(cell_list)
        dist.normalize()
        return dist

class Pinky( GhostAgent ):
    # Pinky not yet complete.  Will be a modified Blinky which targets 4 legal positions ahead of PacMan's current vector.
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution(self, state):
        # Read variables from state
        ghost_state = state.getGhostState(self.index)
        # print(ghost_state)
        legal_actions = state.getLegalActions(self.index)
        # print(legal_actions)
        pos = state.getGhostPosition(self.index)
        # print(pos)
        is_scared = ghost_state.scaredTimer > 0
        # print(is_scared)

        speed = 1
        if is_scared: speed = 0.5

        action_vectors = [Actions.directionToVector(a, speed) for a in legal_actions]
        # print(action_vectors)
        new_positions = [(pos[0]+a[0] + 4, pos[1]+a[1] + 4) for a in action_vectors]
        # print(new_positions)
        pacman_position = state.getPacmanPosition()
        # print(pacman_position)

        # print(state)

        # Select best action for Pinky given the state
        distances_to_pacman = [euclideanDistance(pos, pacman_position) for pos in new_positions]
        # print(distances_to_pacman)
        if is_scared:
            best_score = max(distances_to_pacman)
            best_prob = self.prob_scaredFlee
        else:
            best_score = min(distances_to_pacman)
            best_prob = self.prob_attack
        # print(best_score)
        # print(best_prob)
        best_actions = [action for action, distance in zip(legal_actions, distances_to_pacman) if distance == best_score]
        # print(best_actions)

        # Construct distribution
        dist = util.Counter()
        for a in best_actions: dist[a] = best_prob / len(best_actions)
        for a in legal_actions: dist[a] += (1 - best_prob) / len(legal_actions)
        dist.normalize()
        # print(dist)
        # exit(0)
        return dist


class Inky ( GhostAgent ):
    # Inky not yet complete. Inky needs Pac-Man's current tile/orientation and Blinky's current tile to calculate his final target.
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

        # Select best action or Pinky given the state
        distancesToPacman = [euclideanDistance ( pos, pacmanPosition ) for pos in newPositions ]
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
        for a in legalActions: dist[a] += (1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

class Clyde( GhostAgent ):
    # Cldye not yet complete.  Will be a modified Blinky which targets PacMan's position until it is within 8 blocks away
    # at which point it will retreat to the corner until it is no longer 8 blocks from PacMan, at which point it
    # immediately begins chasing PacMan again.
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

        # Select best actionf or Pinky given the state
        distancesToPacman = [euclideanDistance ( pos, pacmanPosition ) for pos in newPositions ]
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

