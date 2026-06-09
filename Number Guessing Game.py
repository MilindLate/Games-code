import random
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Button, Static, Input, Digits

class GuessingGameApp(App):
    CSS = """
    Screen {
        align: center middle;
        background: $surface;
    }
    #game-container {
        width: 60;
        height: auto;
        border: solid $accent;
        padding: 1 2;
        background: $panel;
    }
    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }
    #range-display {
        text-align: center;
        background: $boost;
        margin: 1 0;
        padding: 1;
    }
    Input {
        margin: 1 0;
    }
    Button {
        width: 100%;
        margin-top: 1;
    }
    #feedback {
        text-align: center;
        text-style: bold;
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        self.secret = random.randint(1, 100)
        self.lower = 1
        self.upper = 100
        self.attempts = 0
        
        yield Header()
        with Vertical(id="game-container"):
            yield Static("🎯 ADVANCED GUESSING GAME 🎯", classes="title")
            yield Static(f"Current Range: {self.lower} - {self.upper}", id="range-display")
            yield Static("Enter a number below and press Submit!", id="feedback")
            yield Input(placeholder="Type your guess...", id="guess-input")
            yield Button("Submit Guess", variant="primary", id="submit-btn")
            yield Button("Reset Game", variant="error", id="reset-btn")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit-btn":
            self.process_guess()
        elif event.button.id == "reset-btn":
            self.reset_game()

    def process_guess(self) -> None:
        input_widget = self.query_one("#guess-input", Input)
        feedback_widget = self.query_one("#feedback", Static)
        range_widget = self.query_one("#range-display", Static)
        
        value = input_widget.value
        if not value.isdigit():
            feedback_widget.update("[b red]⚠️ Please enter a valid number![/]")
            return

        guess = int(value)
        self.attempts += 1

        if guess < self.secret:
            self.lower = max(self.lower, guess + 1)
            feedback_widget.update("[b blue]⬇️ Too Low! Try higher.[/]")
        elif guess > self.secret:
            self.upper = min(self.upper, guess - 1)
            feedback_widget.update("[b orange3]⬆️ Too High! Try lower.[/]")
        else:
            feedback_widget.update(f"[b green]🎉 Winner! Guessed in {self.attempts} tries![/]")
            range_widget.update(f"🏆 The number was {self.secret}!")
            input_widget.disabled = True
            return

        range_widget.update(f"Current Range: {self.lower} - {self.upper}")
        input_widget.value = ""
        input_widget.focus()

    def reset_game(self) -> None:
        self.secret = random.randint(1, 100)
        self.lower = 1
        self.upper = 100
        self.attempts = 0
        
        input_widget = self.query_one("#guess-input", Input)
        input_widget.disabled = False
        input_widget.value = ""
        
        self.query_one("#feedback", Static).update("Game reset! Enter a new guess.")
        self.query_one("#range-display", Static).update(f"Current Range: {self.lower} - {self.upper}")

if __name__ == "__main__":
    GuessingGameApp().run()
