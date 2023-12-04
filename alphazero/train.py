import torch
import torch.optim as optim
from model import Connect4Model
from mcts import run_mcts, Node, prepare_board  # Assume run_mcts is a function you define in mcts.py for running MCTS
from game import get_init_board, place_piece, is_win, is_board_full

torch.autograd.set_detect_anomaly(True)

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize the model
model = Connect4Model(device)
model.train()

# Optimizer and loss function
optimizer = optim.Adam(model.parameters(), lr=0.01)
value_criterion = torch.nn.MSELoss()
policy_criterion = torch.nn.CrossEntropyLoss()

def train_step(board, policy_target, value_target):
    # Convert to tensors
    board_tensor = prepare_board(board).unsqueeze(0).to(device)
    
    # Extract the action index with the highest probability/visit count
    action_index = policy_target.index(max(policy_target))
    policy_target_tensor = torch.tensor([action_index], dtype=torch.long).to(device)
    
    value_target_tensor = torch.tensor([value_target], dtype=torch.float32).to(device)

    # Forward pass
    optimizer.zero_grad()
    value, policy = model(board_tensor)

    value_loss = value_criterion(value.squeeze(), value_target_tensor.squeeze())
    policy_loss = policy_criterion(policy, policy_target_tensor)

    # Backward and optimize
    total_loss = value_loss + policy_loss
    total_loss.backward()
    optimizer.step()

    return total_loss.item()

def collect_data_from_game():
    # Initialize a new game
    board = get_init_board()
    player_turn = 1  # Player 1 starts
    game_data = []

    while not is_board_full(board) and not is_win(board, player_turn):
        root = Node(prior=0, turn=player_turn, state=board)
        action, policy_target = run_mcts(root, model, device)  # run_mcts to be implemented in mcts.py
        print("Policy target from MCTS:", policy_target)
        # Record the state, policy target, and value target (which is unknown at this stage)
        game_data.append([board.copy(), policy_target, None])

        # Make the move
        board = place_piece(board, player_turn, action)
        player_turn *= -1  # Switch player
    print(board)

    # Assign value targets based on game outcome
    value_target = 1 if is_win(board, 1) else -1 if is_win(board, -1) else 0
    for data in game_data:
        if data[2] is None:
            data[2] = value_target if data[1] == player_turn else -value_target

    return game_data

# Main training loop
num_epochs = 100
for epoch in range(num_epochs):
    print(f"Epoch {epoch}")
    game_data = collect_data_from_game()
    print("here")
    total_loss = 0
    for board, policy_target, value_target in game_data:
        loss = train_step(board, policy_target, value_target)
        total_loss += loss
        print(f"Loss {loss}")
    print(f"Epoch {epoch}, Loss: {total_loss/len(game_data)}")

torch.save(model.state_dict(), 'final_trained_model.pth')