# AI Logic
import heapq
from .utils import WIDTH, HEIGHT, BLOCK_SIZE, WHITE, generate_food, game_over
import pygame

# AI Logic for controlling the AI snakes in game.
# Uses A* for pathfinding and movement.
class SnakeAI:
    # Initialize the AI instance
    def __init__(self, game_instance, snake):
        self.game = game_instance
        self.snake = snake
        self.current_direction = ( BLOCK_SIZE, 0 )
        self.path = []
        self.recalculate_path = True

    # A* search to find the shortest path to the food
    # Returns a list of positions from snake/start to food/goal
    def aStar_search(self, start, goal, other_snake=None ):
        self.path = []
        open_set = []   # Priority queue for A*
        heapq.heappush(open_set, (0, start))
        came_from = {}  # Map to reconstruct the path
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal, 'manhattan' )}
        max_iterations = 500
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1
            _, current = heapq.heappop(open_set)    # Get position with lowest cost

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path

            # Check neighbors and calculate their costs
            neighbors = self.get_neighbors( current, other_snake )

            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1

                # If neighbor is cheaper or unvisited
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def heuristic( self, a, b, type='manhattan' ):
        # Manhattan measures the distance between two points for vertical and horizontal movements
        if type == 'manhattan':
            return abs( a[0] - b[0] ) + abs( a[1] - b[1] )
        # Euclidian measures diagonal distance between two points
        if type == 'euclidian':
            return ( ( a[0] - b[0] ) ** 2 + ( a[1] - b[1] ) ** 2 ) ** 0.5
        if type == 'chebyshev':
            return max( abs( a[0] - b[0] ), abs( a[1] - b[1] ) )

    # Gets and returns a list of valid neighboring positions
    def get_neighbors( self, position, other_snake=None ):
        directions = [(0, -BLOCK_SIZE), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0), (BLOCK_SIZE, 0)]
        neighbors = []
        
        for direction in directions:
            neighbor = (position[0] + direction[0], position[1] + direction[1])
            if self.valid_position( neighbor, other_snake ):
                neighbors.append(neighbor)

        return neighbors

    # Returns boolean if a position is valid (within walls/boundaries and not colliding with anything)
    def valid_position( self, position, other_snake=None ):
        within_boundaries = 0 <= position[0] < WIDTH and 0 <= position[1] < HEIGHT
        not_colliding = position not in self.snake

        if other_snake:
            not_colliding = not_colliding and position not in other_snake
        
        is_valid = within_boundaries and not_colliding

        return is_valid

    # Returns a list of positions representing the path
    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.insert(0, current)
            current = came_from[current]
        return path

    # Returns the next position for the AI snake to move to
    def get_next_move( self, food_position, other_snake=None ):
        head = self.snake[0]  # Current head position of the AI snake

        self.path = self.aStar_search( head, food_position, other_snake )

        if self.path:
            # Simulate eating food and escape paths
            test_snake = [ food_position ] + self.snake[:-1]    # Sim new snake body
            
            if not self.escape_possible( test_snake ):
                # print("Path leads to entrapment. Path recalculating.")
                self.path = []    # Force recalculation

        if self.path:   # If path still valid, next step
            next_step = self.path[0]
            return next_step
            
        return None
    
    # Returns boolean if escape is possible
    def escape_possible( self, snake ):
        visited = set()
        queue = [ snake[0] ]

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add( current )

            for neighbor in self.get_neighbors( current ):
                if neighbor not in snake:
                    queue.append( neighbor )

        # Escape is possible if visited area is larger than snake
        return len( visited ) >= len( snake )
    
    # Returns updated snake movement, food collection, score, and running state
    def update_ai_movement( self, ai_snake, next_move, food, score, running, win, sys, gamemode ):
        if next_move:
            # Move the snake to the next position
            ai_snake.insert( 0, next_move )

            # Check for food
            if next_move == food:
                score += 1
                food = generate_food( ai_snake )
            else:
                ai_snake.pop()  # Remove the tail to maintain the length

        else:
            # When AI can't calculate a valid path to food
            fallback_move = self.get_fallback_move( ai_snake )
            
            if fallback_move:
                # Move snake to fallback move
                ai_snake.insert( 0, fallback_move )
                ai_snake.pop()
            else:
                running = False
                # game_over( win, None, score, gamemode, sys )

        return food, score, running     # Return updated vars

    # Returns a valid position to move to if there is no valid path
    def get_fallback_move( self, ai_snake ):
        head = ai_snake[0]
        
        # All possible moves around AI snake's head
        possible_moves = [
            ( head[0] + BLOCK_SIZE, head[1] ),
            ( head[0] - BLOCK_SIZE, head[1] ),
            ( head[0], head[1] + BLOCK_SIZE ),
            ( head[0], head[1] - BLOCK_SIZE ),
        ]

        # Filter out possible moves for valid moves
        valid_moves = [ move for move in possible_moves if self.valid_position( move ) ]
        
        if valid_moves:
            return valid_moves[0]
        else:
            return None
    
    # Displays the caluclated AI path on game
    def draw_path( self, win ):
        if not self.path: return
        
        for start, end in zip( self.path, self.path[1:] ):
            start_center = ( start[0] + BLOCK_SIZE // 2, start[1] + BLOCK_SIZE // 2 )
            end_center = ( end[0] + BLOCK_SIZE // 2, end[1] + BLOCK_SIZE // 2 )
            pygame.draw.line( win, WHITE, start_center, end_center, 2 )  # white path line