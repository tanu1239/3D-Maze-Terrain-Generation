# ## packages
# import pygame
import sys
import math
from cmu_graphics import *
import random
import copy

class Player:
    def __init__(self, player = False, initializer = True, playerEnd = False, win = False, playerAlive = True, playerLevel = None, playerMapSize = 1, playerCellWidth = 1, playerCellHeight = 1, playerHealthBoost = [False, 0], playerShield = [False, 0],
                     playerx = None, playery = None, playerTileSize = None, sword = False, woodenSword = False, stoneSword = False, ironSword = False, goldenSword = False, diamondSword = False, swing = False, swingHeight = 0, swingPeak = False, collectedSwords = [], currSword = None, playerAngle = 0, playerHealth = 500, forward = True):
            self.player = player
            self.initializer = initializer
            self.playerEnd = playerEnd
            self.win = win
            self.playerAlive = playerAlive
            self.playerLevel = playerLevel
            self.playerMapSize = playerMapSize
            self.playerCellWidth = playerCellWidth
            self.playerCellHeight = playerCellHeight
            self.playerHealthBoost = playerHealthBoost
            self.playerShield = playerShield
            self.playerx = playerx
            self.playery = playery
            self.playerTileSize = playerTileSize
            self.sword = sword
            self.woodenSword = woodenSword
            self.stoneSword = stoneSword
            self.ironSword = ironSword
            self.goldenSword = goldenSword
            self.diamondSword = diamondSword
            self.swing = swing
            self.swingHeight = swingHeight
            self.swingPeak = swingPeak
            self.collectedSwords = collectedSwords
            self.currSword = currSword
            self.playerAngle = playerAngle
            self.playerHealth = playerHealth
            self.forward = forward
player1 = Player()
player2 = Player()

## global constants
def onAppStart(app): 
    app.setMaxShapeCount(10000000000000)
    app.mapSize = 10
    app.monsterCount = 0
    app.chestCount = 10
    app.home = True
    app.build = False
    app.userInput = ""
    app.buildDone = False
    app.placeWall = False
    app.placeMonster = False
    app.placeChest = False
    app.placeExit = False
    app.placeSpawn = False
    app.spawningLocations = []
    app.walls = []
    app.buildMap = []
    app.buildMonsterMap = []
    app.exit = []
    app.buildMonsters = []
    app.buildChestMap = []
    app.buildChests = []
    app.buildChestMapCopy = []
    app.buildChestsCopy = []
    app.backgroundurl = 'lowest resolution.mp3'
    app.placeMove = []
    app.selectDone = False
    reset(app)

def reset(app):
    app.screenHeight = app.height
    app.screenWidth = app.width
    app.tileSize = int((app.screenWidth / 2) / app.mapSize)
    app.twoTileSize = app.tileSize / 2
    app.fov = math.pi / 3
    app.halfFov = app.fov / 2
    app.castedRays = 60
    if player2.player == True:
        app.castedRays = 35
    if player2.player == False and app.build == True:
        app.castedRays = 35
    app.stepAngle = app.fov / app.castedRays
    app.maxDepth = int(app.mapSize * app.tileSize) 
    app.scale = (app.screenHeight) / app.castedRays
    player1.playerx = (app.screenWidth / 2) / 2
    if player1.playerLevel == None or player1.playerLevel < 7:
        player1.playery = (app.screenHeight / 2) / 1.25
    if player1.playerLevel != None and player1.playerLevel >= 7:
        player1.playery = (app.screenHeight / 2) / 1.1
    if player1.playerLevel == 20:
        player1.playery = (app.screenHeight / 2) / 1.05
    if app.spawningLocations != []:
        print(app.spawningLocations[0][2])
        player1.playerx = (app.screenWidth / 2) * app.spawningLocations[0][2]
        player1.playery = (app.screenHeight / 2) * app.spawningLocations[0][3]
    player1.playerAngle = math.pi
    player2.playerAngle = math.pi
    if app.buildMap == []:
        app.map = mapGenerator(app)
    if app.buildMap != []:
        app.map = app.buildMap
    player1.win = False
    app.exitRow = []
    app.exitCol = []
    if app.exit == [] and app.build == False:
        app.exitRow = 0
        app.exitCol = int(app.mapSize / 2)
    if app.exit != [] or app.build == True:
        for i in range(len(app.exit)):
            app.exitRow.append(app.exit[i][0])
            app.exitCol.append(app.exit[i][1])
        for i in range (len(app.map)):
            if (0, i) not in app.exit:
                app.map[0][i] = 1
    if app.userInput == "":
        app.cellWidth = (0.5 * app.screenWidth) / app.mapSize
        app.cellHeight = (0.5 * app.screenHeight) / app.mapSize
    if app.userInput != "":
        app.cellWidth = (0.5 * app.screenWidth) / int(app.userInput)
        app.cellHeight = (0.5 * app.screenHeight) / int(app.userInput)
    player2.playerx = None
    player2.playery = None
    if player2.player == True:
        player1.playerx = (app.screenWidth / 2) - (app.cellWidth * 1.5)
        player1.playery = player1.playery
        player2.playerx = (app.screenWidth / 2) - (0.9* app.cellWidth * (app.mapSize - 1))
        player2.playery = player1.playery
        if app.spawningLocations != [] and len(app.spawningLocations) >= 2:
            player1.playerx = (app.screenWidth / 2) * app.spawningLocations[0][2]
            player1.playery = (app.screenHeight / 2) * app.spawningLocations[0][3]
            player2.playerx = (app.screenWidth / 2) * app.spawningLocations[1][2]
            player2.playery = (app.screenHeight / 2) * app.spawningLocations[1][3]
    app.monsterHealth = 50
    app.monsters = []
    if app.buildMonsters == [] and app.build == False:
        while len(app.monsters) < app.monsterCount:
            randRow = random.randint(0, app.mapSize - 1)
            randCol = random.randint(0, app.mapSize - 1)
            randNoise = random.randint(1, 10)
            if app.map[randRow][randCol] == 0:
                monsterx = randCol * app.cellWidth + (app.cellWidth / randNoise)
                monstery = randRow * app.cellHeight + (app.cellHeight / randNoise)
                randomMove = random.randint(1, 4)
                app.monsters.append([monsterx, monstery, randomMove, app.monsterHealth])
    if app.buildMonsters != [] or app.build == True:
        for row in range(len(app.buildMonsterMap)):
            for col in range(len(app.buildMonsterMap)):
                if app.buildMonsterMap[row][col] == 1:
                    monsterRow = math.floor(row / 8)
                    monsterCol = math.floor(col / 8)
                    randNoise = random.randint(1, 10)
                    monsterx = monsterCol * app.cellWidth + (app.cellWidth / randNoise)
                    monstery = monsterRow * app.cellHeight + (app.cellHeight / randNoise)
                    randomMove = random.randint(1, 4)
                    app.monsters.append([monsterx, monstery, randomMove, app.monsterHealth])
    app.monsterMapSize = app.mapSize * 8
    app.monsterMapCellWidth = app.cellWidth / 8
    app.monsterMapCellHeight = app.cellHeight / 8
    if app.buildMonsterMap == [] and app.build == False:
        app.monsterMap = monsterMapGenerator(app)
    if app.buildMonsterMap != [] or app.build == True:
        app.monsterMap = app.buildMonsterMap
    app.monsterTileSize = app.tileSize / 8

    if player2.player == True:

        player1.playerMapSize = app.mapSize * 8
        player1.playerCellWidth = app.cellWidth / 8
        player1.playerCellHeight = app.cellHeight / 8
        player1.playerTileSize = app.tileSize / 8
        app.player1Map = []
        for i in range(player1.playerMapSize):
            app.player1Map.append([0] * player1.playerMapSize)
        player1Row = int(player1.playery / player1.playerCellHeight)
        player1Col = int(player1.playerx / player1.playerCellWidth)
        app.player1Map[player1Row][player1Col] = 1

        player2.playerMapSize = app.mapSize * 8
        player2.playerCellWidth = app.cellWidth / 8
        player2.playerCellHeight = app.cellHeight / 8
        player2.playerTileSize = app.tileSize / 8
        app.player2Map = []
        for i in range(player2.playerMapSize):
            app.player2Map.append([0] * player2.playerMapSize)
        player2Row = int(player2.playery / player2.playerCellHeight)
        player2Col = int(player2.playerx / player2.playerCellWidth)
        app.player2Map[player2Row][player2Col] = 1
    player1.playerHealth = 500
    player2.playerHealth = 500
    player1.playerAlive = True
    player2.playerAlive = True
    app.chests = []
    if app.buildChests == [] and app.build == False:
        while len(app.chests) < app.chestCount:
            if app.mapSize <= 11:
                randRow = random.randint(1, app.mapSize - 3)
            if app.mapSize > 11 and app.mapSize < 20:
                randRow = random.randint(1, app.mapSize - 4)
            if app.mapSize > 20:
                randRow = random.randint(1, app.mapSize - 6)
            randCol = random.randint(1, app.mapSize - 1)
            randNoise = random.randint(1, 20)
            if app.map[randRow][randCol] == 0:
                chestx = randCol * app.cellWidth + (app.cellWidth / 2)
                chesty = randRow * app.cellHeight + (app.cellHeight / 2)
                app.chests.append([chestx, chesty])
    if app.buildChests != [] or app.build == True:
         for i in range (len(app.buildChests)):
            maximumx = app.mapSize * app.cellWidth + (app.cellWidth / 2)
            maximumy = app.mapSize * app.cellHeight + (app.cellHeight / 2)
            app.chests.append([maximumx * app.buildChests[i][2], maximumy * app.buildChests[i][3]])
    app.chestMapSize = app.mapSize * 16
    app.chestMapCellWidth = app.cellWidth / 16
    app.chestMapCellHeight = app.cellHeight / 16
    app.chestTileSize = app.tileSize / 16
    if app.buildChestMap == [] and app.build == False:
        app.chestMap = chestMapGenerator(app)
    if app.buildChestMap != [] or app.build == True:
        app.chestMap = app.buildChestMap
    player1.sword = False
    player2.sword = False
    player1.woodenSword = False
    player1.stoneSword = False
    player1.ironSword = False
    player1.goldenSword = False
    player1.diamondSword = False
    player2.woodenSword = False
    player2.stoneSword = False
    player2.ironSword = False
    player2.goldenSword = False
    player2.diamondSword = False
    player1.swingHeight = 0
    player2.swingHeight = 0
    player1.swing = False
    player1.swingPeak = False
    player2.swing = False
    player2.swingPeak = False
    player1.collectedSwords = []
    player2.collectedSwords = []
    player1.currSword = None
    player2.currSword = None
    player1.playerEnd = False
    player1.win = False
    app.sharpurl = 'https://i.ibb.co/sJ5TZPT/download-1.jpg'
    app.dullurl = 'https://i.ibb.co/YBhHM7D/Realmonster.png'
    app.mazeurl = 'https://i.ibb.co/HTNv1Dz/Minecraft-maze.jpg'
    app.zombieurl = 'https://i.ibb.co/6s82W5z/Zombie-pic.png'
    app.simpleurl = 'https://i.ibb.co/yQ75Sc8/Color-Green.jpg'
    app.greenValues = []
    for i in range(100):
        value = random.randint(100, 255)
        app.greenValues.append(value)
    player1.forward = True
    player2.forward = True

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
    map[0][int(app.mapSize/2)] = 0
    map.pop()
    map.append([1]*app.mapSize)
    return map

def monsterMapGenerator(app):
    map = []
    for row in range(app.monsterMapSize):
        map.append([0] * app.monsterMapSize)
    for i in range(len(app.monsters)):
        monsterCol = math.floor(app.monsters[i][0] / app.monsterMapCellWidth)
        monsterRow = math.floor(app.monsters[i][1] / app.monsterMapCellHeight)
        map[monsterRow][monsterCol] = 1
    return map

def chestMapGenerator(app):
    map = []
    for row in range(app.chestMapSize):
        map.append([0] * app.chestMapSize)
    for i in range(len(app.chests)):
        chestCol = math.floor(app.chests[i][0] / app.chestMapCellWidth)
        chestRow = math.floor(app.chests[i][1] / app.chestMapCellHeight)
        map[chestRow][chestCol] = 1
    return map

