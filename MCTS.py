import math
from DummyData import flights
from collections import namedtuple
from operator import itemgetter
import random
#flights = getFlights(flight_ids, airportArrivals, airportDistances, fuelLevels)
 #TODO: simulate and backprop methods & implement a check for conflicting times, locations, or fuel levels       

class AirspaceState:
    #State of the airspace: all of the flight_ids, list of planes landed, and simulation time 
    def __init__(self, planes_to_land, landed =[], time=0):
        #Pulled the plane numbers from the data 
        self.planes_to_land = planes_to_land #CAN USE THIS TO PULL OUT JUST THE PLANES: map(lambda x: x[0], planes)
        self.landed = landed
        self.time = time
    
    def land_plane(self, action):
        #Land one of the planes and return the new airspace after the plane has landed
        #Basically, take action to create a new node
        #Select at random a plane to land (but need to update to land most pressing plane)
        plane = random.choice(self.planes_to_land)
        if (action == ("Land")):
            self.landed.append(plane)
            self.planes_to_land.remove(plane)
        #INCORPORATE DELAY?
        return AirspaceState(self.planes_to_land, self.landed, self.time+1) 
            
    
    
    def is_terminal(self):
        #checking to see if all of the planes have been landed
        if len(self.planes_to_land) == 0:
            return True
        return False

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
        if len(self.children) == 0:
            return True
        return False
    
    def expand(self):
    # Find all possible planes to land
        if not self.state.is_terminal():
            #For every plane that has not yet landed, create a new node landing that plane 
            for plane_to_land in self.getActions():
                newState = AirspaceState(self.state.planes_to_land.copy(), self.state.landed.copy(), self.state.time)
                newState.planes_to_land.remove(plane_to_land)
                newState.landed.append(plane_to_land)
                newState.time += 1

                # Make new child and append
                childNode = Node(newState, parent=self)
                self.children.append(childNode)
                return self.children
        return None


    
    #Finds the best child node
    def best_next_plane_to_land(self, exploration_weight = 1):
        #select the best child (max score) using the UCT
        best_child = None
        max_uct_val = float('-inf')
        self.expand()
        
        #Iterate over children to find all of their UCT scores, 1e-6 prevens division by 0
        for child in self.children:
            print("CHILD = ", child, "Time = ", self.state.time)
            exploitation = child.value / (child.visits + 1e-6)
            exploration = exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            
            #Combine exploration vs exploitation to get the uct value
            uct = exploration + exploitation 

            #Select the node with the max UCT value
            if uct > max_uct_val:
                max_uct_val = uct
                best_child = child
        #print("BEST CHILD = ", best_child)
        return best_child
    
def simulate(state):
    while not state.is_terminal():
            if state.planes_to_land:
                plane = random.choice(state.planes_to_land)
                state.planes_to_land.remove(plane)
                state.landed.append(plane)
                state.time += 1
            

        #MIGHT NEED TO ADJUST THIS BUT SAYIING THAT SHORTER TIME IS BETTER FOR ALL THE PLANES TO LAND
    return -1*(state.time)

def backpropagate(node, reward):
    #backprop the result of the simulation up the tree, updating the visits and value
    while node is not None:
        node.visits+=1
        node.value+=reward
        node = node.parent

    
        
def MCTS(root, iterations = 1000):
    for _ in range(iterations):
        node = root

        #Select!
        while node.children and node.is_fully_expanded():
            #Using UCTS to find the best plane to select for landing
            node = node.best_next_plane_to_land()
            
            #Expand
            if not node.is_fully_expanded():
                newNode = node.expand()
                if newNode:
                    node = newNode
            
            #Simulate/rollout
            reward = simulate(node.state)

            #Backprop
            backpropagate(node, reward)
    landing_order = []
    curNode = root
    while not curNode.state.is_terminal():
        curNode = curNode.best_next_plane_to_land()

        #If the node is defined, append in reverse order the landed planes list
        #since the most recently landed plane will be at the back
        if curNode:
            landing_order.append(curNode.state.landed[-1])
         
        else:
            break
        
    return landing_order


if __name__ == "__main__":
    initial_ordering = AirspaceState(flights)
    root = Node(initial_ordering)
    sequence = MCTS(root, iterations=1000)
    print()
    print()
    print("landing sequence = ", sequence)
    


