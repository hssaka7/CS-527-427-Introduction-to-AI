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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        finalReturnValue = 0.0

        #accounts the newScore

        finalReturnValue += successorGameState.getScore()


        #accounts the distance to the ghosts.
        (xi,yi) = successorGameState.getPacmanPosition()
        ghostPositions = successorGameState.getGhostPositions()
        distanceToGhosts = []
        for (x,y) in ghostPositions:
            tempDist = abs (x-xi) + abs (y-yi)
            distanceToGhosts.append(tempDist)

        foodPosition = successorGameState.getFood().asList()
        distanceToFoods = []
        for (xf,yf) in foodPosition:
            tempDist = abs(xf-xi) + abs(yf-yi)
            distanceToFoods.append(tempDist)

        if len(distanceToFoods) != 0 :

          if min(distanceToGhosts) <=2 :
              finalReturnValue == -999999
          else:

              finalReturnValue += min(distanceToGhosts)/min(distanceToFoods)
        ## work of scared time:

        if len (newScaredTimes) != 0:
            finalReturnValue = finalReturnValue +0.5*min(newScaredTimes)



        "*** YOUR CODE HERE ***"
        return finalReturnValue

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

        print "minMaxValue ===   ",minMaxValue
        return minMaxValue[1]

    def value (self,gameState,agentId,treeDepth):
        # checking if all the agent has played or not.
        #if yes then resetting the agentId and increasing treeDepth
        if agentId == gameState.getNumAgents():
            agentId = 0
            treeDepth += 1


        # check for the terminal condition

        if (treeDepth ==self.depth) or gameState.isLose() or gameState.isWin():
            return  self.evaluationFunction(gameState)

        # check if maxAgent (pacman)
        if agentId == 0:
            return self.maxValue(gameState,treeDepth,agentId)


        # check if minAgent (ghosts)
        else:
            return self.minValue(gameState,treeDepth,agentId)


    def maxValue(self,state,depth,agentId):
        minVal = float("-inf")
        Val = (minVal,"actionType")
        nextActions = state.getLegalActions(agentId)




        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            newAgentId = agentId + 1
            tempVal = self.value(newState,newAgentId,depth)

            if type(tempVal) is tuple:
                tempVal = tempVal[0]

            maxVal = max(Val[0],tempVal)



            if maxVal != Val[0]:
                Val = (maxVal,action)
        return Val


    def minValue (self,state,depth,agentId):
        maxVal = float("inf")
        Val = (maxVal,"actionType")

        nextActions = state.getLegalActions(agentId)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.value(newState,agentId+1,depth)
            if type(tempVal) is tuple:
                tempVal = tempVal[0]
            minVal = min(Val[0],tempVal)

            if minVal != Val[0]:
                Val = (minVal,action)
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
            return  self.evaluationFunction(gameState)

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

            if type(tempVal) is tuple:
                tempVal = tempVal[0]
                #print "val Without action for max  ===  ", tempVal
            maxVal = max(Val[0],tempVal)

            if maxVal != Val[0]:
                Val = (maxVal,action)
            if Val[0]> beta:
                return Val
            alpha = max(alpha,Val[0])
        return Val


    def minValueab (self,state,depth,agentId,alpha,beta):
        Val = (float("inf"),"actionType")

        nextActions = state.getLegalActions(agentId)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.valueab(newState,agentId+1,depth,alpha,beta)
            if type(tempVal) is tuple:
                tempVal = tempVal[0]
               # print "val Without action for max  ===  ",tempVal
            minVal = min(Val[0],tempVal)


            if minVal != Val[0]:
                Val = (minVal,action)
            if Val[0] < alpha:
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
            return  self.evaluationFunction(gameState)

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

            if type(tempVal) is tuple:
                tempVal = tempVal[0]
                #print "val Without action for max  ===  ", tempVal
            maxVal = max(Val[0],tempVal)



            if maxVal != Val[0]:
                Val = (maxVal,action)
        return Val


    def expValue (self,state,depth,agentId):
        Val = [0,"actionType"]

        nextActions = state.getLegalActions(agentId)
        probability = 1.0/len(nextActions)

        for action in nextActions:
            newState = state.generateSuccessor(agentId,action)
            tempVal = self.value(newState,agentId+1,depth)
            if type(tempVal) is tuple:
                tempVal = tempVal[0]
               # print "val Without action for max  ===  ",tempVal
            Val[0] += tempVal * probability
            Val[1] = action
        return tuple(Val)



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:
      Stuff that's good- ghosts not so close that they can kill Pacman, food, power pellets, scared ghosts
      Stuff that's bad- dying
    """
    "* YOUR CODE HERE *"

    pacmanPos= currentGameState.getPacmanPosition()
    foodPos = currentGameState.getFood().asList()
    ghostPos = currentGameState.getGhostPositions()
    capsulePos = currentGameState.getCapsules()
    walls = currentGameState.getWalls()
    newGhostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    extra = 0;






    distancetoGhost = [manhattanDistance(pacmanPos,xy) for xy in ghostPos]
    distancetoFood = [manhattanDistance(pacmanPos,xy) for xy in foodPos]
    distanceToCapsule =  [manhattanDistance(pacmanPos,xy) for xy in capsulePos]

    if len(distanceToCapsule)==0 : distanceToCapsule+=[1]
    if len(distancetoFood)==0 : distancetoFood+=[1]
    if len(distancetoGhost)==0 : distancetoGhost+=[0]

    if min(distancetoGhost)==0: return -10000

    countPoint = 2000/((len(foodPos)+1) + (10*len(capsulePos))+1)
    foodPoint = 50/min(distancetoFood)
    ghostPoint = min(distancetoGhost)*1.5
    capsulePoint = 20/min(distanceToCapsule)
    total = (foodPoint+ghostPoint+capsulePoint) + countPoint + extra

    return  total

# Abbreviation
better = betterEvaluationFunction

