import torch
import numpy as np
import math
from game import get_init_board, place_piece, get_valid_moves, is_board_full, is_win

# Define the Node class for MCTS
class Node:
    def __init__(self, prior, turn, state):
        self.prior = prior
        self.turn = turn
        self.state = state
        self.children = {}
        self.value = 0
        self.visits = 0

    def expand(self, action_probs):
        valid_moves = get_valid_moves(self.state)  # Get valid moves for the current state
        for action, prob in enumerate(action_probs):
            if prob > 0 and valid_moves[action] == 1:
                next_state = place_piece(board=self.state, player=self.turn, action=action)
                self.children[action] = Node(prior=prob, turn=-self.turn, state=next_state)

    def select_child(self):
        max_score = -float('inf')
        selected_action = None
        selected_child = None
        for action, child in self.children.items():
            score = ucb_score(self, child)
            if score > max_score:
                selected_action = action
                selected_child = child
                max_score = score
        return selected_action, selected_child

def ucb_score(parent, child):
    prior_score = child.prior * math.sqrt(parent.visits) / (child.visits + 1)
    value_score = child.value / child.visits if child.visits > 0 else 0
    return value_score + prior_score

def prepare_board(board):
    # Transform the board into a 3x6x7 tensor
    # Channel 1: Player 1's pieces
    # Channel 2: Player 2's pieces
    # Channel 3: Empty spaces
    player1_channel = (board == 1).astype(float)
    player2_channel = (board == -1).astype(float)
    empty_channel = (board == 0).astype(float)
    board_tensor = np.stack([player1_channel, player2_channel, empty_channel], axis=0)
    return torch.tensor(board_tensor, dtype=torch.float32)

# Function to run MCTS
def run_mcts(root_node, model, device, num_simulations=100):
    for _ in range(num_simulations):
        node = root_node
        search_path = [node]

        # Selection and Expansion
        while len(node.children) > 0:
            action, node = node.select_child()
            search_path.append(node)

        # Rollout and Backpropagation
        if is_board_full(node.state) or is_win(node.state, node.turn):
            value = 1 if is_win(node.state, node.turn) else 0
        else:
            # Use the model for prediction
            board_tensor = prepare_board(node.state).unsqueeze(0).to(device)
            with torch.no_grad():
                model_value, model_policy = model(board_tensor)

            # Adjusted handling of model output
            if model_value.numel() == 1:
                value = model_value.squeeze().item()  # Ensure it's a single scalar
            else:
                print("Unexpected model value shape:", model_value.shape)  # Debug print
                raise ValueError("Model value output is not a single scalar")

            policy = model_policy.squeeze(0).tolist()
            node.expand(policy)

        # Backpropagate the value
        for node in reversed(search_path):
            node.value += value
            node.visits += 1
            value = -value  # Invert value for the opponent

    # Choose the action with the highest visit count
    best_action = max(root_node.children.items(), key=lambda item: item[1].visits)[0]
    policy_vector = [root_node.children[i].visits if i in root_node.children else 0 for i in range(7)]

    return best_action, policy_vector