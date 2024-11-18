## packages
import pygame
import sys
import math
from cmu_graphics import *

## global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
SCALE = (SCREEN_HEIGHT) / CASTED_RAYS

## global variables
player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

# map
MAP = ( 
    '########'
    '#    # #'
    '##     #'
    '####   #'
    '#    ###'
    '#   ####'
    '###    #'
    '########'
)

## initialize pygame
pygame.init()

## create game window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

## set window title
pygame.display.set_caption('Raycasting')

## init timer
clock = pygame.time.Clock()

## draw map
def draw_map():
    # loop over map rows
    for row in range(8):
        # loop over map cols
        for col in range(8):
            #calculate square index
            square = row * MAP_SIZE + col

            # draw map in game window
            pygame.draw.rect(
                win, (200, 200, 200) if MAP[square] == '#' else (100, 100, 100), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2)
            )
    
    # draw player on 2D board
    pygame.draw.circle(win, (255, 0, 0), (int(player_x), int(player_y)), 8)

    # draw player direction
    pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (player_x - math.sin(player_angle) * 50, player_y + math.cos(player_angle) * 50), 3)

## raycasting algorithm

def cast_rays():
    # define left most angle
    start_angle = player_angle - HALF_FOV

    # loop over casted rays
    for ray in range(CASTED_RAYS):
        #cast rays step by step
        for depth in range(MAX_DEPTH):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # convert target X,Y coordinate to map row, col
            row = int(target_y / TILE_SIZE)
            col = int(target_x / TILE_SIZE)

            #calculate map square index
            square = row * MAP_SIZE + col

            if MAP[square] == '#':
                pygame.draw.rect(win, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE - 2, TILE_SIZE - 2))
                # draw casted ray
                pygame.draw.line(win, (0, 255, 0), (player_x, player_y), (target_x, target_y))

                #calculate wall height
                wall_height = (21000 / (depth + 0.0001))

                #draw 3D projection (rectangle by rectangle)
                pygame.draw.rect(win, (255, 255, 255), (
                    SCREEN_HEIGHT + ray * SCALE,
                    (SCREEN_HEIGHT / 2) - wall_height / 2,
                     SCALE, wall_height))

                break

        # increment angle by a single step
        start_angle += STEP_ANGLE

# movement direction
forward = True


## game loop
while True:
    # escape condition
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # convert target X,Y coordinate to map row, col
    row = int(player_y / TILE_SIZE)
    col = int(player_x / TILE_SIZE)

    #calculate map square index
    square = row * MAP_SIZE + col

    # player hits wall (collision detection)
    if MAP[square] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * 3
            player_y -= math.cos(player_angle) * 3
        else:
            player_x += -math.sin(player_angle) * 3
            player_y += math.cos(player_angle) * 3

    # update 2D background
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # update 3D background
    pygame.draw.rect(win, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    # draw 2D map
    draw_map()

    # apply raycasting
    cast_rays()

    # get user input
    keys = pygame.key.get_pressed()

    # handle user input
    if keys[pygame.K_LEFT]: player_angle -= 0.1
    if keys[pygame.K_RIGHT]: player_angle += 0.1
    if keys[pygame.K_UP]: 
        player_x += -math.sin(player_angle) * 3
        player_y += math.cos(player_angle) * 3
        forward = True
    if keys[pygame.K_DOWN]: 
        player_x -= -math.sin(player_angle) * 3
        player_y -= math.cos(player_angle) * 3
        forward = False

    # update display
    pygame.display.flip()
    
    # set FPS
    clock.tick(30)


