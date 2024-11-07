import pygame
import random

# Screen
BLOCK_SIZE = 20
WIDTH, HEIGHT = BLOCK_SIZE * 30, BLOCK_SIZE * 20

# Colors
WHITE = ( 255, 255, 255 )
GRAY = ( 100, 100, 100 )
BLACK = ( 0, 0, 0 )
RED = ( 255, 0, 0 )
GREEN = ( 0, 255, 0 )
BLUE = ( 0, 0, 255 )

def generate_food( snake ):
    # Generate food at random locations
    while True:
        x = random.randint( 0, ( WIDTH - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE
        y = random.randint( 0, ( HEIGHT - BLOCK_SIZE ) // BLOCK_SIZE ) * BLOCK_SIZE
        if ( x, y ) not in snake:
            return ( x, y )
        
def draw_objects( snake, food, win ):
    for segment in snake:
        pygame.draw.rect( win, GREEN, ( *segment, BLOCK_SIZE, BLOCK_SIZE ) )    # Draw snake pieces/segments

    pygame.draw.rect( win, RED, ( *food, BLOCK_SIZE, BLOCK_SIZE ) ) # Draw foods
    pygame.display.update() # Refresh screen

# Background grid
def draw_grid( win ):
    grid_color = ( GRAY )
    for x in range( 0, WIDTH, BLOCK_SIZE ):
        pygame.draw.line( win, grid_color, ( x, 0 ), ( x, HEIGHT ) )    # Vertical lines
    for y in range( 0, HEIGHT, BLOCK_SIZE ):
        pygame.draw.line( win, grid_color, ( 0, y ), ( WIDTH, y ) )     # Horizontal lines

pygame.font.init()
font = pygame.font.Font( None, 30 )
def display_score( win, score ):
    score_text = font.render( f"Score: {score}", True, WHITE )
    win.blit( score_text, ( 10, 10 ) )
