import math
from numpy import random
from DummyData import flights

class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action
        self.children = []
        self.visits = 0
        self.reward = 0
        self.tried_actions = set()

    def is_fully_expanded(self):
        if len(self.tried_actions) == len(self.state["planes"]):
            return True
        return False


def transition(state, action):
    plane_to_land = action
    new_planes = []
    for plane in state["planes"]:
        if plane["id"] != plane_to_land["id"]:
            print("Plane fuel: " , plane["fuel"])
            plane["fuel"] -= 0.1
            # plane["distance"] -=
            new_planes.append(plane)
    return {
        "planes": new_planes,
        "landed_planes": state["landed_planes"] + [{"plane": plane_to_land, "time": state["time"] + 1}],
        "time": state["time"] + 1,
    }


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
        fuel_penalty += max(0, 10 - plane["fuel"])
    return -distance_penalty - fuel_penalty


def select_action(state):
    best_plane = state["planes"][0]
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
        best_child = node.children[0]
        best_value = best_child.reward / best_child.visits + math.sqrt(math.log(node.visits) / best_child.visits)
        for child in node.children:
            child_visits_ratio = child.reward / child.visits
            exploration_value = math.sqrt(math.log(node.visits) / child.visits)
            child_value = child_visits_ratio + exploration_value
            if child_value > best_value:
                best_child = child
                best_value = child_value
        node = best_child
    return node


def expand(node):
    untried_actions = []
    for plane in node.state["planes"]:
        if plane["id"] not in node.tried_actions:
            untried_actions.append(plane)
    if untried_actions:
        action = select_action(node.state)
        new_state = transition(node.state, action)
        child_node = Node(new_state, parent=node, action=action)
        node.children.append(child_node)
        node.tried_actions.add(action["id"])
        return child_node
    return None


def backpropagate(node, reward_value):
    while node:
        node.visits += 1
        node.reward += reward_value
        node = node.parent


def mcts(initial_state, iterations=1000):
    root = Node(initial_state)
    for _ in range(iterations):
        node = select_node(root)
        if not node.is_fully_expanded():
            child = expand(node)
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
        print("Initial state of planes at start of each iteration: ", len(initial_state["planes"]))

        best_action = mcts(initial_state, iterations=500)
        print(f"Landing plane: {best_action} at time {initial_state['time'] + 1}")
        initial_state = transition(initial_state, best_action)

    print("All planes have landed.")
    for landed in initial_state["landed_planes"]:
        print(f"Plane {landed['plane']['id']} landed at time {landed['time']}")


if __name__ == "__main__":
    main()




