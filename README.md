# connect4-agent

Connect 4 agent implemented with MCTS and (potentially) neural nets.

## Protocol

Changes should be pushed to a separate branch (not main) and merged via pull request.

## Citations

https://www.youtube.com/watch?v=EB-NJtNERBQ (majority of current code base)

https://youtu.be/t5V197JVemI?si=2Jrzy814NrhAsL9W (neural nets / alphazero folder)

### Conversations (post anything here)

Luke - The Alphazero implementation below would be cool to (at least try) to implement, using this codebase as a starting point.
https://web.stanford.edu/~surag/posts/alphazero.html#:~:text=AlphaGo%20Zero%20is%20trained%20by,framework%20to%20achieve%20stable%20learning

Liam - I'm working on the alphazero implementation, using the above youtube playlist as a starting point. This is an attempt to explore using a deep neural network to predict the next best move from any given state, using mcts to build training data. I have added a train.py file and a play_game.py file, as well as expanded and edited much of the starting code. You can run play_game.py to test the first trained model as well as train.py to test your own.