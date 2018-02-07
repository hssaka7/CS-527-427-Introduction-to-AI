# search.py
# ---------
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
"""
Edited by,
Aakash Basnet:
Edited function: DepthFirstSearch, BreadthFirstSearch,UniformCostSearch, AstarSearch
"""

"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    """
    ALGORITH FOR DFS
    
    function graph-search(problem, fringe) retuen a sloution or failure
    
    closed <-- an empty set
    fringe <-- insert (make-node (initial-state [problem]), fringe)
    
    loop do :
      if fringe is empty then return failure
      node <-- Remove-front (fringe)
      if goal-test (problem, state[node]) then return node
      if state[node] is not in closed then 
        add STATE[node] to closed
        for child-node in EXPAND(STATE[node],problem) do
            fringe <-- Insert (child-node, fringe)
        end
    end
    """

    templist=[]
    explored = set()
    fringe = util.Stack()
    #print "the stat node is :  ", problem.getStartState()

    fringe.push((problem.getStartState(),templist))
    while (not fringe.isEmpty()):
        (currentNode,currDir) = fringe.pop()
     #   print "Pacman is currently at  :  ", currentNode
        if problem.isGoalState(currentNode):
      #      print " Goal State Found :  ", currentNode
            pathToGoal = currDir
            break
        if not (currentNode in explored):
       #     print "Adding current node to explored"
            explored.add(currentNode)
            for childNode in problem.getSuccessors(currentNode):
        #        print "child node  :  ", childNode , "  is added   "
                fringe.push((childNode[0],currDir+[childNode[1]]))

    return  pathToGoal


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    """
    ALGORITHM FOR bFS 
    Create a queue Q
    enqueue root node to Q
    while Q is not empty:
       dequeu an item v from Q
       mark the item v as visited 
       for each node w that is directed from v:
       enqueue w to Q
    
   
     """

    fringes = util.Queue()
    explored =[]
    fringes.push((problem.getStartState(),[]))

    while(not fringes.isEmpty()):
        currentNode,currDir = fringes.pop()
        if problem.isGoalState(currentNode):
            goal = currentNode
            pathToGoal = currDir
            #print "final path is   :  ", pathToGoal

            break
    #        print "HOraaay goal has been found  === >  ", currentNode

        if not (currentNode in explored):
            explored.append(currentNode)
            for childNode in problem.getSuccessors(currentNode):
                fringes.push((childNode[0],currDir+[childNode[1]]))


    return pathToGoal


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"


    templist=[]
    explored = set()
    fringe = util.PriorityQueue()
    # state, list of directions till now and the cost is pushed in the stack
    # so that algorithm can explore the node with lowest cost first
    fringe.push((problem.getStartState(),templist),1)

    while (not fringe.isEmpty()):
        (currentNode,currDir) = fringe.pop()

        if problem.isGoalState(currentNode):
            pathToGoal = currDir
            break
        if not (currentNode in explored):
            explored.add(currentNode)
            for childNode in problem.getSuccessors(currentNode):
                # total cost is cost till now plus cost to the child node
                totalCost = childNode[2]+problem.getCostOfActions(currDir)
                fringe.push((childNode[0],currDir+[childNode[1]]),totalCost)




    return  pathToGoal;

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    """
    same as UCS function, but total cost is sum of cost till now , cost to the child node and 
    cost to the goal state (heuristic function)
    """
    fringes = util.PriorityQueue()
    explored =set()
    fringes.push((problem.getStartState(),[]),0)

    while(not fringes.isEmpty()):
        currentNode,currDir = fringes.pop()
        if problem.isGoalState(currentNode):
            finalPath = currDir
            break
            #        print "HOraaay goal has been found  === >  ", currentNode

        if not (currentNode in explored):
            explored.add(currentNode)
            for childNode in problem.getSuccessors(currentNode):
                totalCost = (childNode[2] + heuristic(childNode[0],problem)+problem.getCostOfActions(currDir))
                fringes.push((childNode[0],currDir+[childNode[1]]),totalCost)


    return finalPath







    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
