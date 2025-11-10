import tkinter as tk
from tkinter import ttk
import random
from collections import deque
import time

class MazeSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver - BFS & DFS Visualizer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1a1a2e")
        
        # Maze settings
        self.rows = 20
        self.cols = 30
        self.cell_size = 25
        self.maze = []
        self.start = (0, 0)
        self.end = (self.rows-1, self.cols-1)
        
        # Colors
        self.bg_color = "#1a1a2e"
        self.wall_color = "#0f3460"
        self.path_color = "#eaeaea"
        self.start_color = "#00ff88"
        self.end_color = "#ff0055"
        self.visited_bfs_color = "#4fc3f7"
        self.visited_dfs_color = "#ba68c8"
        self.solution_color = "#ffd700"
        
        # Animation state
        self.is_solving = False
        self.animation_speed = 50  # milliseconds
        
        self.setup_ui()
        self.generate_maze()
        self.draw_maze()
    
    def setup_ui(self):
        """Create the user interface."""
        # Title
        title = tk.Label(
            self.root,
            text="🎯 MAZE SOLVER",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg="#eaeaea"
        )
        title.pack(pady=10)
        
        # Info frame
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(pady=5)
        
        self.info_label = tk.Label(
            info_frame,
            text="Click 'Generate Maze' to start!",
            font=("Arial", 12),
            bg=self.bg_color,
            fg="#eaeaea"
        )
        self.info_label.pack()
        
        # Canvas for maze
        self.canvas = tk.Canvas(
            self.root,
            width=self.cols * self.cell_size,
            height=self.rows * self.cell_size,
            bg="#0f0f1e",
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Control panel
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=10)
        
        # Buttons
        self.gen_btn = tk.Button(
            control_frame,
            text="Generate Maze",
            font=("Arial", 11, "bold"),
            bg="#16213e",
            fg="#eaeaea",
            activebackground="#0f3460",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.generate_and_draw
        )
        self.gen_btn.grid(row=0, column=0, padx=5)
        
        self.bfs_btn = tk.Button(
            control_frame,
            text="Solve with BFS",
            font=("Arial", 11, "bold"),
            bg="#1976d2",
            fg="#eaeaea",
            activebackground="#1565c0",
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.solve_maze('bfs')
        )
        self.bfs_btn.grid(row=0, column=1, padx=5)
        
        self.dfs_btn = tk.Button(
            control_frame,
            text="Solve with DFS",
            font=("Arial", 11, "bold"),
            bg="#7b1fa2",
            fg="#eaeaea",
            activebackground="#6a1b9a",
            cursor="hand2",
            padx=15,
            pady=8,
            command=lambda: self.solve_maze('dfs')
        )
        self.dfs_btn.grid(row=0, column=2, padx=5)
        
        self.clear_btn = tk.Button(
            control_frame,
            text="Clear Solution",
            font=("Arial", 11, "bold"),
            bg="#16213e",
            fg="#eaeaea",
            activebackground="#0f3460",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.clear_solution
        )
        self.clear_btn.grid(row=0, column=3, padx=5)
        
        # Speed control
        speed_frame = tk.Frame(control_frame, bg=self.bg_color)
        speed_frame.grid(row=1, column=0, columnspan=4, pady=10)
        
        tk.Label(
            speed_frame,
            text="Animation Speed:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#eaeaea"
        ).pack(side=tk.LEFT, padx=5)
        
        self.speed_scale = tk.Scale(
            speed_frame,
            from_=1,
            to=100,
            orient=tk.HORIZONTAL,
            bg="#16213e",
            fg="#eaeaea",
            highlightthickness=0,
            troughcolor="#0f3460",
            command=self.update_speed
        )
        self.speed_scale.set(50)
        self.speed_scale.pack(side=tk.LEFT)
        
        # Legend
        legend_frame = tk.Frame(self.root, bg=self.bg_color)
        legend_frame.pack(pady=5)
        
        legends = [
            ("Start", self.start_color),
            ("End", self.end_color),
            ("Wall", self.wall_color),
            ("Path", self.path_color),
            ("BFS Visited", self.visited_bfs_color),
            ("DFS Visited", self.visited_dfs_color),
            ("Solution", self.solution_color)
        ]
        
        for i, (text, color) in enumerate(legends):
            frame = tk.Frame(legend_frame, bg=self.bg_color)
            frame.grid(row=0, column=i, padx=8)
            
            box = tk.Canvas(frame, width=15, height=15, bg=color, highlightthickness=1)
            box.pack(side=tk.LEFT, padx=3)
            
            tk.Label(
                frame,
                text=text,
                font=("Arial", 9),
                bg=self.bg_color,
                fg="#eaeaea"
            ).pack(side=tk.LEFT)
    
    def update_speed(self, val):
        """Update animation speed."""
        self.animation_speed = 101 - int(val)
    
    def generate_maze(self):
        """Generate a random maze using DFS."""
        # Initialize maze with all walls
        self.maze = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # DFS maze generation
        stack = [(0, 0)]
        self.maze[0][0] = 0
        
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        
        while stack:
            current = stack[-1]
            row, col = current
            
            # Find unvisited neighbors
            neighbors = []
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.rows and 0 <= new_col < self.cols 
                    and self.maze[new_row][new_col] == 1):
                    neighbors.append((new_row, new_col, dr, dc))
            
            if neighbors:
                # Choose random neighbor
                new_row, new_col, dr, dc = random.choice(neighbors)
                # Remove wall between current and neighbor
                self.maze[row + dr//2][col + dc//2] = 0
                self.maze[new_row][new_col] = 0
                stack.append((new_row, new_col))
            else:
                stack.pop()
        
        # Ensure start and end are paths
        self.maze[0][0] = 0
        self.maze[self.rows-1][self.cols-1] = 0
    
    def generate_and_draw(self):
        """Generate new maze and draw it."""
        if not self.is_solving:
            self.generate_maze()
            self.draw_maze()
            self.info_label.config(text="New maze generated! Choose an algorithm to solve.")
    
    def draw_maze(self):
        """Draw the maze on canvas."""
        self.canvas.delete("all")
        
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                if (row, col) == self.start:
                    color = self.start_color
                elif (row, col) == self.end:
                    color = self.end_color
                elif self.maze[row][col] == 1:
                    color = self.wall_color
                else:
                    color = self.path_color
                
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#0f0f1e",
                    tags=f"cell_{row}_{col}"
                )
    
    def draw_cell(self, row, col, color):
        """Update a cell's color."""
        if (row, col) != self.start and (row, col) != self.end:
            x1 = col * self.cell_size
            y1 = row * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="#0f0f1e",
                tags=f"cell_{row}_{col}"
            )
            self.canvas.update()
    
    def solve_maze(self, algorithm):
        """Solve maze with selected algorithm."""
        if self.is_solving:
            return
        
        self.is_solving = True
        self.clear_solution()
        
        if algorithm == 'bfs':
            self.info_label.config(text="Solving with BFS (Breadth-First Search)...")
            self.root.after(100, self.bfs_solve)
        else:
            self.info_label.config(text="Solving with DFS (Depth-First Search)...")
            self.root.after(100, self.dfs_solve)
    
    def bfs_solve(self):
        """Solve maze using BFS."""
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        steps = 0
        
        def bfs_step():
            nonlocal steps
            
            if not queue:
                self.info_label.config(text="❌ No solution found!")
                self.is_solving = False
                return
            
            current, path = queue.popleft()
            row, col = current
            
            # Visualize exploration
            if current != self.start and current != self.end:
                self.draw_cell(row, col, self.visited_bfs_color)
            
            if current == self.end:
                # Draw solution path
                self.root.after(300, lambda: self.draw_solution(path, steps))
                return
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                new_pos = (new_row, new_col)
                
                if (0 <= new_row < self.rows and 0 <= new_col < self.cols 
                    and self.maze[new_row][new_col] == 0 and new_pos not in visited):
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
            
            steps += 1
            self.root.after(self.animation_speed, bfs_step)
        
        bfs_step()
    
    def dfs_solve(self):
        """Solve maze using DFS."""
        stack = [(self.start, [self.start])]
        visited = {self.start}
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        steps = 0
        
        def dfs_step():
            nonlocal steps
            
            if not stack:
                self.info_label.config(text="❌ No solution found!")
                self.is_solving = False
                return
            
            current, path = stack.pop()
            row, col = current
            
            # Visualize exploration
            if current != self.start and current != self.end:
                self.draw_cell(row, col, self.visited_dfs_color)
            
            if current == self.end:
                # Draw solution path
                self.root.after(300, lambda: self.draw_solution(path, steps))
                return
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                new_pos = (new_row, new_col)
                
                if (0 <= new_row < self.rows and 0 <= new_col < self.cols 
                    and self.maze[new_row][new_col] == 0 and new_pos not in visited):
                    visited.add(new_pos)
                    stack.append((new_pos, path + [new_pos]))
            
            steps += 1
            self.root.after(self.animation_speed, dfs_step)
        
        dfs_step()
    
    def draw_solution(self, path, steps):
        """Draw the solution path."""
        for i, (row, col) in enumerate(path):
            if (row, col) != self.start and (row, col) != self.end:
                self.root.after(i * 30, lambda r=row, c=col: self.draw_cell(r, c, self.solution_color))
        
        self.root.after(len(path) * 30 + 100, lambda: self.info_label.config(
            text=f"✅ Solution found! Path length: {len(path)} | Steps explored: {steps}"
        ))
        self.is_solving = False
    
    def clear_solution(self):
        """Clear the solution and redraw maze."""
        if not self.is_solving:
            self.draw_maze()
            self.info_label.config(text="Cleared! Choose an algorithm to solve.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolver(root)
    root.mainloop()