def redrawAll(app):

    if (player2.player == True and player2.initializer == True) or (player1.player == True and player1.initializer == True):
        drawImage(app.sharpurl, app.screenWidth / 2, app.screenHeight / 2, align = 'center', width = app.screenWidth, height = app.screenHeight)
        if player2.player == True and player2.initializer == True:
            drawLabel('Two Player Mode', (app.screenWidth / 2), (app.screenHeight / 2) - 350, size=64)
        if player1.player == True and player1.initializer == True:
            drawLabel('One Player Mode', (app.screenWidth / 2), (app.screenHeight / 2) - 350, size=64)
        drawLabel('Choose Difficulty', (app.screenWidth / 2), (app.screenHeight / 2) - 250, size =32)
        widths = [-400, -250, -100, 50, 200, 350]
        for i in range(3):
            for j in range(6):
                drawRect((app.screenWidth / 2) + widths[j], (app.screenHeight / 2) - (175 - 150*i), 75, 75, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 100, (app.screenHeight / 2) + 275, 75, 75, fill='white', border='red')
        drawRect((app.screenWidth / 2) + 50, (app.screenHeight / 2) + 275, 75, 75, fill='white', border='red')
        level = 1
        for i in range(3):
            for j in range(6):
                drawLabel(f'{level}', ((app.screenWidth / 2) + widths[j]) + 37.5, (app.screenHeight / 2) - (175 - 150 * i) + 37.5, size = 25)
                level += 1
        drawLabel('19', ((app.screenWidth / 2) - 100 + 37.5), (app.screenHeight / 2) + 275 + 37.5, size = 25)
        drawLabel('20', ((app.screenWidth / 2) + 50 + 37.5), (app.screenHeight / 2) + 275 + 37.5, size = 25)
    
    if app.build == True and player1.win == False and player1.playerAlive == True and app.selectDone == False:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(0, 0, app.screenWidth, app.screenHeight, fill = gradient(darkBlue, lightBlue, start='bottom'))
        drawLabel('What Size Map Do You Want?', app.screenWidth / 2, app.screenHeight / 2 - 350, size=50, fill = 'black')
        drawLabel('Max Map Size is 50, minimum map size is 6. Press enter when done.', app.screenWidth / 2, app.screenHeight / 2 - 250, size=25, fill = 'black')
        drawLabel(app.userInput, app.screenWidth / 2, app.screenHeight / 2 - 200, size=25, fill = 'black')
        if app.buildDone == True:
            drawRect(app.screenWidth / 2 - 200, app.screenHeight / 2 - 175, 400, 400)
            drawRect(app.screenWidth / 2 - 425, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Place Wall', app.screenWidth / 2 - 425 + 50, app.screenHeight / 2 + 275 + 50, size = 20)
            drawRect(app.screenWidth / 2 - 300, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Place Exit', app.screenWidth / 2 - 300 + 50, app.screenHeight / 2 + 275 + 50, size = 20)
            drawRect(app.screenWidth / 2 - 175, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Place', app.screenWidth / 2 - 175 + 50, app.screenHeight / 2 + 275 + 40, size = 20)
            drawLabel('Monsters', app.screenWidth / 2 - 175 + 50, app.screenHeight / 2 + 275 + 70, size = 20)
            drawRect(app.screenWidth / 2 - 50, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Place', app.screenWidth / 2 - 50 + 50, app.screenHeight / 2 + 275 + 40, size = 20)
            drawLabel('Chests', app.screenWidth / 2 - 50 + 50, app.screenHeight / 2 + 275 + 70, size = 20)
            drawRect(app.screenWidth / 2 + 75, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Go Play in', app.screenWidth / 2 + 75 + 50, app.screenHeight / 2 + 275 + 25, size = 20)
            drawLabel('One-player', app.screenWidth / 2 + 75 + 50, app.screenHeight / 2 + 275 + 55, size = 19)
            drawLabel('Mode', app.screenWidth / 2 + 75 + 50, app.screenHeight / 2 + 275 + 85, size = 19)
            drawRect(app.screenWidth / 2 + 200, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Go Play in', app.screenWidth / 2 + 200 + 50, app.screenHeight / 2 + 275 + 25, size = 19)
            drawLabel('Two-Player', app.screenWidth / 2 + 200 + 50, app.screenHeight / 2 + 275 + 55, size = 19)
            drawLabel('Mode', app.screenWidth / 2 + 200 + 50, app.screenHeight / 2 + 275 + 85, size = 19)
            drawRect(app.screenWidth / 2 + 325, app.screenHeight / 2 + 275, 100, 100, fill = 'white', border = 'red')
            drawLabel('Player', app.screenWidth / 2 + 325 + 50, app.screenHeight / 2 + 275 + 25, size = 19)
            drawLabel('Spawning', app.screenWidth / 2 + 325 + 50, app.screenHeight / 2 + 275 + 55, size = 19)
            drawLabel('Location', app.screenWidth / 2 + 325 + 50, app.screenHeight / 2 + 275 + 85, size = 19)
            drawRect(app.screenWidth / 2 - 200 + 400 + 100, app.screenHeight / 2 - 175 + 200, 100, 100, fill = 'white', border = 'red')
            drawLabel('Undo', app.screenWidth / 2 - 200 + 400 + 100 + 50, app.screenHeight / 2 - 175 + 200 + 50, size = 19)
            #compute display cell width and cell height
            cellDisplaySize = 400 / int(app.userInput)
            leftDistance = app.screenWidth / 2 - 200
            topDistance = app.screenHeight / 2 - 175
            # loop over map rows
            for row in range(int(app.userInput)):
                # loop over map cols
                for col in range(int(app.userInput)):
                    #draw map in game window
                    drawRect(leftDistance + (col * cellDisplaySize), topDistance + (row * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='white', border='black')


            for wall in app.walls:
                row = wall[0]
                col = wall[1]
                drawRect(leftDistance + (col * cellDisplaySize), topDistance + (row * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='green', border='black')
                app.buildMap[row][col] = 1
            for row in range(int(app.userInput)):
                drawRect(leftDistance + (0 * cellDisplaySize), topDistance + (row * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='green', border='black')
                drawRect(leftDistance + ((int(app.userInput) - 1) * cellDisplaySize), topDistance + (row * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='green', border='black')
            for col in range(int(app.userInput)):
                drawRect(leftDistance + (col * cellDisplaySize), topDistance + (0 * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='green', border='black')
                drawRect(leftDistance + (col * cellDisplaySize), topDistance + ((int(app.userInput) - 1) * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='green', border='black')
            for exit in app.exit:
                row = exit[0]
                col = exit[1]
                drawRect(leftDistance + (col * cellDisplaySize), topDistance + (row * cellDisplaySize), cellDisplaySize, cellDisplaySize, fill='white', border='black')
                if app.buildMap != []:
                    app.buildMap.pop()
                    app.buildMap.append([1]*int(app.userInput))
                    app.buildMap[row][col] = 0
            for i in range(len(app.buildMonsters)):
                monstercx = app.buildMonsters[i][0]
                monstercy = app.buildMonsters[i][1]
                drawCircle(monstercx, monstercy, 8, fill='red')
            for i in range(len(app.buildChests)):
                chestcx = app.buildChests[i][0]
                chestcy = app.buildChests[i][1]
                drawCircle(chestcx, chestcy, 8, fill='brown')
                drawLabel('Chest', chestcx, chestcy)
            for i in range(len(app.spawningLocations)):
                if i > 1:
                    break
                locationx = app.spawningLocations[i][0]
                locationy = app.spawningLocations[i][1]
                drawCircle(locationx, locationy, 8, fill='green') 

            
        
    if app.home == True:
        drawImage(app.sharpurl, app.screenWidth / 2, app.screenHeight / 2, align = 'center', width = app.screenWidth, height = app.screenHeight)
        drawRect((app.screenWidth / 2) - 350, (app.screenHeight / 2) - 297, 700, 100, fill = 'white', border = 'red')
        drawLabel('Monster Escape Maze', (app.screenWidth / 2), (app.screenHeight / 2) - 250, size=64)
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) - 150, 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2), 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) + 150, 300, 100, fill='white', border='red')
        drawLabel('One Player Mode', (app.screenWidth / 2), (app.screenHeight / 2) - 100, size = 25)
        drawLabel('Two Player Mode', (app.screenWidth / 2), (app.screenHeight / 2) + 50, size = 25)
        drawLabel('Build Your Own Maze', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)
    
    if player1.player == True and (player1.win == True or player1.playerAlive == False) and app.build == False:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(0, 0, app.screenWidth, app.screenHeight, fill = gradient(darkBlue, lightBlue, start='bottom'))
        if player1.playerAlive == False:
            drawLabel('You died', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 30)
        if player1.win == True:
            drawLabel('You won', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 30)
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) - 150, 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2), 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) + 150, 300, 100, fill='white', border='red')
        drawLabel('Play Again', (app.screenWidth / 2), (app.screenHeight / 2) - 100, size = 25)
        drawLabel('Return Home', (app.screenWidth / 2), (app.screenHeight / 2) + 50, size = 25)
        drawLabel('Choose a Different Level', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)

    if player1.player == True and (player1.win == True or player1.playerAlive == False) and app.build == True:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(0, 0, app.screenWidth, app.screenHeight, fill = gradient(darkBlue, lightBlue, start='bottom'))
        if player1.playerAlive == False:
            drawLabel('You died', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 25)
        if player1.win == True:
            drawLabel('You won', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 25)
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) - 150, 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2), 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) + 150, 300, 100, fill='white', border='red')
        drawLabel('Play Again', (app.screenWidth / 2), (app.screenHeight / 2) - 100, size = 25)
        drawLabel('Return Home', (app.screenWidth / 2), (app.screenHeight / 2) + 50, size = 25)
        drawLabel('Build a Different Map', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)

    if player1.player == True and player1.initializer == False:
        if player1.playerAlive == False:
            drawRect(0, 0, app.screenWidth, app.screenHeight, fill=None)

        elif player1.win == True:
            drawRect(0, 0, app.screenWidth, app.screenHeight, fill=None)

        elif player1.win == False:

            # update 3D background
            light = rgb(200, 200, 200)
            dark = rgb(100, 100, 100)
            #draw 3D background
            drawRect(0, 0, app.screenWidth, app.screenHeight / 4, fill=light)
            drawRect(0, app.screenHeight / 4, app.screenWidth, 3 * app.screenHeight / 4, fill=dark)

            # define left most angle
            startAngle = player1.playerAngle - app.halfFov


            # loop over casted rays
            for ray in range(app.castedRays):
                #cast rays step by step
                for depth in range(app.maxDepth):
                    # get ray target coordinates
                    targetx = player1.playerx - math.sin(startAngle) * depth
                    targety = player1.playery + math.cos(startAngle) * depth

                    # convert target X,Y coordinate to map row, col
                    row = int(targety / app.tileSize)
                    col = int(targetx / app.tileSize)
                    monsterRow = int(targety / app.monsterTileSize)
                    monsterCol = int(targetx / app.monsterTileSize)
                    chestRow = int(targety / app.chestTileSize)
                    chestCol = int(targetx / app.chestTileSize)

                    if app.map[row][col] == 1:

                        #calculate wall height
                        wallHeight = (21000 / (depth + 0.0001))

                        color = raytracingColor(app, row, col, depth)

                        #draw 3D projection (rectangle by rectangle)
                        drawRect((ray * app.scale), (app.screenWidth / 4 ) - wallHeight / 2, app.scale, wallHeight, fill=color)
                        
                        break

                    if app.monsterMap != [] and app.monsterMap[monsterRow][monsterCol] == 1:
                        #calculate wall height
                        wallHeight = (21000 / (depth + 0.0001))
                        zombieShirt = rgb(47, 235, 235)
                        zombiePants = rgb(26, 65, 219)
                        zombieColor = gradient(zombiePants, zombieShirt, start='bottom')
                        drawRect((ray * app.scale), ((app.screenWidth / 4) - wallHeight / 2), app.scale, wallHeight / 2, fill='green')
                        drawRect((ray * app.scale), ((app.screenWidth / 4) - wallHeight / 4), app.scale, wallHeight, fill=zombieColor)
                        break

                    if app.chestMap != [] and app.chestMap[chestRow][chestCol] == 1:
                        chestHeight = (21000 / (depth + 0.0001))
                        chestColor = gradient('yellow', 'green', start='bottom')
                        drawRect((ray * app.scale), (app.screenWidth / 4) - chestHeight / 2, app.scale, chestHeight, fill=chestColor)
                        cx = ((ray * app.scale)) + (app.scale / 2)
                        cy = ((app.screenWidth / 4) - chestHeight / 2) + (chestHeight / 2)
                        drawCircle(cx, cy, 8, fill='red')
                        break


                # increment angle by a single step
                startAngle += app.stepAngle

            # draw 2D background
            drawRect(0, 0, app.screenWidth / 4, app.screenHeight / 4, fill='black')
            
            colToDraw = 0
            if app.userInput == "":
                colToDraw = len(app.map[0])
                rowToDraw = len(app.map)
            if app.userInput != "":
                colToDraw = len(app.map[0]) - 1
                rowToDraw = len(app.map) - 1
            # loop over map rows
            for row in range(rowToDraw):
                # loop over map cols
                for col in range(colToDraw):
                    
                    #draw map in game window
                    if app.map[row][col] == 1:
                        color = rgb(100, 100, 100)
                        drawRect(col*app.twoTileSize, row * app.twoTileSize, app.twoTileSize - 2, app.twoTileSize - 2, fill = color)
                    elif app.map[row][col] == 0:
                        color = rgb(200, 200, 200)
                        drawRect(col*app.twoTileSize, row * app.twoTileSize, app.twoTileSize - 2, app.twoTileSize - 2, fill = color)

            
            # draw player on 2D board
            drawCircle(int(player1.playerx) / 2, int(player1.playery) / 2, 8, fill="green")
            for monster in app.monsters:
                drawCircle(int(monster[0]) / 2, int(monster[1]) / 2, 8, fill='red')
            for chest in app.chests:
                drawCircle(int(chest[0]) / 2, int(chest[1]) / 2, 8, fill='brown')
                drawLabel('Chest', int(chest[0]) / 2, int(chest[1]) / 2)


            # draw player direction
            drawLine(player1.playerx / 2, player1.playery / 2, (player1.playerx / 2) - math.sin(player1.playerAngle) * 25, (player1.playery / 2) + math.cos(player1.playerAngle) * 25, lineWidth = 3)


            if player1.sword == True:
                woodenSwordColor = rgb(145, 117, 77)
                stoneSwordColor = rgb(80, 80, 80)
                ironSwordColor = rgb(200, 200, 200)
                goldenSwordColor = rgb(234, 204, 85)
                diamondSwordColor = rgb(52, 235, 201)
                swordColor = None
                if player1.woodenSword == True:
                    swordColor = woodenSwordColor
                if player1.stoneSword == True:
                    swordColor = stoneSwordColor
                if player1.ironSword == True:
                    swordColor = ironSwordColor
                if player1.goldenSword == True:
                    swordColor = goldenSwordColor
                if player1.diamondSword == True:
                    swordColor = diamondSwordColor
                leftSwordx = ((app.screenWidth) / 2 )
                leftSwordy = (app.screenHeight / 2) - player1.swingHeight
                rightSwordx = ((app.screenWidth) / 2) + 50
                rightSwordy = leftSwordy
                topSwordx = (leftSwordx + rightSwordx) / 2
                topSwordy = (rightSwordy - 50) - player1.swingHeight
                drawRect((app.screenWidth) / 2, (app.screenHeight / 2) - player1.swingHeight, 50, (app.screenHeight / 2) + player1.swingHeight, fill=swordColor)
                drawPolygon(leftSwordx, leftSwordy, rightSwordx, rightSwordy, topSwordx, topSwordy, fill=swordColor)

            drawRect((7*app.screenWidth / 8) - 2, 28, (app.screenWidth / 16) + 4, 34, fill = None, border = 'black', borderWidth = 5)
            healthPercentage = player1.playerHealth / 500
            color = None
            if healthPercentage > 0.5:
                color = 'green'
            if 0.2 < healthPercentage <= 0.5:
                color = 'yellow'
            if healthPercentage <= 0.2:
                color = 'red'
            if healthPercentage > 0:
                drawLabel('Health', (7*app.screenWidth / 8) + app.screenWidth / 32, 15, size = 15)
                drawRect(7*app.screenWidth / 8, 30, int((app.screenWidth / 16) * healthPercentage), 30, fill = color)
            if player1.playerHealthBoost[0] == True:
                drawLabel('Received Boost!', (7*app.screenWidth / 8) - 50, 45, fill = 'green')
            if player1.playerShield[0] == True:
                drawLabel('Shielded from Damage!', (7*app.screenWidth / 8) - 80, 45, fill = 'black')


    if player2.player == True and player2.initializer == False and app.home != True:

        if player2.playerAlive == False and player2.playerEnd == True:
            pass

        elif player1.win == True:
            pass

        # update 3D background
        light = rgb(200, 200, 200)
        dark = rgb(100, 100, 100)
        #draw 3D background
        drawRect(0, 0, app.screenWidth/2, app.screenHeight / 4, fill=light)
        drawRect(0, app.screenHeight / 4, app.screenWidth / 2, 3 * app.screenHeight / 4, fill=dark)

        # define left most angle
        startAngle = player2.playerAngle - app.halfFov


        # loop over casted rays
        for ray in range(app.castedRays):
            #cast rays step by step
            for depth in range(app.maxDepth):
                # get ray target coordinates
                targetx = player2.playerx - math.sin(startAngle) * depth
                targety = player2.playery + math.cos(startAngle) * depth

                # convert target X,Y coordinate to map row, col
                row = int(targety / app.tileSize)
                col = int(targetx / app.tileSize)
                monsterRow = int(targety / app.monsterTileSize)
                monsterCol = int(targetx / app.monsterTileSize)
                chestRow = int(targety / app.chestTileSize)
                chestCol = int(targetx / app.chestTileSize)
                player1Row = int(targety / player1.playerTileSize)
                player1Col = int(targetx / player1.playerTileSize)

                if (app.map[row][col] == 1):
                    #calculate wall height
                    wallHeight = (21000 / (depth + 0.0001))

                    color = raytracingColor(app, row, col, depth)
                    #draw 3D projection (rectangle by rectangle)
                    drawRect((ray * app.scale), (app.screenWidth / 4 ) - wallHeight / 2, app.scale, wallHeight, fill=color)
                    break

                if app.monsterMap != [] and app.monsterMap[monsterRow][monsterCol] == 1:
                    #calculate wall height
                    wallHeight = (21000 / (depth + 0.0001))
                    zombieShirt = rgb(47, 235, 235)
                    zombiePants = rgb(26, 65, 219)
                    zombieColor = gradient(zombiePants, zombieShirt, start='bottom')
                    drawRect((ray * app.scale), ((app.screenWidth / 4) - wallHeight / 2), app.scale, wallHeight / 2, fill='green')
                    drawRect((ray * app.scale), ((app.screenWidth / 4) - wallHeight / 4), app.scale, wallHeight, fill=zombieColor)
                    break

                if app.chestMap != [] and app.chestMap[chestRow][chestCol] == 1:
                    chestHeight = (21000 / (depth + 0.0001))
                    chestColor = gradient('yellow', 'green', start='bottom')
                    drawRect((ray * app.scale), (app.screenWidth / 4) - chestHeight / 2, app.scale, chestHeight, fill=chestColor)
                    cx = ((ray * app.scale)) + (app.scale / 2)
                    cy = ((app.screenWidth / 4) - chestHeight / 2) + (chestHeight / 2)
                    drawCircle(cx, cy, 8, fill='red')
                    break

                if app.player1Map[player1Row][player1Col] == 1 and player1.playerHealth > 0:
                    player1Height = (21000 / (depth + 0.0001))
                    color = gradient('white', 'black', start='bottom')
                    if player1.playerShield[0] == False:
                        drawRect((ray * app.scale), ((app.screenWidth / 4) - player1Height / 2), app.scale, player1Height / 2, fill='black')
                        drawRect((ray * app.scale), ((app.screenWidth / 4) - player1Height / 4), app.scale, player1Height, fill=color)
                    if player1.playerShield[0] == True:
                        silver = rgb(192, 192, 192)
                        drawRect((ray * app.scale), ((app.screenWidth / 4) - player1Height / 2), app.scale, player1Height / 2, fill=silver)
                        drawRect((ray * app.scale), ((app.screenWidth / 4) - player1Height / 4), app.scale, player1Height, fill=silver)
                    break


            # increment angle by a single step
            startAngle += app.stepAngle

        # update 2D background
        drawRect(0, 0, app.screenWidth / 4, app.screenHeight / 4, fill='black')

        # shade out other half of screen
        drawRect(app.screenWidth / 2, 0, app.screenWidth / 2, app.screenHeight, fill='black')

        colToDraw = 0
        if app.userInput == "":
            colToDraw = len(app.map[0])
            rowToDraw = len(app.map)
        if app.userInput != "":
            colToDraw = len(app.map[0]) - 1
            rowToDraw = len(app.map) - 1

        # loop over map rows
        for row in range(rowToDraw):
            # loop over map cols
            for col in range(colToDraw):
                
                #draw map in game window
                if app.map[row][col] == 1:
                    color = rgb(100, 100, 100)
                    drawRect(col*app.twoTileSize, row * app.twoTileSize, app.twoTileSize - 2, app.twoTileSize - 2, fill = color)
                elif app.map[row][col] == 0:
                    color = rgb(200, 200, 200)
                    drawRect(col*app.twoTileSize, row * app.twoTileSize, app.twoTileSize - 2, app.twoTileSize - 2, fill = color)

        
        # draw player on 2D board
        drawCircle(int(player2.playerx) / 2, int(player2.playery) / 2, 8, fill="green")
        for monster in app.monsters:
            drawCircle(int(monster[0]) / 2, int(monster[1]) / 2, 8, fill='red')
        for chest in app.chests:
            drawCircle(int(chest[0]) / 2, int(chest[1]) / 2, 8, fill='brown')
            drawLabel('Chest', int(chest[0]) / 2, int(chest[1]) / 2)

        #draw other player
        if player1.playerHealth > 0:
            drawCircle(int(player1.playerx) / 2, int(player1.playery) / 2, 8, fill='white')
            drawLabel('Opp', int(player1.playerx) / 2, int(player1.playery) / 2)

        # draw player direction
        drawLine(player2.playerx / 2, player2.playery / 2, (player2.playerx / 2) - math.sin(player2.playerAngle) * 25, (player2.playery / 2) + math.cos(player2.playerAngle) * 25, lineWidth = 3)


        if player2.sword == True:
            woodenSwordColor = rgb(145, 117, 77)
            stoneSwordColor = rgb(80, 80, 80)
            ironSwordColor = rgb(200, 200, 200)
            goldenSwordColor = rgb(234, 204, 85)
            diamondSwordColor = rgb(52, 235, 201)
            swordColor = None
            if player2.woodenSword == True:
                swordColor = woodenSwordColor
            if player2.stoneSword == True:
                swordColor = stoneSwordColor
            if player2.ironSword == True:
                swordColor = ironSwordColor
            if player2.goldenSword == True:
                swordColor = goldenSwordColor
            if player2.diamondSword == True:
                swordColor = diamondSwordColor
            leftSwordx = ((app.screenWidth) / 4 )
            leftSwordy = (app.screenHeight / 2) - player2.swingHeight
            rightSwordx = ((app.screenWidth) / 4) + 50
            rightSwordy = leftSwordy
            topSwordx = (leftSwordx + rightSwordx) / 2
            topSwordy = (rightSwordy - 50) - player2.swingHeight
            drawRect((app.screenWidth) / 4, (app.screenHeight / 2) - player2.swingHeight, 50, (app.screenHeight / 2) + player2.swingHeight, fill=swordColor)
            drawPolygon(leftSwordx, leftSwordy, rightSwordx, rightSwordy, topSwordx, topSwordy, fill=swordColor)

        # update 3D background
        light = rgb(200, 200, 200)
        dark = rgb(100, 100, 100)
        #draw 3D background
        drawRect(app.screenWidth / 2, 0, app.screenWidth/2, app.screenHeight / 4, fill=light)
        drawRect(app.screenWidth / 2, app.screenHeight / 4, app.screenWidth / 2, 3 * app.screenHeight / 4, fill=dark)

        # define left most angle
        startAngle = player1.playerAngle - app.halfFov

        # loop over casted rays
        for ray in range(app.castedRays):
            #cast rays step by step
            for depth in range(app.maxDepth):
                # get ray target coordinates
                targetx = player1.playerx - math.sin(startAngle) * depth
                targety = player1.playery + math.cos(startAngle) * depth

                # convert target X,Y coordinate to map row, col
                row = int(targety / app.tileSize)
                col = int(targetx / app.tileSize)
                monsterRow = int(targety / app.monsterTileSize)
                monsterCol = int(targetx / app.monsterTileSize)
                chestRow = int(targety / app.chestTileSize)
                chestCol = int(targetx / app.chestTileSize)
                player2Row = int(targety / player2.playerTileSize)
                player2Col = int(targetx / player2.playerTileSize)

                if app.map[row][col] == 1:

                    #calculate wall height
                    wallHeight = (21000 / (depth + 0.0001))

                    color = raytracingColor(app, row, col, depth)

                    #draw 3D projection (rectangle by rectangle)
                    drawRect(app.screenWidth / 2 + (ray * app.scale), (app.screenWidth / 4 ) - wallHeight / 2, app.scale, wallHeight, fill=color)
                    
                    break

                if app.monsterMap != [] and app.monsterMap[monsterRow][monsterCol] == 1:
                    #calculate wall height
                    wallHeight = (21000 / (depth + 0.0001))
                    zombieShirt = rgb(47, 235, 235)
                    zombiePants = rgb(26, 65, 219)
                    zombieColor = gradient(zombiePants, zombieShirt, start='bottom')
                    drawRect(app.screenWidth / 2 + (ray * app.scale), ((app.screenWidth / 4) - wallHeight / 2), app.scale, wallHeight / 2, fill='green')
                    drawRect(app.screenWidth / 2 + (ray * app.scale), ((app.screenWidth / 4) - wallHeight / 4), app.scale, wallHeight, fill=zombieColor)
                    break

                if app.chestMap != [] and app.chestMap[chestRow][chestCol] == 1:
                    chestHeight = (21000 / (depth + 0.0001))
                    chestColor = gradient('yellow', 'green', start='bottom')
                    drawRect(app.screenWidth / 2 + (ray * app.scale), (app.screenWidth / 4) - chestHeight / 2, app.scale, chestHeight, fill=chestColor)
                    cx = (app.screenWidth / 2 + (ray * app.scale)) + (app.scale / 2)
                    cy = ((app.screenWidth / 4) - chestHeight / 2) + (chestHeight / 2)
                    drawCircle(cx, cy, 8, fill='red')
                    break

                if app.player2Map[player2Row][player2Col] == 1 and player2.playerHealth > 0:
                    player2Height = (21000 / (depth + 0.0001))
                    color = gradient('white', 'black', start='bottom')
                    if player2.playerShield[0] == False:
                        drawRect(app.screenWidth / 2 + (ray * app.scale), ((app.screenWidth / 4) - player2Height / 2), app.scale, player2Height / 2, fill='black')
                        drawRect(app.screenWidth / 2 + (ray * app.scale), ((app.screenWidth / 4) - player2Height / 4), app.scale, player2Height, fill=color)
                    if player2.playerShield[0] == True:
                        silver = rgb(192, 192, 192)
                        drawRect(app.screenWidth / 2 + (ray * app.scale), ((app.screenWidth / 4) - player2Height / 2), app.scale, player2Height / 2, fill=silver)
                        drawRect(app.screenWidth / 2 + (ray * app.scale), ((app.screenWidth / 4) - player2Height / 4), app.scale, player2Height, fill=silver)
                    break

            # increment angle by a single step
            startAngle += app.stepAngle

        # draw 2D background
        drawRect(app.screenWidth / 2, 0, app.screenWidth / 4, app.screenWidth / 4, fill='black')

        colToDraw = 0
        if app.userInput == "":
            colToDraw = len(app.map[0])
            rowToDraw = len(app.map)
        if app.userInput != "":
            colToDraw = len(app.map[0]) - 1
            rowToDraw = len(app.map) - 1
        # loop over map rows
        for row in range(rowToDraw):
            # loop over map cols
            for col in range(colToDraw):
                
                #draw map in game window
                if app.map[row][col] == 1:
                    color = rgb(100, 100, 100)
                    drawRect((app.screenWidth / 2) + (col*app.twoTileSize), row * app.twoTileSize, app.twoTileSize - 2, app.twoTileSize - 2, fill = color)
                elif app.map[row][col] == 0:
                    color = rgb(200, 200, 200)
                    drawRect((app.screenWidth / 2) + (col*app.twoTileSize), row * app.twoTileSize, app.twoTileSize - 2, app.twoTileSize - 2, fill = color)

        
        # draw player on 2D board
        drawCircle((app.screenWidth / 2) + (int(player1.playerx) / 2), int(player1.playery) / 2, 8, fill="green")
        for monster in app.monsters:
            drawCircle((app.screenWidth / 2) + (int(monster[0]) / 2), int(monster[1]) / 2, 8, fill='red')
        for chest in app.chests:
            drawCircle((app.screenWidth / 2) + (int(chest[0]) / 2), int(chest[1]) / 2, 8, fill='brown')
            drawLabel('Chest', (app.screenWidth / 2) + (int(chest[0]) / 2), int(chest[1]) / 2)

        #draw other player
        if player2.playerHealth > 0:
            drawCircle((app.screenWidth / 2 ) + int(player2.playerx) / 2, int(player2.playery) / 2, 8, fill='white')
            drawLabel('Opp', (app.screenWidth / 2 ) + int(player2.playerx) / 2, int(player2.playery) / 2)

        # draw player direction
        drawLine((app.screenWidth / 2) + (player1.playerx / 2), player1.playery / 2, ((app.screenWidth / 2) + (player1.playerx / 2)) - math.sin(player1.playerAngle) * 25, (player1.playery / 2) + math.cos(player1.playerAngle) * 25, lineWidth = 3)

        if player1.sword == True:
            woodenSwordColor = rgb(145, 117, 77)
            stoneSwordColor = rgb(80, 80, 80)
            ironSwordColor = rgb(200, 200, 200)
            goldenSwordColor = rgb(234, 204, 85)
            diamondSwordColor = rgb(52, 235, 201)
            swordColor = None
            if player1.woodenSword == True:
                swordColor = woodenSwordColor
            if player1.stoneSword == True:
                swordColor = stoneSwordColor
            if player1.ironSword == True:
                swordColor = ironSwordColor
            if player1.goldenSword == True:
                swordColor = goldenSwordColor
            if player1.diamondSword == True:
                swordColor = diamondSwordColor
            leftSwordx = (3 * (app.screenWidth) / 4 )
            leftSwordy = (app.screenHeight / 2) - player1.swingHeight
            rightSwordx = (3 * (app.screenWidth) / 4) + 50
            rightSwordy = leftSwordy
            topSwordx = (leftSwordx + rightSwordx) / 2
            topSwordy = (rightSwordy - 50) - player1.swingHeight
            drawRect(3 * (app.screenWidth) / 4, (app.screenHeight / 2) - player1.swingHeight, 50, (app.screenHeight / 2) + player1.swingHeight, fill=swordColor)
            drawPolygon(leftSwordx, leftSwordy, rightSwordx, rightSwordy, topSwordx, topSwordy, fill=swordColor)

        drawLine(app.screenWidth / 2, 0, app.screenWidth / 2, app.screenHeight, lineWidth = 5)

        # health bar for player 1
        drawRect((7*app.screenWidth / 8) - 2, 28, (app.screenWidth / 16) + 4, 34, fill = None, border = 'black', borderWidth = 5)
        healthPercentage = player1.playerHealth / 500
        color = None
        if healthPercentage > 0.5:
            color = 'green'
        if 0.2 < healthPercentage <= 0.5:
            color = 'yellow'
        if healthPercentage <= 0.2:
            color = 'red'
        if healthPercentage > 0:
            drawLabel('Health', (7*app.screenWidth / 8) + app.screenWidth / 32, 15, size = 15)
            drawRect(7*app.screenWidth / 8, 30, (app.screenWidth / 16) * healthPercentage, 30, fill = color)
        if player1.playerHealthBoost[0] == True:
            drawLabel('Received Boost!', (7*app.screenWidth / 8) - 50, 45, fill = 'green')
        if player1.playerShield[0] == True:
            drawLabel('Shielded from Damage!', (7*app.screenWidth / 8) - 80, 45, fill = 'black')

        drawRect((3*app.screenWidth / 8) - 2, 28, (app.screenWidth / 16) + 4, 34, fill = None, border = 'black', borderWidth = 5)
        healthPercentage = player2.playerHealth / 500
        color = None
        if healthPercentage > 0.5:
            color = 'green'
        if 0.2 < healthPercentage <= 0.5:
            color = 'yellow'
        if healthPercentage <= 0.2:
            color = 'red'
        if healthPercentage > 0:
            drawLabel('Health', (3*app.screenWidth / 8) + app.screenWidth / 32, 15, size = 15)
            drawRect(3*app.screenWidth / 8, 30, (app.screenWidth / 16) * healthPercentage, 30, fill = color)
        if player2.playerHealthBoost[0] == True:
            drawLabel('Received Boost!', (3*app.screenWidth / 8) - 50, 45, fill = 'green')
        if player2.playerShield[0] == True:
            drawLabel('Shielded from Damage!', (3*app.screenWidth / 8) - 80, 45, fill = 'black')
    
    if (player1.playerAlive == False or player1.playerEnd == True or player1.playerHealth <= 0) and player1.win == False and player2.win == False and player2.playerHealth >= 0 and player1.player == False:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(app.screenWidth / 2, 0, app.screenWidth / 2, app.screenHeight, fill=gradient(darkBlue, lightBlue, start='bottom'))
        drawLabel('You died', 3*app.screenWidth / 4, app.screenHeight / 2, size = 25)

    if (player2.playerAlive == False or player2.playerEnd == True or player2.playerHealth <= 0) and player1.win == False and player2.win == False and player1.playerHealth >= 0 and player1.player == False:
        drawRect(0, 0, app.screenWidth / 2, app.screenHeight, fill=gradient(darkBlue, lightBlue, start='bottom'))
        drawLabel('You died', app.screenWidth / 4, app.screenHeight / 2, size = 25)

    if player1.win == True and player2.win == False and player1.player == False:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(0, 0, app.screenWidth, app.screenHeight, fill = gradient(darkBlue, lightBlue, start='bottom'))
        drawLabel('Player 1 Won', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 25)

        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) - 150, 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2), 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) + 150, 300, 100, fill='white', border='red')
        drawLabel('Play Again', (app.screenWidth / 2), (app.screenHeight / 2) - 100, size = 25)
        drawLabel('Return Home', (app.screenWidth / 2), (app.screenHeight / 2) + 50, size = 25)
        if app.build == False:
            drawLabel('Play a Different Level', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)
        elif app.build == True:
            drawLabel('Build a Different Map', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)
    
    if player2.win == True and player1.win == False and app.home == False and player1.player == False:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(0, 0, app.screenWidth, app.screenHeight, fill = gradient(darkBlue, lightBlue, start='bottom'))
        drawLabel('Player 2 Won', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 25)

        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) - 150, 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2), 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) + 150, 300, 100, fill='white', border='red')
        drawLabel('Play Again', (app.screenWidth / 2), (app.screenHeight / 2) - 100, size = 25)
        drawLabel('Return Home', (app.screenWidth / 2), (app.screenHeight / 2) + 50, size = 25)
        if app.build == False:
            drawLabel('Play a Different Level', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)
        elif app.build == True:
            drawLabel('Build a Different Map', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)

    if (player1.playerHealth <= 0) and (player2.playerHealth <= 0) and player1.player == False:
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
        drawRect(0, 0, app.screenWidth, app.screenHeight, fill = gradient(darkBlue, lightBlue, start='bottom'))
        drawLabel('Both Players Died', app.screenWidth / 2, app.screenHeight / 2 - 300, size = 25)

        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) - 150, 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2), 300, 100, fill='white', border='red')
        drawRect((app.screenWidth / 2) - 150, (app.screenHeight / 2) + 150, 300, 100, fill='white', border='red')
        drawLabel('Play Again', (app.screenWidth / 2), (app.screenHeight / 2) - 100, size = 25)
        drawLabel('Return Home', (app.screenWidth / 2), (app.screenHeight / 2) + 50, size = 25)
        if app.build == False:
            drawLabel('Play a Different Level', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)
        elif app.build == True:
            drawLabel('Build a Different Map', (app.screenWidth / 2), (app.screenHeight / 2) + 200, size = 25)

