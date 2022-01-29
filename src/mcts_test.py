from mcts import *

state = State(StateDice('115555', []), need_to_score=True)
root = Node(state)
tree = Tree(root)

best_child = tree.best_action(100)
# print(root.next_nodes)
print(best_child)
print(tree.root.children)
