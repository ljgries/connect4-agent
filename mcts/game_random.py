import random
from GameState import ConnectState
from mcts import MCTS
from meta import GameMeta

# Random Agent Function
def random_agent(state):
    legal_moves = state.get_legal_moves()
    print("Legal moves for random agent:", legal_moves)  # Debugging print
    if legal_moves:
        return random.choice(legal_moves)
    else:
        print("No legal moves available for random agent")  # Additional debugging print
        return None


def play():
    state = ConnectState()
    mcts = MCTS(state)

    # Randomly choose which player starts
    mcts_starts = random.choice([True, False])
    if mcts_starts:
        player_one, player_two = "mcts", "random"
    else:
        player_one, player_two = "random", "mcts"

    print(f"Player One: {player_one}, Player Two: {player_two}")  # Debugging print

    while not state.game_over():
        state.print()
        move = None

        if state.to_play == GameMeta.PLAYERS["one"]:
            if player_one == "random":
                move = random_agent(state)  # Use random_agent for random player
            elif player_one == "mcts":
                move = get_mcts_move(mcts, state)
        else:
            if player_two == "random":
                print("Random agent is about to make a move")  # Debugging print
                move = random_agent(state)  # Use random_agent for random player
            elif player_two == "mcts":
                move = get_mcts_move(mcts, state)


        if move is not None:
            state.move(move)
            mcts.move(move)
        else:
            print(f"Error: No move generated for player {state.to_play}")
            return None, mcts_starts

        if state.game_over():
            state.print()
            winner = "Player One" if state.check_win() == GameMeta.PLAYERS["one"] else "Player Two"
            print("Game Over. Winner:", winner)
            return winner, mcts_starts

    # If the game loop exits without a winner
    return None, mcts_starts

def get_human_move(state):
    while True:
        try:
            print("Valid moves: ", state.get_legal_moves())
            user_move = int(input("Enter a move: "))
            if user_move in state.get_legal_moves():
                return user_move
            else:
                print("Illegal move!")
        except ValueError:
            print("Please enter a valid integer.")

def get_mcts_move(mcts, state):
    print("Thinking...")
    mcts.search(10)
    num_rollouts, run_time = mcts.statistics()
    print("Statistics: ", num_rollouts, "rollouts in ", run_time, "seconds")
    return mcts.best_move()

def play_multiple_games(num_games):
    mcts_wins = 0
    for _ in range(num_games):
        winner, mcts_was_player_one = play()
        if winner is not None:
            if (winner == "Player One" and mcts_was_player_one) or (winner == "Player Two" and not mcts_was_player_one):
                mcts_wins += 1
    return mcts_wins / num_games * 100

if __name__ == "__main__":
   win_percentage = play_multiple_games(10)
   print("Win Percentage:", win_percentage)
