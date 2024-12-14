import math
from numpy import random
from DummyData import flights

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action #Action we took to get to the node
        self.children = []
        self.visits = 0
        self.reward = 0
        self.tried_actions = set()

    def is_fully_expanded(self):
        #If we haven't tried to land all of our planes, is_fully_expanded returns false
        if len(self.tried_actions) == len(self.state["planes"]):
            return True
        return False


def transition(state, action):
    #Passing in the plane that we'll land (action) and creating a new state list of planes to land
    plane_to_land = action
    new_planes = []
    for plane in state["planes"]:
        if plane["id"] != plane_to_land["id"]:
            # print("Plane fuel: " , plane["fuel"])
            #The next time we need to land a plane, we should have less fuel than we have now
            plane["fuel"] -= 0.1
            new_planes.append(plane)
    #Return the new state S' = transition(state, action)
    return {"planes": new_planes, "landed_planes": state["landed_planes"] + [{"plane": plane_to_land, "time": state["time"] + 1}],"time": state["time"] + 1}


def reward(state):
    fuel_check = False
    for plane in state["planes"]:
        if plane["fuel"] < 0:
            fuel_check = True
            break
    if fuel_check:
        return -1000
    if not state["planes"]:
        return 1000
    distance_penalty = 0
    for plane in state["planes"]:
        #Adding distance to distance penalty (which is bad in reality)
        distance_penalty += plane["distance"]
    fuel_penalty = 0
    for plane in state["planes"]:
        fuel_penalty += max(0, 10000 - plane["fuel"])
    

    #Less negative (higher value) = land first
    return -distance_penalty - fuel_penalty

# def reward(state):
#     fuel_check = False
#     for plane in state["planes"]:
#         if plane["fuel"] < 0:
#             fuel_check = True
#             break
#     if fuel_check:
#         return -1000
#     if not state["planes"]:
#         return 1000
#     fuel_penalty = 0
#     for plane in state["planes"]:
#         fuel_penalty += max(0, 10000 - plane["fuel"])
#     return  fuel_penalty



def select_action(state):
    best_plane = random.choice(state["planes"])
    # print("Best plane: ", best_plane)
    for plane in state["planes"]:
        if plane["fuel"] < best_plane["fuel"] or (plane["fuel"] == best_plane["fuel"] and plane["distance"] < best_plane["distance"]):
            best_plane = plane
    return best_plane


def simulate(state):
    while state["planes"]:
        action = select_action(state)
        state = transition(state, action)
        for plane in state["planes"]:
            if plane["fuel"] < 0:
                return reward(state)
    return reward(state)


def select_node(node):
    while node.children:
        #Take the first child, find its UCB value 
        best_child = node.children[0]
        #Initial best value is the value of the first child we've looked at
        best_value = best_child.reward / best_child.visits + math.sqrt(math.log(node.visits) / best_child.visits)

        #Find UCB  vals of all children
        for child in node.children:
            #UCB formula
            exploit = child.reward / child.visits
            exploration_value = math.sqrt(math.log(node.visits) / child.visits)
            child_value = exploit + exploration_value
            
            #Update the best value if we've found a better child to land first
            if child_value > best_value:
                best_child = child
                best_value = child_value
        #Update node 
        node = best_child
    #If node has no children, we return self (likely have to expand)
    return node


def expand(node):
    untried_actions = []
    for plane in node.state["planes"]:
        # print("length of node.state.planes in expansion: " , len(node.state["planes"]))
        #Haven't tried to land the plane yet 
        if plane["id"] not in node.tried_actions:
            untried_actions.append(plane)
            # print("Length of untried actions = " , len(untried_actions))
    #If there are planes to land still, need to expand and create nodes
    if untried_actions:
        #Choosing a plane to land, which will lead to a new state consisting of the current state as it transitions (decrementing fuel) and 
        # action = select_action(node.state)
        #SELECT ACTION INLINED
        best_plane = random.choice(node.state["planes"])
        #The plane we need to prioritize landing is the one that has the least fuel or the least distance to airport
        for plane in node.state["planes"]:
            if plane["fuel"] < best_plane["fuel"] or (plane["fuel"] == best_plane["fuel"] and plane["distance"] < best_plane["distance"]):
                best_plane = plane
        #Found either closest plane or lowest fuel 
        action = best_plane

        #Find the next state after landing the current plane (take action)
        new_state = transition(node.state, action)
        child_node = Node(new_state, parent=node, action=action)
        node.children.append(child_node)
        print()
        node.tried_actions.add(action["id"])
        return child_node
    return None


def backpropagate(node, reward_value):
    while node:
        node.visits += 1
        node.reward += reward_value
        node = node.parent


def mcts(initial_state, iterations):
    #setting our root to initial state of planes that need to land 
    root = Node(initial_state)

    for _ in range(iterations):
        #Call selection to find the best node to expand 
        node = select_node(root)
        if not node.is_fully_expanded():
            # print("Length of node.children before expansion: " , len(node.children))
            child = expand(node)
            # print("Length of node.children after expansion: " , len(node.children))
        else:
            child = node
        reward_value = simulate(child.state)
        backpropagate(child, reward_value)
    best_child = root.children[0]
    for child in root.children:
        if child.visits > best_child.visits:
            best_child = child
    return best_child.action


def main():
    # Example setup of planes
    planes = flights

    initial_state = {
        "planes": planes,
        "landed_planes": [],
        "time": 0,
    }

    print("Initial state:", initial_state)


    while initial_state["planes"]:
        # print("Initial state of planes at start of each iteration: ", len(initial_state["planes"]))

        #Best action is the plane we need to land in this "timestep", where timestep relates to the number of planes we need to land 
        best_action = mcts(initial_state, iterations=10)
        # print("Best action to take: ", best_action)
        print(f"Landing plane: {best_action} at time {initial_state['time'] + 1}")
        initial_state = transition(initial_state, best_action)

    print("All planes have landed.")
    for landed in initial_state["landed_planes"]:
        print(f"Plane {landed['plane']['id']} landed at time {landed['time']}")


if __name__ == "__main__":
    main()




