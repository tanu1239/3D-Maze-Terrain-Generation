# ## packages
# import pygame
import sys
import math
from cmu_graphics import *
import random

## global constants
def onAppStart(app): 
    sys.setrecursionlimit(99999999)
    reset(app)

def reset(app):
    app.screenHeight = app.height
    app.screenWidth = app.width
    app.mapSize = 40
    app.tileSize = int((app.screenWidth / 2) / app.mapSize)
    app.fov = math.pi / 3
    app.halfFov = app.fov / 2
    app.castedRays = 120
    app.stepAngle = app.fov / app.castedRays
    app.maxDepth = int(app.mapSize * app.tileSize)
    app.scale = (app.screenHeight) / app.castedRays
    app.playerx = (app.screenWidth / 2) / 2
    app.playery = (app.screenWidth / 2) / 2
    app.playerAngle = math.pi
    app.map = mapGenerator(app)
    #[
    #     [1, 1, 1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 0, 1, 0, 0, 1],
    #     [1, 0, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 0, 1, 1, 0, 0, 1],
    #     [1, 1, 0, 0, 0, 0, 0, 1],
    #     [1, 0, 0, 0, 1, 1, 1, 1],
    #     [1, 1, 1, 0, 0, 0, 0, 1],
    #     [1, 1, 1, 1, 1, 1, 1, 1],
    # ]
    app.forward = True

def mapGenerator(app):
    map = []
    for row in range(app.mapSize):
        # adding all the rows into the map
        map.append([])
    for row in range(app.mapSize):
        for col in range(app.mapSize):
            value = random.randint(1, 10)
            # making it 60% percent chance open space
            if value <= 8:
                map[row].append(1)
            else:
                map[row].append(0)
    # making sure that first and last rows are closed
    firstAndLastRow = [1] * app.mapSize
    map.pop(0)
    map.insert(0, firstAndLastRow)
    map.pop()
    map.append(firstAndLastRow)
    # making sure that first and last columns are closed
    for row in range(app.mapSize):
        map[row][0] = 1
        map[row][-1] = 1

    for row in range(app.mapSize):
        for col in range(app.mapSize):
                if col > 1 and col < app.mapSize - 2 and row > 1 and row < app.mapSize - 2:
                    closedNum = 0
                    # check right neighbor
                    if map[row][col + 1] == 1:
                        closedNum += 1
                    #check left neighbor
                    if map[row][col - 1] == 1:
                        closedNum += 1
                    # check up neighbor
                    if map[row - 1][col] == 1:
                        closedNum += 1
                    # check down neighbor
                    if map[row + 1][col] == 1:
                        closedNum += 1

                    if closedNum > 2:
                        map[row][col] == 0
                        delete = random.randint(1, 4)
                        if delete == 1:
                            map[row][col + 1] = 0
                        if delete == 2:
                            map[row][col - 1] = 0
                        if delete == 3:
                            map[row - 1][col] = 0
                        else:
                            map[row + 1][col] = 0
    for row in range(1, app.mapSize - 1):
        map[row][1] = 0
        map[row][-2] = 0
    for col in range(1, app.mapSize - 1):
        map[1][col] = 0
        map[-2][col] = 0
    return map
    
    # # making sure that the map has no internal closures
    # if isGood(app, map) == True:
    #     return map
    # # regenerate map if it has any internal closures
    # else:
    #     return mapGenerator(app)
    
# def isGood(app, map):
#     for row in range(2, app.mapSize - 2):
#         for col in range(2, app.mapSize - 2):
#             closedNum = 0
#             if map[row][col] == 0 or map[row][col] == 1:
#                 # check right neighbor
#                 if map[row][col + 1] == 1:
#                     closedNum += 1
#                 #check left neighbor
#                 if map[row][col - 1] == 1:
#                     closedNum += 1
#                 # check up neighbor
#                 if map[row - 1][col] == 1:
#                     closedNum += 1
#                 # check down neighbor
#                 if map[row + 1][col] == 1:
#                     closedNum += 1
#             if closedNum > 2:
#                 return False
#     return True


