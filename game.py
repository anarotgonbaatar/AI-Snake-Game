import pygame
import random
import sys
from buttons import Button
from utils import generate_food, draw_objects, draw_grid, display_score
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLACK, RED, WHITE

clock = pygame.time.Clock()

def play_game( win ):
    print( "Starting player only mode" )

    # Snake initial location and rotation
    snake = [ ( WIDTH // 2 // BLOCK_SIZE * BLOCK_SIZE, HEIGHT // 2 // BLOCK_SIZE * BLOCK_SIZE ) ]
    direction = ( BLOCK_SIZE, 0 )

    # Generate the first food
    food = generate_food( snake )
    score = 0

    # Main Game
    running = True
    while running:
        fps = 8    # Game runs frames per second
        clock.tick( fps )

        # Handle key events
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Move Up
                if event.key == pygame.K_UP and direction != ( 0, BLOCK_SIZE ):
                    direction = ( 0, -BLOCK_SIZE )
                # Move Down
                if event.key == pygame.K_DOWN and direction != ( 0, -BLOCK_SIZE ):
                    direction = ( 0, BLOCK_SIZE )
                # Move Left
                if event.key == pygame.K_LEFT and direction != ( BLOCK_SIZE, 0 ):
                    direction = ( -BLOCK_SIZE, 0 )
                # Move Right
                if event.key == pygame.K_RIGHT and direction != ( -BLOCK_SIZE, 0 ):
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
            game_over( win, score )
            running = False

        # Draw everything
        win.fill( BLACK )
        draw_grid( win )
        draw_objects( snake, food, win )
        display_score( win, score )

        pygame.display.update()

    pygame.quit()

def game_over( win, score ):
    font = pygame.font.Font( None, 40 )

    # Game Over text
    game_over_text = font.render( "Game Over", True, RED )
    score_text = font.render( f"Your Score: {score}", True, WHITE )
    buttons = [
        Button( "Restart", ( WIDTH / 2 - 100, 150 )),
        Button( "Return to Menu", ( WIDTH / 2 - 100, 210 )),
        Button( "QUIT", ( WIDTH / 2 - 100, 390 ))
    ]

    # Draw them
    # Black background
    win.fill( BLACK )

    # Draw buttons
    for button in buttons:
        button.draw( win )

    win.blit( game_over_text, ( WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 200 ) )
    win.blit( score_text, ( WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 0 ) )
    
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
                            play_game( win )
                        elif button.text == "Return to Menu":
                            return
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()