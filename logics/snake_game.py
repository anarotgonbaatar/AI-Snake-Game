# Separate snake game class for modularity
import pygame
import sys
from .utils import generate_food, draw_grid, display_score, draw_snake_and_food
from .utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK
from .utils import GREEN, DARK_GREEN, BLUE, DARK_BLUE, RED, YELLOW

class SnakeGame:
    def __init__( self, win ) -> None:
        self.win = win
        self.snake = [( WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 2 // BLOCK_SIZE * BLOCK_SIZE )]
        self.food = generate_food( self.snake )
        self.score = 0
        self.player_direction = ( BLOCK_SIZE, 0 )
        self.running = True

    def handle_input( self ):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.update_direction( event.key )

    def update_direction( self, key ):
        if key == pygame.K_UP and self.player_direction != ( 0, BLOCK_SIZE ):
            self.player_direction = ( 0, -BLOCK_SIZE )
        # Move Down
        if key == pygame.K_DOWN and self.player_direction != ( 0, -BLOCK_SIZE ):
            self.player_direction = ( 0, BLOCK_SIZE )
        # Move Left
        if key == pygame.K_LEFT and self.player_direction != ( BLOCK_SIZE, 0 ):
            self.player_direction = ( -BLOCK_SIZE, 0 )
        # Move Right
        if key == pygame.K_RIGHT and self.player_direction != ( -BLOCK_SIZE, 0 ):
            self.player_direction = ( BLOCK_SIZE, 0 )

    def update_player_snake_location( self, player_snake, food, score ):
        new_head = (
            player_snake[0][0] + self.player_direction[0], player_snake[0][1] + self.player_direction[1]
        )

        player_snake.insert( 0, new_head )

        if new_head == food:
            score += 1
            food = generate_food( player_snake )
        else:
            player_snake.pop()

        return food, score

    def check_collisions( self, snake1, snake2=None ):
        # Collision for snake 1
        if snake1 and self.check_collision( snake1, snake2 ): return True
        # Collision for snake 2 if valid
        if snake2 and self.check_collision( snake2, snake1 ): return True
        
        return False

    def check_collision( self, snake1, snake2=None ):
        head = snake1[0]
        # Collision with walls
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT: return True
        # Collision with itself
        if head in snake1[1:]: return True
        # Collision with other snake if snake 2 is valid
        if snake2 and head in snake2: return True
        
        return False

    def draw_all( self, snake1, snake2, food1, food2, player_score, ai_score, win ):
        self.win.fill( BLACK )
        draw_grid( self.win )
        
        if snake1: draw_snake_and_food( snake1, GREEN, DARK_GREEN, food1, RED, win )
        if snake2: draw_snake_and_food( snake2, BLUE, DARK_BLUE, food2, YELLOW, win )
        
        display_score( self.win, player_score, ai_score )
        pygame.display.update()