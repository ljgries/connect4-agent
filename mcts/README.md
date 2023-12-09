# Commands

## Play a game

You can play a game against the MCTS implementation using `python3 game.py`. This will render the current state of the board and provide you a list of valid moves for that state. By default, the MCTS search runs for 10 secs- you can increase or decrease this time to adjust the difficulty of the algorithm.

## Evaluate performance against random player

To evaluate the performance of the MCTS algorithm against a random opponent, run `python3 game_random.py`. This defines two opponents- the MCTS player that searches for 10 secs and a random player that picks any valid move. By default, 10 games are played and the percent of games won by MCTS are reported.
