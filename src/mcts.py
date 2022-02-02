from ai_test import *
import numpy as np
from util import *


class Node(object):
    def __init__(self, state: State, parent=None):
        self.state = state
        self._next_states = state.next_states
        self.value = 0
        self.number_visit = 0
        self.parent = parent
        self.children = []

    def __repr__(self):
        return 'Scoring dice: %-15s' % self.state.state_dice.scoring_dice + ', last action: ' + str(self.state.last_action) + ', state score: ' + str(self.state.score) +\
               ', value: ' + str(self.value) + ', number visit: ' + str(self.number_visit) + '\n'

    @property
    def n(self):
        return self.number_visit

    # @property
    # def next_states(self):
    #     """
    #
    #     Returns: list of State
    #     """
    #     if not hasattr(self, '_next_states'):
    #         pass
    #     return self.state.next_states

    def expand(self):
        next_state = self._next_states.pop()
        child_node = Node(next_state, self)
        self.children.append(child_node)
        return child_node

    def simulate(self):
        # return 1/pow(get_num_round(self.state), 0.1)
        return 1 / get_num_round(self.state)

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
        return len(self._next_states) == 0

    def best_child(self, c_param=1.4):
        if not self.children:
            # Farkle!
            return Node(self.state.action_farkle(), self)
        choices_weights = [
            sigmoid(c.value) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            # 1 * (c.value/c.n) + c_param * np.sqrt((2 * np.log(self.n) / c.n))
            for c in self.children
        ]

        # for c in self.children:
        #     print('value: ' + str(self.value) + ', para: ' + str(c_param * np.sqrt((2 * np.log(self.n) / c.n))))
        # if c_param==0:
        #     print('choices: ' + str(choices_weights))
        #     print('children: ' + str(self.children))
        return self.children[np.argmax(choices_weights)]


class Tree:

    def __init__(self, node: Node):
        self.root = node

    def best_action(self, simulations_number):
        for _ in range(0, simulations_number):
            # Selection
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
