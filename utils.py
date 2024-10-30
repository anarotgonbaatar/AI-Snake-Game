import pygame
import random

# Screen
WIDTH, HEIGHT = 900, 600
BLOCK_SIZE = 20

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
    win.fill( BLACK )

    for segment in snake:
        pygame.draw.rect( win, GREEN, ( *segment, BLOCK_SIZE, BLOCK_SIZE ) )    # Draw snake pieces/segments

    pygame.draw.rect( win, RED, ( *food, BLOCK_SIZE, BLOCK_SIZE ) ) # Draw foods
    pygame.display.update() # Refresh screen