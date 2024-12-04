import time
import pygame
import sys
import tracemalloc
from logics.utils import GRID_WIDTH, GRID_HEIGHT
from logics.utils import snake_position, generate_food
from logics.ai_logic import SnakeAI
from logics.snake_game import SnakeGame

class BenchmarkMode( SnakeGame ):
    def __init__( self, win, runs = 100 ) -> None:
        super().__init__( win )
        self.ai = SnakeAI( self, self.snake )
        self.runs = runs
        self.results = []
        self.fps = 0

    def benchmark( self ):
        clock = pygame.time.Clock()

        for run in range( self.runs ):
            print( f"Run { run + 1 }/{ self.runs }..." )
            self.reset_game()

            start_time = time.time()
            tracemalloc.start()
            survival_ticks = 0
            pf_time_total = 0
            pf_calls = 0

            while self.running:
                # Avoid freezing
                pygame.event.pump()
                # clock.tick( self.fps )

                next_move = self.ai.get_next_move( self.food )
        
                # AI snake movement logic
                self.food, self.score, self.running = self.ai.update_ai_movement(
                    self.snake, next_move, self.food, self.score, self.running, self.win, sys, BenchmarkMode
                )

                if self.check_collision( self.snake ):
                    self.running = False
                    # game_over( self.win, None, self.score, BenchmarkMode, sys )

                # self.draw_all( None, self.snake, None, self.food, None, self.score, self.win )
                # self.ai.draw_path( self.win )

                # pygame.display.update()
                
                # Measure pathfinding time
                pf_start = time.time()
                next_move = self.ai.get_next_move( self.food )
                pf_time = time.time() - pf_start
                pf_time_total += pf_time
                pf_calls += 1

                survival_ticks += 1

                clock.tick( self.fps )

            memory_usage = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            total_time = time.time() - start_time

            # Save results for this run
            if pf_calls > 0: average_pf_time = pf_time_total / pf_calls
            else: average_pf_time = 0

            self.results.append({
                "run": run + 1,
                "pathfinding_time": average_pf_time,
                "survival_ticks": survival_ticks,
                "score": self.score,
                "memory_usage": memory_usage,
            })

        # Log results for this run
        self.log_results()

    # Reset the game after each run
    def reset_game( self ):
        self.snake = snake_position( 2, 2 )
        self.food = generate_food( self.snake )
        self.score = 0
        self.running = True
        self.ai = SnakeAI( self, self.snake )

    # Prepare all metrics and log them to the output file
    def log_results( self ):
        with open( "performance_metrics.txt", "a" ) as log_file:
            grid_size = f"{ GRID_WIDTH }/{ GRID_HEIGHT }"
            runs = len( self.results )
            avg_pf = sum( r["pathfinding_time"] for r in self.results ) / runs
            avg_survival = sum( r["survival_ticks"] for r in self.results ) / runs
            avg_score = sum( r["score"] for r in self.results ) / runs
            avg_memory = sum( r["memory_usage"] for r in self.results ) / runs

            log_file.write(
                f"Grid Size: { grid_size } | Number of Runs: { runs } | "
                f"Avg Pathfinding Speed: { avg_pf:.4f }s | "
                f"Avg Survival Time: { avg_survival:.2f } ticks | "
                f"Avg Score: { avg_score:.2f } | "
                f"Avg Memory Usage: { avg_memory / 1024:.4f } KB/n"
            )
        
        print( "Results logged to performance_metrics.txt" )