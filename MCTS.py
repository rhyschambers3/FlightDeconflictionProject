import math
from DummyData import landing_planes

class MCTS:

    def __init__(self, explorationWeight = 1):
        self.Q = 0
        self.N = 0
        self.children = dict()
        self.explorationWeight = explorationWeight
    
    #SELECT METHOD
    
    #EXPAND METHOD
    
    #SIMULATE/ROLOUT METHOD
    
    #BACKPROP METHOD
        

class AirspaceNode():
    def findChildren(state):
    
    def findRandomChild(state):

    def reward(state):

    def terminalState(state):
    
    def makeMove(state):
    
    def displayLandingPattern(state):
    
    def __hash__(state):

    def __eq__(self, other):

if __name__ == "__main__":
    
    initial_ordering = initialize_landing_pattern(landing_planes)
    tree = MCTS()
    current_state = initial_ordering

    while not current_state.terminal:
        for _ in range (1000):
            tree.rollout(current_state)
        #Select next state to roll explore
        current_state = tree.choose(current_state)
        #Show the orderings as we go
        print(current_state.displayLandingPattern)