def raytracingColor(app, row, col, depth):
    #calculate wall height
    wallHeight = (21000 / (depth + 0.0001))

    if row % 2 == 1:
        color = 'red'
    if row % 2 == 0:
        color = 'orange'
    if app.build == False and row == 0 and (col == app.exitCol - 1 or col == app.exitCol + 1):
        rand1 = random.randint(0, 255)
        rand2 = random.randint(0, 255)
        rand3 = random.randint(0, 255)
        color = rgb(rand1, rand2, rand3)
    if app.build == False and row == -1:
        rand1 = random.randint(0, 255)
        rand2 = random.randint(0, 255)
        rand3 = random.randint(0, 255)
        color = rgb(rand1, rand2, rand3)
    if app.build == True:
        for i in range(len(app.exit)):
            if row == app.exit[i][0] == 0 and (col == app.exit[i][1] - 1 or col == app.exit[i][1] + 1):
                rand1 = random.randint(0, 255)
                rand2 = random.randint(0, 255)
                rand3 = random.randint(0, 255)
                color = rgb(rand1, rand2, rand3)
        if row == -1:
            rand1 = random.randint(0, 255)
            rand2 = random.randint(0, 255)
            rand3 = random.randint(0, 255)
            color = rgb(rand1, rand2, rand3)
        for i in range(len(app.exit)):
            if row == app.exit[i][0] == app.mapSize - 1 and (col == app.exit[i][1] -1 or col == app.exit[i][1] + 1):
                rand1 = random.randint(0, 255)
                rand2 = random.randint(0, 255)
                rand3 = random.randint(0, 255)
                color = rgb(rand1, rand2, rand3)
        if row == app.mapSize:
            rand1 = random.randint(0, 255)
            rand2 = random.randint(0, 255)
            rand3 = random.randint(0, 255)
            color = rgb(rand1, rand2, rand3)
        for i in range(len(app.exit)):
            if col == app.exit[i][1] == 0 and (row == app.exit[i][0] - 1 or row == app.exit[i][0] + 1):
                rand1 = random.randint(0, 255)
                rand2 = random.randint(0, 255)
                rand3 = random.randint(0, 255)
                color = rgb(rand1, rand2, rand3)
        if col == -1:
            rand1 = random.randint(0, 255)
            rand2 = random.randint(0, 255)
            rand3 = random.randint(0, 255)
            color = rgb(rand1, rand2, rand3)
        for i in range(len(app.exit)):
            if col == app.exit[i][1] == app.mapSize - 1 and (row == app.exit[i][0] - 1 or row == app.exit[i][0] + 1):
                rand1 = random.randint(0, 255)
                rand2 = random.randint(0, 255)
                rand3 = random.randint(0, 255)
                color = rgb(rand1, rand2, rand3)
        if col == app.mapSize:
            rand1 = random.randint(0, 255)
            rand2 = random.randint(0, 255)
            rand3 = random.randint(0, 255)
            color = rgb(rand1, rand2, rand3)

    return color

