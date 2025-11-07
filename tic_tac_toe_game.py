import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")
        
        # Game state
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.game_mode = None  # 'pvp' or 'pvc'
        self.game_active = False
        self.scores = {'X': 0, 'O': 0, 'Tie': 0}
        
        # Colors
        self.bg_color = "#1a1a2e"
        self.button_bg = "#16213e"
        self.button_hover = "#0f3460"
        self.x_color = "#e94560"
        self.o_color = "#00d9ff"
        self.text_color = "#eaeaea"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface."""
        # Title
        title = tk.Label(
            self.root,
            text="TIC TAC TOE",
            font=("Arial", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        title.pack(pady=20)
        
        # Score board
        self.score_frame = tk.Frame(self.root, bg=self.bg_color)
        self.score_frame.pack(pady=10)
        
        self.score_label = tk.Label(
            self.score_frame,
            text=f"X: {self.scores['X']}  |  O: {self.scores['O']}  |  Ties: {self.scores['Tie']}",
            font=("Arial", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.score_label.pack()
        
        # Current player indicator
        self.player_label = tk.Label(
            self.root,
            text="Select Game Mode",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.player_label.pack(pady=10)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg=self.bg_color)
        self.board_frame.pack(pady=10)
        
        # Create buttons
        self.buttons = []
        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Arial", 36, "bold"),
                width=4,
                height=2,
                bg=self.button_bg,
                fg=self.text_color,
                activebackground=self.button_hover,
                relief="flat",
                cursor="hand2",
                command=lambda i=i: self.make_move(i)
            )
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)
            btn.config(state='disabled')
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg=self.bg_color)
        control_frame.pack(pady=20)
        
        # Mode selection buttons
        self.pvp_btn = tk.Button(
            control_frame,
            text="Player vs Player",
            font=("Arial", 12, "bold"),
            bg=self.button_bg,
            fg=self.text_color,
            activebackground=self.button_hover,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self.start_game('pvp')
        )
        self.pvp_btn.grid(row=0, column=0, padx=10)
        
        self.pvc_btn = tk.Button(
            control_frame,
            text="Player vs Computer",
            font=("Arial", 12, "bold"),
            bg=self.button_bg,
            fg=self.text_color,
            activebackground=self.button_hover,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=lambda: self.start_game('pvc')
        )
        self.pvc_btn.grid(row=0, column=1, padx=10)
        
        # Reset button
        self.reset_btn = tk.Button(
            control_frame,
            text="New Game",
            font=("Arial", 12, "bold"),
            bg=self.button_bg,
            fg=self.text_color,
            activebackground=self.button_hover,
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10,
            command=self.reset_game
        )
        self.reset_btn.grid(row=1, column=0, columnspan=2, pady=10)
    
    def start_game(self, mode):
        """Start a new game with selected mode."""
        self.game_mode = mode
        self.game_active = True
        self.reset_board()
        
        for btn in self.buttons:
            btn.config(state='normal')
        
        mode_text = "Player vs Player" if mode == 'pvp' else "Player vs Computer"
        self.player_label.config(text=f"{mode_text} | Player X's Turn", fg=self.x_color)
    
    def make_move(self, index):
        """Handle a player's move."""
        if not self.game_active or self.board[index] != '':
            return
        
        # Make the move
        self.board[index] = self.current_player
        self.buttons[index].config(
            text=self.current_player,
            fg=self.x_color if self.current_player == 'X' else self.o_color,
            state='disabled'
        )
        
        # Check for winner
        if self.check_winner():
            self.game_active = False
            self.scores[self.current_player] += 1
            self.update_score()
            self.show_winner(f"Player {self.current_player} Wins! 🎉")
            return
        
        # Check for tie
        if '' not in self.board:
            self.game_active = False
            self.scores['Tie'] += 1
            self.update_score()
            self.show_winner("It's a Tie! 🤝")
            return
        
        # Switch player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        player_name = f"Player {self.current_player}" if self.game_mode == 'pvp' else ("Computer" if self.current_player == 'O' else "Your")
        self.player_label.config(
            text=f"{player_name}'s Turn",
            fg=self.x_color if self.current_player == 'X' else self.o_color
        )
        
        # Computer's turn
        if self.game_mode == 'pvc' and self.current_player == 'O' and self.game_active:
            self.root.after(500, self.computer_move)
    
    def computer_move(self):
        """Make a move for the computer."""
        # Simple AI: try to win, block, or random
        move = self.get_best_move()
        if move is not None:
            self.make_move(move)
    
    def get_best_move(self):
        """Get the best move for computer."""
        # Try to win
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'O'
                if self.check_winner():
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        
        # Try to block
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = 'X'
                if self.check_winner():
                    self.board[i] = ''
                    return i
                self.board[i] = ''
        
        # Take center if available
        if self.board[4] == '':
            return 4
        
        # Take a corner
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if self.board[i] == '']
        if available_corners:
            return random.choice(available_corners)
        
        # Take any available space
        available = [i for i in range(9) if self.board[i] == '']
        return random.choice(available) if available else None
    
    def check_winner(self):
        """Check if current player has won."""
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combos:
            if (self.board[combo[0]] == self.board[combo[1]] == 
                self.board[combo[2]] == self.current_player):
                # Highlight winning combination
                for i in combo:
                    self.buttons[i].config(bg=self.button_hover)
                return True
        return False
    
    def show_winner(self, message):
        """Display winner message."""
        self.player_label.config(text=message, fg="#00d9ff")
        for btn in self.buttons:
            btn.config(state='disabled')
    
    def update_score(self):
        """Update the score display."""
        self.score_label.config(
            text=f"X: {self.scores['X']}  |  O: {self.scores['O']}  |  Ties: {self.scores['Tie']}"
        )
    
    def reset_board(self):
        """Reset the board for a new game."""
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        
        for btn in self.buttons:
            btn.config(
                text="",
                bg=self.button_bg,
                state='disabled'
            )
    
    def reset_game(self):
        """Reset everything including scores."""
        self.reset_board()
        self.game_active = False
        self.game_mode = None
        self.scores = {'X': 0, 'O': 0, 'Tie': 0}
        self.update_score()
        self.player_label.config(text="Select Game Mode", fg=self.text_color)

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
