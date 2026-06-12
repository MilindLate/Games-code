import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
pygame.font.init()

# --- CONSTANTS & CONFIG ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Palette (Neon / Cyberpunk Space Theme)
COLOR_BG = (10, 10, 25)
COLOR_SHIP = (0, 255, 204)      # Cyan
COLOR_LASER = (255, 0, 128)     # Neon Pink
COLOR_ENEMY = (255, 102, 0)     # Neon Orange
COLOR_TEXT = (240, 240, 255)
COLOR_UI_BAR = (40, 40, 80)

# --- GAME OBJECTS ---

class Player:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 80
        self.speed = 6
        self.vx = 0  # Velocity X for smooth movement inertia
        self.friction = 0.85
        self.max_health = 100
        self.health = 100
        self.laser_cooldown = 0
        self.cooldown_max = 15 # Frames between shots

    def move(self, keys):
        # Smooth horizontal movement using inertia
        moved = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
            moved = True
            
        if not moved:
            self.vx *= self.friction # Decelerate smoothly

        self.x += self.vx
        
        # Clamp to screen boundaries
        if self.x < 0:
            self.x = 0
            self.vx = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            self.vx = 0

        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

    def draw(self, surface):
        # Draw a sleek, modern fighter triangle with a neon glow effect
        points = [
            (self.x + self.width // 2, self.y),  # Nose
            (self.x, self.y + self.height),      # Bottom Left
            (self.x + self.width, self.y + self.height) # Bottom Right
        ]
        # Glow layer
        pygame.draw.polygon(surface, (0, 100, 100), points, 6)
        # Main body
        pygame.draw.polygon(surface, COLOR_SHIP, points)
        # Thruster core
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x + self.width//2), int(self.y + self.height)), 4)


class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 15
        self.speed = 10

    def update(self):
        self.y -= self.speed

    def draw(self, surface):
        # Neon laser strip
        pygame.draw.rect(surface, (255, 150, 200), (self.x - 2, self.y, self.w + 4, self.h))
        pygame.draw.rect(surface, COLOR_LASER, (self.x, self.y, self.w, self.h))


class Enemy:
    def __init__(self):
        self.width = random.randint(30, 50)
        self.height = self.width
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(-150, -50)
        # Random speed variations for a dynamic feel
        self.speed = random.uniform(2.0, 4.5)
        self.hp = 1 if self.width < 40 else 2
        self.points = 10 if self.hp == 1 else 25

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        # Hexagonal / Diamond structure for alien vibe
        cx, cy = self.x + self.width//2, self.y + self.height//2
        r = self.width // 2
        points = [
            (cx, cy - r),
            (cx + r, cy - r//3),
            (cx + r//2, cy + r),
            (cx - r//2, cy + r),
            (cx - r, cy - r//3)
        ]
        pygame.draw.polygon(surface, (150, 50, 0), points, 4)
        pygame.draw.polygon(surface, COLOR_ENEMY, points)


class Particle:
    """ Used for crisp juicy explosion effects """
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 6)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(15, 30)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = min(255, self.life * 10)
            color_with_alpha = self.color + (alpha,)
            # Pygame circles don't natively support alpha without a surface, so we draw small rects
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), 3, 3))


# --- MAIN GAME ENGINE ---

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Worries")
        self.clock = pygame.time.Clock()
        
        # UI Fonts
        self.font_main = pygame.font.SysFont("Impact", 24)
        self.font_title = pygame.font.SysFont("Impact", 64)
        self.font_sub = pygame.font.SysFont("Arial", 18, bold=True)
        
        self.state = "START" # START, PLAYING, GAMEOVER
        self.reset_game()
        
        # Background: Parallax Starfield Layer
        self.stars_far = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)] for _ in range(40)]
        self.stars_near = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)] for _ in range(25)]

    def reset_game(self):
        self.player = Player()
        self.lasers = []
        self.enemies = []
        self.particles = []
        self.score = 0
        self.spawn_timer = 0
        self.screen_shake = 0

    def spawn_particles(self, x, y, color, count=15):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == "START" and event.key == pygame.K_SPACE:
                    self.state = "PLAYING"
                elif self.state == "GAMEOVER" and event.key == pygame.K_SPACE:
                    self.reset_game()
                    self.state = "PLAYING"

    def update(self):
        if self.state != "PLAYING":
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys)

        # Shoot mechanism (Hold SPACE or tap)
        if keys[pygame.K_SPACE] and self.player.laser_cooldown == 0:
            # Dual wingtip lasers
            self.lasers.append(Laser(self.player.x, self.player.y + 10))
            self.lasers.append(Laser(self.player.x + self.player.width, self.player.y + 10))
            self.player.laser_cooldown = self.player.cooldown_max

        # Update Stars (Background Parallax Velocity)
        for star in self.stars_far:
            star[1] += 0.5
            if star[1] > SCREEN_HEIGHT: star[1] = 0; star[0] = random.randint(0, SCREEN_WIDTH)
        for star in self.stars_near:
            star[1] += 1.5
            if star[1] > SCREEN_HEIGHT: star[1] = 0; star[0] = random.randint(0, SCREEN_WIDTH)

        # Update Lasers
        for laser in self.lasers[:]:
            laser.update()
            if laser.y < -20:
                self.lasers.remove(laser)

        # Enemy Spawning Management (Gets faster as score scales up)
        self.spawn_timer += 1
        spawn_rate = max(20, 50 - (self.score // 100) * 5)
        if self.spawn_timer >= spawn_rate:
            self.enemies.append(Enemy())
            self.spawn_timer = 0

        # Update Enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Reached Bottom (Player Missed)
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.player.health -= 15  # Penalty to shields
                self.screen_shake = 10
                if self.player.health <= 0:
                    self.state = "GAMEOVER"

            # Collision: Player Ship vs Enemy
            player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            if player_rect.colliderect(enemy_rect):
                self.spawn_particles(enemy.x + enemy.width//2, enemy.y + enemy.height//2, COLOR_ENEMY, 20)
                self.enemies.remove(enemy)
                self.player.health -= 25
                self.screen_shake = 15
                if self.player.health <= 0:
                    self.state = "GAMEOVER"

        # Collisions: Lasers vs Enemies
        for laser in self.lasers[:]:
            laser_rect = pygame.Rect(laser.x, laser.y, laser.w, laser.h)
            for enemy in self.enemies[:]:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if laser_rect.colliderect(enemy_rect):
                    if laser in self.lasers:
                        self.lasers.remove(laser)
                    enemy.hp -= 1
                    if enemy.hp <= 0:
                        self.spawn_particles(enemy.x + enemy.width//2, enemy.y + enemy.height//2, COLOR_ENEMY, 15)
                        self.score += enemy.points
                        self.enemies.remove(enemy)
                        self.screen_shake = 4
                    else:
                        # Direct spark hit indication
                        self.spawn_particles(laser.x, laser.y, (255, 255, 255), 4)

        # Update Particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)

        # Dampen screen shake
        if self.screen_shake > 0:
            self.screen_shake -= 1

    def draw(self):
        # Setup Screen Shake Offset Matrix
        render_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        render_surface.fill(COLOR_BG)

        # 1. Draw Space Background
        for star in self.stars_far:
            pygame.draw.circle(render_surface, (80, 80, 140), star, 1)
        for star in self.stars_near:
            pygame.draw.circle(render_surface, (180, 180, 220), star, 2)

        if self.state == "PLAYING":
            # 2. Draw Entities
            for laser in self.lasers: laser.draw(render_surface)
            for enemy in self.enemies: enemy.draw(render_surface)
            for particle in self.particles: particle.draw(render_surface)
            self.player.draw(render_surface)

            # 3. Micro-interactions / Clean UI Overlay
            # Score Display
            score_txt = self.font_main.render(f"SCORE: {self.score}", True, COLOR_TEXT)
            render_surface.blit(score_txt, (25, 20))
            
            # Health / Shield Bar Container
            pygame.draw.rect(render_surface, COLOR_UI_BAR, (SCREEN_WIDTH - 225, 25, 200, 16), border_radius=4)
            # Health fill with danger warning color shift
            health_color = (0, 255, 150) if self.player.health > 40 else (255, 50, 50)
            health_w = int(200 * (max(0, self.player.health) / self.player.max_health))
            if health_w > 0:
                pygame.draw.rect(render_surface, health_color, (SCREEN_WIDTH - 225, 25, health_w, 16), border_radius=4)
            
            shield_lbl = self.font_sub.render("SHIELDS", True, (120, 120, 160))
            render_surface.blit(shield_lbl, (SCREEN_WIDTH - 225, 5))

        elif self.state == "START":
            # Clean Typographic Title Card
            title = self.font_title.render("SPACE WORRIES", True, COLOR_SHIP)
            subtitle = self.font_sub.render("PRESS [ SPACE ] TO DEPLOY DEFENSES", True, COLOR_LASER)
            controls = self.font_sub.render("A/D or LEFT/RIGHT Arrow keys to Glide. SPACE to fire.", True, COLOR_TEXT)
            
            render_surface.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, SCREEN_HEIGHT//3))
            render_surface.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, SCREEN_HEIGHT//2))
            render_surface.blit(controls, (SCREEN_WIDTH//2 - controls.get_width()//2, SCREEN_HEIGHT//2 + 60))

        elif self.state == "GAMEOVER":
            # Game Over Screen UI
            go_title = self.font_title.render("SYSTEM CRASHED", True, (255, 50, 50))
            go_score = self.font_main.render(f"FINAL SCORE: {self.score}", True, COLOR_TEXT)
            go_sub = self.font_sub.render("PRESS [ SPACE ] TO REBOOT CORE", True, COLOR_SHIP)
            
            render_surface.blit(go_title, (SCREEN_WIDTH//2 - go_title.get_width()//2, SCREEN_HEIGHT//3))
            render_surface.blit(go_score, (SCREEN_WIDTH//2 - go_score.get_width()//2, SCREEN_HEIGHT//2))
            render_surface.blit(go_sub, (SCREEN_WIDTH//2 - go_sub.get_width()//2, SCREEN_HEIGHT//2 + 60))

        # Apply Screen Shake Transformation if triggered
        offset_x = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        offset_y = random.randint(-self.screen_shake, self.screen_shake) if self.screen_shake > 0 else 0
        
        self.screen.blit(render_surface, (offset_x, offset_y))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()