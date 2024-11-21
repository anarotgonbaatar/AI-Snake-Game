import pygame
from logics.snake_game import SnakeGame
from logics.utils import BLOCK_SIZE
from logics.utils import snake_position, game_over
import sys

class PlayerMode( SnakeGame ):
    def __init__( self, win ):
        super().__init__( win )
        self.snake = snake_position( 3, 3 )
        self.score = 0
        self.player_direction = ( BLOCK_SIZE, 0 )  # Right starting direction
        self.fps = 8
    
    def run( self ):
        pygame.init()

        clock = pygame.time.Clock()

        while self.running:
            
            self.handle_input()
            self.food, self.score = self.update_player_snake_location( self.snake, self.food, self.score )

            if self.check_collisions( self.snake, None ):
                self.running = False
                game_over( self.win, self.score, None, PlayerMode, sys )

            self.draw_all( self.snake, None, self.food, None, self.score, None, self.win )
            clock.tick( self.fps )  # Control game speed
            
            pygame.event.pump()  # pump processes internal events within the event queue, preventing the game from crashing