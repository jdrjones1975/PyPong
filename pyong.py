#!/usr/bin/env python3
#learning pygame from programarcadegames.com
#pong game

'''
sounds from: http://opengameart.org/content/3-ping-pong-sounds-8-bit-style

The first code a Pygame program needs to do is load and initialize
the Pygame library. Every program that uses Pygame should start
with these lines:
'''


# Import a library of functions called 'pygame'
import pygame
import random

# Initialize the game engine
pygame.init()

# Next, we need to add variables that define our program's colors.
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
GREY     = ( 128, 128, 128)

SENS = 10 # Keyboard repeat interval constant, the lower the number the faster the paddle

class Pong(pygame.sprite.Sprite):
    '''
    This will be the pong ball class.
    '''
    def __init__(self, color, size):
        # Call to parent class
        super().__init__()

        
        #load the image
        self.image = pygame.Surface([size, size]).convert()
        self.image.fill(color)


        #set transparent color
        self.image.set_colorkey(BLACK)

        #Fetch the image rect.
        self.rect = self.image.get_rect()

    def set_pong(self):
        '''
        Reset pong to center of screen, give random x, y speed
        '''
        self.rect.x, self.rect.y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        self.x_speed = random.randrange(-2 , 3, 4) #random left or right needed here
        self.y_speed = random.randint(-5, 5) #random up or down
        
    def wall_bounce(self):
        hit_wall.play()
        self.y_speed *= -1
        
    def score(self):
        point_score.play()
        self.set_pong()

class Paddle(pygame.sprite.Sprite):
    '''
    This will be the paddle class.
    '''
    def __init__(self, color, width, height, paddle_x, paddle_y, speed):
        # Call to parent class
        super().__init__()
        
        #load the image
        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(color)


        #set transparent color
        self.image.set_colorkey(BLACK)

        #Fetch the image rect.
        self.rect = self.image.get_rect()

        # score keeper
        self.score = 0

        self.speed = speed

    def add_point(self, point):
        self.score += point

# player input configuration
player_left_up = pygame.K_a
player_left_down = pygame.K_z
player_right_up = pygame.K_k
player_right_down = pygame.K_m

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

size = (SCREEN_WIDTH, SCREEN_HEIGHT)
title = "PyPong"

paddle_width = 10
paddle_height = 80
paddle_speed = 10

pong_size = 10

netwidth = 10

hit_paddle = pygame.mixer.Sound('paddle.wav')
hit_wall = pygame.mixer.Sound('wall.wav')
point_score = pygame.mixer.Sound('miss.wav')

score_down = 20 # how far down the score text is placed on the screen
score_text_size = 60 # size of the scoreboard text
max_score = 10 # play until someone gets the max_score


# Left paddle init variables
init_l_paddle_x = 10
init_l_paddle_y = (SCREEN_HEIGHT / 2) - (paddle_height / 2)


# Right paddle init variables
init_r_paddle_x = SCREEN_WIDTH - (2*paddle_width)
init_r_paddle_y = (SCREEN_HEIGHT / 2) - (paddle_height / 2)

# create the display
screen = pygame.display.set_mode(size)
pygame.display.set_caption(title)

# Create lists to hold the sprites
all_sprites_list = pygame.sprite.Group()
paddle_list = pygame.sprite.Group()

def paddle_bounce(paddle, pong):
    if pong.x_speed > 0:
        pong.x_speed +=1
    elif pong.x_speed < 0:
        pong.x_speed -=1
    pong.x_speed *= -1
    if pong.rect.y < ( paddle_height/5 + paddle.rect.y ):
        pong.y_speed = -5
    elif pong.rect.y > (paddle_height/5 + paddle.rect.y) and pong.rect.y < (2 * (paddle_height/5) + paddle.rect.y ):
        pong.y_speed = -3
    elif pong.rect.y > (2 * (paddle_height/5) + paddle.rect.y ) and pong.rect.y < (3 * (paddle_height/5) + paddle.rect.y):
        pong.y_speed = 0
    elif pong.rect.y > (3 * (paddle_height/5) + paddle.rect.y) and pong.rect.y < (4 * (paddle_height/5) + paddle.rect.y):
        pong.y_speed = 3
    else:
        pong.y_speed = 5
    hit_paddle.play()

