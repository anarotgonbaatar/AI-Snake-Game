import pygame
from utils import WHITE, GRAY

class Button:
    def __init__( self, text, pos ):
        self.text = text
        self.pos = pos
        self.rect = pygame.Rect( pos[0], pos[1], 250, 50 )
        self.color = GRAY

    def draw( self, screen ):
        pygame.draw.rect( screen, self.color, self.rect )
        font = pygame.font.Font( None, 40 )
        text_surf = font.render( self.text, True, WHITE )
        screen.blit( text_surf, ( self.rect.x + 20, self.rect.y + 10 ) )

    def is_clicked( self, mouse_pos ):
        return self.rect.collidepoint( mouse_pos )