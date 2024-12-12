import math
from DummyData import flights
from collections import namedtuple
from operator import itemgetter
import random
#flights = getFlights(flight_ids, airportArrivals, airportDistances, fuelLevels)
 #TODO: simulate and backprop methods & implement a check for conflicting times, locations, or fuel levels       

class AirspaceState:
    #State of the airspace: all of the flight_ids, list of planes landed, and simulation time 
    def __init__(self, planes_to_land, landed = [], time=0):
        #Pulled the plane numbers from the data 
        self.planes_to_land = planes_to_land #CAN USE THIS TO PULL OUT JUST THE PLANES: map(lambda x: x[0], planes)
        self.landed = landed
        self.time = time
    
    def land_plane(self, action):
        #Land one of the planes and return the new airspace after the plane has landed
        #Basically, take action to create a new node
        new_planes = []
        for plane in self.planes_to_land:
            if plane != action:
                new_planes.append(plane)
        new_landed = self.landed + [action]
        return AirspaceState(new_planes, new_landed, self.time + 1)
    

    #Method to show how each Node as Time: __ Queue of planes: ___ and Planes landed: ___
    def __repr__(self):
        return f"Time: {self.time}, Queue: {self.planes_to_land}, Landed: {self.landed}"
        

class Node():
    def __init__(self, AirspaceState, parent=None):
        self.visits = 1
        self.value = 0
        self.state = AirspaceState
        self.children = []
        self.parent=parent

    def getActions(self):
        #Legal actions are landing one of the planes in the queue
        return self.state.planes_to_land
    
    def is_fully_expanded(self):
        #check that all of the possible actions have been tried
        return len(self.children) >= len(self.getActions())
    
    def expand(self):
        #Find all possible planes to land
        possible_landings = self.getActions()
        print("Possible landings = ", possible_landings)

        #Find the planes that have already been landed (children)
        tried_landings = []
        for child in self.children:
            last_landing = child.state.landed[-1]
            tried_landings.append(last_landing)

        #Find the planes that we haven't tried to land yet  
        unattempted_landings = []
        for plane in possible_landings:
            if plane not in tried_landings:
                unattempted_landings.append(plane)
    
        #If there are still planes that need to land, randomly choose a plane to land and make a new node
        if unattempted_landings:
            action = random.choice(unattempted_landings)
            new_state = self.state.land_plane(action)
            child_node = Node(new_state, parent=self)
            self.children.append(child_node)
            return child_node
        return None
    
    #Finds the best child node
    def best_next_plane_to_land(self, exploration_weight = 1):
        #select the best child (max score) using the UCT
        best_child = None
        max_uct_val = float('-inf')

        #Iterate over children to find all of their UCT scores, 1e-6 prevens division by 0
        for child in self.children:
            exploitation = child.value / (child.visits + 1e-6)
            exploration = exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            
            #Combine exploration vs exploitation to get the uct value
            uct = exploration + exploitation 

            #Select the node with the max UCT value
            if uct > max_uct_val:
                max_uct_val = uct
                best_child = child

        return best_child
    

    def MCTS(root, iterations = 1000):
        for i in range(iterations):
            node = root

            #Select!
            while node.children and node.is_fully_expanded():
                #Using UCTS to find the best plane to select for landing
                node = node.best_next_plane_to_land()
            
            #Expand
            if not node.is_fully_expanded():
                node = node.expand()
            

            #Simulate/rollout
            reward = simulate(node.state)

            #Backprop
            backpropagate(node, reward)

        return root.best_next_plane_to_land(exploration_weight=0)


if __name__ == "__main__":
    initial_ordering = AirspaceState(flights)
    root = Node(initial_ordering)
    print(root)
    root.expand()
    for child in root.children:
        print("child state" , child.state)
    print("NEXT BEST PLANE TO LAND = " , root.best_next_plane_to_land().state)
    print()

  

    # best_node = MCTS(root, iterations = 1000)
    # tree = MCTS()
    # current_state = initial_ordering

    # while not current_state.terminal:
    #     for _ in range (1000):
    #         tree.rollout(current_state)
    #     #Select next state to roll explore
    #     current_state = tree.choose(current_state)
    #     #Show the orderings as we go
    #     print(current_state.displayLandingPattern)
