# Separate snake game class for modularity
import pygame
import sys
from utils import generate_food, draw_grid, draw_objects, display_score
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK

class SnakeGame:
    def __init__( self, win ) -> None:
        self.win = win
        self.snake = [( WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 2 // BLOCK_SIZE * BLOCK_SIZE )]
        self.food = generate_food( self.snake )
        self.score = 0
        self.direction = ( BLOCK_SIZE, 0 )
        self.running = True

    def handle_events( self ):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.update_direction(event.key)

    def update_direction( self, key ):
        if key == pygame.K_UP and self.direction != ( 0, BLOCK_SIZE ):
            self.direction = ( 0, -BLOCK_SIZE )
        # Move Down
        if key == pygame.K_DOWN and self.direction != ( 0, -BLOCK_SIZE ):
            self.direction = ( 0, BLOCK_SIZE )
        # Move Left
        if key == pygame.K_LEFT and self.direction != ( BLOCK_SIZE, 0 ):
            self.direction = ( -BLOCK_SIZE, 0 )
        # Move Right
        if key == pygame.K_RIGHT and self.direction != ( -BLOCK_SIZE, 0 ):
                self.direction = ( BLOCK_SIZE, 0 )

    def update_snake_position( self ):
        new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = generate_food(self.snake)
        else:
            self.snake.pop()

    def check_collisions( self ):
        # Wall and self-collision check
        head = self.snake[0]
        return ( head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in self.snake[1:] )

    def draw( self ):
        self.win.fill( BLACK )
        draw_grid( self.win )
        draw_objects( self.snake, self.food, self.win )
        display_score( self.win, self.score )
        pygame.display.update()