"""
This Python code uses the arrow keys to controls the left and right movement of an object
assumed to be a car at a constant speed.  Other parameters and features of the TrafficNode are coming up
"""
import pygame, sys
from pygame import *

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Car Movement')


CAR_WIDTH = 50
CAR_HEIGHT = 10
carSpeedX = 0
p1Car = pygame.Rect(10, 430, CAR_WIDTH, CAR_HEIGHT)
CAR_COLOR = pygame.color.Color("red")
# clock object that will be used to make the game
# have the same speed on all machines regardless
# of the actual machine speed.
clock = pygame.time.Clock()

while True:
    # limit the demo to 50 frames per second
    clock.tick( 50 );

    # clear screen with black color
    screen.fill( (0,0,0) )

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            pygame.display.update()

    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        p1Car.left = p1Car.left + carSpeedX - 10
    if keys[K_RIGHT]:
         p1Car.left = p1Car.left + carSpeedX + 10

    # draw the car
    screen.fill( CAR_COLOR, p1Car );

    pygame.display.update()