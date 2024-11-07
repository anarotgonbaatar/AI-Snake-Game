import heapq
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK, RED, WHITE, BLUE
from utils import generate_food, draw_grid, draw_objects, display_score
from buttons import Button
import sys
import pygame

class SnakeAI:
    def __init__(self, game_instance):
        self.game = game_instance
        self.current_direction = ( BLOCK_SIZE, 0 )

    def aStar_search(self, start, goal):
        # print(f"Starting A* from {start} to {goal}")
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
                # print(f"Path found: {path}")
                return path

            neighbors = self.get_neighbors(current)
            # print(f"Current position: {current}, Neighbors: {neighbors}")
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # print("No path found")
        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position):
        directions = [(0, -BLOCK_SIZE), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0), (BLOCK_SIZE, 0)]
        neighbors = []
        for direction in directions:
            neighbor = (position[0] + direction[0], position[1] + direction[1])
            if self.valid_position(neighbor):
                neighbors.append(neighbor)
        # print(f"Position: {position}, Valid neighbors: {neighbors}")
        return neighbors

    def valid_position(self, position):
        within_boundaries = 0 <= position[0] < WIDTH and 0 <= position[1] < HEIGHT
        not_colliding = position not in self.game.snake
        is_valid = within_boundaries and not_colliding
        # print( f"Checking position: {position}, Within boundaries: {within_boundaries}, Not colliding: {not_colliding}, Valid: {is_valid}")
        return is_valid

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.insert(0, current)
            current = came_from[current]
        return path



    def get_next_move(self, food_position):
        head = self.game.snake[0]
        # Calculate the difference in x and y coordinates
        dx = food_position[0] - head[0]
        dy = food_position[1] - head[1]

        possible_moves = [
            ( head[0] + BLOCK_SIZE, head[1] ),  # right
            ( head[0] - BLOCK_SIZE, head[1] ),  # left
            ( head[0], head[1] + BLOCK_SIZE ),  # down
            ( head[0], head[1] - BLOCK_SIZE )  # up
        ]

        directions = [
            ( BLOCK_SIZE, 0 ),   # right
            ( -BLOCK_SIZE, 0 ),   # left
            ( 0, BLOCK_SIZE ),   # down
            ( 0, -BLOCK_SIZE )   # up
        ]

        # Step 1: Filter out reverse direction; don't want the AI snake running into itself or move wrongly
        valid_moves = [
            move for move, direction in zip( possible_moves, directions )
            if direction != ( -self.current_direction[0], -self.current_direction[1] ) and self.valid_position( move )
        ]
        
        # Step 2: Choose the move towards food
        next_move = min( valid_moves, key=lambda move: abs( food_position[0] - move[0]) + abs( food_position[1] - move[1] ) )

        # Step 3: Update current direction
        self.current_direction = ( next_move[0] - head[0], next_move[1] - head[1] )

        # print(f"Move decision: Head={head}, Food={food_position}, Next Move={next_move}")
        return next_move

# AI Only Gamemode
def ai_only(win):
    print("Starting AI-only mode")

    # Set up initial snake position and food
    snake = [ ( WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 2 // BLOCK_SIZE * BLOCK_SIZE ) ]
    food = generate_food(snake)
    ai = SnakeAI(game_instance=type('', (object,), {"snake": snake})())
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.event.pump()  # Keep the game responsive

        # AI decides the next move
        path = ai.aStar_search( snake[0], food )
        if path: next_move = path[0]
        else: next_move = ai.get_next_move( food )

        # Check if the snake reaches the food
        if next_move == food:
            score += 1
            snake.insert(0, food)  # Grow the snake by adding the food position to the head
            food = generate_food(snake)  # Generate new food
        else:
            # Move the snake to the next position
            snake.insert(0, next_move)  # Move the head
            snake.pop()  # Remove the tail segment unless food was eaten

        # Check for collisions with walls or itself
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT or
            snake[0] in snake[1:]):
                ai_game_over(win, score)
                running = False

        # Drawing
        win.fill(BLACK)  # Clear the screen
        draw_grid(win)  # Draw the grid background
        draw_objects(snake, food, win)  # Draw snake and food
        display_score(win, score)  # Display the score

        # Draw the A* path
        if path:
            for i in range( len( path ) - 1 ):
                start = path[i]
                end = path[ i + 1 ]
                pygame.draw.line( win, BLUE, ( start[0] + BLOCK_SIZE // 2, start[1] + BLOCK_SIZE // 2 ),
                                 ( end[0] + BLOCK_SIZE // 2, end[1] + BLOCK_SIZE // 2), 2 )

        pygame.display.update()  # Update the display
        pygame.time.delay(25)  # More = Slow, Less = Fast

    pygame.quit()

# AI Game Over screen
def ai_game_over( win, score ):
    font = pygame.font.Font( None, 40 )

    # Game Over text
    game_over_text = font.render( "Game Over", True, RED )
    score_text = font.render( f"Your Score: {score}", True, WHITE )
    buttons = [
        Button( "Restart", ( WIDTH / 2 - 100, 150 )),
        Button( "Return to Menu", ( WIDTH / 2 - 100, 210 )),
        Button( "QUIT", ( WIDTH / 2 - 100, 390 ))
    ]

    # Draw them
    # Black background
    win.fill( BLACK )

    # Draw buttons
    for button in buttons:
        button.draw( win )

    win.blit( game_over_text, ( WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 200 ) )
    win.blit( score_text, ( WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 0 ) )
    
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked( event.pos ):
                        if button.text == "Restart":
                            ai_only( win )
                        elif button.text == "Return to Menu":
                            return
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()


def player_vs_ai( win ):
    print("Starting Player vs AI mode")
    # Add player vs AI logic here

def ai_vs_ai( win ):
    print("Starting AI vs AI mode")
    # Add AI vs AI logic here