def onKeyPress(app, key):
    if key == 'space':
        swordSwitcher(app, player1)
    if key == 'e':
        swordSwitcher(app, player2)
    if app.build == True:
        if key.isdigit() == True:
            app.userInput = app.userInput + key
        if key == "backspace":
            if app.userInput != "":
                app.userInput = str(int(app.userInput) // 10)
            if app.userInput == "0":
                app.userInput = ""
        if key == "enter":
            inputtedSize = int(app.userInput)
            if inputtedSize < 6 or inputtedSize > 50:
                pass
            elif inputtedSize >= 6 and inputtedSize < 51:
                app.buildDone = True

def swordSwitcher(app, somePlayer):
    if somePlayer.sword == True:
        if len(somePlayer.collectedSwords) == 1:
            pass
        else:
            index = None
            length = len(somePlayer.collectedSwords)
            if somePlayer.currSword == 'wood':
                index = somePlayer.collectedSwords.index('wood')
            if somePlayer.currSword == 'stone':
                index = somePlayer.collectedSwords.index('stone')
            if somePlayer.currSword == 'iron':
                index = somePlayer.collectedSwords.index('iron')
            if somePlayer.currSword == 'gold':
                index = somePlayer.collectedSwords.index('gold')
            if somePlayer.currSword == 'diamond':
                index = somePlayer.collectedSwords.index('diamond')
            newIndex = (index + 1) % length
            somePlayer.sword = True
            somePlayer.woodenSword = False
            somePlayer.stoneSword = False
            somePlayer.ironSword = False
            somePlayer.goldenSword = False
            somePlayer.diamondSword = False
            somePlayer.currSword = None
            if somePlayer.collectedSwords[newIndex] == 'wood':
                somePlayer.woodenSword = True
                somePlayer.currSword = 'wood'
                print('now wood')
            if somePlayer.collectedSwords[newIndex] == 'stone':
                somePlayer.stoneSword = True
                somePlayer.currSword = 'stone'
                print('now stone')
            if somePlayer.collectedSwords[newIndex] == 'iron':
                somePlayer.ironSword = True
                somePlayer.currSword = 'iron'
                print('now iron')
            if somePlayer.collectedSwords[newIndex] == 'gold':
                somePlayer.goldenSword = True
                somePlayer.currSword = 'gold'
                print('now gold')
            if somePlayer.collectedSwords[newIndex] == 'diamond':
                somePlayer.diamondSword = True
                somePlayer.currSword = 'diamond'
                print('now diamond')


def onKeyHold(app, keys):
    if 'left' in keys:
        player1.playerAngle -= 0.1
    if 'right' in keys:
        player1.playerAngle += 0.1
    if 'up' in keys:
        player1.playerx += -math.sin(player1.playerAngle) * 5
        player1.playery += math.cos(player1.playerAngle) * 5
        player1.forward = True
    if 'down' in keys:
        player1.playerx -= -math.sin(player1.playerAngle) * 5
        player1.playery -= math.cos(player1.playerAngle) * 5
        player1.forward = False

    if 'a' in keys:
        player2.playerAngle -= 0.1
    if 'd' in keys:
        player2.playerAngle += 0.1
    if 'w' in keys:
        player2.playerx += -math.sin(player2.playerAngle) * 5
        player2.playery += math.cos(player2.playerAngle) * 5
        player2.forward = True
    if 's' in keys:
        player2.playerx -= -math.sin(player2.playerAngle) * 5
        player2.playery -= math.cos(player2.playerAngle) * 5
        player2.forward = False


    if 'q' in keys:
        if player2.sword == True:
            player2.swing = True
            i = 0
            while i != len(app.monsters):
                if distance(app.monsters[i][0], app.monsters[i][1], player2.playerx, player2.playery) < 45:
                    if player2.woodenSword == True:
                        app.monsters[i][3] -= 1
                    if player2.stoneSword == True:
                        app.monsters[i][3] -= 2
                    if player2.ironSword == True:
                        app.monsters[i][3] -= 3
                    if player2.goldenSword == True:
                        app.monsters[i][3] -= 5
                    if player2.diamondSword == True:
                        app.monsters[i][3] -= 10
                    if app.monsters[i][3] <= 0:
                        app.monsters.pop(i)
                        continue
                    print(app.monsters[i][3])
                i += 1
            if player2.player == True:
                if distance(player1.playerx, player1.playery, player2.playerx, player2.playery) < 45:
                    if player1.playerShield[0] == False:
                        player1.playerHealth -= 50
                if player1.playerHealth <= 0:
                    player1.playerAlive = False
                    player1.playerEnd = True
                print(player1.playerHealth)


    # convert target X,Y coordinate to map row, col
    row = int(player1.playery / app.tileSize)
    col = int(player1.playerx / app.tileSize)

    # player hits wall (collision detection)
    if app.map[row][col] == 1:
        if player1.forward:
            player1.playerx -= -math.sin(player1.playerAngle) * 5
            player1.playery -= math.cos(player1.playerAngle) * 5
        else:
            player1.playerx += -math.sin(player1.playerAngle) * 5
            player1.playery += math.cos(player1.playerAngle) * 5

    if player2.playerx != None and player2.playery != None:
        twoRow = int(player2.playery / app.tileSize)
        twoCol = int(player2.playerx / app.tileSize)
        if app.map[twoRow][twoCol] == 1:
            if player2.forward:
                player2.playerx -= -math.sin(player2.playerAngle) * 5
                player2.playery -= math.cos(player2.playerAngle) * 5
            else:
                player2.playerx += -math.sin(player2.playerAngle) * 5
                player2.playery += math.cos(player2.playerAngle) * 5
    
    checkIfNearbyMonsters(app)

    if onePlayerInExit(app) == True:
        player1.win = True
        player1.playerLevel = None
        player1.playerEnd = True
    if player2.playerx != None and player2.playery != None:
        if twoPlayerInExit(app) == True:
            player2.win = True
            player2.playerLevel = None
            player2.playerEnd = True

def checkIfNearbyMonsters(app):
    for monster in app.monsters:
        if distance(monster[0], monster[1], player1.playerx, player1.playery) < 20:
            if player1.playerShield[0] == False:
                player1.playerHealth -= 10
        if player2.playerx != None and player2.playery != None:
            if distance(monster[0], monster[1], player2.playerx, player2.playery) < 20:
                if player2.playerShield[0] == False:
                    player2.playerHealth -= 10
    return True

def onStep(app):
    if player1.initializer == True:
        player1.playerEnd = False
    if player2.initializer == True:
        player2.playerEnd = False
    for i in range(len(app.monsters)):
        if app.monsters[i][2] == 1:
            app.monsters[i][0] += 2
        if app.monsters[i][2] == 2:
            app.monsters[i][0] -= 2
        if app.monsters[i][2] == 3:
            app.monsters[i][1] -= 2
        if app.monsters[i][2] == 4:
            app.monsters[i][1] += 2
        monsterRow = math.floor(app.monsters[i][1] / app.cellHeight)
        monsterCol = math.floor(app.monsters[i][0] / app.cellWidth)
        if app.map[monsterRow][monsterCol] == 1:
            if app.monsters[i][2] == 1:
                app.monsters[i][0] -= 2
            if app.monsters[i][2] == 2:
                app.monsters[i][0] += 2
            if app.monsters[i][2] == 3:
                app.monsters[i][1] += 2
            if app.monsters[i][2] == 4:
                app.monsters[i][1] -= 2
            newRandomMove = newRandomDirectionProvider(app, i)
            app.monsters[i][2] = newRandomMove
    if player1.playerHealth <= 0:
        player1.playerAlive = False
        player1.playerEnd = True
        player1.playerLevel = None
    if player2.playerHealth <= 0:
        player2.playerAlive = False
        player2.playerEnd = True
        player2.playerLevel = None
    app.monsterMap = monsterMapGenerator(app)
    i = 0
    while i < len(app.chests):
        if distance(app.chests[i][0], app.chests[i][1], player1.playerx, player1.playery) < 25:
            chestOpener(app, player1, i)
        else:
            i += 1


    if player2.playerx != None and player2.playery != None:
        i = 0
        while i < len(app.chests):
            if distance(app.chests[i][0], app.chests[i][1], player2.playerx, player2.playery) < 25:
                chestOpener(app, player2, i)
            else:
                i += 1

    if player1.sword == True and player1.swing == True:
        if player1.swingHeight < 100 and player1.swingPeak == False:
            player1.swingHeight += 50
        if player1.swingHeight >= 100:
            player1.swingPeak = True
            player1.swingHeight -= 50
        if player1.swingHeight > 0 and player1.swingPeak == True:
            player1.swingHeight -= 50
        if player1.swingHeight == 0 and player1.swingPeak == True:
            player1.swingHeight = 0
            player1.swing = False
            player1.swingPeak = False

    if player2.sword == True and player2.swing == True:
        if player2.swingHeight < 100 and player2.swingPeak == False:
            player2.swingHeight += 50
        if player2.swingHeight >= 100:
            player2.swingPeak = True
            player2.swingHeight -= 50
        if player2.swingHeight > 0 and player2.swingPeak == True:
            player2.swingHeight -= 50
        if player2.swingHeight == 0 and player2.swingPeak == True:
            player2.swingHeight = 0
            player2.swing = False
            player2.swingPeak = False

    if player2.player == True and player1.playerx != None and player1.playery != None and player2.playerx != None and player2.playery != None:
    
        app.player1Map = []
        for i in range(player1.playerMapSize):
            app.player1Map.append([0] * player1.playerMapSize)
        player1Row = int(player1.playery / player1.playerCellHeight)
        player1Col = int(player1.playerx / player1.playerCellWidth)
        if app.player1Map != [] and 0 <= player1Row <= len(app.player1Map) and 0 <= player1Col <= len(app.player1Map[0]):
            app.player1Map[player1Row][player1Col] = 1


        app.player2Map = []
        for i in range(player2.playerMapSize):
            app.player2Map.append([0] * player2.playerMapSize)
        player2Row = int(player2.playery / player2.playerCellHeight)
        player2Col = int(player2.playerx / player2.playerCellWidth)
        if app.player2Map != [] and 0 <= player2Row <= len(app.player2Map) and 0 <= player2Col <= len(app.player2Map[0]):
            app.player2Map[player2Row][player2Col] = 1
    
    if player1.playerHealthBoost[0] == True:
        player1.playerHealthBoost[1] += 1
        if player1.playerHealthBoost[1] >= 10:
            player1.playerHealthBoost = [False, 0]

    if player2.playerHealthBoost[0] == True:
        player2.playerHealthBoost[1] += 1
        if player2.playerHealthBoost[1] >= 10:
            player2.playerHealthBoost = [False, 0]
    
    if player1.playerShield[0] == True:
        player1.playerShield[1] += 1
        if player1.playerShield[1] >= 100:
            player1.playerShield = [False, 0]

    if player2.playerShield[0] == True:
        player2.playerShield[1] += 1
        if player2.playerShield[1] >= 100:
            player2.playerShield = [False, 0]

    if player1.player == True and (player1.win == True or player1.playerHealth <= 0):
        print('hi')
        app.sound.pause()
    
    if player2.player == True and (player1.win == True or player2.win == True or (player1.playerHealth <= 0 and player2.playerHealth <= 0)):
        app.sound.pause()

def chestOpener(app, somePlayer, i):
    swordSelector = random.randint(1, 100)
    print(swordSelector)
    if swordSelector < 86:
        somePlayer.sword = True
        somePlayer.sword = True
        somePlayer.woodenSword = False
        somePlayer.stoneSword = False
        somePlayer.ironSword = False
        somePlayer.goldenSword = False
        somePlayer.diamondSword = False
        somePlayer.currSword = None
    chestCol = math.floor(app.chests[i][0] / app.chestMapCellWidth)
    chestRow = math.floor(app.chests[i][1] / app.chestMapCellHeight)
    if swordSelector <= 25:
        somePlayer.woodenSword = True
        if 'wood' not in somePlayer.collectedSwords:
            somePlayer.collectedSwords.append('wood')
        somePlayer.currSword = 'wood'
    if swordSelector >= 26 and swordSelector <= 55:
        somePlayer.stoneSword = True
        if 'stone' not in somePlayer.collectedSwords:
            somePlayer.collectedSwords.append('stone')
        somePlayer.currSword = 'stone'
    if swordSelector >= 56 and swordSelector <= 70:
        somePlayer.ironSword = True
        if 'iron' not in somePlayer.collectedSwords:
            somePlayer.collectedSwords.append('iron')
        somePlayer.currSword = 'iron'
    if swordSelector >= 71 and swordSelector <= 80:
        somePlayer.goldenSword = True
        if 'gold' not in somePlayer.collectedSwords:
            somePlayer.collectedSwords.append('gold')
        somePlayer.currSword = 'gold'
    if swordSelector >= 81 and swordSelector <= 85:
        somePlayer.diamondSword = True
        if 'diamond' not in somePlayer.collectedSwords:
            somePlayer.collectedSwords.append('diamond')
        somePlayer.currSword = 'diamond'
    if swordSelector >= 86 and swordSelector <= 95:
        somePlayer.playerHealth = 500
        somePlayer.playerHealthBoost = [True, 0]
    if swordSelector >= 96:
        somePlayer.playerShield = [True, 0]
    print(somePlayer.collectedSwords)
    app.chestMap[chestRow][chestCol] = 0
    if app.build == True:
        for rowdy in range(-10, 10):
            for coldx in range(-10, 10):
                if app.chestMap[chestRow + rowdy][chestCol + coldx] == 1:
                    app.chestMap[chestRow + rowdy][chestCol + coldx] = 0
                    print('chest removed')
    print(chestRow, chestCol)
    for row in range(len(app.chestMap)):
        for col in range(len(app.chestMap[0])):
            if app.chestMap[row][col] == 1:
                print(row, col)
    app.chests.pop(i)

    
def onMousePress(app, mouseX, mouseY):
    if isinstance(app.placeWall, list) and app.placeWall[0] == True:
        app.placeWall[1] = mouseX
        app.placeWall[2] = mouseY
        if app.buildMap == []:
                for row in range(int(app.userInput)):
                    app.buildMap.append([0] * int(app.userInput))
                # making sure that first and last rows are closed
                firstAndLastRow = [1] * int(app.userInput)
                app.buildMap.pop(0)
                app.buildMap.insert(0, firstAndLastRow)
                app.buildMap.pop()
                app.buildMap.append(firstAndLastRow)
                # making sure that first and last columns are closed
                for row in range(int(app.userInput)):
                    app.buildMap[row][0] = 1
                    app.buildMap[row][-1] = 1
        if app.walls == []:
                app.walls.append((0,0))
                for row in range(int(app.userInput)):
                    app.walls.append((row, 0))
                    app.walls.append((row, int(app.userInput) - 1))
                for col in range(int(app.userInput) - 2):
                    app.walls.append((0, col + 1))
                    app.walls.append((int(app.userInput) - 1, col + 1))
        cellDisplaySize = 400 / int(app.userInput)
        leftDistance = app.screenWidth / 2 - 200
        topDistance = app.screenHeight / 2 - 175
        if app.placeWall[0] == True and app.placeWall[1] >= (app.screenWidth / 2 - 200) and app.placeWall[1] <= (app.screenWidth / 2 - 200 + 400) and app.placeWall[2] >= (app.screenHeight / 2 - 175) and app.placeWall[2] <= (app.screenHeight / 2 - 175 + 400):
                app.placeMove.append('wall')
                row = math.floor((app.placeWall[2] - topDistance) / cellDisplaySize)
                col = math.floor((app.placeWall[1] - leftDistance) / cellDisplaySize)
                counter = 0
                for i in range (len(app.spawningLocations)):
                    if row == app.spawningLocations[i][4] and col == app.spawningLocations[i][5]:
                        counter += 1
                if counter == 0:
                    app.walls.append((row, col))
        row = math.floor((app.placeWall[2] - topDistance) / cellDisplaySize)
        col = math.floor((app.placeWall[1] - leftDistance) / cellDisplaySize)
        if 0 <= row <= int(app.userInput) and 0 <= col <= int(app.userInput):
            counter = 0
            for i in range (len(app.spawningLocations)):
                if row == app.spawningLocations[i][4] and col == app.spawningLocations[i][5]:
                    counter += 1
            if counter == 0:
                app.buildMap[row][col] = 1
            

    if isinstance(app.placeExit, list) and app.placeExit[0] == True:
        app.placeExit[1] = mouseX
        app.placeExit[2] = mouseY
        if app.buildMap == []:
            for row in range(int(app.userInput)):
                app.buildMap.append([0] * int(app.userInput))
            # making sure that first and last rows are closed
            firstAndLastRow = [1] * int(app.userInput)
            app.buildMap.pop(0)
            app.buildMap.insert(0, firstAndLastRow)
            app.buildMap.pop()
            app.buildMap.append(firstAndLastRow)
            # making sure that first and last columns are closed
            for row in range(int(app.userInput)):
                app.buildMap[row][0] = 1
                app.buildMap[row][-1] = 1
        cellDisplaySize = 400 / int(app.userInput)
        leftDistance = app.screenWidth / 2 - 200
        topDistance = app.screenHeight / 2 - 175
        row = math.floor((app.placeExit[2] - topDistance) / cellDisplaySize)
        col = math.floor((app.placeExit[1] - leftDistance) / cellDisplaySize)
        if app.buildMap != [] and 0 <= row <= int(app.userInput) and 0 <= col <= int(app.userInput):
            app.buildMap[row][col] = 0
            count = 0
            for row in range(int(app.userInput)):
                if app.buildMap[row][0] == 0:
                    count += 1
                if app.buildMap[row][-1] == 0:
                    count += 1
            for col in range(int(app.userInput)):
                if app.buildMap[0][col] == 0:
                    count += 1
                if app.buildMap[-1][col] == 0:
                    count += 1
            print(count)
        if app.placeExit[0] == True and app.placeExit[1] >= (app.screenWidth / 2 - 200) and app.placeExit[1] <= (app.screenWidth / 2 - 200 + 400) and app.placeExit[2] >= (app.screenHeight / 2 - 175) and app.placeExit[2] <= (app.screenHeight / 2 - 175 + 400):
                app.placeMove.append('exit')
                row = math.floor((app.placeExit[2] - topDistance) / cellDisplaySize)
                col = math.floor((app.placeExit[1] - leftDistance) / cellDisplaySize)
                if row == 0 or col == 0 or row == int(app.userInput) -1 or col == int(app.userInput) - 1:
                    app.exit.append((row, col))

    if isinstance(app.placeMonster, list) and app.placeMonster[0] == True:
        app.placeMonster[1] = mouseX
        app.placeMonster[2] = mouseY
        if app.buildMap == []:
            for row in range(int(app.userInput)):
                app.buildMap.append([0] * int(app.userInput))
            # making sure that first and last rows are closed
            firstAndLastRow = [1] * int(app.userInput)
            app.buildMap.pop(0)
            app.buildMap.insert(0, firstAndLastRow)
            app.buildMap.pop()
            app.buildMap.append(firstAndLastRow)
            # making sure that first and last columns are closed
            for row in range(int(app.userInput)):
                app.buildMap[row][0] = 1
                app.buildMap[row][-1] = 1
        if app.buildMonsterMap == []:
            for row in range(int(app.userInput) * 8):
                app.buildMonsterMap.append([0] * int(app.userInput) * 8)
        randomMove = random.randint(1, 4)
        if mouseX >= (app.screenWidth / 2 - 200) and mouseX <= (app.screenWidth /2 - 200 + 400) and mouseY >= (app.screenHeight / 2 - 175) and mouseY <= (app.screenHeight / 2 - 175 + 400):
            app.placeMove.append('monster')
            app.buildMonsters.append([mouseX, mouseY, randomMove, app.monsterHealth])
        cellDisplaySize = 400 / int(app.userInput)
        leftDistance = app.screenWidth / 2 - 200
        topDistance = app.screenHeight / 2 - 175
        for i in range(len(app.buildMonsters)):
            buildMonsterRow = math.floor((app.buildMonsters[i][1] - topDistance) / (cellDisplaySize / 8))
            buildMonsterCol = math.floor((app.buildMonsters[i][0] - leftDistance) / (cellDisplaySize / 8))
            if 0 <= buildMonsterRow <= int(app.userInput) * 8 and 0 <= buildMonsterCol <= int(app.userInput) * 8:
                app.buildMonsterMap[buildMonsterRow][buildMonsterCol] = 1
    

    if isinstance(app.placeChest, list) and app.placeChest[0] == True:
        app.placeChest[1] = mouseX
        app.placeChest[2] = mouseY
        if app.buildMap == []:
            for row in range(int(app.userInput)):
                app.buildMap.append([0] * int(app.userInput))
            # making sure that first and last rows are closed
            firstAndLastRow = [1] * int(app.userInput)
            app.buildMap.pop(0)
            app.buildMap.insert(0, firstAndLastRow)
            app.buildMap.pop()
            app.buildMap.append(firstAndLastRow)
            # making sure that first and last columns are closed
            for row in range(int(app.userInput)):
                app.buildMap[row][0] = 1
                app.buildMap[row][-1] = 1
        if app.buildChestMap == []:
            for row in range(int(app.userInput) * 16):
                app.buildChestMap.append([0] * int(app.userInput) * 16)
                # app.buildChestMapCopy = app.buildChestMap
        if mouseX >= (app.screenWidth / 2 - 200) and mouseX <= (app.screenWidth /2 - 200 + 400) and mouseY >= (app.screenHeight / 2 - 175) and mouseY <= (app.screenHeight / 2 - 175 + 400):
            app.placeMove.append('chest')
            dx = mouseX - (app.screenWidth / 2 - 200)
            dy = mouseY - (app.screenHeight / 2 - 175)
            percentx = dx / 400
            percenty = dy / 400
            app.buildChests.append([mouseX, mouseY, percentx, percenty])
            # app.buildChestsCopy = app.buildChests
        cellDisplaySize = 400 / int(app.userInput)
        leftDistance = app.screenWidth / 2 - 200
        topDistance = app.screenHeight / 2 - 175
        for i in range(len(app.buildChests)):
            buildChestRow = math.floor((app.buildChests[i][1] - topDistance) / (cellDisplaySize / 16))
            buildChestCol = math.floor((app.buildChests[i][0] - leftDistance) / (cellDisplaySize / 16))
            if 0 <= buildChestRow <= int(app.userInput) * 16 and 0 <= buildChestCol <= int(app.userInput) * 16:
                app.buildChestMap[buildChestRow][buildChestCol] = 1

    if isinstance(app.placeSpawn, list) and app.placeSpawn[0] == True:
        cellDisplaySize = 400 / int(app.userInput)
        leftDistance = app.screenWidth / 2 - 200
        topDistance = app.screenHeight / 2 - 175
        if app.buildMap == []:
            for row in range(int(app.userInput)):
                app.buildMap.append([0] * int(app.userInput))
            # making sure that first and last rows are closed
            firstAndLastRow = [1] * int(app.userInput)
            app.buildMap.pop(0)
            app.buildMap.insert(0, firstAndLastRow)
            app.buildMap.pop()
            app.buildMap.append(firstAndLastRow)
            # making sure that first and last columns are closed
            for row in range(int(app.userInput)):
                app.buildMap[row][0] = 1
                app.buildMap[row][-1] = 1
        row = math.floor((mouseY - topDistance) / cellDisplaySize)
        col = math.floor((mouseX - leftDistance) / cellDisplaySize)
        print(row, col)
        print(len(app.buildMap), len(app.buildMap[0]))
        if 0 <= row <= len(app.buildMap) and 0 <= col <= len(app.buildMap[0]) and app.buildMap[row][col] != 1 and (row, col) not in app.walls:
            if mouseX >= (app.screenWidth / 2 - 200) and mouseX <= (app.screenWidth /2 - 200 + 400) and mouseY >= (app.screenHeight / 2 - 175) and mouseY <= (app.screenHeight / 2 - 175 + 400):
                    app.placeMove.append('spawn')
                    fractionx = mouseX - app.screenWidth / 2
                    fractiony = mouseY - app.screenHeight / 2
                    fractionx = (fractionx + 200) / 400
                    fractiony = (fractiony + 175) / 400
                    app.spawningLocations.append((mouseX, mouseY, fractionx, fractiony, row, col))
    
    if mouseX >= (app.screenWidth / 2 + 300) and mouseX <= (app.screenWidth / 2 + 400) and mouseY >= (app.screenHeight / 2 + 25) and mouseY <= (app.screenHeight / 2 + 125) and len(app.placeMove) > 0:
        cellDisplaySize = 400 / int(app.userInput)
        leftDistance = app.screenWidth / 2 - 200
        topDistance = app.screenHeight / 2 - 175
        if app.placeMove[-1] == 'wall':
            rowPop = app.walls[-1][0]
            colPop = app.walls[-1][1]
            app.walls.pop()
            app.buildMap[rowPop][colPop] = 0
        elif app.placeMove[-1] == 'exit':
            rowPop = app.exit[-1][0]
            colPop = app.exit[-1][1]
            print(len(app.exit))
            app.exit.pop()
            print(len(app.exit))
            app.buildMap[rowPop][colPop] = 1
        elif app.placeMove[-1] == 'monster':
            rowCoordinate = app.buildMonsters[-1][1]
            colCoordinate = app.buildMonsters[-1][0]
            popRow = math.floor((rowCoordinate - topDistance) / (cellDisplaySize / 8))
            popCol = math.floor((colCoordinate - leftDistance) / (cellDisplaySize / 8))
            app.buildMonsters.pop()
            app.buildMonsterMap[popRow][popCol] = 0
        elif app.placeMove[-1] == 'chest':
            rowCoordinate = app.buildChests[-1][1]
            colCoordinate = app.buildChests[-1][0]
            popRow = math.floor((rowCoordinate - topDistance) / (cellDisplaySize / 16)) 
            popCol = math.floor((colCoordinate - leftDistance) / (cellDisplaySize / 16))
            app.buildChests.pop()
            app.buildChestMap[popRow][popCol] = 0
        elif app.placeMove[-1] == 'spawn':
            app.spawningLocations.pop()
        app.placeMove.pop()
        app.placeWall = False
        app.placeExit = False
        app.placeMonster = False
        app.placeChest = False
        app.placeSpawn = False

    if app.build == True and app.buildDone == True:
        if mouseX >= (app.screenWidth / 2 - 425) and mouseX <= (app.screenWidth / 2 - 425 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100):
            print('Place Walls')
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.placeSpawn = False
            app.placeWall = [True, mouseX, mouseY]
        if mouseX >= (app.screenWidth / 2 - 300) and mouseX <= (app.screenWidth / 2 - 300 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100):
            print('Place Exit')
            app.placeMonster = False
            app.placeChest = False
            app.placeWall = False
            app.placeSpawn = False
            app.placeExit = [True, mouseX, mouseY]
        if mouseX >= (app.screenWidth / 2 - 175) and mouseX <= (app.screenWidth / 2 - 175 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100):
            print('Place Monsters')
            app.placeWall = False
            app.placeChest = False
            app.placeSpawn = False
            app.placeMonster = [True, mouseX, mouseY]
            app.placeExit = False
        if mouseX >= (app.screenWidth / 2 - 50) and mouseX <= (app.screenWidth / 2 - 50 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100):
            print('Place Chests')
            app.placeWall = False
            app.placeMonster = False
            app.placeSpawn = False
            app.placeChest = [True, mouseX, mouseY]
            app.placeExit = False
        if mouseX >= (app.screenWidth / 2 + 75) and mouseX <= (app.screenWidth / 2 + 75 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100) and len(app.spawningLocations) == 1:
            print('Play One Player')
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.placeSpawn = False
            app.build = True
            app.walls = []
            app.buildChestsCopy = copy.deepcopy(app.buildChests)
            app.buildChestMapCopy = copy.deepcopy(app.buildChestMap)
            app.placeMove = []
            onePlayerInitializer(app)
            app.selectDone = True
        if mouseX >= (app.screenWidth / 2 + 200) and mouseX <= (app.screenWidth / 2 + 200 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100) and len(app.spawningLocations) > 1:
            print('Play Two Player')
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.placeSpawn = False
            app.build = True
            app.walls = []
            app.build = True
            player1.player = False
            player2.player = True
            player1.initializer = False
            player2.initializer = False
            app.buildChestsCopy = copy.deepcopy(app.buildChests)
            app.buildChestMapCopy = copy.deepcopy(app.buildChestMap)
            app.placeMove = []
            twoPlayerInitializer(app)
            app.selectDone = True
        if mouseX >= (app.screenWidth / 2 + 325) and mouseX <= (app.screenWidth / 2 + 325 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100):
            print('Place Spawning Locations')
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.placeSpawn = [True, mouseX, mouseY]
    if app.home == True:
        reset(app)
        player1.playerEnd = False
        if mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) + 150 and mouseY >= (app.screenHeight / 2) - 150 and mouseY <= (app.screenHeight / 2) - 50:
            app.home = False
            player1.player = True
            player1.initializer = True
            player2.initializer = False
            app.buildDone = False
            reset(app)
            player2.player = False
            app.build = False
            player1.playerEnd = False
            player1.win = False
            player1.playerAlive = True
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.walls = []
            app.exit = []
            app.buildMap = []
        elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) + 150 and mouseY >= (app.screenHeight / 2) and mouseY <= (app.screenHeight / 2) + 100:
            reset(app)
            app.home = False
            player1.player = False
            player2.player = True
            app.build = False
            player1.playerEnd = False
            player1.win = False
            player1.playerAlive = True
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            player2.initializer = True
            app.walls = []
            app.exit = []
            app.buildMap = []
        elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) + 150 and mouseY >= (app.screenHeight / 2) + 150 and mouseY <= (app.screenHeight / 2) + 250:
            reset(app)
            app.home = False
            player1.player = False
            player2.player = False
            app.build = True
            player1.playerEnd = False
            player1.win = False
            player1.playerAlive = True
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            player2.initializer = False
            app.walls = []
            app.exit = []
            app.buildMap = []

    elif player1.player == True and player1.playerEnd == True and app.build == False:
        if mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) - 150 and mouseY <= (app.screenHeight / 2) - 150 + 100:
            app.home = False
            player1.player = True
            player2.player = False
            app.build = False
            player1.initializer = False
            player1.win = False
            player1.playerAlive = True
            reset(app)
            app.sound = Sound(app.backgroundurl)
            app.sound.play(loop = True)
            player1.playerEnd = False
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.walls = []
            app.exit = []
            app.buildMap = []
        elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2 ) - 150 + 300 and mouseY >= (app.screenHeight / 2) and mouseY <= (app.screenHeight / 2) + 100:
            app.home = True
            player1.player = False
            player2.player = False
            app.build = False
            player1.initializer = False
            player1.win = False
            player1.playerAlive = True
            player1.playerEnd = False
            reset(app)
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.walls = []
            app.exit = []
            app.buildMap = []
        elif mouseX >= ((app.screenWidth / 2) - 150) and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) + 150 and mouseY <= (app.screenHeight / 2) + 150 + 100:
            app.home = False
            player1.player = True
            player2.player = False
            app.build = False
            player1.initializer = True
            player1.win = False
            player1.playerAlive = True
            player1.playerEnd = False
            reset(app)
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.walls = []
            app.exit = []
            app.buildMap = []

    elif player1.player == True and player1.playerEnd == True and app.build == True:
        if mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) - 150 and mouseY <= (app.screenHeight / 2) - 150 + 100:
            app.home = False
            player1.player = True
            player2.player = False
            app.build = True
            player1.initializer = False
            player1.win = False
            player1.playerAlive = True
            app.buildChestMap = copy.copy(app.buildChestMapCopy)
            app.buildChests = copy.copy(app.buildChestsCopy)
            reset(app)
            app.sound = Sound(app.backgroundurl)
            app.sound.play(loop = True)
            player1.playerEnd = False
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.selectDone = True
        elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2 ) - 150 + 300 and mouseY >= (app.screenHeight / 2) and mouseY <= (app.screenHeight / 2) + 100:
            app.home = True
            player1.player = False
            player2.player = False
            app.build = False
            player1.initializer = False
            player1.win = False
            player1.playerAlive = True
            player1.playerEnd = False
            reset(app)
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.walls = []
            app.exit = []
            app.buildMap = []
            app.userInput = ""
            app.buildMonsters = []
            app.buildMonsterMap = []
            app.buildChests = []
            app.buildChestMap = []
            app.walls = []
            app.spawningLocations = []
            app.placeWall = False
            app.placeExit = False
            app.placeMonster = False
            app.placeChest = False
            app.placeSpawn = False
            app.selectDone = False
            reset(app)
        elif mouseX >= ((app.screenWidth / 2) - 150) and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) + 150 and mouseY <= (app.screenHeight / 2) + 150 + 100:
            reset(app)
            app.home = False
            player1.player = False
            player2.player = False
            app.build = True
            player1.playerEnd = False
            player1.win = False
            player1.playerAlive = True
            app.buildDone = False
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.placeSpawn = False
            app.walls = []
            app.exit = []
            app.buildMap = []
            app.userInput = ""
            app.buildMonsters = []
            app.buildMonsterMap = []
            app.buildChests = []
            app.buildChestMap = []
            app.walls = []
            app.spawningLocations = []
            app.selectDone = False
            reset(app)

    # play again, return home, play a different level
    elif player2.player == True and player2.initializer == False and app.build == False:
        if (player1.win == True and player2.win == False) or (player2.win == True and player1.win == False) or ((player1.playerAlive == False or player1.playerEnd == True or player1.playerHealth <= 0) and (player2.playerAlive == False or player2.playerEnd == True or player2.playerHealth <= 0)):
            if mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) - 150 and mouseY <= (app.screenHeight / 2) - 150 + 100:
                if app.build == False:
                    app.userInput = ""
                    app.exit = []
                app.home = False
                player1.player = False
                player2.player = True
                app.build = False
                player1.initializer = False
                player1.win = False
                player2.win = False
                player1.playerAlive = True
                player2.playerAlive = True
                reset(app)
                app.sound = Sound(app.backgroundurl)
                app.sound.play(loop = True)
                player1.playerEnd = False
                player2.playerEnd = False
                player1.playerHealth = 500
                player2.playerHealth = 500
                app.buildDone = False
                app.placeWall = False
                app.placeMonster = False
                app.placeChest = False
                app.placeExit = False
                app.walls = []
                app.buildMap = []
            elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) and mouseY <= (app.screenHeight / 2) + 100:
                print('hi')
                app.home = True
                player1.player = False
                player2.player = False
                app.build = False
                player1.initializer = False
                player2.initializer = False
                player1.win = False
                player2.win = False
                player1.playerAlive = True
                player1.playerEnd = False
                player1.playerHealth = 500
                player2.playerAlive = True
                player2.playerEnd = False
                player2.playerHealth = 500
                player2.playerLevel = None
                reset(app)
                app.buildDone = False
                app.placeWall = False
                app.placeMonster = False
                app.placeChest = False
                app.placeExit = False
                app.walls = []
                app.exit = []
                app.buildMap = []
                app.userInput = ""
            elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) + 150 and mouseY <= (app.screenHeight / 2) + 150 + 100:
                app.home = False
                player1.player = False
                player2.player = True
                app.build = False
                player1.initializer = False
                player2.initializer = True
                player1.win = False
                player2.win = False
                player1.playerAlive = True
                player2.playerAlive = True
                player1.playerEnd = False
                player2.playerEnd = False
                player1.playerHealth = 500
                player2.playerHealth = 500
                player2.playerLevel = None
                reset(app)
                app.buildDone = False
                app.placeWall = False
                app.placeMonster = False
                app.placeChest = False
                app.placeExit = False
                app.walls = []
                app.exit = []
                app.buildMap = []
                app.userInput = ""
    
    elif player2.player == True and player2.initializer == False and app.build == True:
        if (player1.win == True and player2.win == False) or (player2.win == True and player1.win == False) or ((player1.playerAlive == False or player1.playerEnd == True or player1.playerHealth <= 0) and (player2.playerAlive == False or player2.playerEnd == True or player2.playerHealth <= 0)):
            if mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) - 150 and mouseY <= (app.screenHeight / 2) - 150 + 100:
                app.home = False
                player1.player = False
                player2.player = True
                app.build = True
                player1.initializer = False
                player2.initializer = False
                player1.win = False
                player2.win = False
                player1.playerAlive = True
                player2.playerAlive = True
                app.buildChestMap = copy.deepcopy(app.buildChestMapCopy)
                app.buildChests = copy.deepcopy(app.buildChestsCopy)
                reset(app)
                app.sound = Sound(app.backgroundurl)
                app.sound.play(loop = True)
                player1.playerEnd = False
                player2.playerEnd = False
                player1.playerHealth = 500
                player2.playerHealth = 500
                app.buildDone = False
                app.placeWall = False
                app.placeMonster = False
                app.placeChest = False
                app.placeExit = False
                app.selectDone = True
                app.walls = []
                app.buildMap = []
            elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) and mouseY <= (app.screenHeight / 2) + 100:
                print('hi')
                app.home = True
                player1.player = False
                player2.player = False
                app.build = False
                player1.initializer = False
                player2.initializer = False
                player1.win = False
                player2.win = False
                player1.playerAlive = True
                player1.playerEnd = False
                player1.playerHealth = 500
                player2.playerAlive = True
                player2.playerEnd = False
                player2.playerHealth = 500
                player2.playerLevel = None
                reset(app)
                app.buildDone = False
                app.placeWall = False
                app.placeMonster = False
                app.placeChest = False
                app.placeExit = False
                app.placeSpawn = False
                app.walls = []
                app.exit = []
                app.buildMonsters = []
                app.buildMonsterMap = []
                app.monsters = []
                app.buildChests = []
                app.buildChestMap = []
                app.buildMap = []
                app.spawningLocations = []
                app.userInput = ""
                app.selectDone = False
            elif mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) + 150 and mouseY <= (app.screenHeight / 2) + 150 + 100:
                app.home = False
                player1.player = False
                player2.player = False
                app.build = True
                player1.initializer = False
                player2.initializer = False
                player1.win = False
                player2.win = False
                player1.playerAlive = True
                player2.playerAlive = True
                player1.playerEnd = False
                player2.playerEnd = False
                player1.playerHealth = 500
                player2.playerHealth = 500
                player2.playerLevel = None
                reset(app)
                app.buildDone = False
                app.placeWall = False
                app.placeMonster = False
                app.placeChest = False
                app.placeExit = False
                app.placeSpawn = False
                app.walls = []
                app.exit = []
                app.buildMap = []
                app.userInput = ""
                app.buildMonsters = []
                app.buildMonsterMap = []
                app.buildChests = []
                app.buildChestMap = []
                app.spawningLocations = []
                app.selectDone = False
                reset(app)

   
    elif player1.player == True and player1.initializer == True:
        player1.playerEnd = False
        player1.win = False
        player1.playerAlive = True
        widths = [-400, -250, -100, 50, 200, 350]
        for i in range(3):
            for j in range(6):
                if player1.playerLevel == None:
                    player1.playerLevel = 1
                elif player1.playerLevel != None:
                    player1.playerLevel += 1
                if mouseX >= ((app.screenWidth / 2) + widths[j]) and mouseX <= ((app.screenWidth / 2) + widths[j] + 75) and mouseY >= (app.screenHeight / 2) - (175 - 150*i) and mouseY <= (app.screenHeight / 2) - (175 - 150*i) + 75:
                    # print('hi')
                    onePlayerInitializer(app)
                    break
        if mouseX >= ((app.screenWidth / 2) - 100) and mouseX <= (app.screenWidth / 2) - 100 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player1.playerLevel = 19
            onePlayerInitializer(app)
        elif mouseX >= ((app.screenWidth / 2) + 50) and mouseX <= (app.screenWidth / 2) + 50 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player1.playerLevel = 20
            onePlayerInitializer(app)

    elif player2.player == True and player2.initializer == True:
        player2.playerEnd = True
        player2.win = False
        player2.playerAlive = True
        widths = [-400, -250, -100, 50, 200, 350]
        for i in range(3):
            for j in range(6):
                if player2.playerLevel == None:
                    player2.playerLevel = 1
                elif player2.playerLevel != None:
                    player2.playerLevel += 1
                if mouseX >= ((app.screenWidth / 2) + widths[j]) and mouseX <= ((app.screenWidth / 2) + widths[j] + 75) and mouseY >= (app.screenHeight / 2) - (175 - 150*i) and mouseY <= (app.screenHeight / 2) - (175 - 150*i) + 75:
                    # print('hi')
                    twoPlayerInitializer(app)
                    break
        if mouseX >= ((app.screenWidth / 2) - 100) and mouseX <= (app.screenWidth / 2) - 100 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player2.playerLevel = 19
            twoPlayerInitializer(app)
        elif mouseX >= ((app.screenWidth / 2) + 50) and mouseX <= (app.screenWidth / 2) + 50 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player2.playerLevel = 20
            twoPlayerInitializer(app)


    if player1.player == True or player2.player == True:
        if player1.sword == True:
            player1.swing = True
            i = 0
            while i != len(app.monsters):
                if distance(app.monsters[i][0], app.monsters[i][1], player1.playerx, player1.playery) < 45:
                    if player1.woodenSword == True:
                        app.monsters[i][3] -= 1
                    if player1.stoneSword == True:
                        app.monsters[i][3] -= 2
                    if player1.ironSword == True:
                        app.monsters[i][3] -= 3
                    if player1.goldenSword == True:
                        app.monsters[i][3] -= 5
                    if player1.diamondSword == True:
                        app.monsters[i][3] -= 10
                    if app.monsters[i][3] <= 0:
                        app.monsters.pop(i)
                        continue
                i += 1


            if player2.player == True:
                if distance(player1.playerx, player1.playery, player2.playerx, player2.playery) < 45:
                    if player2.playerShield[0] == False:
                        player2.playerHealth -= 50
                if player2.playerHealth <= 0:
                    player2.playerAlive = False
                    player2.playerEnd = True
                print(player2.playerHealth)


