import turtle
 
player_a_score = 0
player_b_score = 0
 
window = turtle.Screen()
window.title("Pong Game")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0)
 
# Paddles
left_paddle = turtle.Turtle()
left_paddle.speed(0)
left_paddle.shape("square")
left_paddle.color("white")
left_paddle.shapesize(stretch_wid=5, stretch_len=1)
left_paddle.penup()
left_paddle.goto(-350, 0)
 
right_paddle = turtle.Turtle()
right_paddle.speed(0)
right_paddle.shape("square")
right_paddle.color("white")
right_paddle.shapesize(stretch_wid=5, stretch_len=1)
right_paddle.penup()
right_paddle.goto(350, 0)
 
# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball_dx = 0.15
ball_dy = 0.15
 
# Score display
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)
score_pen.write(f"Player A: {player_a_score}  |  Player B: {player_b_score}",
    align="center", font=("Arial", 24, "normal"))
 
def left_paddle_up():
    y = left_paddle.ycor()
    if y < 250: left_paddle.sety(y + 20)
 
def left_paddle_down():
    y = left_paddle.ycor()
    if y > -250: left_paddle.sety(y - 20)
 
def right_paddle_up():
    y = right_paddle.ycor()
    if y < 250: right_paddle.sety(y + 20)
 
def right_paddle_down():
    y = right_paddle.ycor()
    if y > -250: right_paddle.sety(y - 20)
 
window.listen()
window.onkeypress(left_paddle_up, "w")
window.onkeypress(left_paddle_down, "s")
window.onkeypress(right_paddle_up, "Up")
window.onkeypress(right_paddle_down, "Down")
 
while True:
    window.update()
    ball.setx(ball.xcor() + ball_dx)
    ball.sety(ball.ycor() + ball_dy)
 
    if ball.ycor() > 290:
        ball.sety(290)
        ball_dy *= -1
    if ball.ycor() < -290:
        ball.sety(-290)
        ball_dy *= -1
 
    if ball.xcor() > 390:
        ball.goto(0, 0)
        ball_dx *= -1
        player_a_score += 1
        score_pen.clear()
        score_pen.write(f"Player A: {player_a_score}  |  Player B: {player_b_score}",
            align="center", font=("Arial", 24, "normal"))
 
    if ball.xcor() < -390:
        ball.goto(0, 0)
        ball_dx *= -1
        player_b_score += 1
        score_pen.clear()
        score_pen.write(f"Player A: {player_a_score}  |  Player B: {player_b_score}",
            align="center", font=("Arial", 24, "normal"))
 
    if (340 < ball.xcor() < 350 and
            right_paddle.ycor() - 50 < ball.ycor() < right_paddle.ycor() + 50):
        ball.setx(340)
        ball_dx *= -1
 
    if (-350 < ball.xcor() < -340 and
            left_paddle.ycor() - 50 < ball.ycor() < left_paddle.ycor() + 50):
        ball.setx(-340)
        ball_dx *= -1
