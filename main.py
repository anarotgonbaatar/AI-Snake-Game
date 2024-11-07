import pygame
import sys
from utils import BLACK, WIDTH, HEIGHT
from buttons import Button
from player_mode import PlayerMode
from ai_mode import AI_Mode

pygame.init()
pygame.font.init()

# Screen settings
win = pygame.display.set_mode(( WIDTH, HEIGHT ))
pygame.display.set_caption( "AI Snake Game" )
font = pygame.font.Font( None, 40 )

buttons = [
    Button( "Player Only", ( WIDTH / 2 - 100, 150 )),
    Button( "AI Only", ( WIDTH / 2 - 100, 210 )),
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
                        if button.text == "Player Only":
                            game = PlayerMode( win )
                            game.run()
                        elif button.text == "AI Only":
                            game = AI_Mode( win )
                            game.run()
                        elif button.text == "You vs AI":
                            game = AI_Mode( win )
                            game.run()
                        elif button.text == "AI vs AI":
                            game = AI_Mode( win )
                            game.run()
                        elif button.text == "QUIT":
                            pygame.quit()
                            sys.exit()

if __name__ == "__main__":
    menu()