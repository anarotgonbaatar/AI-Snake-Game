import pygame
import sys
from snake_game import SnakeGame
from ai_logic import SnakeAI
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK, RED, WHITE, generate_food, draw_objects, draw_grid

class PlayerVsAIMode(SnakeGame):
    def __init__(self, win):
        super().__init__(win)
        # Initialize AI snake
        self.ai_snake = self.snake  # Use the existing snake for AI
        self.ai_direction = self.direction
        self.ai = SnakeAI(self)


        # Initialize player snake
        self.player_snake = [(WIDTH // 4, HEIGHT // 4)]  # Initial position of player snake
        self.player_direction = (BLOCK_SIZE, 0)  # player direction


        # Food for both snakes
        self.player_food = self.food
        self.ai_food = generate_food(self.player_snake + self.ai_snake)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.event.pump()
            self.handle_player_input()  # Handle player input
            # Update player snake position
            self.update_snake_position_1(self.player_snake, self.player_direction)

            # Update AI snake position
            #////////////////////////////////////////////////////////////////////////////////////////
                                            #need to debunk this section

            next_move = self.ai.get_next_move(self.food)  # Get AI’s next move
            self.direction = (next_move[0] - self.snake[0][0], next_move[1] - self.snake[0][1])
            self.update_snake_position()
            #//////////////////////////////////////////////////////////////////////////////////////////


            # Check for wall collisions
            if self.check_collisions_1(self.player_snake) or self.check_collisions_1(self.ai_snake) :
                print("Game Over: collision with wall")
                running = False


            # Draw everything
            self.win.fill(BLACK)
            draw_grid(self.win)
            draw_objects(self.player_snake, self.player_food, self.win)  # Draw player snake and food
            draw_objects(self.ai_snake, self.ai_food, self.win)  # Draw AI snake and food
            pygame.display.update()
            clock.tick(8)  # Control game speed

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.player_direction != (0, BLOCK_SIZE):
            self.player_direction = (0, -BLOCK_SIZE)
        elif keys[pygame.K_DOWN] and self.player_direction != (0, -BLOCK_SIZE):
            self.player_direction = (0, BLOCK_SIZE)
        elif keys[pygame.K_LEFT] and self.player_direction != (BLOCK_SIZE, 0):
            self.player_direction = (-BLOCK_SIZE, 0)
        elif keys[pygame.K_RIGHT] and self.player_direction != (-BLOCK_SIZE, 0):
            self.player_direction = (BLOCK_SIZE, 0)






