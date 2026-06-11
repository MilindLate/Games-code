import random
import time
import os
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored text
init(autoreset=True)

# --- Game Configuration ---
BOARD_SIZE = 100

LADDERS = {3: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 99}
SNAKES = {17: 7, 54: 34, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 79}
POWER_UPS = {15: 5, 45: 5, 75: 5} # Landing here gives +5 bonus steps

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def roll_die():
    return random.randint(1, 6)

def check_square(position, player_name):
    """Checks for snakes, ladders, or power-ups."""
    if position in LADDERS:
        print(f"\n  🪜  {Fore.GREEN}{Style.BRIGHT}CLIMB!{Style.RESET_ALL} {player_name} found a ladder! Scaling from {position} to {LADDERS[position]}.")
        return LADDERS[position]
    elif position in SNAKES:
        print(f"\n  🐍  {Fore.RED}{Style.BRIGHT}HISSS!{Style.RESET_ALL} {player_name} stepped on a snake! Sliding from {position} to {SNAKES[position]}.")
        return SNAKES[position]
    elif position in POWER_UPS:
        bonus = POWER_UPS[position]
        print(f"\n  ⚡  {Fore.MAGENTA}{Style.BRIGHT}POWER-UP!{Style.RESET_ALL} {player_name} hit a speed boost! Jumping {bonus} steps ahead to {position + bonus}.")
        return position + bonus
    return position

def print_board(p1_pos, p2_pos, p1_name, p2_name):
    """Renders a fully colored, scannable 10x10 game board grid."""
    print(f"\n=== {Fore.YELLOW}{Style.BRIGHT}BOARD MAP{Style.RESET_ALL} ===")
    
    # Grid goes from row 9 (91-100) down to row 0 (1-10)
    for row in range(9, -1, -1):
        row_str = ""
        # Handle snake-like alternating row directions
        if row % 2 == 0:
            squares = range(row * 10 + 1, row * 10 + 11)
        else:
            squares = range(row * 10 + 10, row * 10, -1)
            
        for square in squares:
            # Player overlapping checks
            if square == p1_pos and square == p2_pos:
                cell = f"{Back.CYAN}{Fore.BLACK} P12 "
            elif square == p1_pos:
                cell = f"{Back.BLUE}{Fore.WHITE}  P1  "
            elif square == p2_pos:
                cell = f"{Back.YELLOW}{Fore.BLACK}  P2  "
            # Entity checks
            elif square in LADDERS:
                cell = f" {Fore.GREEN} 🪜  {Style.RESET_ALL}"
            elif square in SNAKES:
                cell = f" {Fore.RED} 🐍  {Style.RESET_ALL}"
            elif square in POWER_UPS:
                cell = f" {Fore.MAGENTA} ⚡  {Style.RESET_ALL}"
            else:
                cell = f"  {square:02d}  "
                
            row_str += cell + " "
        print(row_str)
    print("=" * 65)

def main():
    clear_screen()
    print(f"{Fore.GREEN}{Style.BRIGHT}" + "="*45)
    print(f"   🐍  {Fore.YELLOW}WELCOME TO SUPER SNAKES & LADDERS{Fore.GREEN}  🪜")
    print("="*45 + "\n")
    
    # Mode Selection
    print("Select Game Mode:")
    print("1. Two Players (Local PvP)")
    print("2. Play against AI Bot")
    choice = input("Enter choice (1 or 2): ").strip()
    
    p1_name = input("\nEnter Player 1 Name: ").strip() or "Player 1"
    if choice == "2":
        p2_name = "🤖 AI Bot"
        is_ai = True
    else:
        p2_name = input("Enter Player 2 Name: ").strip() or "Player 2"
        is_ai = False
        
    positions = {p1_name: 0, p2_name: 0}
    players = [p1_name, p2_name]
    turn = 0
    
    clear_screen()
    print(f"\n{Fore.GREEN}Game Started! Good luck!")
    
    while True:
        current_player = players[turn % 2]
        is_current_ai = (current_player == p2_name and is_ai)
        
        print_board(positions[p1_name], positions[p2_name], p1_name, p2_name)
        
        # Display Scoreboard
        print(f"📊 {Fore.BLUE}{p1_name}: {positions[p1_name]}{Style.RESET_ALL} | {Fore.YELLOW}{p2_name}: {positions[p2_name]}{Style.RESET_ALL}")
        print(f"👉 Current Turn: {Fore.HEADER}{Style.BRIGHT}{current_player}{Style.RESET_ALL}")
        
        if is_current_ai:
            print("🤖 AI is thinking...", end="", flush=True)
            time.sleep(1.2)
            print(" Rolled!")
        else:
            input("Press [Enter] to roll the dice... ")
            
        # Dice Roll Animation Effect
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.1)
            
        die_value = roll_die()
        print(f"\n🎲 {current_player} rolled a {Fore.YELLOW}{Style.BRIGHT}{die_value}!{Style.RESET_ALL}")
        
        old_pos = positions[current_player]
        new_pos = old_pos + die_value
        
        if new_pos > BOARD_SIZE:
            print(f"⚠️  {Fore.LIGHTBLACK_EX}Rolled too high! Needs exactly {BOARD_SIZE - old_pos} to win. Staying at {old_pos}.{Style.RESET_ALL}")
            bonus_turn = False
        else:
            positions[current_player] = new_pos
            # Process board event mechanics
            positions[current_player] = check_square(positions[current_player], current_player)
            print(f"📍 {current_player} moves from {old_pos} ➡️ {Fore.CYAN}{positions[current_player]}{Style.RESET_ALL}")
            
            # Bonus turn logic
            bonus_turn = (die_value == 6 and positions[current_player] != BOARD_SIZE)
            if bonus_turn:
                print(f"🔥 {Fore.YELLOW}{Style.BRIGHT}CONSECUTIVE 6!{Style.RESET_ALL} {current_player} gets an extra turn!")
                time.sleep(1)
        
        # Check Win state
        if positions[current_player] == BOARD_SIZE:
            clear_screen()
            print_board(positions[p1_name], positions[p2_name], p1_name, p2_name)
            print("\n" + "🎉" * 15)
            print(f"👑 {Fore.YELLOW}{Style.BRIGHT}{current_player.upper()} WINS THE GAME!!!!{Style.RESET_ALL} 👑")
            print("🎉" * 15 + "\n")
            break
            
        # Increment turn cycle if no bonus turn earned
        if not bonus_turn:
            turn += 1
            
        time.sleep(1.5)
        clear_screen()

if __name__ == "__main__":
    main()
