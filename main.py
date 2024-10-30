import pygame
import sys
from utils import BLACK, WIDTH, HEIGHT
from buttons import Button
from game import play_game
from ai import ai_only, player_vs_ai, ai_vs_ai

pygame.init()

# Screen settings
win = pygame.display.set_mode(( WIDTH, HEIGHT ))
pygame.display.set_caption( "AI Snake Game" )
font = pygame.font.Font( None, 40 )

buttons = [
    Button( "Play Game", ( WIDTH / 2 - 100, 150 )),
    Button( "Play AI", ( WIDTH / 2 - 100, 210 )),
    Button( "You vs AI", ( WIDTH / 2 - 100, 270 )),
    Button( "AI vs AI", ( WIDTH / 2 - 100, 330 )),
    Button( "QUIT", ( WIDTH / 2 - 100, 390 ))
]

def menu():
    while True:
        # Black background
        win.fill( BLACK )

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
                        if button.text == "Play Game":
                            play_game( win )
                        elif button.text == "Play AI":
                            ai_only( win )
                        elif button.text == "You vs AI":
                            player_vs_ai( win )
                        elif button.text == "AI vs AI":
                            ai_vs_ai( win )
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    menu()