def onePlayerInitializer(app):
    if app.userInput == "":
        app.mapSize = player1.playerLevel + 5
    if app.userInput != "":
        app.mapSize = int(app.userInput)
        for row in range(int(app.userInput)):
            app.buildMap[row].append(1)
        app.buildMap.append([1] * int(app.userInput))
        for exit in app.exit:
            row = exit[0]
            col = exit[1]
            if row == int(app.userInput) - 1:
                app.buildMap[row][col] = 0
    if player1.playerLevel == None:
        app.monsterCount = len(app.buildMonsters)
        app.chestCount = len(app.buildChests)
    if player1.playerLevel != None:
        app.monsterCount = int(app.mapSize * player1.playerLevel * 0.2)
        if player1.playerLevel < 10:
            app.chestCount = int(player1.playerLevel * 0.5) + (10 - player1.playerLevel)
        else:
            app.chestCount = int(player1.playerLevel * 0.5)
        if player1.playerLevel < 8:
            player1.playery = (app.screenHeight / 2) / 2
    player1.player = True
    player1.initializer = False
    player1.playerEnd = False
    reset(app)
    app.sound = Sound(app.backgroundurl)
    app.sound.play(loop = True)

def twoPlayerInitializer(app):
    if app.userInput == "":
        app.mapSize = player2.playerLevel + 5
        app.monsterCount = int(app.mapSize * player2.playerLevel * 0.2)
        if player2.playerLevel < 10:
            app.chestCount = int(player2.playerLevel * 0.5) + (10 - player2.playerLevel)
        else:
            app.chestCount = int(player2.playerLevel * 0.5)
        if player2.playerLevel < 8:
            player1.playery = (app.screenHeight / 2) / 2
        player2.player = True
        player1.win = False
        player2.win = False
        player1.playerAlive = True
        player2.playerAlive = True
        app.PlayerEnd = False
        player2.initializer = False
        player2.playerEnd = False
        reset(app)
    if app.userInput != "":
        app.mapSize = int(app.userInput)
        for row in range(int(app.userInput)):
            app.buildMap[row].append(1)
        app.buildMap.append([1] * int(app.userInput))
        for exit in app.exit:
            row = exit[0]
            col = exit[1]
            if row == int(app.userInput) - 1:
                app.buildMap[row][col] = 0
        app.map = app.buildMap
        app.monsterCount = len(app.buildMonsters)
        app.chestCount = len(app.buildChests)
        player2.player = True
        player1.player = False
        player1.win = False
        player2.win = False
        player1.playerAlive = True
        player2.playerAlive = True
        app.PlayerEnd = False
        player2.initializer = False
        player2.playerEnd = False
        reset(app)
    app.sound = Sound(app.backgroundurl)
    app.sound.play(loop = True)

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
def newRandomDirectionProvider(app, i):
    currentDirection = app.monsters[i][2]
    newRandomDirection = currentDirection
    while newRandomDirection == currentDirection:
        randomMoveDirection = random.randint(1, 4)
        newRandomDirection = randomMoveDirection
    return newRandomDirection