def redrawAll(app):

    # # update 2D background
    drawRect(0, 0, app.screenWidth / 2, app.screenHeight, fill='black')

    # update 3D background
    light = rgb(200, 200, 200)
    #draw 3D background
    drawRect(app.screenWidth/2, 0, app.screenWidth/2, app.screenHeight, fill=light)

    # loop over map rows
    for row in range(len(app.map)):
        # loop over map cols
        for col in range(len(app.map[0])):
            
            #draw map in game window
            if app.map[row][col] == 1:
                color = rgb(100, 100, 100)
                drawRect(col*app.tileSize, row * app.tileSize, app.tileSize - 2, app.tileSize - 2, fill = color)
            elif app.map[row][col] == 0:
                color = rgb(200, 200, 200)
                drawRect(col*app.tileSize, row * app.tileSize, app.tileSize - 2, app.tileSize - 2, fill = color)
            # drawRect(col*app.tileSize, row * app.tileSize, app.tileSize - 2, app.tileSize - 2, fill = color)
    
    # draw player on 2D board
    drawCircle(int(app.playerx), int(app.playery), 8, fill="red")

    # draw player direction
    drawLine(app.playerx, app.playery, app.playerx - math.sin(app.playerAngle) * 50, app.playery + math.cos(app.playerAngle) * 50, lineWidth = 3)

    # define left most angle
    startAngle = app.playerAngle - app.halfFov

    # loop over casted rays
    for ray in range(app.castedRays):
        #cast rays step by step
        for depth in range(app.maxDepth):
            # get ray target coordinates
            targetx = app.playerx - math.sin(startAngle) * depth
            targety = app.playery + math.cos(startAngle) * depth

            # convert target X,Y coordinate to map row, col
            row = int(targety / app.tileSize)
            col = int(targetx / app.tileSize)

            # #calculate map square index
            # square = row * app.mapSize + col

            if app.map[row][col] == 1:
                drawRect(col * app.tileSize, row * app.tileSize, app.tileSize - 2, app.tileSize - 2, fill="green")
                
                # draw casted ray
                drawLine(app.playerx, app.playery, targetx, targety, fill="green")

                #calculate wall height
                wallHeight = (21000 / (depth + 0.0001))

                #draw 3D projection (rectangle by rectangle)
                drawRect(app.screenWidth / 2 + (ray * app.scale), (app.screenWidth / 4 ) - wallHeight / 2, app.scale, wallHeight)

                break

        # increment angle by a single step
        startAngle += app.stepAngle
    
    # castRays(app)



# ## raycasting algorithm
# def castRays(app):
#     # define left most angle
#     startAngle = app.playerAngle - app.halfFov

#     # loop over casted rays
#     for ray in range(app.castedRays):
#         #cast rays step by step
#         for depth in range(app.maxDepth):
#             # get ray target coordinates
#             targetx = app.playerx - math.sin(startAngle) * depth
#             targety = app.playery + math.cos(startAngle) * depth

#             # convert target X,Y coordinate to map row, col
#             row = int(targety / app.tileSize)
#             col = int(targetx / app.tileSize)

#             # #calculate map square index
#             # square = row * app.mapSize + col

#             if app.map[row][col] == 1:
#                 drawRect(col * app.tileSize, row * app.tileSize, app.tileSize - 2, app.tileSize - 2, fill="green")
#                 # draw casted ray
#                 drawLine(app.playerx, app.playery, targetx, targety, fill="green")

#                 #calculate wall height
#                 wallHeight = (21000 / (depth + 0.0001))

#                 #draw 3D projection (rectangle by rectangle)
#                 drawRect(app.screenHeight + ray * app.scale, (app.screenHeight / 2) - wallHeight / 2, app.scale, wallHeight, fill="white")

#                 break

#         # increment angle by a single step
#         startAngle += app.stepAngle


def onKeyPress(app, key):
    if key == 'left':
        app.playerAngle -= 0.1
    if key == 'right':
        app.playerAngle += 0.1
    if key == 'up':
        app.playerx += -math.sin(app.playerAngle) * 5
        app.playery += math.cos(app.playerAngle) * 5
        app.forward = True
    if key == 'down':
        app.playerx -= -math.sin(app.playerAngle) * 5
        app.playery -= math.cos(app.playerAngle) * 5
        app.forward = False

    # convert target X,Y coordinate to map row, col
    row = int(app.playery / app.tileSize)
    col = int(app.playerx / app.tileSize)

    # player hits wall (collision detection)
    if app.map[row][col] == 1:
        if app.forward:
            app.playerx -= -math.sin(app.playerAngle) * 5
            app.playery -= math.cos(app.playerAngle) * 5
        else:
            app.playerx += -math.sin(app.playerAngle) * 5
            app.playery += math.cos(app.playerAngle) * 5

def main():
    runApp(width = 1200, height = 1200)

main()


