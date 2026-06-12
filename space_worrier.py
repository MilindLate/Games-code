import pygame
import sys
import random
import math

# --- INITIALIZATION ---
pygame.init()
pygame.font.init()

# --- CONSTANTS & DESIGN SYSTEM ---
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
TARGET_FPS = 60

# Cyberpunk Palette
COLOR_BG = (6, 5, 16)
COLOR_SHIP = (0, 255, 204)
COLOR_LASER = (255, 0, 128)
COLOR_ENEMY = (255, 110, 0)
COLOR_SCRAP = (255, 215, 0)
COLOR_UI_PANEL = (20, 20, 35)
COLOR_TEXT = (240, 240, 255)
COLOR_MUTED = (110, 110, 140)

# --- GLOBAL UTILITIES & MANAGERS ---

class FontManager:
    def __init__(self):
        # Fallbacks to default system fonts if specific ones aren't found
        self.title = pygame.font.SysFont("Impact", 60)
        self.header = pygame.font.SysFont("Impact", 28)
        self.body = pygame.font.SysFont("Arial", 16, bold=True)
        self.ui = pygame.font.SysFont("Consolas", 14)

class VFXManager:
    """Handles visual feedback systems without cluttering the main loop"""
    def __init__(self):
        self.particles = []
        self.texts = []
        self.screen_shake = 0

    def spawn_burst(self, x, y, color, count=12):
        for _ in range(count):
            self.particles.append({
                "x": x, "y": y,
                "vx": random.uniform(-4, 4), "vy": random.uniform(-4, 4),
                "life": random.randint(20, 40), "color": color
            })

    def spawn_text(self, x, y, text, color):
        self.texts.append({"x": x, "y": y, "text": text, "color": color, "life": 40})

    def shake(self, amount):
        self.screen_shake = max(self.screen_shake, amount)

    def update(self, dt):
        if self.screen_shake > 0:
            self.screen_shake -= 8 * dt
        
        # Update particles
        for p in self.particles[:]:
            p["x"] += p["vx"] * dt * 60
            p["y"] += p["vy"] * dt * 60
            p["life"] -= 1
            if p["life"] <= 0:
                self.particles.remove(p)

        # Update floating texts
        for t in self.texts[:]:
            t["y"] -= 1.5 * dt * 60  # Float upwards
            t["life"] -= 1
            if t["life"] <= 0:
                self.texts.remove(t)

    def draw(self, surface):
        for p in self.particles:
            alpha = min(255, p["life"] * 8)
            # Fade colors gracefully
            c = p["color"]
            pygame.draw.rect(surface, (max(0, c[0]-50), max(0, c[1]-50), max(0, c[2]-50)), (int(p["x"]), int(p["y"]), 4, 4))
        
        for t in self.texts:
            font = pygame.font.SysFont("Impact", 20)
            txt_surf = font.render(t["text"], True, t["color"])
            surface.blit(txt_surf, (int(t["x"]), int(t["y"])))


# --- ENTITIES ---

