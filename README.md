# BitChess

BitChess is a simple chess game written in Python using the `python-chess` and `pygame` libraries. It allows you to play
against any compatible chess engine.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Code Structure](#code-structure)

## Features

- Play against any compatible chess engine.
- Simple and intuitive graphical interface.
- Sound effects for moves and captures.
- Game over detection (checkmate, stalemate, draw).

## Installation

1. Make sure you have Python 3 installed.
2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```
3. Download a compatible chess engine executable for your operating system. You can find the Stockfish executable
   [here](https://stockfishchess.org/).
4. Place the Stockfish executable in a folder named `engine` in the same directory as the Python script.
5. Change the `ENGINE_PATH` variable in the `main.py` script to point to the engine executable.

## How to Play

1. Run the `main.py` script:

   ```bash
   python main.py
   ```

2. Click on a white piece to select it.
3. Click on a valid square to move the piece to.
4. The engine will play its move after you.
5. The game ends when there is a checkmate, stalemate or draw.

## Code Structure

The code is organized into the following functions:

- `draw_chessboard()`: Draws the chessboard on the screen.
- `draw_pieces()`: Draws the pieces on the chessboard.
- `play_ai()`: Makes the engine play a move.
- `display_game_over()`: Displays the game over message.
- `update_display()`: Updates the display.
- `main()`: The main function that runs the game loop.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

We hope you enjoy BitChess! If you'd like to contribute, feel free to open an issue or submit a pull request. Your
feedback and improvements are always valued!

---
