# Just AI Logic
import heapq
from utils import WIDTH, HEIGHT, BLOCK_SIZE, WHITE
import pygame

class SnakeAI:
    def __init__(self, game_instance, snake):
        self.game = game_instance
        self.snake = snake
        self.current_direction = ( BLOCK_SIZE, 0 )
        self.path = []
        self.recalculate_path = True

    def aStar_search(self, start, goal):
        self.path = []
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        max_iterations = 500
        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path

            neighbors = self.get_neighbors(current)

            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def heuristic( self, a, b, type='manhattan'):
        if type == 'manhattan':
            return abs( a[0] - b[0] ) + abs( a[1] - b[1] )
        if type == 'euclidian':
            return ( ( a[0] - b[0] ) ** 2 + ( a[1] - b[1] ) ** 2 ) ** 0.5

    def get_neighbors(self, position):
        directions = [(0, -BLOCK_SIZE), (0, BLOCK_SIZE), (-BLOCK_SIZE, 0), (BLOCK_SIZE, 0)]
        neighbors = []
        for direction in directions:
            neighbor = (position[0] + direction[0], position[1] + direction[1])
            if self.valid_position(neighbor):
                neighbors.append(neighbor)
        # print(f"Position: {position}, Valid neighbors: {neighbors}")
        return neighbors

    def valid_position(self, position):
        within_boundaries = 0 <= position[0] < WIDTH and 0 <= position[1] < HEIGHT
        not_colliding = position not in self.snake

        if hasattr( self.game, "player_snake" ):
            not_colliding = not_colliding and position not in self.game.player_snake
        is_valid = within_boundaries and not_colliding

        return is_valid

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.insert(0, current)
            current = came_from[current]
        return path

    def get_next_move(self, food_position):
        head = self.snake[0]  # Current head position of the AI snake

        self.path = self.aStar_search(head, food_position)

        if self.path:
            # Simulate eating food and escape paths
            test_snake = [ food_position ] + self.snake[:-1]    # Sim new snake body
            if not self.escape_possible( test_snake ):
                print("Path leads to entrapment. Path recalculating.")
                self.path = []    # Force recalculation

        if self.path:   # If path still valid, next step
            next_step = self.path[0]
            return next_step
            
        return None     # None if no path
    
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
        
    def draw_path( self, win ):
        for start, end in zip( self.path, self.path[1:] ):
            start_center = ( start[0] + BLOCK_SIZE // 2, start[1] + BLOCK_SIZE // 2 )
            end_center = ( end[0] + BLOCK_SIZE // 2, end[1] + BLOCK_SIZE // 2 )
            pygame.draw.line( win, WHITE, start_center, end_center, 2 )  # white path line