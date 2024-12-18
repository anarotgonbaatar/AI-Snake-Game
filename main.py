import pygame
import sys
from logics.utils import BLACK, WIDTH, HEIGHT, WHITE, Button
# Import game modes
from game_modes.player_mode import PlayerMode
from game_modes.ai_mode import AI_Mode
from game_modes.player_vs_ai_mode import PlayerVsAIMode
from game_modes.ai_vs_ai_mode import AIvsAImode
from game_modes.benchmark_mode import BenchmarkMode

pygame.init()
pygame.font.init()

# Screen settings
win = pygame.display.set_mode(( WIDTH, HEIGHT ))
pygame.display.set_caption( "AI Snake Game" )
font = pygame.font.Font( None, 40 )

buttons = [
    Button( "Player Only", ( WIDTH / 2 - 250 / 2, 150 )),
    Button( "AI Only", ( WIDTH / 2 - 250 / 2, 210 )),
    Button( "Player vs AI", ( WIDTH / 2 - 250 / 2, 270 )),
    Button( "AI vs AI", ( WIDTH / 2 - 250 / 2, 330 )),
    Button( "Benchmark", ( WIDTH / 2 - 250 / 2, 390 )),
    Button( "QUIT", ( WIDTH / 2 - 250 / 2, 450 )),
]

def menu():
    while True:
        # Black background
        win.fill( BLACK )

        # Draw title
        font = pygame.font.Font( None, 50 )
        title_text = font.render( "AI Snake Game", True, WHITE )   
        win.blit( title_text, ( WIDTH / 2 - title_text.get_width() / 2, 50 ) )

        # Draw buttons
        for button in buttons:
            button.draw( win )

        # Refresh screen
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.is_clicked( event.pos ):
                        if button.text == "Player Only":
                            game = PlayerMode( win )
                            game.run()
                        elif button.text == "AI Only":
                            game = AI_Mode( win )
                            game.run()
                        elif button.text == "Player vs AI":
                            game = PlayerVsAIMode( win )
                            game.run()
                        elif button.text == "AI vs AI":
                            game = AIvsAImode( win )
                            game.run()
                        elif button.text == "Benchmark":
                            game = BenchmarkMode( win )
                            game.benchmark()
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    menu()