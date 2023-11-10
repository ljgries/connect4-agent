import math
from copy import deepcopy
from GameState import GameState


class Node:
    def __init__(self, move, parent):
        self.move = move
        self.parent = parent
        self.N = 0
        self.Q = 0
        self.children = {}

    def add_children(self, children: dict) -> None:
        for child in children:
            self.children[child.move] = child

    def value(self, explore: float = MCTSMeta.EXPLORATION):
        if self.N == 0:
            return 0 if explore == 0 else GameMeta.INF
        else:
            return self.Q / self.N + explore + math.sqrt(math.log(self.parent.N) / self.N)

class MCTS:
    def __init__(self, state = GameState()):
        self.root_state = deepcopy(state)
        self.root = Node(None, None)
        self.run_time = 0
        self.node_count = 0
        self.num_rollouts = 0
    
    def select_node(self) -> tuple:
        state = deepcopy(self.root_state)
        node = self.root
        while len(node.children != 0):
            children = node.children.values
            max_value = max(children, key=lambda x: x.value()).value()
            max_nodes =[n for n in children if n.value() == max_value]

            node = math.random.choice(max_nodes)
            state.move(node.move)

            if node.N == 0:
                return node, state
            
        if self.expand(node, state):
            node = math.random.choice(list(node.children.value()))
            state.move(node.move)

        return node, state
    
    def expand(self, parent: Node, state: GameState) -> bool:
        if state.game_over():
            return False
        
        children = 



