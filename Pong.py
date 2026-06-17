import turtle
import random
import time

# --- CONSTANTS & DESIGN CONFIG ---
WIDTH, HEIGHT = 800, 600
COLOR_BG = "#111424"          # Deep Cyberpunk Navy
COLOR_PADDLE_A = "#00FFCC"    # Cyan
COLOR_PADDLE_B = "#FF007F"    # Neon Pink
COLOR_BALL = "#FFFF00"        # Electric Yellow
COLOR_TEXT = "#F0F0FF"
MAX_SCORE = 5

# Game Variables
player_a_score = 0
player_b_score = 0
game_state = "START"          # START, PLAYING, GAMEOVER
vs_ai = True                  # Set to True for Solo AI mode, False for local 2-player

# --- WINDOW SETUP ---
window = turtle.Screen()
window.title("⚡ PONG: OVERDRIVE ⚡")
window.bgcolor(COLOR_BG)
window.setup(width=WIDTH, height=HEIGHT)
window.tracer(0)

# --- GAME OBJECTS ---

# Left Paddle (Player A)
left_paddle = turtle.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color(COLOR_PADDLE_A)
left_paddle.shapesize(stretch_wid=5, stretch_len=1.2)
left_paddle.penup()
left_paddle.goto(-350, 0)

# Right Paddle (Player B / AI)
right_paddle = turtle.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color(COLOR_PADDLE_B)
right_paddle.shapesize(stretch_wid=5, stretch_len=1.2)
right_paddle.penup()
right_paddle.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color(COLOR_BALL)
ball.penup()
ball.goto(0, 0)
ball_base_speed = 4
ball_dx = ball_base_speed
ball_dy = random.choice([-2, -1, 1, 2])

# UI / Text Pen
ui_pen = turtle.Turtle()
ui_pen.speed(0)
ui_pen.color(COLOR_TEXT)
ui_pen.penup()
ui_pen.hideturtle()

# Particles container for visual trails
particles = []

# --- VFX FUNCTIONS ---

def create_flash(color):
    """Flashes the background temporarily on a critical hit/score event"""
    window.bgcolor(color)
    window.update()
    time.sleep(0.05)
    window.bgcolor(COLOR_BG)

def leave_particle_trail():
    """Leaves a fading kinetic particle trail behind the high-velocity ball"""
    if random.random() > 0.4:  # Optimize rendering load
        p = turtle.Turtle()
        p.speed(0)
        p.shape("circle")
        p.shapesize(0.3, 0.3)
        p.color("#444970")
        p.penup()
        p.goto(ball.xcor(), ball.ycor())
        particles.append((p, 8)) # Turtle object and life points

def update_particles():
    """Manages lifecycle decay of on-screen elements"""
    for item in particles[:]:
        p, life = item
        idx = particles.index(item)
        life -= 1
        if life <= 0:
            p.hideturtle()
            p.clear()
            particles.remove(item)
        else:
            particles[idx] = (p, life)

# --- CONTROLS & LOGIC ---

def left_up():
    if game_state == "PLAYING" and left_paddle.ycor() < 240:
        left_paddle.sety(left_paddle.ycor() + 30)

def left_down():
    if game_state == "PLAYING" and left_paddle.ycor() > -240:
        left_paddle.sety(left_paddle.ycor() - 30)

def right_up():
    if game_state == "PLAYING" and not vs_ai and right_paddle.ycor() < 240:
        right_paddle.sety(right_paddle.ycor() + 30)

def right_down():
    if game_state == "PLAYING" and not vs_ai and right_paddle.ycor() > -240:
        right_paddle.sety(right_paddle.ycor() - 30)

def start_game():
    global game_state, player_a_score, player_b_score
    if game_state in ["START", "GAMEOVER"]:
        player_a_score = 0
        player_b_score = 0
        game_state = "PLAYING"
        reset_ball()

def toggle_mode():
    global vs_ai
    if game_state == "START":
        vs_ai = not vs_ai
        draw_ui()

def reset_ball():
    global ball_dx, ball_dy
    ball.goto(0, 0)
    ball_dx = ball_base_speed if random.choice([True, False]) else -ball_base_speed
    ball_dy = random.uniform(-2, 2)

def handle_ai():
    """Advanced predictive lagging AI behavior matrix"""
    if vs_ai and game_state == "PLAYING":
        # Introduce a slight reaction delay threshold by checking x coordinate
        if ball.xcor() > -100:
            # Follow ball with customized structural tracking speed limits
            if right_paddle.ycor() < ball.ycor() - 15:
                right_paddle.sety(right_paddle.ycor() + 3.5)
            elif right_paddle.ycor() > ball.ycor() + 15:
                right_paddle.sety(right_paddle.ycor() - 3.5)

