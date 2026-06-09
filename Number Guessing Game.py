import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.progress import track

# Initialize Rich Console for beautiful terminal output
console = Console()

class NumberGuessingGame:
    def __init__(self):
        self.lower = 1
        self.upper = 100
        self.secret_number = 0
        self.attempts = 0
        self.max_attempts = 0
        self.score = 1000

    def display_welcome(self):
        """Displays a beautiful title card."""
        console.clear()
        console.print(
            Panel.fit(
                "[bold cyan]🎯 THE ULTIMATE NUMBER GUESSING GAME 🎯[/bold cyan]\n"
                "[dim]Can you outsmart the computer? Let's find out.[/dim]",
                border_style="magenta",
                padding=(1, 4)
            )
        )

    def select_difficulty(self):
        """Allows the player to choose a difficulty, dynamically setting the range and attempts."""
        console.print("\n[bold yellow]Select your Difficulty Level:[/bold yellow]")
        console.print("[green]1. Easy[/green] (Range: 1-50, Unlimited Attempts)")
        console.print("[yellow]2. Medium[/yellow] (Range: 1-100, 10 Attempts)")
        console.print("[red]3. Hard[/red] (Range: 1-200, 6 Attempts)")
        
        choice = Prompt.ask("Choose (1/2/3)", choices=["1", "2", "3"], default="2")
        
        if choice == "1":
            self.upper = 50
            self.max_attempts = float('inf')
        elif choice == "2":
            self.upper = 100
            self.max_attempts = 10
        else:
            self.upper = 200
            self.max_attempts = 6

        # Simulate "thinking" animation for the AI
        for _ in track(range(5), description="[purple]Generating secret number..."):
            time.sleep(0.1)
            
        self.secret_number = random.randint(self.lower, self.upper)

    def play_round(self):
        """Handles the core gameplay loop with smart boundary tracking."""
        self.display_welcome()
        self.select_difficulty()
        
        console.print(f"\n[bold green]Game Started![/bold green] I'm thinking of a number between [bold]{self.lower}[/bold] and [bold]{self.upper}[/bold].")
        if self.max_attempts != float('inf'):
            console.print(f"You have a maximum of [bold red]{self.max_attempts}[/bold red] attempts. Good luck!\n")

        while True:
            # Check if player ran out of attempts
            if self.attempts >= self.max_attempts:
                console.print(Panel(
                    f"[bold red]💥 GAME OVER! 💥[/bold red]\n\nYou've run out of attempts. The correct number was [bold cyan]{self.secret_number}[/bold cyan].",
                    title="Better luck next time!", border_style="red"
                ))
                break

            # Prompt user for input (IntPrompt automatically handles input validation)
            guess = IntPrompt.ask(f"[bold]Enter your guess[/bold] [dim]({self.lower}-{self.upper})[/dim]")

            # Smart boundary validation
            if guess < self.lower or guess > self.upper:
                console.print(f"[bold orange3]⚠️ Out of Bounds![/bold orange3] Please guess between {self.lower} and {self.upper}.")
                continue

            self.attempts += 1
            self.score = max(100, self.score - 75)  # Score decays with each wrong guess

            # Check the guess
            if guess < self.secret_number:
                console.print("[bold blue]⬇️ Too low![/bold blue] Try aiming higher.")
                self.lower = max(self.lower, guess + 1)
            elif guess > self.secret_number:
                console.print("[bold red]⬆️ Too high![/bold red] Try aiming lower.")
                self.upper = min(self.upper, guess - 1)
            else:
                # Victory screen!
                attempt_text = f"{self.attempts} attempt" if self.attempts == 1 else f"{self.attempts} attempts"
                console.print("\n")
                console.print(Panel(
                    f"[bold green]🎉 CONGRATULATIONS! 🎉[/bold green]\n\n"
                    f"You guessed the right number: [bold gold1]{self.secret_number}[/bold gold1]\n"
                    f"Attempts taken: [bold cyan]{attempt_text}[/bold cyan]\n"
                    f"Final Score: [bold magenta]{self.score} pts[/bold magenta]",
                    title="🌟 VICTORY 🌟",
                    border_style="green",
                    padding=(1, 2)
                ))
                break

def main():
    while True:
        game = NumberGuessingGame()
        game.play_round()
        
        play_again = Prompt.ask("\nWant to play another round?", choices=["y", "n"], default="y")
        if play_again.lower() != 'y':
            console.print("\n[bold magenta]Thanks for playing! Goodbye! 👋[/bold magenta]\n")
            break

if __name__ == "__main__":
    main()
