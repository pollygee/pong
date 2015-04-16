# Implementation of classic arcade game Pong

import simplegui
import random
import math

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
pad1_x = 0
pad1_y = 160
pad2_x = 592
pad2_y = 160
paddle1_vel = 0
paddle2_vel = 0


# initialize ball_pos and ball_vel for new bal in middle of table
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [1.5 ,-.5]



# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == 'right':
        vertical_velocity = random.randrange(60, 180) / 60
        horizontal_velocity = random.randrange(120, 240) / 60
        ball_vel = [ horizontal_velocity, - vertical_velocity]
    if direction == 'left':
        vertical_velocity = random.randrange(60, 180) / 60
        horizontal_velocity = random.randrange(120, 240) / 60
        ball_vel = [- horizontal_velocity, - vertical_velocity]
    

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    direction = "right"
    score1 = 0
    score2 = 0
    spawn_ball(direction)
    

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, pad1_y, pad2_y
    
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #Bounce off top and bottom
    if (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    elif (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = - ball_vel[1]
        
    #Spawn a new game if ball falls off the canvas
    if ball_pos[0] < 8 + BALL_RADIUS:
        if((pad1_y + 80) > ball_pos[1] and (ball_pos[1] > pad1_y)):
            ball_vel[0] = -ball_vel[0]
        else:
            score2 += 1
            spawn_ball("right")
        
    #Bounce of the paddle        
    elif (ball_pos[0] > ((WIDTH-8) - BALL_RADIUS)):
        if ((pad2_y +80) > ball_pos[1] and (ball_pos[1] > pad2_y)):
            ball_vel[0] = -ball_vel[0]
        else:
            score1 += 1
            spawn_ball("left")
            
    # draw ball
    c.draw_circle((ball_pos[0], ball_pos[1]), BALL_RADIUS, 2, 'White', 'White')

    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos = [(pad1_x, pad1_y), (pad1_x + PAD_WIDTH, pad1_y), (pad1_x + PAD_WIDTH, pad1_y + PAD_HEIGHT), (pad1_x, pad1_y + PAD_HEIGHT)]
    paddle2_pos = [(pad2_x, pad2_y), (pad2_x + PAD_WIDTH, pad2_y), (pad2_x + PAD_WIDTH, pad2_y + PAD_HEIGHT), (pad2_x, pad2_y + PAD_HEIGHT)]
    if pad2_y + paddle2_vel < (HEIGHT - PAD_HEIGHT) and pad2_y + paddle2_vel> 0:
        pad2_y = pad2_y + paddle2_vel
    if pad1_y + paddle1_vel < (HEIGHT - PAD_HEIGHT) and pad1_y + paddle1_vel> 0:
        pad1_y = pad1_y + paddle1_vel
    
    # draw paddles
    c.draw_polygon(paddle1_pos, 1, 'White','White')
    c.draw_polygon(paddle2_pos, 1, 'White', 'White')
    
    
    # draw scores
    c.draw_text(str(score1), (150, 80), 35, 'White')
    c.draw_text(str(score2), (450, 80), 35, 'White')
        
def keydown(key):
    acc = 2
    global paddle1_vel, paddle2_vel, pad2_y, pad1_y
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
        
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
       
       
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
        
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
        
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    acc = 0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = acc
        
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = acc
       
       
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = acc
        
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = acc

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", new_game, 45)



# start frame
new_game()
frame.start()

