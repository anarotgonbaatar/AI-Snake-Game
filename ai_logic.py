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

        # Recalculate path only when required
        if self.recalculate_path or not self.path or self.path[-1] != food_position or self.path[0] != head:
            self.path = self.aStar_search(head, food_position)
            self.recalculate_path = False

        # Follow the path step-by-step
        if self.path and len(self.path) > 1:
            next_step = self.path[1]

            # If the head reaches the current step, move to the next step
            if head == self.path[0]:
                self.path.pop(0)

            # Update direction for potential debugging (optional)
            self.current_direction = (next_step[0] - head[0], next_step[1] - head[1])
            return next_step

        # Fallback if no valid path
        print("AI couldn't find a valid path.")
        next_position = (head[0] + self.current_direction[0], head[1] + self.current_direction[1])
        return next_position if self.valid_position(next_position) else None
        
    def draw_path( self, win ):
        if self.path:
            for i in range( len( self.path ) - 1 ):
                start = ( self.path[i][0] + BLOCK_SIZE // 2, self.path[i][1] + BLOCK_SIZE // 2 )
                end = ( self.path[i + 1][0] + BLOCK_SIZE // 2, self.path[i + 1][1] + BLOCK_SIZE // 2 )
                pygame.draw.line( win, (0, 255, 255), start, end, 2 )  # Light blue line