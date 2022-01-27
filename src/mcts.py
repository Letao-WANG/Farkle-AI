from ai_test import *
import numpy as np


class Node(object):
    def __init__(self, state: State, parent=None):
        self.state = state
        self.value = 0
        self.number_visit = 0
        self.parent = parent
        self.children = []

    def __repr__(self):
        return str(self.state.last_action) + ' \n' + str(self.state)

    @property
    def n(self):
        return self.number_visit

    @property
    def next_nodes(self):
        """

        Returns: list of Node
        """
        return [Node(next_state, self) for next_state in self.state.next_states]

    def expand(self):
        print('Before: ' + str(self.state.next_states))
        next_state = self.state.next_states.pop()
        print('After: ' + str(self.state.next_states))
        child_node = Node(next_state, self)
        self.children.append(child_node)
        return child_node

    def simulate(self):
        return 1/get_num_round(self.state)

    def is_terminal_node(self):
        return self.state.game_over

    def backpropagation(self, result):
        """
        :param result: result of simulation
        :return:
        """
        self.number_visit += 1
        self.value += result
        if self.parent:
            self.parent.backpropagation(result)

    def is_fully_expanded(self):
        return len(self.next_nodes) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            self.value + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]


class Tree:

    def __init__(self, node: Node):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            # Selection and expansion
            v = self.select()
            # Simulation
            result = v.simulate()
            # Backpropagation
            v.backpropagation(result)
        return self.root.best_child(c_param=0)

    def select(self):
        current_node = self.root
        while not current_node.is_terminal_node():

            # Expansion
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                # Selection
                current_node = current_node.best_child()
        return current_node
