import pygame
import sys
from snake_game import SnakeGame
from ai_logic import SnakeAI
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK
from utils import RED, YELLOW, GREEN, DARK_GREEN, BLUE, DARK_BLUE
from utils import generate_food, draw_grid

class PlayerVsAIMode(SnakeGame):
    def __init__(self, win):
        super().__init__(win)
        self.win = win
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize AI snake
        self.ai_snake = [( WIDTH // 4 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 4 // BLOCK_SIZE * BLOCK_SIZE )]
        self.ai_direction = ( BLOCK_SIZE, 0 )
        self.ai = SnakeAI( self, self.ai_snake )

        # Initialize player snake
        self.player_snake = [( WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 2 // BLOCK_SIZE * BLOCK_SIZE )]  # Initial position of player snake
        self.player_direction = (BLOCK_SIZE, 0)  # player direction

        # Food for both snakes
        self.player_food = generate_food( self.player_snake + self.ai_snake )
        self.ai_food = generate_food(self.player_snake + self.ai_snake)

    def run(self):

        while self.running:
            self.clock.tick(6)
            self.handle_player_input()
            self.update_ai()
            self.update_positions()
            self.check_collisions()
            self.draw()

            pygame.event.pump()

    def handle_player_input(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.player_direction != (0, BLOCK_SIZE):
                    self.player_direction = (0, -BLOCK_SIZE)
                elif event.key == pygame.K_DOWN and self.player_direction != (0, -BLOCK_SIZE):
                    self.player_direction = (0, BLOCK_SIZE)
                elif event.key == pygame.K_LEFT and self.player_direction != (BLOCK_SIZE, 0):
                    self.player_direction = (-BLOCK_SIZE, 0)
                elif event.key == pygame.K_RIGHT and self.player_direction != (-BLOCK_SIZE, 0):
                    self.player_direction = (BLOCK_SIZE, 0)

    def update_ai( self ):
        next_move = self.ai.get_next_move( self.ai_food )
        if next_move:
            self.ai_direction = ( next_move[0] - self.ai_snake[0][0], next_move[1] - self.ai_snake[0][1] )
        else:
            print( "AI couldn't find a valid path" )
            self.running = False

    def update_positions( self ):
        # Update player snake
        new_player_head = ( self.player_snake[0][0] + self.player_direction[0],
                           self.player_snake[0][1] + self.player_direction[1] )
        self.player_snake.insert( 0, new_player_head )
        if new_player_head == self.player_food:
            self.player_food = generate_food( self.player_snake + self.ai_snake )
        else:
            self.player_snake.pop()

        # Update AI snake
        new_ai_head = ( self.ai_snake[0][0] + self.ai_direction[0],
                       self.ai_snake[0][1] + self.ai_direction[1] )
        self.ai_snake.insert( 0, new_ai_head )
        if new_ai_head == self.ai_food:
            self.ai_food = generate_food( self.player_snake + self.ai_snake )
        else:
            self.ai_snake.pop()

    def check_collisions( self ):
        # Wall and self collision for player
        player_head = self.player_snake[0]
        if ( player_head[0] < 0 or player_head[0] >= WIDTH or
            player_head[1] < 0 or player_head[1] >= HEIGHT or
            player_head in self.player_snake[1:] or player_head in self.ai_snake ):
            print( "Game Over: Player Snake Collision" )
            self.running = False

        # Wall and self collision for AI
        ai_head = self.ai_snake[0]
        if ( ai_head[0] < 0 or ai_head[0] >= WIDTH or
            ai_head[1] < 0 or ai_head[1] >= HEIGHT or
            ai_head in self.ai_snake[1:] or ai_head in self.player_snake ):
            print( "Game Over: AI Snake Collided" )
            self.running = False

    # Draw everything
    def draw( self ):
        self.win.fill(BLACK)
        draw_grid(self.win)

        # Draw player snake
        for i, segment in enumerate( self.player_snake ):
            color = GREEN if i % 2 == 0 else DARK_GREEN
            pygame.draw.rect( self.win, color, ( *segment, BLOCK_SIZE, BLOCK_SIZE ) )
        # Draw player food in red
        pygame.draw.rect( self.win, RED, ( *self.player_food, BLOCK_SIZE, BLOCK_SIZE ) )
        # Draw AI snake
        for i, segment in enumerate( self.ai_snake ):
            color = BLUE if i % 2 == 0 else DARK_BLUE
            pygame.draw.rect( self.win, color, ( *segment, BLOCK_SIZE, BLOCK_SIZE ) )
        # Draw AI food in yellow
        pygame.draw.rect( self.win, YELLOW, ( *self.ai_food, BLOCK_SIZE, BLOCK_SIZE ) )

        self.ai.draw_path( self.win )
        pygame.display.update()