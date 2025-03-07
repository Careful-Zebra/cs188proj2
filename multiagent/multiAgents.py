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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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

        # print("successorGameState: " + str(successorGameState))
        # print("newPos: " + str(newPos))
        # print("newFood: " + str(newFood))
        # print("newGhostStates: " + str(newGhostStates))
        # print("newScaredTimes: " + str(newScaredTimes))

        score = successorGameState.getScore()
        foodList = newFood.asList()
        if len(foodList) != 0:
            foodRemaining = 1 / len(foodList)
        else:
            foodRemaining = 1
        #get the distance to every food
        foodDist = []
        for x in range(0, newFood.width):
            for y in range(0, newFood.height):
                if (newFood[x][y]):
                    foodDist.append(manhattanDistance(newPos, [x, y]) + 1)
        if (len(foodDist) != 0):
            foodMin = min(foodDist)
        else:
            foodMin = 1
        # avgFoodDist /= foodRemaining
        foodChoice = foodMin 
        foodRemaining *= 10000
        foodEval = (1 / foodChoice) * 10
        ghostDists = []
        for ghost in newGhostStates:
            ghostDists.append(manhattanDistance(newPos, ghost.getPosition()))
        avgGhostDist = sum(ghostDists) / len(newGhostStates)

        
        ghostEval = avgGhostDist

        if min(ghostDists) < 9:
            ghostEval = avgGhostDist
        else:
            ghostEval = 9
        

        if min(ghostDists) < 3:
            ghostEval = -1000
        curPos = currentGameState.getPacmanPosition()
        standingStill = (newPos == curPos)
        standing = ((not standingStill) * 100) 
        if (standing == 0 ):
            standing = -10000

        finalEval = score + foodRemaining + foodEval + ghostEval + standing

        

        return finalEval


        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    

    def getAction(self, gameState: GameState):
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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """

        #counter is agent, increases with mod

        def value(state, deepness, counter):
            if (counter == 0):
                deepness -= 1
            if state.isWin() or state.isLose() or (deepness == 0):
                return self.evaluationFunction(state)
            
            if (counter == 0):
                return maxValue(state, deepness)
            else:
                return minValue(state, deepness, counter)
            
        def maxValue(state, deepness):
            v = -10000000000
            actions = state.getLegalActions(0)
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, value(successor, deepness, 1))
            return v
        
        def minValue(state, deepness, counter):
            v = 10000000000
            actions = state.getLegalActions(counter)
            for action in actions:
                successor = state.generateSuccessor(counter, action)
                newCounter = (counter + 1) % gameState.getNumAgents()
                v = min(v, value(successor, deepness, newCounter))
            return v


            
            


        actions = gameState.getLegalActions(0)
        actionValues = {}
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            actionValues[action] = value(successor, self.depth, 1)
        return [key for key in actionValues if actionValues[key] == max(actionValues.values())][0]
    

    
    


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def alphabeta(state, alpha, beta, counter, deepness):

            if state.isWin() or state.isLose() or (deepness == 0):
                return (self.evaluationFunction(state), -1)
            if counter == 0:
                v = -10000000
                actions = state.getLegalActions(0)
                for action in actions:
                    successor = state.generateSuccessor(0, action)
                    vPrev = v
                    v = max(v, alphabeta(successor, alpha, beta, 1, deepness)[0])
                    if vPrev != v:
                        minAction = action
                    if v > beta:
                        return (v, minAction)
                    alpha = max(alpha, v)
                return (v, minAction)
            else:
                v = 10000000
                actions = state.getLegalActions(counter)
                for action in actions:
                    successor = state.generateSuccessor(counter, action)
                    numAgents = gameState.getNumAgents()
                    newCounter = (counter + 1) % numAgents
                    if (newCounter == 0):
                        newDeepness = deepness - 1
                    else:
                        newDeepness = deepness
                    vPrev = v
                    v = min(v, alphabeta(successor, alpha, beta, newCounter, newDeepness)[0])
                    if vPrev != v:
                        minAction = action
                    if v < alpha:
                        return (v, minAction)
                    beta = min(beta, v)
                return (v, minAction)
            
        return alphabeta(gameState, -100000000000, 10000000000000, 0, self.depth)[1]
        actions = gameState.getLegalActions(0)
        actionValues = {}
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            actionValues[action] = alphabeta(successor, -1000000000000000, 10000000000, 1, self.depth)
        return [key for key in actionValues if actionValues[key] == max(actionValues.values())][0]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def value(state, deepness, counter):
            if (counter == 0):
                deepness -= 1
            if state.isWin() or state.isLose() or (deepness == 0):
                return self.evaluationFunction(state)
            
            if (counter == 0):
                return maxValue(state, deepness)
            else:
                return expValue(state, deepness, counter)
            
        def maxValue(state, deepness):
            v = -10000000000
            actions = state.getLegalActions(0)
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, value(successor, deepness, 1))
            return v
        
        def expValue(state, deepness, counter):
            v = 0
            actions = state.getLegalActions(counter)
            p = 1 / len(actions)
            for action in actions:
                successor = state.generateSuccessor(counter, action)
                newCounter = (counter + 1) % gameState.getNumAgents()
                v += p * value(successor, deepness, newCounter)
            return v


            
            


        actions = gameState.getLegalActions(0)
        actionValues = {}
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            actionValues[action] = value(successor, self.depth, 1)
        return [key for key in actionValues if actionValues[key] == max(actionValues.values())][0]
    


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: A combination of minimum distance to food, average ghost distance when within a 9 square radius, overall food remaining, score, and stopping him from standing still
    """

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # print("successorGameState: " + str(successorGameState))
    # print("newPos: " + str(newPos))
    # print("newFood: " + str(newFood))
    # print("newGhostStates: " + str(newGhostStates))
    # print("newScaredTimes: " + str(newScaredTimes))

    score = currentGameState.getScore()
    foodList = newFood.asList()
    if len(foodList) != 0:
        foodRemaining = 1 / len(foodList)
    else:
        foodRemaining = 1
    #get the distance to every food
    foodDist = []
    for x in range(0, newFood.width):
        for y in range(0, newFood.height):
            if (newFood[x][y]):
                foodDist.append(manhattanDistance(newPos, [x, y]) + 1)
    if (len(foodDist) != 0):
        foodMin = min(foodDist)
    else:
        foodMin = 1
    # avgFoodDist /= foodRemaining
    foodChoice = foodMin 
    foodRemaining *= 20000
    foodEval = (1 / foodChoice) * 10
    ghostDists = []
    for ghost in newGhostStates:
        ghostDists.append(manhattanDistance(newPos, ghost.getPosition()))
    avgGhostDist = sum(ghostDists) / len(newGhostStates)

    
    ghostEval = avgGhostDist

    if min(ghostDists) < 9:
        ghostEval = avgGhostDist / 2
    else:
        ghostEval = 0
    

    if min(ghostDists) < 2:
        ghostEval = -1000
    curPos = currentGameState.getPacmanPosition()
    standingStill = (newPos == curPos)
    standing = ((not standingStill) * 100) 
    if (standing == 0 ):
        standing = -10000
    if min(newScaredTimes) > 1:
        ghostEval = (0 - ghostEval) + 10

    finalEval = score + foodRemaining + foodEval + ghostEval 

    

    return finalEval

# Abbreviation
better = betterEvaluationFunction
