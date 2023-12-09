# Commands

## Train a model

To train a model for Connect 4 you can run: `python3 main.py`. This uses the neural network architecture defined in `Connect4NNet.py` with training logic in `NNet.py` and mcts logic in `MCTS.py` to train a model using self-play. By default, it runs for 250 iterations and outputs a `./temp/best.pth.tar` file representing the model.

## Play against model

To play against a pre-trained model, you can run: `python3 pit.py` (from this folder).. By default, this will let a human player (you) interactively play 2 games against the model in `models/best.pth.tar` by generating a board and asking you to make moves. You can make changes to this file to evaluate the model's performance against different type of players such as a random player or a one step lookahead player.
