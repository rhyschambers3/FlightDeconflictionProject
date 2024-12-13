import math
from DummyData import flights, high_threshold, low_threshold, med_threshold
from collections import namedtuple
from operator import itemgetter
import random
from copy import deepcopy


#flights = getFlights(flight_ids, airportArrivals, airportDistances, fuelLevels)
 #TODO: simulate and backprop methods & implement a check for conflicting times, locations, or fuel levels       
result = list()

class AirspaceState:
    #State of the airspace: all of the flight_ids, list of planes landed, and simulation time 
    def __init__(self, planes_to_land = [], landed =[], time=0):
        #Pulled the plane numbers from the data 
        self.planes_to_land = planes_to_land #CAN USE THIS TO PULL OUT JUST THE PLANES: map(lambda x: x[0], planes)
        self.landed = landed
        self.time = time
    
    def land_plane(self, plane):
        #Land one of the planes and return the new airspace after the plane has landed
        #Basically, take action to create a new node
        #Select at random a plane to land (but need to update to land most pressing plane)
        self.landed.append(plane)
        self.planes_to_land.remove(plane)
        return AirspaceState(self.planes_to_land, self.landed,self.time+1)
     
            
    
    def is_terminal(self):
        #checking to see if all of the planes have been landed
        if  len(self.planes_to_land) == 0 and len(self.landed)==100: 
            return True
        return False

    #Method to show how each Node as Time: __ Queue of planes: ___ and Planes landed: ___
    def __repr__(self):
        return f"Time: {self.time}, Queue: {self.planes_to_land}, Landed: {self.landed}"
    
    def copy(self):
        # Return a new instance with the same attributes
        return AirspaceState(
            planes_to_land=deepcopy(self.planes_to_land),
            landed=deepcopy(self.landed),
            time=self.time                            # Time is immutable, so it can be directly assigned
        )

class Node():
    def __init__(self, AirspaceState, parent=None):
        self.N = 1 
        self.T = 0
        self.state = AirspaceState
        self.children = []
        self.parent= parent

    def getActions(self):
        #Legal actions are landing one of the planes in the queue 
        return self.state.planes_to_land
    
    def is_fully_expanded(self):
        #check that all of the possible actions have been tried
        if len(self.children) >= len(self.state.planes_to_land):
            return True
        return False
    
    def has_parent(self):
        #Check if the node has a parent node
        if self.parent is not None:
            return True
        return False

    def expand(self):
        # Check that the state isn't a leaf node and is not fully expanded
        if not self.state.is_terminal() and not self.is_fully_expanded():
            # Get the list of planes we still need to land
            actions = self.getActions()
            actions_length = len(actions)
            
            # Initialize index for iteration
            index = 0
            
            while index < actions_length:
                plane_to_land = actions[index]

                # Copy the states and append to landed if landed, and remove from planes_to_land
                planes_to_land_copy = self.state.planes_to_land.copy()
                landed_copy = self.state.landed.copy()
                planes_to_land_copy.remove(plane_to_land)
                landed_copy.append(plane_to_land)

                # Create the new state
                new_state = AirspaceState(
                    planes_to_land=planes_to_land_copy, 
                    landed=landed_copy, 
                    time=self.state.time + 1
                )

                # Check for duplicates
                duplicate_found = False
                for child in self.children:
                    if child.state == new_state:
                        duplicate_found = True
                        break

                if not duplicate_found:
                    # Create the child node and add it to the list of children
                    child_node = Node(new_state, parent=self)
                    #print("Child node state we just created: ", child_node.state, "Child node's landed planes = ", child_node.state.landed)
                    # print("self.children 0: ", len(self.children))
                    self.children.append(child_node)
                    # print("self.children 1: ", len(self.children))
                index += 1

            # Optionally mark the node as fully expanded
            self.is_fully_expanded_flag = True
            # print("Flag = " , self.is_fully_expanded_flag)
            # print("Children in backprop: ", self.children)


        #Finds the best child node
    def select(self):
        print("in select")
        #select the best child (max score) using the UCT
        # node = self.state
        exploration_weight = 1
        best_child = None
        max_ucb_val = float('-inf')
        
        #Iterate over children to find all of their UCT scores, 1e-6 prevens division by 0
        for child in self.children:
            #Finding the average T value in exploit
            exploitation = child.T / (child.N)
            #C value is 1 because we want to explore more 
            exploration = exploration_weight * math.sqrt(math.log(self.N) / (child.N)) #N is never 0 because init node state initialized self.N = 1
            
            #Combine exploration vs exploitation to get the uct T
            ucb = exploration + exploitation 

            #Select the node with the max UCT T
            if ucb > max_ucb_val:
                max_ucb_val = ucb
                best_child = child
        #print("BEST CHILD = ", best_child)
        return best_child

    
    def simulate(self):
        # print(state.planes_to_land)
        # print("Children of self : ", self.children, "N value of self: ", self.N)
        current_state = self.state.copy()
        planes_to_land = current_state.planes_to_land
        total_reward = 0
        landed = list()
        while planes_to_land:
            # Assign probabilities based on priority to create that stochastic environment
            total_priority = 0 
            for plane in planes_to_land:
                # Priority is determined by fuel level and hours until arrival
                # Lower fuel and fewer hours are critical; they should have higher priority.
                priority = 1 / (plane["fuel"] +1) + 1 / (plane["eta_arr"] + 1)
                # priority = 1 / (plane["fuel"] + 100)
                total_priority += priority  # Sum up the priorities for normalization

            # Initialize a list to hold probabilities
            # Divide each plane's priority by the total priority to ensure probabilities sum to 1.
            probabilities = list()  
            for plane in planes_to_land:
                priority = 1 / (plane["fuel"] + 1) + 1 / (plane["eta_arr"] + 1)
                # priority = 1 / (plane["fuel"] + 100) + 1

                probability = priority / total_priority
                probabilities.append(probability) 
            # Randomly select a plane based on probabilities
            # print("probabilities", probabilities)
            selected_plane = random.choices(planes_to_land, weights=probabilities, k=1)[0]
            # print("selected plane:", )
            planes_to_land.remove(selected_plane)

            #Find the reward based on the fuel and time till arrival
            #Prioritizes lower fuel and less time till arrival 
            fuel_reward = max(0, 100 - selected_plane["fuel"])
            time_penalty = max(0, selected_plane["eta_arr"] * 100)
            
            #Rewarding fuel more than time
            landing_reward = fuel_reward - time_penalty


            #update the total reward with the reward for landing this plane
            total_reward += landing_reward
            # if total_reward <= 0:
            #     print("total reward is off")

            # Update the state (e.g., land the plane, adjust others)
            current_state.landed.append(selected_plane)
            landed = current_state.landed #last path is the only we care about
            
            # print("Current Plane: ", selected_plane)
            # print("List of landed planes: ", current_state.landed)
            # print("Number of planes landed = ", len(current_state.landed))
            # print("List of planes to land: ", current_state.planes_to_land)
            #Check crashes
            for plane in planes_to_land:
                plane["fuel"] -= 1
                plane["eta_arr"] -= .001             
                if plane["fuel"] <= 0 or plane["eta_arr"] <= 0:
                    #Penalize crashes
                    total_reward -= 1000 
        
        print("total reward: at the end of simulate", total_reward)
        return total_reward,deepcopy(landed)

    def backpropagate(self, reward):
        #backprop the result of the simulation up the tree, updating the N and value
        curr_node = self
        count = 0
        while curr_node is not None:
            curr_node.N+=1
            curr_node.T+=reward
            curr_node =curr_node.parent
            
            count+=1
        print("count :", count)
            

        
        
