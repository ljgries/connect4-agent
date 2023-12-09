# Connect4 Agent

Connect 4 "Alpha Zero" agent implemented with MCTS and CNNs.

## Structure

We have the follwing three components for our project that build on each other:

- Monte Carlo Tree Search
- Initial AlphaZero implementation
- Refined AlphaZero implementation using a general framework

The files for each of these are contained in their own sub-directories along with a README.md with information about how to run various commands. The Python dependencies are defined in the requirements.txt file provided at project root.

## Installation

Open a terminal and navigate to project root directory (where this file is located). 

We recommend creating a python 3.8 venv:

0. `brew install python@3.8` (if needed)
1. `python3.8 -m venv "testenv"`
2. `source testenv/bin/activate`

Then run `pip3 install -r requirements.txt` to download all dependencies. Note: this operation may take some time to finish as `torch` is a large package with its own dependencies.

## Citations

Initial MCTS:
https://www.youtube.com/watch?v=EB-NJtNERBQ

Initial Alpha-Zero:
https://youtu.be/t5V197JVemI?si=2Jrzy814NrhAsL9W

Final Alpha-Zero:
https://github.com/suragnair/alpha-zero-general

