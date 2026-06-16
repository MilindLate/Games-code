import os
import random
import time

# --- CONSTANTS & DATA ---
CATEGORIES = {
    "1": ("Programming", ["python", "javascript", "developer", "algorithm", "compiler", "database"]),
    "2": ("Animals", ["kangaroo", "chameleon", "platypus", "leopard", "dolphin", "elephant"]),
    "3": ("Countries", ["switzerland", "australia", "madagascar", "brazil", "japan", "canada"]),
    "4": ("Movies", ["inception", "gladiator", "interstellar", "avengers", "parasite", "matrix"])
}

# HANGMAN ASCII STAGES
STAGES = [
    """
       +---+
       |   |
           |
           |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
           |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
     =========
    """,
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
     =========
    """
]

# UI Color Codes
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"

# --- HELPER FUNCTIONS ---
def clear_screen():
    """Clears the terminal screen for a clean UI experience."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Prints a styled header."""
    print(f"{BLUE}========================================={RESET}")
    print(f"{CYAN}  {title}  {RESET}")
    print(f"{BLUE}========================================={RESET}\n")

def select_category():
    """UX flow for picking a word category."""
    while True:
        clear_screen()
        print_header("WELCOME TO ADVANCED HANGMAN")
        print("Select a category to begin:")
        for key, value in CATEGORIES.items():
            print(f" [{key}] {value[0]}")
        print(" [E] Exit Game\n")
        
        choice = input("Enter your choice: ").strip().lower()
        if choice == 'e':
            return None
        if choice in CATEGORIES:
            return CATEGORIES[choice]
        
        print(f"{RED}Invalid selection. Please try again.{RESET}")
        time.sleep(1)

# --- CORE GAME LOOP ---
def play_hangman(category_name, word_list):
    word = random.choice(word_list).lower()
    guessed_letters = set()
    wrong_guesses = 0
    max_lives = len(STAGES) - 1
    message = f"Welcome! Good luck guessing the word."
    message_color = GREEN

    while wrong_guesses < max_lives:
        clear_screen()
        print_header(f"CATEGORY: {category_name.upper()}")
        
        # Display Hangman Art
        print(STAGES[wrong_guesses])
        
        # Display Hidden Word Progress
        display_word = [letter if letter in guessed_letters else "_" for letter in word]
        print(f"Word:  {' '.join(display_word).upper()}\n")
        
        # Display Guessed Letters Bank
        if guessed_letters:
            sorted_guesses = sorted(list(guessed_letters))
            print(f"Guessed letters: {YELLOW}{', '.join(sorted_guesses).upper()}{RESET}")
        else:
            print("Guessed letters: None")
            
        print(f"Lives remaining: {RED}{'♥ ' * (max_lives - wrong_guesses)}{RESET}\n")
        
        # Status/Feedback Message from previous turn
        if message:
            print(f"{message_color}• {message}{RESET}\n")
            message = "" # Clear after displaying

        # Check if player won
        if "_" not in display_word:
            clear_screen()
            print_header("YOU WIN! 🎉")
            print(f"{GREEN}Congratulations! You guessed the word: {word.upper()}{RESET}\n")
            print(STAGES[wrong_guesses])
            break

        # Get Player Input
        guess = input("Guess a letter: ").strip().lower()

        # Input Validation (UX First)
        if len(guess) != 1 or not guess.isalpha():
            message = "Please enter a single valid letter (A-Z)."
            message_color = RED
            continue
            
        if guess in guessed_letters:
            message = f"You already guessed '{guess.upper()}'. Try a different one!"
            message_color = YELLOW
            continue

        # Process Guess
        guessed_letters.add(guess)
        
        if guess in word:
            message = f"Nice! '{guess.upper()}' is in the word."
            message_color = GREEN
        else:
            wrong_guesses += 1
            message = f"Oops! '{guess.upper()}' is not in the word."
            message_color = RED

    else:
        # Runs if the while loop completes without a 'break' (Player Lost)
        clear_screen()
        print_header("GAME OVER 💀")
        print(STAGES[max_lives])
        print(f"{RED}You ran out of lives!{RESET}")
        print(f"The correct word was: {BLUE}{word.upper()}{RESET}\n")

# --- MAIN ENTRY POINT ---
def main():
    while True:
        selection = select_category()
        if selection is None:
            clear_screen()
            print(f"\n{CYAN}Thanks for playing Hangman! Goodbye!{RESET}\n")
            break
        
        category_name, word_list = selection
        play_hangman(category_name, word_list)
        
        # Post-game choice
        play_again = input("Play again? (Y/N): ").strip().lower()
        if play_again != 'y':
            clear_screen()
            print(f"\n{CYAN}Thanks for playing Hangman! Goodbye!{RESET}\n")
            break

if __name__ == "__main__":
    main()
