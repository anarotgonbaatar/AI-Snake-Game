# AI Snake Game

## Overview

AI Snake Game is a python implementation of the classic Snake game with 4 game modes, including AI controlled snakes. The project demonstrates the use of the A\* pathfinding algorithm in a grid-based environment.

## Game Modes

- **Single-Player Mode:** Classic Snake game. Control the snake, eat food, and grow your score.
- **AI Mode:** Watch the AI snake navigate towards the food using the A\* pathfinding algorithm.
- **Player vs AI Mode:** Compete agaisnt the AI snake.
- **AI vs AI Mode:** Watch two AI snakes compete against each other.

## Installation

1. **Clone the repository:**

   - `git clone https://github.com/anarotgonbaatar/AI-Snake-Game.git`

2. **Install dependencies:**

   - Install Python
   - `pip install pygame`

3. **Run the game:**

   - `python main.py`

## Core Concepts

### Pathfinding with A\* Algorithm:

- `ai_logic.py`:
  - Uses the A\* algorithm to calculate the shortest path from the snake head to the food position
  - Supports different heuristics:
    - **Manhattan:** Ideal for grid based movement, such as this
    - **Euclidian:** Ideal for diagonal movement
    - **Chebyshev:** Maximum distance along any axis

### Collision Handling:

- `check_collisions` makes sure the snakes avoid walls, themselves, and other snakes.

### Grid-based Movement:

- Snakes move in steps on a grid platform with the `BLOCK_SIZE` dimensions.

## Controls

- **Player movement:**
  - Arrow keys: up, down, right, and left arrow keys to control the snake.

## How It Works

### Game Loop

- Each game mode inherits from the `SnakeGame` class from `snake_game.py`, which provides shared functions like:
  - Snake movement: `update_player_snake_location()`
  - Collision detection: `check_collisions()`
  - Rendering: `draw_all()`

### AI Pathfinding

- The AI calculates its path using `aStar_search()` function in `ai_logic.py`.
- It dynamically avoid the walls/bounds, itself, and other snakes using the `valid_position()` function.

### Future Improvements

- Implement reinforcement learning (RL) to make AI snakes learn from their mistakes.

## Credits

- **Developers:**
  - Anar Otgonbaatar
  - Puthioudom Chum
  - Steven Ly
  - Tri Bui
- **Framework:** Python with `pygame`