# Select the font to use, size, bold, italics
font = pygame.font.SysFont('Calibri', score_text_size, False, False)

def draw_score(paddle):
    return font.render(str(paddle.score), True, WHITE)

def draw_net(screen):
    pygame.draw.line(screen, GREY, [(SCREEN_WIDTH/2) - (netwidth/2), 0] , [(SCREEN_WIDTH/2) - (netwidth/2) , SCREEN_HEIGHT], netwidth)

def reset_all(pong, paddle1, paddle2):
    pong.set_pong()
    paddle1.score = 0
    paddle2.score = 0


# Create the pong
pong = Pong(WHITE, pong_size)
pong.set_pong()
all_sprites_list.add(pong)

# Create the left paddle
left_paddle = Paddle(WHITE, paddle_width, paddle_height, init_l_paddle_x, init_l_paddle_y, paddle_speed)
left_paddle.rect.x = init_l_paddle_x
left_paddle.rect.y = init_l_paddle_y
paddle_list.add(left_paddle)
all_sprites_list.add(left_paddle)

# Create the right paddle
right_paddle = Paddle(WHITE, paddle_width, paddle_height, init_r_paddle_x, init_r_paddle_y, paddle_speed)
right_paddle.rect.x = init_r_paddle_x
right_paddle.rect.y = init_r_paddle_y
paddle_list.add(right_paddle)
all_sprites_list.add(right_paddle)

# set the scores for rendering for each paddle
left_paddle_score = draw_score(left_paddle)
right_paddle_score = draw_score(right_paddle)
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Set the repeat interval of held keys
pygame.key.set_repeat(SENS, SENS)

# Loop until the user clicks the close button.
done = False
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for paddle in paddle_list:
        if paddle.score == max_score:  #what to do at max_score--could end game or just reset and keep playing
            reset_all(pong, left_paddle, right_paddle)
            left_paddle_score = draw_score(left_paddle)
            right_paddle_score = draw_score(right_paddle)
            '''
            pong.set_pong()
            left_paddle.score = 0
            right_paddle.score = 0
            left_paddle_score = draw_score(left_paddle)
            right_paddle_score = draw_score(right_paddle)
            '''
            
    for event in pygame.event.get(): # User did something
        
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        # This will handle multiple key presses, allowing both paddles to
        # move simultaneously
        
        elif event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[player_left_up]:
                    left_paddle.rect.y -= left_paddle.speed
            if key[player_left_down]:
                    left_paddle.rect.y += left_paddle.speed
            if key[player_right_up]:
                    right_paddle.rect.y -= right_paddle.speed
            if key[player_right_down]:
                    right_paddle.rect.y += right_paddle.speed


    # move stuff
    pong.rect.x += pong.x_speed
    pong.rect.y += pong.y_speed

    # determine collision or miss
    # if the pong hits the left paddle
    if pygame.sprite.collide_rect(pong, left_paddle):
        paddle_bounce(left_paddle, pong)

    # if the pong hits the right paddle
    elif pygame.sprite.collide_rect(pong, right_paddle):
        paddle_bounce(right_paddle, pong)

    # if the pong hits the bottom of the screen
    elif pong.rect.y >= SCREEN_HEIGHT - pong_size:
        pong.wall_bounce()
        
    # if the pong hits the top of the screen
    elif pong.rect.y <= 0:
        pong.wall_bounce()

    # if the pong goes off the left, point for right paddle
    elif pong.rect.x <= 0 - pong_size:
        right_paddle.add_point(1)
        right_paddle_score = draw_score(right_paddle)
        pong.score()

    # if the pong goes off the right, point for the left paddle
    elif pong.rect.x >= SCREEN_WIDTH:
        left_paddle.add_point(1)
        left_paddle_score = draw_score(left_paddle)
        pong.score()


    # --- Drawing code should go here
    # First, clear the screen to white (or black, or whatever).
    # Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    draw_net(screen)
    
    # draw the score
    screen.blit(left_paddle_score, [SCREEN_WIDTH/4, score_down])
    screen.blit(right_paddle_score, [3 * (SCREEN_WIDTH/4), score_down])
    
    # Draw all sprites
    all_sprites_list.draw(screen)

    # update the screen with what has been drawn
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit() #required to actually quit and close the window without hanging


            
