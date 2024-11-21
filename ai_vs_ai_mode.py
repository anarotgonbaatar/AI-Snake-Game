import pygame
import sys
from snake_game import SnakeGame
from ai_logic import SnakeAI
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK
from utils import RED, YELLOW, GREEN, DARK_GREEN, BLUE, DARK_BLUE
from utils import generate_food, draw_grid, snake_position, game_over

class AIvsAImode( SnakeGame ):
    def __init__( self, win ):
        super().__init__( win )
        self.win = win
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 24

        # Init AI 1
        self.snake1 = snake_position( 2, 2 )
        self.ai1_direction = ( BLOCK_SIZE, 0 )
        self.ai1 = SnakeAI( self, self.snake1 )
        self.score1 = 0

        # Init AI 2
        self.snake2 = snake_position( 4, 4 )
        self.ai2_direction = ( -BLOCK_SIZE, 0 )
        self.ai2 = SnakeAI( self, self.snake2 )
        self.score2 = 0

        # Food for both snakes
        self.food1 = generate_food( self.snake1 + self.snake2 )
        self.food2 = generate_food( self.snake1 + self.snake2 )

    def run( self ):

        while self.running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.clock.tick( self.fps )

            # AI 1 movement logic
            snake1_next_move = self.ai1.get_next_move( self.food1, self.snake2 )
            self.food1, self.score1, self.running = self.ai1.update_ai_movement(
                self.snake1, snake1_next_move, self.food1, self.score1, self.running, self.win, sys, AIvsAImode
            )
            # AI 2 movement logic
            snake2_next_move = self.ai2.get_next_move( self.food2, self.snake1 )
            self.food2, self.score2, self.running = self.ai2.update_ai_movement(
                self.snake2, snake2_next_move, self.food2, self.score2, self.running, self.win, sys, AIvsAImode
            )

            # Check collisions for both snakes
            if self.check_collisions( self.snake1, self.snake2 ):
                self.running = False
                game_over( self.win, self.score1, self.score2, AIvsAImode, sys )

            # Draw both snakes and their paths
            self.draw_all( self.snake1, self.snake2, self.food1, self.food2, self.score1, self.score2, self.win )
            self.ai1.draw_path( self.win )
            self.ai2.draw_path( self.win )

            pygame.event.pump()
            pygame.display.update()