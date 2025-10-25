import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
MISSILE_WIDTH, MISSILE_HEIGHT = 30, 15
PLAYER_SPEED = 5
BULLET_SPEED = 10
MISSILE_SPEED = 7
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 15, 50  # Reduced size of obstacles
OBSTACLE_SPEED = 3
FPS = 60
MAX_MISSILES = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2-Player Shooting Game with Multiple Obstacles and Guns")

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Initialize variables
player1 = pygame.Rect(50, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
player2 = pygame.Rect(WIDTH - 50 - PLAYER_WIDTH, HEIGHT // 2 - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
player1_score = 0
player2_score = 0
bullets = []
missiles = []
WINNING_SCORE = None

# Obstacle list
obstacles = [pygame.Rect(WIDTH // 3, HEIGHT // 4, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
             pygame.Rect(WIDTH // 2, HEIGHT // 2, OBSTACLE_WIDTH, OBSTACLE_HEIGHT),
             pygame.Rect(WIDTH * 2 // 3, HEIGHT * 3 // 4, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)]
obstacle_directions = [1, -1, 1]  # Directions for each obstacle (up or down)

# Gun states
player1_missiles = MAX_MISSILES
player2_missiles = MAX_MISSILES

# Reset game
def reset_game():
    global player1_score, player2_score, bullets, missiles, player1_missiles, player2_missiles
    player1_score, player2_score = 0, 0
    bullets.clear()
    missiles.clear()
    player1_missiles = MAX_MISSILES
    player2_missiles = MAX_MISSILES

# Winning screen
def display_winning_screen(winner):
    while True:
        screen.fill(BLACK)
        winner_text = font.render(f"{winner} Wins!", True, YELLOW)
        restart_text = small_font.render("Press ESC to Restart or Q to Quit", True, WHITE)

        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 3))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "restart"
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Setup screen for winning score
def setup_winning_score():
    input_text = ""
    while True:
        screen.fill(BLACK)

        title_text = font.render("Set Winning Score", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        input_surface = font.render(input_text, True, YELLOW)
        screen.blit(input_surface, (WIDTH // 2 - input_surface.get_width() // 2, HEIGHT // 2))

        instruction_text = small_font.render("Press ENTER to confirm", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text.isdigit():
                    return int(input_text)
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.unicode.isdigit():
                    input_text += event.unicode

# Instructions screen
def display_instructions():
    while True:
        screen.fill(BLACK)

        title_text = font.render("Instructions", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))

        instruction_lines = [
            "Player 1: Use W/S to move, F to fire bullets, R for missiles.",
            "Player 2: Use Arrow Keys to move, / to fire bullets, M for missiles.",
            "Hit each other with bullets or missiles to score.",
            "Each player has 3 missiles, use them wisely.",
            "Obstacles not effects Missiles .",
            "Avoid obstacles that move up and down.",
            "Press Enter to start the game!"
        ]

        for i, line in enumerate(instruction_lines):
            text = small_font.render(line, True, WHITE)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Start the game after pressing Enter

# Main game loop
clock = pygame.time.Clock()
running = True

# Prompt for winning score
WINNING_SCORE = setup_winning_score()

# Display instructions screen after setting winning score
display_instructions()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Player 1 fires bullets (f key)
            if event.key == pygame.K_f:
                bullet_rect = pygame.Rect(player1.right, player1.centery - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append({'rect': bullet_rect, 'direction': 1, 'owner': 1})
            # Player 1 fires missiles (r key)
            if event.key == pygame.K_r and player1_missiles > 0:
                missile_rect = pygame.Rect(player1.right, player1.centery - MISSILE_HEIGHT // 2, MISSILE_WIDTH, MISSILE_HEIGHT)
                missiles.append({'rect': missile_rect, 'direction': 1, 'owner': 1})
                player1_missiles -= 1

            # Player 2 fires bullets (slash key)
            if event.key == pygame.K_SLASH:
                bullet_rect = pygame.Rect(player2.left - BULLET_WIDTH, player2.centery - BULLET_HEIGHT // 2, BULLET_WIDTH, BULLET_HEIGHT)
                bullets.append({'rect': bullet_rect, 'direction': -1, 'owner': 2})
            # Player 2 fires missiles (m key)
            if event.key == pygame.K_m and player2_missiles > 0:
                missile_rect = pygame.Rect(player2.left - MISSILE_WIDTH, player2.centery - MISSILE_HEIGHT // 2, MISSILE_WIDTH, MISSILE_HEIGHT)
                missiles.append({'rect': missile_rect, 'direction': -1, 'owner': 2})
                player2_missiles -= 1

    # Player movement
    keys = pygame.key.get_pressed()
    # Player 1 movement (W, S)
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= PLAYER_SPEED
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += PLAYER_SPEED
    # Player 2 movement (UP, DOWN)
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += PLAYER_SPEED

    # Move bullets
    for bullet in bullets[:]:
        bullet['rect'].x += bullet['direction'] * BULLET_SPEED

        # Check if bullet collides with any obstacle
        for obstacle in obstacles:
            if bullet['rect'].colliderect(obstacle):
                bullets.remove(bullet)
                break  # Stop checking other obstacles if the bullet hits one

        # Check collision with players
        if bullet['owner'] == 1 and player2.colliderect(bullet['rect']):
            player1_score += 1
            bullets.remove(bullet)
        elif bullet['owner'] == 2 and player1.colliderect(bullet['rect']):
            player2_score += 1
            bullets.remove(bullet)

        # Remove bullets that go off screen
        if bullet['rect'].x < 0 or bullet['rect'].x > WIDTH:
            bullets.remove(bullet)

    # Move missiles and check collision
    for missile in missiles[:]:
        missile['rect'].x += missile['direction'] * MISSILE_SPEED

        # Check missile hit
        if missile['owner'] == 1 and player2.colliderect(missile['rect']):
            player1_score += WINNING_SCORE // 3
            missiles.remove(missile)
        elif missile['owner'] == 2 and player1.colliderect(missile['rect']):
            player2_score += WINNING_SCORE // 3
            missiles.remove(missile)

        # Remove missiles that go off screen
        if missile['rect'].x < 0 or missile['rect'].x > WIDTH:
            missiles.remove(missile)

    # Move obstacles
    for i, obstacle in enumerate(obstacles):
        obstacle.y += obstacle_directions[i] * OBSTACLE_SPEED
        if obstacle.top <= 0 or obstacle.bottom >= HEIGHT:
            obstacle_directions[i] *= -1

    # Check for winning condition
    if player1_score >= WINNING_SCORE:
        result = display_winning_screen("Player 1")
        if result == "restart":
            WINNING_SCORE = setup_winning_score()
            reset_game()
    if player2_score >= WINNING_SCORE:
        result = display_winning_screen("Player 2")
        if result == "restart":
            WINNING_SCORE = setup_winning_score()
            reset_game()

    # Drawing
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)

    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet['rect'])

    for missile in missiles:
        pygame.draw.rect(screen, GREEN, missile['rect'])

    for obstacle in obstacles:
        pygame.draw.rect(screen, GRAY, obstacle)

    score_text = font.render(f"{player1_score} - {player2_score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    missile_text1 = small_font.render(f"Missiles: {player1_missiles}", True, RED)
    missile_text2 = small_font.render(f"Missiles: {player2_missiles}", True, BLUE)
    screen.blit(missile_text1, (20, 20))
    screen.blit(missile_text2, (WIDTH - missile_text2.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

