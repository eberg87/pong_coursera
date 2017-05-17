# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [2, 2]
ball_dir = RIGHT
score1 = 0
score2 = 0
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = 150
paddle2_pos = 150

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    
    if direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 3)
    if direction == LEFT:
        ball_vel[0] = - random.randrange(2, 4)
        ball_vel[1] = - random.randrange(1, 3)

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    # vertical position
    if ball_pos[1] >= HEIGHT - BALL_RADIUS or ball_pos[1] <= 0 + BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # score
    if ball_pos[0] >= WIDTH - BALL_RADIUS:
        spawn_ball(LEFT)
        score1 += 1
    elif ball_pos[0] <= 0 + BALL_RADIUS:
        spawn_ball (RIGHT)
        score2 += 1
       
    #print ball_vel[0], ball_vel[1], ball_pos[0], ball_pos[1]
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle([ball_pos[0], ball_pos[1]], BALL_RADIUS, 1, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos < 0:
        paddle1_pos = 0
    elif paddle1_pos > HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT
    elif paddle1_pos >= 0 and paddle1_pos <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel

    if paddle2_pos < 0:
        paddle2_pos = 0
    elif paddle2_pos > HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT
    elif paddle2_pos >= 0 and paddle2_pos <= HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    # paddle 1
    canvas.draw_polygon([(0, paddle1_pos), (0, paddle1_pos + PAD_HEIGHT), (0 + PAD_WIDTH, paddle1_pos + PAD_HEIGHT), (0 + PAD_WIDTH, paddle1_pos)], 1, "White", "White")

    #paddle 2
    canvas.draw_polygon([(WIDTH, paddle2_pos), (WIDTH, paddle2_pos + PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos)], 1, "White", "White")
    
    # determine whether paddle and ball collide
    # paddle 1
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] += 1
    
    # paddle 2
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS and ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
        ball_vel[0] = - ball_vel[0]
        ball_vel[0] -= 1
    
    # draw scores
    scr1 = str(score1)
    scr2 = str(score2)
    canvas.draw_text(scr1, (220, 80), 40, 'Grey')
    canvas.draw_text(scr2, (350, 80), 40, 'Grey')

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['W']:
        paddle1_vel = -10
    if key == simplegui.KEY_MAP['s'] or key == simplegui.KEY_MAP['S']:
        paddle1_vel = 10
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -10
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 10
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
label0 = frame.add_label('PONG')
label00 = frame.add_label('')
label1 = frame.add_label('CONTROLS')
label2 = frame.add_label('')
label3 = frame.add_label('PLAYER 1')
label4 = frame.add_label('Use W and S keys to move paddle up and down')
label5 = frame.add_label('-----------')
label6 = frame.add_label('PLAYER 2')
label7 = frame.add_label('Use UP and DOWN arrow keys to move paddle up and down')

# start frame
new_game()
frame.start()
