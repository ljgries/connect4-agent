import torch
from model import Connect4Model
from mcts import Node, run_mcts  # Assuming run_mcts is implemented in mcts.py
from game import get_init_board, get_valid_moves, place_piece, is_win, is_board_full  # Assuming draw_board is a function to visually represent the board

def play_game(model, device):
    board = get_init_board()
    player_turn = 1  # Assuming player 1 is the model, and -1 would be the human or another strategy

    while not is_board_full(board) and not is_win(board, player_turn):
        if player_turn == 1:
            # AI's turn
            root = Node(prior=0, turn=player_turn, state=board)
            action, _ = run_mcts(root, model, device)
            board = place_piece(board, player_turn, action)
        else:
            # Human's turn (or another strategy)
            # Here you can implement human input or another strategy
            valid_moves = get_valid_moves(board)
            action = int(input(f"Enter your move (0-6): "))
            while action < 0 or action > 6 or valid_moves[action] != 1:
                action = int(input(f"Invalid move. Enter your move (0-6): "))
            board = place_piece(board, player_turn, action)

        player_turn *= -1  # Switch player
        print(board)  # Draw the board after each move

    # Check the game outcome
    if is_win(board, 1):
        print("AI wins!")
    elif is_win(board, -1):
        print("Human wins!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = Connect4Model(device)
    model_name = 'final_trained_model.pth' # change to your trained model
    model_path = 'models/' + model_name
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    play_game(model, device)