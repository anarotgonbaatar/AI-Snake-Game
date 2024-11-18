import pygame
import sys
from snake_game import SnakeGame
from ai_logic import SnakeAI
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK
from utils import RED, YELLOW, GREEN, DARK_GREEN, BLUE, DARK_BLUE
from utils import generate_food, draw_grid

class AIvsAImode( SnakeGame ):
    def __init__( self, win ):
        super().__init__( win )
        self.win = win
        self.clock = pygame.time.Clock()
        self.running = True

        # Init AI 1
        self.ai_snake_1 = [( WIDTH // 4 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 4 // BLOCK_SIZE * BLOCK_SIZE )]
        self.ai1_direction = ( BLOCK_SIZE, 0 )
        self.ai1 = SnakeAI( self, self.ai_snake_1 )

        # Init AI 2
        self.ai_snake_2 = [( WIDTH // 3 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 3 // BLOCK_SIZE * BLOCK_SIZE )]
        self.ai2_direction = ( -BLOCK_SIZE, 0 )
        self.ai2 = SnakeAI( self, self.ai_snake_2 )

        self.food = generate_food( self.ai_snake_1 + self.ai_snake_2 )

    def run( self ):
        while self.running:
            self.clock.tick( 20 )
            self.update_ai_snakes()
            self.update_positions()
            self.check_collisions()
            self.draw()
            pygame.event.pump()

    def update_ai_snakes( self ):

    
    def update_positions( self ):


    def check_collisions( self ):