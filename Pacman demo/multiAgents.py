# multiAgents.py
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

from __future__ import division
from util import manhattanDistance
from game import Directions
import random, util


from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        # print bestScore
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        # print bestIndices
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
                

        dist_from_ghost = 0
        for index, newGhostState in enumerate(newGhostStates):
            dist_from_ghost = manhattanDistance(newPos,newGhostState.getPosition())
            if (dist_from_ghost <= 1):
                return float("-inf")

        food_available = []
        food_data = []
        food_distance = 0
        
        for i in range(0,newFood.width):
            for j in range(0,newFood.height):
                if (newFood[i][j] == True):
                    food_location = (i,j)
                    food_available.append(food_location)
        
        successor_food_count = len(food_available)
        
        if successor_food_count == 0:
            return float("inf")
        
        for food_loc in food_available:
            food_distance = manhattanDistance(newPos,food_loc)
            food_data.append(food_distance)
        
        closest_food_dist = min(food_data)
        
        current_food_count = currentGameState.getNumFood()
        
        if (successor_food_count < current_food_count):
            return 1000

        score = 0.0
        score = (10*(1/closest_food_dist))
        return score


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        
        root_value = self.value(gameState,0,self.index)
        action = root_value[1]
        return action
        
    def value(self,gameState,CurrentDepth,agentIndex):
        
        if agentIndex == gameState.getNumAgents():
            CurrentDepth = CurrentDepth + 1
            agentIndex = agentIndex = 0
            
        legal_action = []
        legal_action = gameState.getLegalActions(agentIndex)
        
        if len(legal_action) == 0:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        if CurrentDepth == self.depth:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        if agentIndex == 0:
            return self.max_value(gameState,CurrentDepth,agentIndex)
        else:
            return self.min_value(gameState,CurrentDepth,agentIndex)
        
    def max_value(self,gameState,CurrentDepth,agentIndex):
        
        node_value = [-float("inf")]
        
        action_possible = []
        action_possible = gameState.getLegalActions(agentIndex)
        
        for action in action_possible:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1)

            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue >= node_value[0]):
                node_value = [successor_evalvalue,action]

        return node_value
    
    def min_value(self,gameState,CurrentDepth,agentIndex):
        
        node_value = [float("inf")]
        
        action_list = []
        action_list = gameState.getLegalActions(agentIndex)
                
        for action in action_list:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1)
            
            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue <= node_value[0]):
                node_value = [successor_evalvalue,action]

        return node_value
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        root_value = self.value(gameState,0,self.index,-float("inf"),float("inf"))
        action = root_value[1]
        return action
        
    def value(self,gameState,CurrentDepth,agentIndex,alpha,beta):
        
        if agentIndex == gameState.getNumAgents():
            CurrentDepth = CurrentDepth + 1
            agentIndex = agentIndex = 0
        
        if CurrentDepth == self.depth:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        legal_action = []
        legal_action = gameState.getLegalActions(agentIndex)
        
        if len(legal_action) == 0:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        if agentIndex == 0:
            return self.max_value(gameState,CurrentDepth,agentIndex,alpha,beta)
        else:
            return self.min_value(gameState,CurrentDepth,agentIndex,alpha,beta)
        
    def max_value(self,gameState,CurrentDepth,agentIndex,alpha,beta):
        
        node_value = [-float("inf")]
        
        action_list = []
        action_list = gameState.getLegalActions(agentIndex)
        
        for action in action_list:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1,alpha,beta)

            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue >= node_value[0]):
                node_value = [successor_evalvalue,action]
            
            max_value = node_value[0]
            
            if max_value > beta:
                return node_value
            
            alpha = max(max_value,alpha)

        return node_value
    
    def min_value(self,gameState,CurrentDepth,agentIndex,alpha,beta):
        
        node_value = [float("inf")]
        
        action_list = []
        action_list = gameState.getLegalActions(agentIndex)
                
        for action in action_list:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1,alpha,beta)
            
            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue <= node_value[0]):
                node_value = [successor_evalvalue,action]
                
            min_value = node_value[0]
            
            if min_value < alpha:
                return node_value
            
            beta = min(min_value,beta)

        return node_value

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        root_value = self.value(gameState,0,self.index)
        action = root_value[1]
        return action
        
    def value(self,gameState,CurrentDepth,agentIndex):
        
        if agentIndex == gameState.getNumAgents():
            CurrentDepth = CurrentDepth + 1
            agentIndex = agentIndex = 0
            
        legal_action = []
        legal_action = gameState.getLegalActions(agentIndex)
        
        if len(legal_action) == 0:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        if CurrentDepth == self.depth:
            eval_value =  self.evaluationFunction(gameState)
            return [eval_value]
        
        if agentIndex == 0:
            return self.max_value(gameState,CurrentDepth,agentIndex)
        else:
            return self.min_value(gameState,CurrentDepth,agentIndex)
        
    def max_value(self,gameState,CurrentDepth,agentIndex):
        
        node_value = [-float("inf")]
        
        action_possible = []
        action_possible = gameState.getLegalActions(agentIndex)
        
        for action in action_possible:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1)

            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue >= node_value[0]):
                node_value = [successor_evalvalue,action]

        return node_value
    
    def min_value(self,gameState,CurrentDepth,agentIndex):
        
        node_value = [float("inf")]
        
        action_list = []
        action_list = gameState.getLegalActions(agentIndex)
                
        for action in action_list:
            successor_state = gameState.generateSuccessor(agentIndex, action)
            successor_evalvalue = self.value(successor_state, CurrentDepth, agentIndex + 1)
            
            successor_evalvalue = successor_evalvalue[0] 
            
            if (successor_evalvalue <= node_value[0]):
                node_value = [successor_evalvalue,action]

        return node_value