def onePlayerInExit(app):
    if app.exitRow == 0:
        playerRow = math.floor(player1.playery * 2 / app.cellHeight) 
        playerCol = math.floor(player1.playerx / app.cellWidth)
        if playerRow == 0 and playerCol == app.exitCol:
            return True
        return False
    if app.exitRow != 0:
        playerRow = math.floor(player1.playery / app.cellHeight) 
        playerCol = math.floor(player1.playerx / app.cellWidth)
        for i in range(len(app.exitRow)):
            if playerRow == app.exitRow[i] and playerCol == app.exitCol[i]:
                return True
        return False
    
def twoPlayerInExit(app):
    if app.exit == []:
        twoPlayerRow = math.floor(player2.playery * 2 / app.cellHeight) 
        twoPlayerCol = math.floor(player2.playerx / app.cellWidth)
        if twoPlayerRow == 0 and twoPlayerCol == app.exitCol:
            return True
        return False
    if app.exit != []:
        twoPlayerRow = math.floor(player2.playery / app.cellHeight) 
        twoPlayerCol = math.floor(player2.playerx / app.cellWidth)
        print(twoPlayerRow, twoPlayerCol)
        for i in range(len(app.exit)):
            if twoPlayerRow == app.exitRow[i] and twoPlayerCol == app.exitCol[i]:
                print('hi')
                return True
        return False


def main():
    runApp(width = 900, height = 900)

main()