# --- RENDER/UI DRAW PIPELINE ---

def draw_ui():
    ui_pen.clear()
    
    if game_state == "START":
        ui_pen.goto(0, 100)
        ui_pen.write("PONG: OVERDRIVE", align="center", font=("Impact", 44, "normal"))
        ui_pen.goto(0, 20)
        mode_str = "SOLO VS AI" if vs_ai else "LOCAL 2 PLAYER"
        ui_pen.write(f"MODE: {mode_str} (Press 'M' to Toggle)", align="center", font=("Arial", 16, "bold"))
        ui_pen.goto(0, -60)
        ui_pen.write("Press [SPACEBAR] to Launch Match", align="center", font=("Arial", 14, "italic"))
        ui_pen.goto(0, -140)
        ui_pen.write("Controls: Player A [ W / S ]  |  Player B [ Arrow Up / Down ]", align="center", font=("Arial", 12, "normal"))
        
    elif game_state == "PLAYING":
        # Modern split scoreboard design
        ui_pen.goto(-150, 220)
        ui_pen.write(f"{player_a_score}", align="center", font=("Impact", 48, "normal"))
        ui_pen.goto(150, 220)
        ui_pen.write(f"{player_b_score}", align="center", font=("Impact", 48, "normal"))
        
        # Center court structural net line
        ui_pen.setheading(270)
        ui_pen.goto(0, 280)
        for _ in range(15):
            ui_pen.pendown()
            ui_pen.forward(20)
            ui_pen.penup()
            ui_pen.forward(15)
            
    elif game_state == "GAMEOVER":
        winner = "PLAYER A" if player_a_score >= MAX_SCORE else ("BOT AI" if vs_ai else "PLAYER B")
        ui_pen.goto(0, 50)
        ui_pen.write(f"{winner} WINS!", align="center", font=("Impact", 44, "normal"))
        ui_pen.goto(0, -20)
        ui_pen.write("Press [SPACEBAR] to Restart System", align="center", font=("Arial", 16, "bold"))

# --- INPUT BINDINGS ---
window.listen()
window.onkeypress(left_up, "w")
window.onkeypress(left_up, "W")
window.onkeypress(left_down, "s")
window.onkeypress(left_down, "S")
window.onkeypress(right_up, "Up")
window.onkeypress(right_down, "Down")
window.onkeypress(start_game, "space")
window.onkeypress(toggle_mode, "m")
window.onkeypress(toggle_mode, "M")

# Initialize display
draw_ui()

# --- MAIN GAME LOOP ---
while True:
    window.update()
    
    if game_state == "PLAYING":
        leave_particle_trail()
        update_particles()
        
        # Move ball natively relative to direction frame vectors
        ball.setx(ball.xcor() + ball_dx)
        ball.sety(ball.ycor() + ball_dy)
        
        handle_ai()

        # Ceiling and Floor Collision Matrix
        if ball.ycor() > 285:
            ball.sety(285)
            ball_dy *= -1
        elif ball.ycor() < -285:
            ball.sety(-285)
            ball_dy *= -1

        # Point Scoring (Right boundary exit)
        if ball.xcor() > 390:
            player_a_score += 1
            create_flash("#005544")
            if player_a_score >= MAX_SCORE:
                game_state = "GAMEOVER"
            reset_ball()
            draw_ui()

        # Point Scoring (Left boundary exit)
        elif ball.xcor() < -390:
            player_b_score += 1
            create_flash("#550022")
            if player_b_score >= MAX_SCORE:
                game_state = "GAMEOVER"
            reset_ball()
            draw_ui()

        # --- DYNAMIC CONTROLLER COLLISION PHYSICS ---
        
        # Right Paddle Interaction Matrix
        if 330 < ball.xcor() < 350 and (right_paddle.ycor() - 60 < ball.ycor() < right_paddle.ycor() + 60):
            ball.setx(330)
            
            # Vector manipulation based on hit location offset (adds bounce angle variety)
            hit_offset = ball.ycor() - right_paddle.ycor()
            ball_dy = hit_offset * 0.12
            
            # Invert direction and apply velocity compound scaling acceleration
            ball_dx = -(abs(ball_dx) + 0.4) 

        # Left Paddle Interaction Matrix
        elif -350 < ball.xcor() < -330 and (left_paddle.ycor() - 60 < ball.ycor() < left_paddle.ycor() + 60):
            ball.setx(-330)
            
            hit_offset = ball.ycor() - left_paddle.ycor()
            ball_dy = hit_offset * 0.12
            
            ball_dx = (abs(ball_dx) + 0.4)
            
    else:
        # Passive update processing for trails when waiting on screens
        update_particles()