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

SENS = 25 # Keyboard repeat interval constant

class Pong(pygame.sprite.Sprite):
    '''
    This will be the pong ball class.
    '''
    def __init__(self, color, width, height):
        # Call to parent class
        super().__init__()
        
        #load the image
        self.image = pygame.Surface([width, height]).convert()
        self.image.fill(color)


        #set transparent color
        self.image.set_colorkey(BLACK)

        #Fetch the image rect.
        self.rect = self.image.get_rect()

    def set_pong(self):
        self.rect.x = init_pong_x
        self.rect.y = init_pong_y
        self.x_speed = 2 #random left or right needed here
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

width = 640
height = 480

size = (width, height)
title = "PyPong"

paddle_width = 10
paddle_height = 80
paddle_speed = 10
pong_size = 10

hit_paddle = pygame.mixer.Sound('paddle.wav')
hit_wall = pygame.mixer.Sound('wall.wav')
point_score = pygame.mixer.Sound('miss.wav')


# pong initialization variables
init_pong_x = width / 2
init_pong_y = height / 2

# Left paddle init variables
init_l_paddle_x = 10
init_l_paddle_y = (height / 2) - (paddle_height / 2)


# Right paddle init variables
init_r_paddle_x = width - (2*paddle_width)
init_r_paddle_y = (height / 2) - (paddle_height / 2)


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

# Create the pong
pong = Pong(WHITE, pong_size, pong_size)
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

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

pygame.key.set_repeat(SENS, SENS)

# Select the font to use, size, bold, italics

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

        # This will handle multiple key presses, allowing both paddles to
        # move simultaneously
        
        elif event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_a]:
                    left_paddle.rect.y -= left_paddle.speed
            if pygame.key.get_pressed()[pygame.K_z]:
                    left_paddle.rect.y += left_paddle.speed
            if pygame.key.get_pressed()[pygame.K_k]:
                    right_paddle.rect.y -= right_paddle.speed
            if pygame.key.get_pressed()[pygame.K_m]:
                    right_paddle.rect.y += right_paddle.speed

                
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

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
    elif pong.rect.y >= height - pong_size:
        pong.wall_bounce()
        
    # if the pong hits the top of the screen
    elif pong.rect.y <= 0:
        pong.wall_bounce()

    # if the pong goes off the left, point for right paddle
    elif pong.rect.x <= 0 - pong_size:
        right_paddle.add_point(1)
        pong.score()

        
    # if the pong goes off the right, point for the left paddle
    elif pong.rect.x >= width:
        left_paddle.add_point(1)
        pong.score()

        
    # update score if necessary

    # draw the score

    # Draw all sprites
    all_sprites_list.draw(screen)

    # update the screen with what has been drawn
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

pygame.quit() #required to actually quit and close the window without hanging


            
