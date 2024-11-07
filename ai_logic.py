# Just AI Logic
import heapq
from utils import WIDTH, HEIGHT, BLOCK_SIZE, BLUE
import pygame

class SnakeAI:
    def __init__(self, game_instance):
        self.game = game_instance
        self.current_direction = ( BLOCK_SIZE, 0 )
        self.path = []

    def aStar_search(self, start, goal):
        # print(f"Starting A* from {start} to {goal}")
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
                # print(f"Path found: {path}")
                return path

            neighbors = self.get_neighbors(current)
            # print(f"Current position: {current}, Neighbors: {neighbors}")
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # print("No path found")
        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

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
        not_colliding = position not in self.game.snake
        is_valid = within_boundaries and not_colliding
        # print( f"Checking position: {position}, Within boundaries: {within_boundaries}, Not colliding: {not_colliding}, Valid: {is_valid}")
        return is_valid

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.insert(0, current)
            current = came_from[current]
        return path

    def get_next_move(self, food_position):
        head = self.game.snake[0]
        # Calculate the difference in x and y coordinates
        dx = food_position[0] - head[0]
        dy = food_position[1] - head[1]

        possible_moves = [
            ( head[0] + BLOCK_SIZE, head[1] ),  # right
            ( head[0] - BLOCK_SIZE, head[1] ),  # left
            ( head[0], head[1] + BLOCK_SIZE ),  # down
            ( head[0], head[1] - BLOCK_SIZE )  # up
        ]

        directions = [
            ( BLOCK_SIZE, 0 ),   # right
            ( -BLOCK_SIZE, 0 ),   # left
            ( 0, BLOCK_SIZE ),   # down
            ( 0, -BLOCK_SIZE )   # up
        ]

        # Step 1: Filter out reverse direction; don't want the AI snake running into itself or move wrongly
        valid_moves = [
            move for move, direction in zip( possible_moves, directions )
            if direction != ( -self.current_direction[0], -self.current_direction[1] ) and self.valid_position( move )
        ]
        
        # Step 2: Choose the move towards food
        next_move = min( valid_moves, key=lambda move: abs( food_position[0] - move[0]) + abs( food_position[1] - move[1] ) )

        # Step 3: Update current direction
        self.current_direction = ( next_move[0] - head[0], next_move[1] - head[1] )

        # print(f"Move decision: Head={head}, Food={food_position}, Next Move={next_move}")
        return next_move
    
    def draw_path( self, win, path=None ):
        if path is None:
            path = self.path
        if path:
            for i in range( len( path ) - 1 ):
                start = path[i]
                end = path[ i + 1 ]
                pygame.draw.line( win, BLUE, ( start[0] + BLOCK_SIZE // 2, start[1] + BLOCK_SIZE // 2 ),
                                 ( end[0] + BLOCK_SIZE // 2, end[1] + BLOCK_SIZE // 2 ), 2 )