def betterEvaluationFunction(currentGameState, action):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    current_food_count = currentGameState.getNumFood()
    
    if current_food_count == 0:
        return float("inf")
    
    dist_from_ghost = 0
    
    newGhostStates = currentGameState.getGhostStates()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
        
    for ghostState in newGhostStates:
        dist_from_ghost = manhattanDistance(newPos,ghostState.getPosition())
        if (dist_from_ghost <= 1):
            return float("-inf")
        
    food_available = []
    food_data = []
    food_distance = 0
    
    for i in range(0,newFood.width):
        for j in range(0,newFood.height):
            if (newFood[i][j] == True):
                food_location = (i,j)
                food_available.append(food_location)
                
    for food_loc in food_available:
        food_distance = manhattanDistance(newPos,food_loc)
        food_data.append(food_distance)
    
    closest_food_dist = min(food_data)
        
    score = 0.0
    
    score = (5*(-closest_food_dist)+(200*(-current_food_count)))
    
    return score

# Abbreviation
better = betterEvaluationFunction

##################
# CPSC 481
##################
class CPSC481Agent(Agent):
    """
    An agent to drive PAC-MAN's behavior.
    """

    def getAction(self, gameState):
        # Collect legal moves and successor states
        # legalMoves = gameState.getLegalActions()
        legalMoves = gameState.getBetterPacmanActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        # CPSC 481 - Call a function that adjust weights....
        import __main__
        if __main__.__dict__['_reinforcementLearning']:
            gameState.weights = __main__.__dict__['_weights']
            self.adjustWeights(gameState, legalMoves[chosenIndex])

        return legalMoves[chosenIndex]

    def adjustWeights(self, currentGameState, action):
        import __main__
        if __main__.__dict__['_reinforcementLearning']:
            weights = __main__.__dict__['_weights']

            # I need to check whether this particular state is the first state in the game....
            ghostDistanceValue = self.ghostDistance(currentGameState, action)
            powerPelletValue = self.powerPellet(currentGameState, action)
            nearerToFoodValue = self.nearerToFood(currentGameState, action)
            # scoreDifferenceValue = self.scoreDifference(currentGameState, action)
            foodEatenValue = self.foodEaten(currentGameState, action)
            # scoreChangeValue = self.scoreChange(currentGameState, action)
            didGameLoseValue = self.didGameLose(currentGameState, action)
            ghostDistanceToNearestValue = self.ghostDistanceToNearest(currentGameState, action)
            # nextFeatureValues = [ghostDistanceToNearestValue, ghostDistanceValue, powerPelletValue, nearerToFoodValue,
            #                      scoreDifferenceValue, foodEatenValue, scoreChangeValue, didGameLoseValue]
            nextFeatureValues = [ghostDistanceToNearestValue, ghostDistanceValue, powerPelletValue, nearerToFoodValue,
                                 foodEatenValue]

            if len(currentGameState.explored) == 0:  # This is the first state of the game... set initial values.
                __main__.__dict__['_featureValues'] = nextFeatureValues  # this may or may not ever happen...
            else:  # We have made at least one move.. we can compare featureValues...
                # I need to check in __main__.__dict__['_featureValues'] to see if it exists....
                if '_featureValues' in __main__.__dict__:
                    currentFeatureValues = __main__.__dict__['_featureValues']

                    # Could be used to compare old qValues to new qValues to determine if the change was an upgrade
                    # TODO: Currently not used...
                    newqValue = oldqValue = 0
                    for index, nextFeatureValue in enumerate(nextFeatureValues):
                        newqValue += weights[index] * nextFeatureValue
                        oldqValue += weights[index] * currentFeatureValues[index]
                    # for index, currentFeatureValue in enumerate(currentFeatureValues):
                    #     oldqValue += weights[index] * currentFeatureValue
                else:
                    currentFeatureValues = nextFeatureValues  # condition occurs once. initialization happens below

                # Iterate through both featureValues, adjust weight of feature with biggest difference...
                differences = []
                for index, currentFeatureValue in enumerate(currentFeatureValues):
                    currentFeatureValue *= weights[index]
                    nextFeatureValue = nextFeatureValues[index] * weights[index]
                    differences.append(abs(nextFeatureValue - currentFeatureValue))  # if > 0, new state is better

                # Determine which feature is responsible for the biggest change in value from current to next. Blame it.
                biggestDifference = max(differences)
                biggestDifferenceIndices = [index for index in range(len(differences)) if differences[index] == biggestDifference]
                chosenIndex = random.choice(biggestDifferenceIndices)  # Pick randomly among the best

                # Make a change to the weight responsible for the biggest difference in qValue
                # This thing can be improved.... specifically to handle negatives when comparing things.
                # if nextFeatureValues[chosenIndex] - currentFeatureValues[chosenIndex] > 0:
                #     # if weights[chosenIndex] < .81:
                #     weights[chosenIndex] += .1
                # elif nextFeatureValues[chosenIndex] - currentFeatureValues[chosenIndex] < 0:
                #     if weights[chosenIndex] >= .11:
                #         weights[chosenIndex] -= .1
                if nextFeatureValues[chosenIndex] - currentFeatureValues[chosenIndex] > 0:
                    weights[chosenIndex] += .1
                # if nextFeatureValues[chosenIndex] - currentFeatureValues[chosenIndex] > 0:
                #     if weights[chosenIndex] <= 1.9:
                #         weights[chosenIndex] += .1
                # if nextFeatureValues[chosenIndex] - currentFeatureValues[chosenIndex] > 0:
                #     weights[chosenIndex] += .1

                __main__.__dict__['_weights'] = weights
                __main__.__dict__['_featureValues'] = nextFeatureValues

    def evaluationFunction(self, currentGameState, action):
        #################################################################
        # CPSC 481 - we bring in some weights....
        #################################################################
        ghostDistanceValue = self.ghostDistance(currentGameState, action)
        powerPelletValue = self.powerPellet(currentGameState, action)
        nearerToFoodValue = self.nearerToFood(currentGameState, action)
        # scoreDifferenceValue = self.scoreDifference(currentGameState, action)
        foodEatenValue = self.foodEaten(currentGameState, action)
        # scoreChangeValue = self.scoreChange(currentGameState, action)
        # didGameLoseValue = self.didGameLose(currentGameState, action)
        ghostDistanceToNearestValue = self.ghostDistanceToNearest(currentGameState, action)
        # nextFeatureValues = [ghostDistanceToNearestValue, ghostDistanceValue, powerPelletValue, nearerToFoodValue, scoreDifferenceValue,
        #                      foodEatenValue, scoreChangeValue, didGameLoseValue]
        nextFeatureValues = [ghostDistanceToNearestValue, ghostDistanceValue, powerPelletValue, nearerToFoodValue,
                             foodEatenValue]

        import __main__
        qValue = 0
        if __main__.__dict__['_reinforcementLearning']:
            currentGameState.weights = __main__.__dict__['_weights']
            for index, nextFeatureValue in enumerate(nextFeatureValues):
                qValue += currentGameState.weights[index] * nextFeatureValue
        else:
            for index, nextFeatureValue in enumerate(nextFeatureValues):
                qValue += nextFeatureValue

        return qValue

    def ghostDistance(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newGhostStates = successorGameState.getGhostStates()
        ghost_dist_diff = 0
        for index, newGhostState in enumerate(newGhostStates):
            pacman_position = currentGameState.getPacmanPosition()
            ghost_position = currentGameState.getGhostStates()[index].getPosition()
            distance = manhattanDistance(ghost_position, pacman_position)
            ghost_position_next = newGhostState.getPosition()
            distance_next = manhattanDistance(ghost_position_next, newPos)
            if currentGameState.getGhostStates()[index].scaredTimer == 0:  # if the ghost is not scared...
                if distance_next < distance:  # if the ghost is now closer to pacman...
                    ghost_dist_diff -= 1
                elif distance_next > distance:
                    ghost_dist_diff += 1
            else:  # ghost is scared..
                if distance_next < distance:
                    ghost_dist_diff += 1
                elif distance_next > distance:
                    ghost_dist_diff -= 1

        # return ghost_dist_diff
        if ghost_dist_diff < 0:
            return -1
        elif ghost_dist_diff >= 0:
            return 1

    def ghostDistanceToNearest(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        ghost_distances = [manhattanDistance(currentGameState.getPacmanPosition(), ghost.getPosition())
                           for index, ghost in enumerate(currentGameState.getGhostStates())]
        closest_ghost = min(ghost_distances)

        ghost_distances_next = [manhattanDistance(successorGameState.getPacmanPosition(), ghost.getPosition())
                           for index, ghost in enumerate(successorGameState.getGhostStates())]
        closest_ghost_next = min(ghost_distances_next)

        if closest_ghost_next <= 1:
            return -9999

        if closest_ghost_next >= closest_ghost:
            return 1
        # elif closest_ghost_next == closest_ghost:
        #     return 0.5
        else: # closest_ghost_next < closest_ghost:
            return -1

    def powerPellet(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        curGhostStates = currentGameState.getGhostStates()
        newGhostStates = successorGameState.getGhostStates()
        curScaredTimes = [ghostState.scaredTimer for ghostState in curGhostStates]
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        if newScaredTimes > curScaredTimes:
            return 2
        else:
            return 1

    def nearerToFood(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        currentDistanceToFood = self.distanceToNearestFood(currentGameState)
        successorDistanceToFood = self.distanceToNearestFood(successorGameState)
        if successorDistanceToFood <= currentDistanceToFood:
            return 1
        elif successorDistanceToFood > currentDistanceToFood:
            return -1

    def distanceToNearestFood(self, currentGameState):
        curPos = currentGameState.getPacmanPosition()
        curFood = currentGameState.getFood()
        new_food_available = []
        food_data = []

        for i in range(0, curFood.width):
            for j in range(0, curFood.height):
                if (curFood[i][j] == True):
                    food_location = (i, j)
                    new_food_available.append(food_location)

        successor_food_count = len(new_food_available)

        if successor_food_count == 0:
            return float("inf")

        for food_loc in new_food_available:
            food_distance = manhattanDistance(curPos, food_loc)
            food_data.append(food_distance)
        return min(food_data)

    def scoreDifference(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        if currentGameState.data.score < successorGameState.data.score:
            return 1
        else:
            return -0.5

    def foodEaten(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        successor_food_count = successorGameState.getNumFood()
        current_food_count = currentGameState.getNumFood()
        if (successor_food_count < current_food_count):
            return 1
        else: # successor_food_count == current_food_count:
            return 0.5

    def ghostHeadingTowardsMe(self, currentGameState, action):
        # TODO: Check whether or not a ghost I'm maybe moving closer to is headed in my direction..
        return 1

    def scoreChange(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        return successorGameState.data.scoreChange
        # if successorGameState.data.scoreChange > 0:
        #     return 1
        # else:
        #     return -1

    def didGameLose(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        if successorGameState.isLose():
            return -1
        elif successorGameState.isWin():
            return 2
        else:
            return 1


