import heapq
import game
import utils
import pygame
import random


class SnakeAI:
    def __init__(self, game_instance):
        self.game = game_instance

    def aStar_search(self, start, goal):
        print(f"Starting A* from {start} to {goal}")
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        max_iterations = 500
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                print(f"Path found: {path}")
                return path

            neighbors = self.get_neighbors(current)
            print(f"Current position: {current}, Neighbors: {neighbors}")
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        print("No path found")
        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position):
        directions = [(0, -utils.BLOCK_SIZE), (0, utils.BLOCK_SIZE), (-utils.BLOCK_SIZE, 0), (utils.BLOCK_SIZE, 0)]
        neighbors = []
        for direction in directions:
            neighbor = (position[0] + direction[0], position[1] + direction[1])
            if self.valid_position(neighbor):
                neighbors.append(neighbor)
        print(f"Position: {position}, Valid neighbors: {neighbors}")
        return neighbors

    def valid_position(self, position):
        within_boundaries = 0 <= position[0] < utils.WIDTH and 0 <= position[1] < utils.HEIGHT
        not_colliding = position not in self.game.snake
        is_valid = within_boundaries and not_colliding
        print(
            f"Checking position: {position}, Within boundaries: {within_boundaries}, Not colliding: {not_colliding}, Valid: {is_valid}")
        return is_valid

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.insert(0, current)
            current = came_from[current]
        return path



    def get_next_move(self, food_position):
        head = self.game.snake[0]

        snake = [(utils.WIDTH // 2 // utils.BLOCK_SIZE * utils.BLOCK_SIZE, utils.HEIGHT // 2 // utils.BLOCK_SIZE * utils.BLOCK_SIZE)]
        direction = (utils.BLOCK_SIZE, 0)

        # Calculate the difference in x and y coordinates
        dx = food_position[0] - head[0]
        dy = food_position[1] - head[1]

        # Step 1: If one step away, move directly to food to prevent oscillation
        if abs(dx) == utils.BLOCK_SIZE and dy == 0:
            next_move = (head[0] + dx, head[1])
        elif abs(dy) == utils.BLOCK_SIZE and dx == 0:
            next_move = (head[0], head[1] + dy)
        # Step 2: Otherwise, move toward the food in the direction with the largest gap
        elif abs(dx) > abs(dy):
            next_move = (head[0] + (utils.BLOCK_SIZE if dx > 0 else -utils.BLOCK_SIZE), head[1])
        elif abs(dy) > 0:
            next_move = (head[0], head[1] + (utils.BLOCK_SIZE if dy > 0 else -utils.BLOCK_SIZE))
        else:
            # If already at the food position, stay there
            next_move = head

        print(f"Move decision: Head={head}, Food={food_position}, Next Move={next_move}")
        return next_move



def ai_only(win):
    print("Starting AI-only mode")

    # Set up initial snake position and food
    snake = [(utils.WIDTH // 2, utils.HEIGHT // 2)]
    food = utils.generate_food(snake)
    ai = SnakeAI(game_instance=type('', (object,), {"snake": snake})())
    score = 0
    running = True

    while running:
        pygame.event.pump()  # Keep the game responsive

        # AI decides the next move
        next_move = ai.get_next_move(food)

        # Check if the snake reaches the food
        if next_move == food:
            score += 1
            snake.insert(0, food)  # Grow the snake by adding the food position to the head
            food = utils.generate_food(snake)  # Generate new food
        else:
            # Move the snake to the next position
            snake.insert(0, next_move)  # Move the head

            snake.pop()  # Remove the tail segment unless food was eaten

        # Check for collisions with walls or itself
        if (snake[0][0] < 0 or snake[0][0] >= utils.WIDTH or
            snake[0][1] < 0 or snake[0][1] >= utils.HEIGHT or
            snake[0] in snake[1:]):
            game.game_over(win, score)
            running = False

        # Drawing
        win.fill(utils.BLACK)  # Clear the screen
        utils.draw_grid(win)  # Draw the grid background
        utils.draw_objects(snake, food, win)  # Draw snake and food
        utils.display_score(win, score)  # Display the score
        pygame.display.update()  # Update the display

        pygame.time.delay(100)  # Slow down AI for visual clarity

    pygame.quit()




def player_vs_ai( win ):
    print("Starting Player vs AI mode")
    # Add player vs AI logic here

def ai_vs_ai( win ):
    print("Starting AI vs AI mode")
    # Add AI vs AI logic here