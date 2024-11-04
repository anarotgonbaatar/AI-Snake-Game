import heapq
import game
import utils

class SnakeAI:
    def __init__( self, game_instance ) -> None:
        self.game = game_instance

    # A* search algorithm to get the shortast path to food
    def aStar_search( self, start, goal ):
        # A* Logic

        return []
    
    def heuristic( self, a, b ):
        return
    
    # Get valid neighboring positions for snake to move to
    def get_neighbors( self, position ):
        return

    # Check if position is within the screen and not colliding with snake
    def valid_position( self, position ):
        return

    # Reconstruct path from start to goal
    def reconstruct_path( self, came_from, current ):
        return

    # Get next move for snake using A*
    def get_next_move( self ):
        return
    

def ai_only( win ):
    print("Starting AI-only mode")
    # Add AI-only gameplay logic here

def player_vs_ai( win ):
    print("Starting Player vs AI mode")
    # Add player vs AI logic here

def ai_vs_ai( win ):
    print("Starting AI vs AI mode")
    # Add AI vs AI logic here