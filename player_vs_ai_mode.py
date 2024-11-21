import pygame
import sys
from snake_game import SnakeGame
from ai_logic import SnakeAI
from utils import WIDTH, HEIGHT, BLOCK_SIZE
from utils import generate_food, snake_position, game_over

class PlayerVsAIMode( SnakeGame ):
    def __init__(self, win):
        super().__init__(win)
        self.win = win
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 8

        # Initialize player snake
        self.player_snake = snake_position( 2, 2 )
        self.player_direction = ( BLOCK_SIZE, 0 )  # player direction
        self.player_score = 0

        # Initialize AI snake
        self.ai_snake = snake_position( 4, 4 )
        self.ai_direction = ( BLOCK_SIZE, 0 )
        self.ai = SnakeAI( self, self.ai_snake )
        self.ai_score = 0

        # Food for both snakes
        self.player_food = generate_food( self.player_snake + self.ai_snake )
        self.ai_food = generate_food(self.player_snake + self.ai_snake)

    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.clock.tick( self.fps )

            # AI snake movement logic
            next_move = self.ai.get_next_move( self.ai_food, self.player_snake )
            self.ai_food, self.ai_score, self.running = self.ai.update_ai_movement(
                self.ai_snake, next_move, self.ai_food, self.ai_score, self.running, self.win, sys, PlayerVsAIMode
            )

            # Player movement logic
            self.handle_input()
            self.player_food, self.player_score = self.update_player_snake_location(
                self.player_snake, self.player_food, self.player_score
            )

            # Check collisions for both snakes
            if self.check_collisions( self.player_snake, self.ai_snake ):
                self.running = False
                game_over( self.win, self.player_score, self.ai_score, PlayerVsAIMode, sys )

            self.draw_all( self.player_snake, self.ai_snake, self.player_food, self.ai_food, self.player_score, self.ai_score, self.win )
            self.ai.draw_path( self.win )
            
            pygame.event.pump()
            pygame.display.update()