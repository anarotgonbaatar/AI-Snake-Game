import pygame
import random

# Screen variables
BLOCK_SIZE = 20
GRID_WIDTH = 40
GRID_HEIGHT = 40
WIDTH, HEIGHT = BLOCK_SIZE * GRID_WIDTH, BLOCK_SIZE * GRID_HEIGHT

# Colors
WHITE = ( 255, 255, 255 )
GRAY = ( 100, 100, 100 )
DARK_GRAY = ( 25, 25, 25 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
DARK_GREEN = ( 0, 200, 0 )
BLUE = ( 0, 170, 255 )
DARK_BLUE = ( 0, 100, 200 )
YELLOW = ( 255, 255, 0 )

# Buttons class
class Button:
    def __init__( self, text, pos ):
        self.text = text
        self.pos = pos
        self.width = 250
        self.rect = pygame.Rect( pos[0], pos[1], self.width, 50 )
        self.color = GRAY

    def draw( self, screen ):
        pygame.draw.rect( screen, self.color, self.rect )
        font = pygame.font.Font( None, 40 )
        text_surf = font.render( self.text, True, WHITE )
        screen.blit( text_surf, ( self.rect.x + 20, self.rect.y + 10 ) )

    def is_clicked( self, mouse_pos ):
        return self.rect.collidepoint( mouse_pos )

# Returns a position for the snake that fits in the grid
def snake_position( width, height ):
    return [( WIDTH // width // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // height // BLOCK_SIZE * BLOCK_SIZE )]

# Returns a random position for the food that fits in the grid
def generate_food( snake ):
    while True:
        x = random.randint( 0, ( WIDTH - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE
        y = random.randint( 0, ( HEIGHT - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE
        
        if ( x, y ) not in snake:
            return ( x, y )

# Draw snakes and their foods
def draw_snake_and_food( snake, snake_color, snake_alt_color, food, food_color, win ):
    for i, segment in enumerate( snake ):
        color = snake_color if i % 2 == 0 else snake_alt_color                  # Alternate snake color
        pygame.draw.rect( win, color, ( *segment, BLOCK_SIZE, BLOCK_SIZE ) )    # Draw snake pieces/segments

    pygame.draw.rect( win, food_color, ( *food, BLOCK_SIZE, BLOCK_SIZE ) )      # Draw food

# Background grid
def draw_grid( win ):
    grid_color = ( DARK_GRAY )
    for x in range( 0, WIDTH, BLOCK_SIZE ):
        pygame.draw.line( win, grid_color, ( x, 0 ), ( x, HEIGHT ) )    # Vertical lines
    for y in range( 0, HEIGHT, BLOCK_SIZE ):
        pygame.draw.line( win, grid_color, ( 0, y ), ( WIDTH, y ) )     # Horizontal lines

# Display score for single player modes
def display_score( win, player_score, ai_score ):
    pygame.font.init()
    font = pygame.font.Font( None, 30 )
    
    if player_score:
        player_score_text = font.render( f"Player Score: { player_score }", True, GREEN )
        win.blit( player_score_text, ( 10, 10 ) )
    
    if ai_score:
        ai_score_text = font.render( f"AI Score: { ai_score }", True, BLUE )
        win.blit( ai_score_text, ( WIDTH - ai_score_text.get_width() - 10, 10 ) )

# Game over screen
def game_over( win, player_score, ai_score, gamemode, sys ):
    font = pygame.font.Font( None, 40 )

    # Game Over screen
    win.fill( BLACK )
    game_over_text = font.render( "Game Over", True, RED )
    if player_score: player_score_text = font.render( f"Player Score: { player_score }", True, GREEN )
    if ai_score: ai_score_text = font.render( f"AI Score: { ai_score }", True, BLUE )
    
    buttons = [
        Button( "Restart", ( WIDTH / 2 - 250 / 2, 150 ) ),
        Button( "Return to Menu", ( WIDTH / 2 - 250 / 2, 210 ) ),
        Button( "QUIT", ( WIDTH / 2 - 250 / 2, 390 ) )
    ]

    # Draw game over and scores
    win.blit( game_over_text, ( WIDTH / 2 - game_over_text.get_width() / 2, 75 ) )
    if player_score: win.blit( player_score_text, ( WIDTH / 2 - player_score_text.get_width() / 2, 240 + 130/3 ) )
    if ai_score: win.blit( ai_score_text, ( WIDTH / 2 - ai_score_text.get_width() / 2, 240 + 130/3*2 ) )

    # Draw buttons
    for button in buttons:
        button.draw( win )
    
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
                            game = gamemode( win )
                            game.run()
                        elif button.text == "Return to Menu":
                            running = False
                            return
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()