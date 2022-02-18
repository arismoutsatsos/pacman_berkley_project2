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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
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

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        capsules = currentGameState.getCapsules()
        "*** YOUR CODE HERE ***"
        #some of the numbers are based on how pacman performed after multiple tests

        ghost_pos = childGameState.getGhostPositions()
        food_pos = newFood.asList()
    
        if childGameState.isWin():
            return float("inf")
        
        scared_ghosts = [x for x in newScaredTimes if x != 0]
        distance_food = min(util.manhattanDistance( newPos , position) for position in food_pos)

        total = 0
        if capsules:
            distance_caps = min(util.manhattanDistance( newPos , position) for position in capsules)
            if distance_caps == 0:
                total +=50   #capsules score a lot of points and give advantage
            elif distance_caps < 2 :
                total +=  15 * distance_caps #give an advantage to the state if a capsule is close 

        for i in range(len(ghost_pos)):
            if util.manhattanDistance( newPos , ghost_pos[i]) <= 1:
                if newScaredTimes[i] == 0:
                    return -float("inf")  
                else :
                    return currentGameState.getScore() + 150 #give lots of points for eating a ghost
            

        if action == Directions.STOP: #give a penalty for stoping since it costs points
            total -=10
        
        return childGameState.getScore() + 1/distance_food + total



        ghost_pos = childGameState.getGhostPositions()
        food_pos = newFood.asList()
        if childGameState.isWin():
            return 100000
        distance_food = min(util.manhattanDistance( newPos , position) for position in food_pos)
        for ghost in ghost_pos:
            if ghost in scared_ghosts:
                return 1000
            if util.manhattanDistance( newPos , ghost) <= 1:
                return -100000
        return childGameState.getScore() + 1/distance_food

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

    def minimax(self ,agent , depth , gameState):
        if gameState.isLose() or gameState.isWin() or depth == self.depth  :
            return self.evaluationFunction(gameState)

        if agent == 0: #pacman
            return max(self.minimax(1 , depth , gameState.getNextState(agent , action)) for action in gameState.getLegalActions(agent)) 
        else:
            next_agent = agent + 1  
            if next_agent == gameState.getNumAgents()  :
                next_agent = 0
            if next_agent == 0:  #increase depth if its pacmans turn again
                depth += 1
            return min(self.minimax(next_agent , depth , gameState.getNextState(agent, action)) for action in gameState.getLegalActions(agent))



    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        maximum = -float("inf")
        for move in gameState.getLegalActions(0):
            value = self.minimax(1 , 0 , gameState.getNextState(0, move))
            if value > maximum :
                actiontotake = move
                maximum = value
        return actiontotake


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    #same philosophy as minimax with pruning
    def alphaBeta(self ,agent , depth ,a , b, gameState):
        if gameState.isLose() or gameState.isWin() or depth == self.depth  :
            return self.evaluationFunction(gameState)

        if agent == 0:
            value = -float("inf")
            for action in  gameState.getLegalActions(agent):
                value = max(self.alphaBeta(1 , depth , a , b ,gameState.getNextState(agent, action)) , value )
                if value > b: #prune
                    break
                a = max(a , value)
            return value
        else:
            value = float("inf")
            next_agent = agent + 1 
            if next_agent == gameState.getNumAgents()  :
                next_agent = 0
            if next_agent == 0:
                depth += 1
            for action in  gameState.getLegalActions(agent):
                value = min(self.alphaBeta(next_agent , depth , a , b ,gameState.getNextState(agent, action))  , value)
                if value <  a: #prune
                    break
                b = min(b , value)
            return value



    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        maximum = -float("inf")
        a = -float("inf")
        b = float("inf")
        for move in gameState.getLegalActions(0):
            value = self.alphaBeta(1 , 0 , a , b , gameState.getNextState(0,  move))
            if value > maximum :
                actiontotake = move
                maximum = value
            a = max ( a, value)
        return actiontotake

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def expectimax(self , agent , depth , gameState):
        if gameState.isLose() or gameState.isWin() or depth == self.depth  :
            return self.evaluationFunction(gameState)

        if agent == 0:
            return max(self.expectimax(1 , depth , gameState.getNextState(agent , action)) for action in gameState.getLegalActions(agent)) 
        else:
            sum = 0
            next_agent = agent + 1 
            if next_agent == gameState.getNumAgents()  :
                next_agent = 0
            if next_agent == 0:
                depth += 1
            actions = gameState.getLegalActions(agent)
            for action in actions:
                sum += self.expectimax(next_agent , depth , gameState.getNextState(agent, action))
            return sum / len(actions) #return the avg 






    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        


        maximum = -float("inf")
        for smt in gameState.getLegalActions(0):
            value = self.expectimax(1 , 0 , gameState.getNextState(0, smt))
            if value > maximum :
                actiontotake = smt
                maximum = value
        return actiontotake

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    number_of_ghosts = currentGameState.getNumAgents()

    scared_ghosts = [x for x in newScaredTimes if x != 0]
    capsules = currentGameState.getCapsules()
    ghost_pos = currentGameState.getGhostPositions()
    food_pos = newFood.asList()



    if currentGameState.isWin():
        return 10000
    if currentGameState.isLose():
        return -10000

    total = 0
    min_distance_threat = float("inf")

    for i in range (len(ghost_pos)):
        distance = util.manhattanDistance(newPos , ghost_pos[i])

        if newScaredTimes[i] != 0: 
            if distance <= 2:    #calculate a lot of points for eating a ghost to make high scores
                total += 150 - distance
            elif distance < min_distance_threat:
                min_distance_threat = distance

    distance_food =  min(util.manhattanDistance( newPos , position) for position in food_pos)
    if capsules:
        distance_capsule = min(util.manhattanDistance(newPos , capsule) for capsule in capsules)
        if distance_capsule <= 2 : 
            total += 50  
    foodlenght = len(food_pos) #calculate how many foods are left. substract from the evaluation score so that few foods left = better score
    
    #take into account the ghosts positions in the evaluation if they are close only 
    if min_distance_threat < 2: 
        return currentGameState.getScore() + 11/distance_food  + total  - 0.5 *foodlenght - 21/min_distance_threat
    else:
        return currentGameState.getScore() + 11/distance_food  + total  - 0.5 *foodlenght  



# Abbreviation
better = betterEvaluationFunction
