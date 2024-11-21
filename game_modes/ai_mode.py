import sys
import pygame
from logics.utils import game_over
from logics.ai_logic import SnakeAI
from logics.snake_game import SnakeGame

# AI Only Gamemode
class AI_Mode( SnakeGame ):
    def __init__( self, win ) -> None:
        super().__init__( win )
        self.ai = SnakeAI( self, self.snake )
        self.fps = 60

    def run( self ):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            next_move = self.ai.get_next_move( self.food )
            
            # AI snake movement logic
            self.food, self.score, self.running = self.ai.update_ai_movement(
                self.snake, next_move, self.food, self.score, self.running, self.win, sys, AI_Mode
            )

            if self.check_collisions( self.snake ):
                self.running = False
                game_over( self.win, None, self.score, AI_Mode, sys )

            self.draw_all( None, self.snake, None, self.food, None, self.score, self.win )
            self.ai.draw_path( self.win )

            clock.tick( self.fps )
            pygame.event.pump()
            pygame.display.update()