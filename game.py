import pygame
import random
import sys
from utils import generate_food, draw_objects, WIDTH, HEIGHT, BLOCK_SIZE

clock = pygame.time.Clock()

def play_game( win ):
    print( "Starting player only mode" )

    # Snake initial location and rotation
    snake = [ ( WIDTH / 2, HEIGHT / 2 ) ]
    direction = ( BLOCK_SIZE, 0 )

    # Generate the first food
    food = generate_food( snake )
    score = 0

    # Game
    running = True
    while running:
        fps = 5    # Game runs frames per second
        clock.tick( fps )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Move Up
                if event.key == pygame.K_UP and direction != ( 0, BLOCK_SIZE ):
                    direction = ( 0, -BLOCK_SIZE )
                # Move Down
                elif event.key == pygame.K_DOWN and direction != ( 0, BLOCK_SIZE ):
                    direction = ( 0, BLOCK_SIZE )
                # Move Left
                elif event.key == pygame.K_LEFT and direction != ( 0, BLOCK_SIZE ):
                    direction = ( -BLOCK_SIZE, 0 )
                # Move Right
                elif event.key == pygame.K_RIGHT and direction != ( 0, BLOCK_SIZE ):
                    direction = ( BLOCK_SIZE, 0 )

        # Move snake
        new_head = ( snake[0][0] + direction[0], snake[0][1] + direction[1] )
        snake.insert( 0, new_head )

        # Check for food
        if new_head == food:
            score += 1
            food = generate_food( snake )   # Make new food
        else:
            snake.pop() # Pop last segment to keep the same length
        
        # Check for wall or self
        if ( new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT or new_head in snake[1:] ):
            print( "Game Over." )
            running = False

        # Draw everything
        draw_objects( snake, food, win )

    pygame.quit()