def MCTS(root, iterations = 100):
    # print("in MCTS")
    reward_path = list ()
    for _ in range(iterations):
        node = root
        # print(node.state.planes_to_land)
        #TODO: MUST SELECT!!!
        # print("children before expand: ", node.children)
        while node.children: 
            node = node.select()
            # select(node)
        
        # print("returned node: ", node.state)
        if not node.state.is_terminal():
            node.expand()
            # print("Number of children: ", len(node.children))
        #simulate!
        """
            1. node is a leaf node (node has no children)
            2. the node is visited for the first time 
        """
        if node.children:
            #Random rollout 
            # print("Node.children right before simulate: ", node.children)
            node = random.choice(node.children)
            # print("Node that we chose to simulate on: ", node, "Children of selected node: ", node.children)
        reward, landed = node.simulate()
        print("reward after return of simulate: ", reward)
        #reward_path.append({"reward": reward, "landed": landed})
        print("reward after return of simulate: ", reward)
        print("Reward: ", reward, "path length: ", len(landed), ", Path: ", landed)
        #Add to data structure to hold the rewards and associated landing pattern
        result.append((reward, landed))

    
        #Backprop!
        node.backpropagate(reward)
        # print("children from backproppppp = ", node.children)
        # backpropagate(node, reward)
    # print("\n\n\n\n root children: ", len(root.children))
    print("r0: " ,result[0])
    print("r1: ", result[1])
    highest_reward = -999999
    optimal_path = None
    best_index = 0

    for pair in result: 
        if pair[0] > highest_reward: 
            highest_reward = pair[0]
            optimal_path = pair[1]
    print(highest_reward)
    return optimal_path
        


   


if __name__ == "__main__":
    landed_planes = list()
    
    initial_ordering = AirspaceState(flights,landed_planes, time=0 )
    
    root = Node(initial_ordering)
    # print(root.state.planes_to_land)
    sequence = MCTS(root, iterations=100)
    print("Sequence = ", sequence)
 


    #find the highest reward of all the sequences and output the schedule of planes
    # maximum_rew = -999999
    # for r in sequence
    # print()
    # print()
    # print("landing sequence = ", sequence)