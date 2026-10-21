# Tic-Tac-Toe

A desktop Tic-Tac-Toe game built with Python and PySide6, featuring local multiplayer, a disappearing-marks mode, and AI opponents powered by a neural network built from scratch.

This project started as a way to practice Python, learn GitHub and build a playable GUI to then implement and train my first AI using reinforcement learning. 

## Game modes

| Mode | Description |
| --- | --- |
| Classic PvP | Two players take turns on the same computer. Get three marks in a row to win. |
| Disappearing PvP | Each player can keep only three marks on the board. Placing a fourth removes their oldest mark. |
| Classic PvE | Play traditional Tic-Tac-Toe against a trained AI. |
| Disappearing PvE | Play against an AI while keeping track of which marks will disappear next. |

In classic mode, a full board without a winner ends in a draw. In disappearing mode, the board keeps changing, so filling it up does not end the game. You have to plan around both players' oldest marks.

## Features

- Desktop interface built with PySide6.
- A menu for choosing game modes.
- An in-app guide explaining how to play.
- Local two-player gameplay.
- AI opponents trained through reinforcement learning and self-play.
- Saved model weights for loading trained agents.

## About the AI

The neural network and its learning logic were implemented from scratch in Python as I didn't want to use any tools for my first ever neural network. The AI uses separate weights for X and O and learns from rewards associated with game outcomes.

During training, the agents explore moves and play against each other. In classic mode, the board is represented numerically using empty cells, X marks, and O marks. In disappearing mode, the representation also includes the age of each mark, since knowing which one disappears next matters when choosing a move.

Training the agents involved experimenting with rewards, exploration, and state representations. It also involved fixing problems such as illegal moves and unstable network values.

The AI has learned useful strategies, but it is not guaranteed to play perfectly. It can still miss blocks or struggle with particular board positions. Exploring those weaknesses is part of the project.

## Built with

- **Python** for the game and AI logic.
- **PySide6** for the desktop interface.
- **JSON** for saved neural network weights.

## Running the game

Download or clone the project, then open a terminal in its root folder.

Install PySide6:

```bash
py -m pip install PySide6
```

Start the application:

```bash
py main.py
```

These commands use the Windows Python launcher. If your system uses `python` or `python3`, substitute that command for `py`.

Keep the project's images, weight files, and other supporting files in their original locations. The AI modes need their saved weights to load correctly.

> These setup steps assume `main.py` is the entry point and PySide6 is the GUI dependency. They should be checked against the current project before publishing this README.

## What I learned

- Building and connecting windows in a desktop application.
- Managing turns, win conditions, and changing board states.
- Implementing a neural network and backpropagation from scratch.
- Training agents through self-play.
- How reward design and state representation affect learning.
- Why strong training results do not always mean an agent handles every situation well.

## Possible improvements

- Improve the AI's consistency when blocking immediate wins.
- Evaluate trained agents against a wider range of opponents and board positions.
- Experiment with minimax-based feedback to help the agents identify better and worse moves during training.

## Author

Adriel Yens
