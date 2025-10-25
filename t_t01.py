import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 15
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SPEED = 5
PADDLE_SPEED = 7
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Table Tennis Game")

# Game reset function
def reset_game():
    return {
        "ball_x": WIDTH // 2,
        "ball_y": HEIGHT // 2,
        "ball_dx": random.choice([-BALL_SPEED, BALL_SPEED]),
        "ball_dy": random.choice([-BALL_SPEED, BALL_SPEED]),
        "left_paddle_y": HEIGHT // 2 - PADDLE_HEIGHT // 2,
        "right_paddle_y": HEIGHT // 2 - PADDLE_HEIGHT // 2,
        "left_score": 0,
        "right_score": 0,
        "game_over": False,
        "winner": None,
    }

# Initialize game state
game_state = reset_game()
WINNING_SCORE = None

# Function to display the setup screen
def display_setup_screen():
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)
    input_active = True
    input_text = ""
    while input_active:
        screen.fill(BLACK)
        title_text = font.render("Set Winning Score", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Render input text
        input_surface = font.render(input_text, True, GREEN)
        screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))

        instruction_text = small_font.render("Press ENTER to confirm", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

# Function to display the instructions page
def display_instructions_page():
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)
    
    instructions = [
        "Welcome to Table Tennis!",
        "Player 1: Use W (up) and S (down) to move",
        "Player 2: Use UP (up) and DOWN (down) to move",
        "Press ENTER to start the game",
        "First to reach the set score wins!"
    ]
    
    while True:
        screen.fill(BLACK)
        
        # Display instructions
        y_offset = HEIGHT // 4
        for line in instructions:
            text = font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
            y_offset += 50
        
        # Instruction to start game
        start_text = small_font.render("Press ENTER to start", True, GREEN)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 100))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

# Prompt for winning score
if WINNING_SCORE is None:
    WINNING_SCORE = display_setup_screen()

# Show instructions page before starting the game
display_instructions_page()

while True:
    # Game loop
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Restart game when ESC is pressed
                if event.key == pygame.K_ESCAPE:
                    WINNING_SCORE = display_setup_screen()
                    game_state = reset_game()

        if not game_state["game_over"]:
            # Get keys for paddle movement
            keys = pygame.key.get_pressed()
            # Left paddle movement
            if keys[pygame.K_w] and game_state["left_paddle_y"] > 0:
                game_state["left_paddle_y"] -= PADDLE_SPEED
            if keys[pygame.K_s] and game_state["left_paddle_y"] < HEIGHT - PADDLE_HEIGHT:
                game_state["left_paddle_y"] += PADDLE_SPEED
            # Right paddle movement
            if keys[pygame.K_UP] and game_state["right_paddle_y"] > 0:
                game_state["right_paddle_y"] -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and game_state["right_paddle_y"] < HEIGHT - PADDLE_HEIGHT:
                game_state["right_paddle_y"] += PADDLE_SPEED

            # Ball movement
            game_state["ball_x"] += game_state["ball_dx"]
            game_state["ball_y"] += game_state["ball_dy"]

            # Ball collision with top and bottom walls
            if game_state["ball_y"] - BALL_RADIUS <= 0 or game_state["ball_y"] + BALL_RADIUS >= HEIGHT:
                game_state["ball_dy"] = -game_state["ball_dy"]

            # Ball collision with paddles
            if (game_state["ball_x"] - BALL_RADIUS <= PADDLE_WIDTH and
                    game_state["left_paddle_y"] <= game_state["ball_y"] <= game_state["left_paddle_y"] + PADDLE_HEIGHT):
                game_state["ball_dx"] = -game_state["ball_dx"]
            if (game_state["ball_x"] + BALL_RADIUS >= WIDTH - PADDLE_WIDTH and
                    game_state["right_paddle_y"] <= game_state["ball_y"] <= game_state["right_paddle_y"] + PADDLE_HEIGHT):
                game_state["ball_dx"] = -game_state["ball_dx"]

            # Scoring
            if game_state["ball_x"] - BALL_RADIUS <= 0:  # Right player scores
                game_state["right_score"] += 1
                game_state["ball_x"], game_state["ball_y"] = WIDTH // 2, HEIGHT // 2
                game_state["ball_dx"] = random.choice([-BALL_SPEED, BALL_SPEED])
                game_state["ball_dy"] = random.choice([-BALL_SPEED, BALL_SPEED])
            if game_state["ball_x"] + BALL_RADIUS >= WIDTH:  # Left player scores
                game_state["left_score"] += 1
                game_state["ball_x"], game_state["ball_y"] = WIDTH // 2, HEIGHT // 2
                game_state["ball_dx"] = random.choice([-BALL_SPEED, BALL_SPEED])
                game_state["ball_dy"] = random.choice([-BALL_SPEED, BALL_SPEED])

            # Check for game over
            if game_state["left_score"] >= WINNING_SCORE:
                game_state["game_over"] = True
                game_state["winner"] = "Left Player"
            if game_state["right_score"] >= WINNING_SCORE:
                game_state["game_over"] = True
                game_state["winner"] = "Right Player"

        # Drawing
        screen.fill(BLACK)
        if not game_state["game_over"]:
            # Draw center line
            pygame.draw.line(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
            # Draw paddles
            pygame.draw.rect(screen, GREEN, (0, game_state["left_paddle_y"], PADDLE_WIDTH, PADDLE_HEIGHT))
            pygame.draw.rect(screen, RED, (WIDTH - PADDLE_WIDTH, game_state["right_paddle_y"], PADDLE_WIDTH, PADDLE_HEIGHT))
            # Draw ball
            pygame.draw.circle(screen, WHITE, (game_state["ball_x"], game_state["ball_y"]), BALL_RADIUS)
            # Draw scores
            font = pygame.font.Font(None, 74)
            left_text = font.render(str(game_state["left_score"]), True, WHITE)
            right_text = font.render(str(game_state["right_score"]), True, WHITE)
            screen.blit(left_text, (WIDTH // 4, 20))
            screen.blit(right_text, (3 * WIDTH // 4, 20))
        else:
            # Display winner
            font = pygame.font.Font(None, 74)
            winner_text = font.render(f"{game_state['winner']} Wins!", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
            restart_text = font.render("Press ESC to Restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()