class PlayerShip:
    def __init__(self):
        self.width, self.height = 46, 46
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.vx = 0
        self.friction = 0.82

        # Upgradable Meta Statistics
        self.stats = {"speed": 1, "fire_rate": 1, "max_shields": 1}
        self.shields = 100
        self.laser_cooldown = 0

    def get_max_shields(self): return 100 + (self.stats["max_shields"] - 1) * 25
    def get_speed(self): return 6 + (self.stats["speed"] - 1) * 1.5
    def get_cooldown_max(self): return max(6, 16 - (self.stats["fire_rate"] - 1) * 2)

    def reset_health(self):
        self.shields = self.get_max_shields()

    def move(self, keys, dt):
        move_speed = self.get_speed()
        moved = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -move_speed
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = move_speed
            moved = True

        if not moved:
            self.vx *= self.friction

        self.x += self.vx * dt * 60
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))

        if self.laser_cooldown > 0:
            self.laser_cooldown -= 60 * dt

    def draw(self, surface):
        # Animated engine flame trail
        flame_h = random.randint(8, 20)
        pygame.draw.polygon(surface, (255, 100, 0), [
            (self.x + self.width//2, self.y + self.height + flame_h),
            (self.x + self.width//2 - 8, self.y + self.height),
            (self.x + self.width//2 + 8, self.y + self.height)
        ])
        # Kinetic Poly Hull Design
        points = [(self.x + self.width//2, self.y), (self.x, self.y + self.height), (self.x + self.width, self.y + self.height)]
        pygame.draw.polygon(surface, COLOR_SHIP, points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)


class EliteEnemy:
    def __init__(self, target_score):
        self.width = random.randint(35, 60)
        self.height = self.width
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -60
        
        # Scale dynamic difficulty based on current score run
        speed_modifier = min(3.0, (target_score / 300))
        self.speed = random.uniform(2.0, 4.0) + speed_modifier
        self.max_hp = 1 if self.width < 45 else 3
        self.hp = self.max_hp

    def update(self, dt):
        self.y += self.speed * dt * 60

    def draw(self, surface):
        cx, cy = self.x + self.width//2, self.y + self.height//2
        r = self.width // 2
        # Armored Hex shape outline
        pts = [(cx, cy-r), (cx+r, cy-r//2), (cx+r, cy+r//2), (cx, cy+r), (cx-r, cy+r//2), (cx-r, cy-r//2)]
        pygame.draw.polygon(surface, COLOR_ENEMY, pts)
        pygame.draw.polygon(surface, (255,255,255), pts, 1 if self.hp == 1 else 3)


class UpgradeButton:
    def __init__(self, x, y, w, h, stat_key, label, base_cost):
        self.rect = pygame.Rect(x, y, w, h)
        self.stat_key = stat_key
        self.label = label
        self.base_cost = base_cost

    def get_cost(self, current_level):
        return int(self.base_cost * (current_level ** 1.6))

    def draw(self, surface, fonts, player_lv, total_scrap):
        cost = self.get_cost(player_lv)
        can_afford = total_scrap >= cost
        
        # Button container highlights on hover/affordability state
        bg_col = (30, 45, 80) if can_afford else (25, 25, 35)
        border_col = COLOR_SHIP if can_afford else COLOR_MUTED
        
        pygame.draw.rect(surface, bg_col, self.rect, border_radius=6)
        pygame.draw.rect(surface, border_col, self.rect, 2, border_radius=6)
        
        # Texts layout
        lbl_surf = fonts.header.render(f"{self.label} (LV {player_lv})", True, COLOR_TEXT)
        cost_surf = fonts.body.render(f"COST: {cost} SCRAP" if player_lv < 5 else "MAX LEVEL", True, COLOR_SCRAP if player_lv < 5 else COLOR_MUTED)
        
        surface.blit(lbl_surf, (self.rect.x + 15, self.rect.y + 10))
        surface.blit(cost_surf, (self.rect.x + 15, self.rect.y + 40))


# --- GAME MACHINE CONTROLLER ---

class AdvancedGameEngine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Worries: Overdrive Edition")
        self.clock = pygame.time.Clock()
        self.fonts = FontManager()
        self.vfx = VFXManager()
        
        # Game State
        self.state = "START_MENU" # START_MENU, GAMEPLAY, UPGRADE_SHOP, GAME_OVER
        self.scrap_bank = 0      # Meta progression currency
        self.score = 0
        
        self.player = PlayerShip()
        self.lasers = []
        self.enemies = []
        self.spawn_cooldown = 0
        
        # Parallax background setup
        self.stars = [[random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.uniform(0.5, 2.5)] for _ in range(80)]
        
        # Interactive Shop Setup
        self.shop_buttons = [
            UpgradeButton(150, 220, 600, 75, "speed", "ENGINE INERTIA THRUSTERS", 15),
            UpgradeButton(150, 320, 600, 75, "fire_rate", "PLASMA MATRIC COOLDOWN", 25),
            UpgradeButton(150, 420, 600, 75, "max_shields", "DEFLECTIVE SHIELD CAPACITY", 20)
        ]

    def start_new_run(self):
        self.score = 0
        self.lasers.clear()
        self.enemies.clear()
        self.player.reset_health()
        self.state = "GAMEPLAY"

    def process_input(self):
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.state == "START_MENU" and event.key == pygame.K_SPACE:
                    self.start_new_run()
                elif self.state == "GAME_OVER" and event.key == pygame.K_SPACE:
                    self.state = "UPGRADE_SHOP"
                elif self.state == "UPGRADE_SHOP" and event.key == pygame.K_RETURN:
                    self.start_new_run()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == "UPGRADE_SHOP":
                mx, my = pygame.mouse.get_pos()
                for btn in self.shop_buttons:
                    if btn.rect.collidepoint(mx, my):
                        curr_lv = self.player.stats[btn.stat_key]
                        cost = btn.get_cost(curr_lv)
                        if self.scrap_bank >= cost and curr_lv < 5:
                            self.scrap_bank -= cost
                            self.player.stats[btn.stat_key] += 1
                            self.vfx.spawn_burst(mx, my, COLOR_SHIP, count=25)
        return keys

    def update(self, dt):
        # Starfield parallax running in all states
        for star in self.stars:
            star[1] += star[2] * dt * 40
            if star[1] > SCREEN_HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, SCREEN_WIDTH)

        self.vfx.update(dt)

        if self.state != "GAMEPLAY":
            return

        keys = self.process_input()
        self.player.move(keys, dt)

        # Fire Input Handling
        if keys[pygame.K_SPACE] and self.player.laser_cooldown <= 0:
            # Multi-laser alignment offsets
            self.lasers.append(pygame.Rect(self.player.x + 4, self.player.y, 4, 16))
            self.lasers.append(pygame.Rect(self.player.x + self.player.width - 8, self.player.y, 4, 16))
            self.player.laser_cooldown = self.player.get_cooldown_max()

        # Update Lasers
        for laser in self.lasers[:]:
            laser.y -= 12 * dt * 60
            if laser.y < -20: self.lasers.remove(laser)

        # Spawning Rate curves
        self.spawn_cooldown -= 60 * dt
        if self.spawn_cooldown <= 0:
            self.enemies.append(EliteEnemy(self.score))
            self.spawn_cooldown = max(18, 55 - (self.score // 8))

        # Update Enemies & Collisions
        for enemy in self.enemies[:]:
            enemy.update(dt)
            e_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            
            # Reached Bottom Breach
            if enemy.y > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.player.shields -= 20
                self.vfx.shake(12)
                if self.player.shields <= 0: self.state = "GAME_OVER"
                continue

            # Ship vs Enemy Contact Crash
            p_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
            if p_rect.colliderect(e_rect):
                self.vfx.spawn_burst(enemy.x + enemy.width//2, enemy.y + enemy.height//2, COLOR_ENEMY, 25)
                self.enemies.remove(enemy)
                self.player.shields -= 40
                self.vfx.shake(20)
                if self.player.shields <= 0: self.state = "GAME_OVER"
                continue

            # Laser Hit Registrations
            for laser in self.lasers[:]:
                if laser.colliderect(e_rect):
                    if laser in self.lasers: self.lasers.remove(laser)
                    enemy.hp -= 1
                    self.vfx.spawn_burst(laser.x, laser.y, (255,255,255), 4)
                    
                    if enemy.hp <= 0:
                        # Success Reward Generation
                        scrap_gained = random.randint(2, 5)
                        self.scrap_bank += scrap_gained
                        self.score += 10 if enemy.max_hp == 1 else 30
                        
                        self.vfx.spawn_burst(enemy.x+enemy.width//2, enemy.y+enemy.height//2, COLOR_ENEMY, 18)
                        self.vfx.spawn_text(enemy.x, enemy.y, f"+{scrap_gained} SCRAP", COLOR_SCRAP)
                        self.enemies.remove(enemy)
                        break

    def draw(self):
        # Viewport creation container to handle isolated screen-shake transformations
        render_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        render_surface.fill(COLOR_BG)

        # Background Star Layer rendering
        for star in self.stars:
            pygame.draw.circle(render_surface, (140, 140, 200) if star[2] > 1.8 else (60, 60, 100), (int(star[0]), int(star[1])), 1 if star[2] < 1.8 else 2)

        if self.state == "GAMEPLAY":
            # Entities rendering
            for laser in self.lasers: pygame.draw.rect(render_surface, COLOR_LASER, laser, border_radius=2)
            for enemy in self.enemies: enemy.draw(render_surface)
            self.player.draw(render_surface)
            self.vfx.draw(render_surface)

            # Dashboard UI Panels
            score_txt = self.fonts.header.render(f"SCORE: {self.score}", True, COLOR_TEXT)
            scrap_txt = self.fonts.header.render(f"BANK: {self.scrap_bank}⚙", True, COLOR_SCRAP)
            render_surface.blit(score_txt, (30, 20))
            render_surface.blit(scrap_txt, (30, 55))

            # Shield Level Monitor Container
            max_s = self.player.get_max_shields()
            shield_percentage = max(0, self.player.shields) / max_s
            pygame.draw.rect(render_surface, COLOR_UI_PANEL, (SCREEN_WIDTH - 280, 25, 250, 18), border_radius=5)
            pygame.draw.rect(render_surface, COLOR_SHIP if shield_percentage > 0.35 else COLOR_LASER, (SCREEN_WIDTH - 280, 25, int(250 * shield_percentage), 18), border_radius=5)
            s_label = self.fonts.ui.render(f"SYSTEM INTEGRITY: {int(shield_percentage*100)}%", True, COLOR_TEXT)
            render_surface.blit(s_label, (SCREEN_WIDTH - 275, 45))

        elif self.state == "START_MENU":
            t_surf = self.fonts.title.render("SPACE WORRIES: OVERDRIVE", True, COLOR_SHIP)
            st_surf = self.fonts.header.render("PRESS [ SPACEBAR ] TO DEPLOY DEFENDER", True, COLOR_LASER)
            render_surface.blit(t_surf, (SCREEN_WIDTH//2 - t_surf.get_width()//2, SCREEN_HEIGHT//3))
            render_surface.blit(st_surf, (SCREEN_WIDTH//2 - st_surf.get_width()//2, SCREEN_HEIGHT//2))

        elif self.state == "GAME_OVER":
            go_surf = self.fonts.title.render("HULL DESTROYED", True, COLOR_LASER)
            scr_surf = self.fonts.header.render(f"FINAL SCORE GENERATED: {self.score}", True, COLOR_TEXT)
            nxt_surf = self.fonts.body.render("PRESS [ SPACE ] TO ACCESS HYPER-SPACE REPAIR WORKSHOP", True, COLOR_SHIP)
            render_surface.blit(go_surf, (SCREEN_WIDTH//2 - go_surf.get_width()//2, SCREEN_HEIGHT//3))
            render_surface.blit(scr_surf, (SCREEN_WIDTH//2 - scr_surf.get_width()//2, SCREEN_HEIGHT//2))
            render_surface.blit(nxt_surf, (SCREEN_WIDTH//2 - nxt_surf.get_width()//2, SCREEN_HEIGHT//2 + 80))

        elif self.state == "UPGRADE_SHOP":
            sh_surf = self.fonts.title.render("REPAIR & UPGRADE STATION", True, COLOR_SHIP)
            bal_surf = self.fonts.header.render(f"AVAILABLE SCRAP SALVAGE: {self.scrap_bank} UNITS", True, COLOR_SCRAP)
            instruction = self.fonts.body.render("CLICK MODULE TO UPGRADE  •  PRESS [ ENTER ] TO LAUNCH NEXT WAVE", True, COLOR_TEXT)
            render_surface.blit(sh_surf, (SCREEN_WIDTH//2 - sh_surf.get_width()//2, 40))
            render_surface.blit(bal_surf, (SCREEN_WIDTH//2 - bal_surf.get_width()//2, 120))
            render_surface.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, SCREEN_HEIGHT - 70))
            
            for btn in self.shop_buttons:
                btn.draw(render_surface, self.fonts, self.player.stats[btn.stat_key], self.scrap_bank)
            self.vfx.draw(render_surface)

        # Apply Screen Shake Offset Matrix
        sx = random.randint(-int(self.vfx.screen_shake), int(self.vfx.screen_shake)) if self.vfx.screen_shake > 0 else 0
        sy = random.randint(-int(self.vfx.screen_shake), int(self.vfx.screen_shake)) if self.vfx.screen_shake > 0 else 0
        
        self.screen.blit(render_surface, (sx, sy))
        pygame.display.flip()

    def loop(self):
        while True:
            # Enforce rigid framing clock delta tracking
            dt = self.clock.tick(TARGET_FPS) / 1000.0
            # Prevent catastrophic frame drop skips breaking collision matrices
            dt = min(dt, 0.1) 
            
            self.process_input()
            self.update(dt)
            self.draw()

if __name__ == "__main__":
    engine = AdvancedGameEngine()
    engine.loop()