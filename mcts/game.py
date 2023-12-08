from GameState import ConnectState
from mcts import MCTS


def play():
    state = ConnectState()
    mcts = MCTS(state)

    while not state.game_over():
        print("Current state:")
        state.print()

        while True:
            try:
                print("Valid moves: ", state.get_legal_moves())
                user_move = int(input("Enter a move: "))
                if user_move in state.get_legal_moves():
                    break  # Exit the loop if the move is legal
                else:
                    print("Illegal move!")
            except ValueError:
                print("Please enter a valid integer.")

        state.move(user_move)
        mcts.move(user_move)

        state.print()

        if state.game_over():
            print("Player one won!")
            break

        print("Thinking...")

        mcts.search(10)
        num_rollouts, run_time = mcts.statistics()
        print("Statistics: ", num_rollouts, "rollouts in ", run_time, "seconds")
        move = mcts.best_move()

        print("MCTS chose move: ", move)

        state.move(move)
        mcts.move(move)

        if state.game_over():
            state.print()
            print("Player two won!")
            break


if __name__ == "__main__":
    play()
