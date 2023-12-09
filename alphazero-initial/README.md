# Commands

## Train a model

To train a model for Connect 4 you can run: `python3 train.py`. This uses the neural network architecture defined in `model.py` and mcts logic in `mcts.py` to train a model using self-play. By default, it runs for a 100 iterations and outputs a final_trained_model.pth file representing the model.

## Play against model

To play against a pre-trained model, you can run: `python3 play_game.py`. By default, this will let a human player (you) interactively play against the model in `models/final_trained_model.pth` by generating a board and asking you to make moves. You can also change the name of the model in `play_game.py` to play against one that you have trained.
