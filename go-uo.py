import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
HELI_WIDTH, HELI_HEIGHT = 60, 40
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
GRAVITY = 0.5
JUMP_STRENGTH = -10
FPS = 60
PLATFORM_FALL_SPEED = 2  # Initial speed of platforms falling
BACKGROUND_COLOR = (0, 0, 0)  # Black background color

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Helicopter Adventure - Falling Obstacles")

# Load default helicopter shape (a simple rectangle here)
helicopter_color = (255, 255, 0)  # Yellow helicopter

# Score and high score
score = 0
high_score = 0
font = pygame.font.SysFont("Arial", 24)

# Helicopter properties
helicopter_x = WIDTH // 2
helicopter_y = HEIGHT // 2
helicopter_velocity_y = 0
is_jumping = False

# Platform properties
platforms = []

# Create platforms
def create_platforms():
    global platforms
    platforms.clear()
    for _ in range(5):  # Create 5 platforms
        plat_x = random.randint(100, WIDTH - 100)
        plat_y = random.randint(-600, -20)  # Start platforms above the screen
        platforms.append(pygame.Rect(plat_x, plat_y, PLATFORM_WIDTH, PLATFORM_HEIGHT))

# Initialize the first set of platforms
create_platforms()

# Function to display the score
def display_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the instructions
def display_instructions():
    instructions_text = font.render("Press SPACE to Start the Game", True, WHITE)
    screen.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT // 3))

    instructions_text2 = font.render("Use LEFT/RIGHT Arrow keys to move.", True, WHITE)
    screen.blit(instructions_text2, (WIDTH // 2 - instructions_text2.get_width() // 2, HEIGHT // 2))

    instructions_text3 = font.render("Press SPACE to Jump.", True, WHITE)
    screen.blit(instructions_text3, (WIDTH // 2 - instructions_text3.get_width() // 2, HEIGHT // 2 + 30))

# Game loop
clock = pygame.time.Clock()
running = True
game_started = False

while running:
    if not game_started:
        # Show instructions screen
        screen.fill(BLACK)
        display_instructions()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True  # Start the game
                if event.key == pygame.K_q:
                    running = False  # Quit the game

    else:
        # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_started = False  # Restart the game
                    score = 0  # Reset the score
                    create_platforms()  # Create new platforms
                if event.key == pygame.K_q:
                    running = False  # Quit the game
                if event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    helicopter_velocity_y = JUMP_STRENGTH

        # Helicopter movement
        if is_jumping:
            helicopter_y += helicopter_velocity_y
            helicopter_velocity_y += GRAVITY
            if helicopter_y >= HEIGHT - HELI_HEIGHT:  # Helicopter hits the ground
                helicopter_y = HEIGHT - HELI_HEIGHT
                is_jumping = False

        # Helicopter horizontal movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            helicopter_x -= 5
        if keys[pygame.K_RIGHT]:
            helicopter_x += 5

        # Prevent helicopter from going out of bounds horizontally
        if helicopter_x < 0:
            helicopter_x = 0  # Keep it at the left edge
        if helicopter_x > WIDTH - HELI_WIDTH:
            helicopter_x = WIDTH - HELI_WIDTH  # Keep it at the right edge

        # Increase platform fall speed based on score
        current_fall_speed = PLATFORM_FALL_SPEED + score // 10  # Increase speed every 10 points

        # Platform falling
        for platform in platforms:
            platform.y += current_fall_speed  # Platforms move down with increasing speed
            if platform.y > HEIGHT:  # If platform goes below the screen, reset
                platform.y = random.randint(-100, -20)
                platform.x = random.randint(100, WIDTH - 100)
                score += 1  # Increase score when platform passes

        # Platform collision detection
        game_over = False
        for platform in platforms:
            if platform.colliderect(pygame.Rect(helicopter_x, helicopter_y, HELI_WIDTH, HELI_HEIGHT)):
                game_over = True
                break

        if game_over:
            if score > high_score:
                high_score = score  # Update high score if the current score is higher
            # Display Game Over screen
            game_over_text = font.render("Game Over", True, WHITE)
            score_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            
            screen.fill(BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
            screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 40))
            pygame.display.flip()

            # Wait for key press to restart or quit
            waiting_for_key = True
            while waiting_for_key:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting_for_key = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game_started = False  # Restart the game
                            score = 0  # Reset the score
                            create_platforms()  # Create new platforms
                            waiting_for_key = False
                        if event.key == pygame.K_q:
                            running = False  # Quit the game
                            waiting_for_key = False

        # Draw everything
        screen.fill(BLACK)

        # Draw helicopter (represented as a simple rectangle here)
        pygame.draw.rect(screen, helicopter_color, (helicopter_x, helicopter_y, HELI_WIDTH, HELI_HEIGHT))

        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, GREEN, platform)

        # Display the score
        display_score()

        pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
