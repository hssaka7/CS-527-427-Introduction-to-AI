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

# 02/19/2018
#CS 427
# edited by Aakash Basnet and Himanshu Chaudhary


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
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
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
        currentGameState = currentGameState.generatePacmanSuccessor(action)
        pacmanPos= currentGameState.getPacmanPosition()
        foodPos = currentGameState.getFood().asList()
        ghostPos = currentGameState.getGhostPositions()
        capsulePos = currentGameState.getCapsules()

        distancetoGhost = [manhattanDistance(pacmanPos,xy) for xy in ghostPos]
        distancetoFood = [manhattanDistance(pacmanPos,xy) for xy in foodPos]
        distanceToCapsule = [manhattanDistance(pacmanPos,xy) for xy in capsulePos]

        #if action is stop, we don't want pacman to stay idle
        if action=='stop' : return -10000000
        #avoid direction if ghost is in that tile
        if min(distancetoGhost)==0: return -10000

        #when capsule,food,ghost are not present, default values passed
        if len(distanceToCapsule)==0 : distanceToCapsule+=[1]
        if len(distancetoFood)==0 : distancetoFood+=[1]
        if len(distancetoGhost)==0 : distancetoGhost+=[0]

        #average of distances to food, capsule(with high priority) added with minimun distance to food and capsule
        p1t = (-2 * (sum(distancetoFood)/len(distancetoFood))) + (- 20*(sum(distanceToCapsule)/len(distanceToCapsule)))
        p1 = p1t - min(distancetoFood) - min(distancetoGhost)

        p2 = 10*currentGameState.getScore()

        #the number of food and capsule should inversely affect the total
        p3 = (-4*len(distancetoGhost)) + (-40*(len (distanceToCapsule)+1))

        #ghost should also negatively affect the total
        p4 = -2*(100/min(distancetoGhost))


        total = p1+p2+p3+p4
        return total

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
        "*** YOUR CODE HERE ***"
        agentId = 0
        treeDepth = 0

        minMaxValue = self.value(gameState,agentId,treeDepth)


        return minMaxValue[1]

    def value (self,gameState,agentId,treeDepth):
        """
        :param gameState: current state of game
        :param agentId: agent id
        :param treeDepth: current id
        :return: the utilities

        this function is a helper function that identifies either the agent is min ,max or terminal condition and calls the
        respective function.
        """
        # checking if all the agent has played or not.
        #if yes then resetting the agentId and increasing treeDepth
        if agentId == gameState.getNumAgents():
            agentId = 0
            treeDepth += 1


        # check for the terminal condition

        if (treeDepth ==self.depth) or gameState.isLose() or gameState.isWin():
            return  (self.evaluationFunction(gameState),"Stop")

        # check if maxAgent (pacman)
        if agentId == 0:
            return self.maxValue(gameState,treeDepth,agentId)


        # check if minAgent (ghosts)
        else:
            return self.minValue(gameState,treeDepth,agentId)


    def maxValue(self,state,depth,agentId):
        """
        This function is the maximium function for pacman
        :param state
        :param depth
        :param agentId
        :return: returns the maximum value from the leaves
        """
        minVal = float("-inf")
        Val = (minVal,"actionType")
        nextActions = state.getLegalActions(agentId)



        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            newAgentId = agentId + 1
            tempVal = self.value(newState,newAgentId,depth)


            if tempVal[0]>Val[0]:
                Val = (tempVal[0],action)
        return Val


    def minValue (self,state,depth,agentId):
        """
        This function is the minimum function for the ghost
        :param state:
        :param depth:
        :param agentId:
        :return: the minimum value from the leaves
        """
        maxVal = float("inf")
        Val = (maxVal,"actionType")

        nextActions = state.getLegalActions(agentId)


        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.value(newState,agentId+1,depth)

            if tempVal[0]<Val[0]:
                Val = (tempVal[0],action)
        return Val




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        agentId = 0
        treeDepth = 0
        alpha = float("-inf")
        beta = float("inf")
        minMaxValue = self.valueab(gameState,agentId,treeDepth,alpha,beta)
        return minMaxValue[1]


    def valueab (self,gameState,agentId,treeDepth,alpha,beta):
        # checking if all the agent has played or not.
        #if yes then resetting the agentId and increasing treeDepth
        if agentId == gameState.getNumAgents():
            agentId = 0
            treeDepth += 1


        # check for the terminal condition

        if (treeDepth ==self.depth) or gameState.isLose() or gameState.isWin():
            return  (self.evaluationFunction(gameState),"Stop")

        # check if maxAgent (pacman)
        if agentId == 0:
            return self.maxValueab(gameState,treeDepth,agentId,alpha,beta)


        # check if minAgent (ghosts)
        else:
            return self.minValueab(gameState,treeDepth,agentId,alpha,beta)


    def maxValueab(self,state,depth,agentId,alpha,beta):
        Val = (float ("-inf"),"actionType")
        nextActions = state.getLegalActions(agentId)
        if len(nextActions)== 0: return self.evaluationFunction(state)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.valueab(newState,agentId+1,depth,alpha,beta)

            if tempVal[0] > Val[0]:
                Val = (tempVal[0],action)
            #comparing with global beta and updating global alpha
            if Val[0]> beta:
                #prunged
                return Val
            alpha = max(alpha,Val[0])
        return Val


    def minValueab (self,state,depth,agentId,alpha,beta):
        Val = (float("inf"),"actionType")

        nextActions = state.getLegalActions(agentId)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.valueab(newState,agentId+1,depth,alpha,beta)

            if tempVal[0] < Val[0]:
                Val = (tempVal[0],action)
            #comparing with global alpha and updating global beta
            if Val[0] < alpha:
                #prunged
                return Val
            beta = min(beta,Val[0])
        return Val


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
        "*** YOUR CODE HERE ***"

        agentId = 0
        treeDepth = 0
        minMaxValue = self.value(gameState,agentId,treeDepth)


        return minMaxValue[1]

    def value (self,gameState,agentId,treeDepth):
        # checking if all the agent has played or not.
        #if yes then resetting the agentId and increasing treeDepth
        if agentId == gameState.getNumAgents():
            agentId = 0
            treeDepth += 1


        # check for the terminal condition

        if (treeDepth ==self.depth) or gameState.isLose() or gameState.isWin():
            return  (self.evaluationFunction(gameState),"Stop")

        # check if maxAgent (pacman)
        if agentId == 0:
            return self.maxValue(gameState,treeDepth,agentId)


        # check if minAgent (ghosts)
        else:
            return self.expValue(gameState,treeDepth,agentId)


    def maxValue(self,state,depth,agentId):
        Val = (float ("-inf"),"actionType")
        nextActions = state.getLegalActions(agentId)
        if len(nextActions)== 0: return self.evaluationFunction(state)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.value(newState,agentId+1,depth)

            if tempVal[0] > Val[0]:
                Val = (tempVal[0],action)
        return Val


    def expValue (self,state,depth,agentId):
        """
        :param state:
        :param depth:
        :param agentId:
        :return: the expected vaue from the given leaved
        """
        Val = [0,"actionType"]

        nextActions = state.getLegalActions(agentId)
        #probability calculation for expected value
        probability = 1.0/len(nextActions)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.value(newState,agentId+1,depth)

            Val[0] += tempVal[0] * probability
            Val[1] = action
        return tuple(Val)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION:
      There are four main priority points used to calculate the final value

       1) the average distance to nearest food and capsule negatively affect the total score
           it gathers information from all areas of the game

       2) the game score
            the game score is the ultimate priority and it's calculation uses many important values

       3) the number of food and capsule
            used mainly to prioritize the move that will finally eat food or capsule

       4) distance to nearest ghost negatively affect total
            the distance had direct negative effects to the overal chances of winning


    """
    "* YOUR CODE HERE *"

    pacmanPos= currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostPos = currentGameState.getGhostPositions()
    capsulePos = currentGameState.getCapsules()

    #calculating distances to ghost, food and capsule from pacman
    distancetoGhost = [manhattanDistance(pacmanPos,xy) for xy in ghostPos]
    distancetoFood = [manhattanDistance(pacmanPos,xy) for xy in foodPos]
    distanceToCapsule =  [manhattanDistance(pacmanPos,xy) for xy in capsulePos]


    #setting default values when the lists are empty
    if len(distanceToCapsule)==0 : distanceToCapsule+=[1]
    if len(distancetoFood)==0 : distancetoFood+=[1]
    if len(distancetoGhost)==0 : distancetoGhost+=[0]

    #if the ghots is present in next tile, it avoids it
    if min(distancetoGhost)==0: return -10000

    #average of distances to food, capsule(with high priority) added with minimun distance to food and capsule
    p1t = (-2 * (sum(distancetoFood)/len(distancetoFood))) + (- 2*(sum(distanceToCapsule)/len(distanceToCapsule)))
    p1 = p1t - min(distancetoFood) - min(distancetoGhost)
    p2 = 10*currentGameState.getScore()
    #the number of food and capsule should inversely affect the total
    p3 = (-4*len(distancetoGhost)) + (-40*len (distanceToCapsule))
    #ghost should also negatively affect the total
    p4 = -2*(10/min(distancetoGhost))

    total = p1+p2+p3+p4

    return total


# Abbreviation
better = betterEvaluationFunction

