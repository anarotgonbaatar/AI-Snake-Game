from utils import WIDTH, HEIGHT, BLACK, RED, WHITE, generate_food, BLOCK_SIZE
from buttons import Button
import sys
import pygame
from ai_logic import SnakeAI
from snake_game import SnakeGame

# AI Only Gamemode
class AI_Mode( SnakeGame ):
    def __init__( self, win ) -> None:
        super().__init__( win )
        self.ai = SnakeAI( self, self.snake )

    def run( self ):
        clock = pygame.time.Clock()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # Properly exit the program

            clock.tick( 30 )
            pygame.event.pump()  # So it doesn't crash when I move the window

            next_move = self.ai.get_next_move(self.food)
            if next_move:
                # Move the snake directly to the next position
                self.snake.insert(0, next_move)

                # Check if the food is eaten
                if next_move == self.food:
                    self.food = generate_food(self.snake)
                    self.score += 1
                else:
                    self.snake.pop()  # Remove the tail to maintain the length

            else:
                print("AI couldn't find a valid path.")
                fallback_move = self.get_fallback_move()
                if fallback_move:
                    self.snake.insert( 0, fallback_move )
                    self.snake.pop()
                else:
                    print( "AI snake is completely stuck" )
                    self.running = False

            if self.check_collisions():
                self.running = False
                ai_game_over( self.win, self.score )

            self.draw()
            self.ai.draw_path( self.win )
            pygame.display.update()

    def get_fallback_move( self ):
        head = self.snake[0]
        valid_moves = [
            ( head[0] + BLOCK_SIZE, head[1] ),
            ( head[0] - BLOCK_SIZE, head[1] ),
            ( head[0], head[1] + BLOCK_SIZE ),
            ( head[0], head[1] - BLOCK_SIZE ),
        ]

        valid_moves = [ move for move in valid_moves if self.ai.valid_position( move ) ]
        return valid_moves[0] if valid_moves else None

# AI Game Over screen
def ai_game_over( win, score ):
    font = pygame.font.Font( None, 40 )

    # Game Over text
    game_over_text = font.render( "Game Over", True, RED )
    score_text = font.render( f"Your Score: {score}", True, WHITE )
    buttons = [
        Button( "Restart", ( WIDTH / 2 - 100, 150 ) ),
        Button( "Return to Menu", ( WIDTH / 2 - 100, 210 ) ),
        Button( "QUIT", ( WIDTH / 2 - 100, 390 ) )
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
                            game = AI_Mode( win )
                            game.run()
                        elif button.text == "Return to Menu":
                            return
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()