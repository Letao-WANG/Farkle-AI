from mcts import *

# state = State(StateDice('224455', []), need_to_score=True)
combo = '5'
state = State(StateDice('224455', []), need_to_score=True).action_score(combo)
root = Node(state)
tree = Tree(root)

# best_child = tree.best_action(500)
best_child = ai_minMax(state)
# print(root.next_nodes)
print(root)
print(best_child)
print(tree.root.children)



