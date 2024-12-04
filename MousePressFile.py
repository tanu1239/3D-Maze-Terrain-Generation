import sys
import math
from cmu_graphics import *
import random
import copy

from generatorFile import reset


def mousePresser(app, mouseX, mouseY, player1, player2):
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
            onePlayerInitializer(app, player1, player2)
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
            twoPlayerInitializer(app, player1, player2)
            app.selectDone = True
        if mouseX >= (app.screenWidth / 2 + 325) and mouseX <= (app.screenWidth / 2 + 325 + 100) and mouseY >= (app.screenHeight / 2 + 275) and mouseY <= (app.screenHeight / 2 + 275 + 100):
            print('Place Spawning Locations')
            app.placeWall = False
            app.placeMonster = False
            app.placeChest = False
            app.placeExit = False
            app.placeSpawn = [True, mouseX, mouseY]
    if app.home == True:
        reset(app, player1, player2)
        player1.playerEnd = False
        if mouseX >= (app.screenWidth / 2) - 150 and mouseX <= (app.screenWidth / 2) + 150 and mouseY >= (app.screenHeight / 2) - 150 and mouseY <= (app.screenHeight / 2) - 50:
            app.home = False
            player1.player = True
            player1.initializer = True
            player2.initializer = False
            app.buildDone = False
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
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
            reset(app, player1, player2)
        elif mouseX >= ((app.screenWidth / 2) - 150) and mouseX <= (app.screenWidth / 2) - 150 + 300 and mouseY >= (app.screenHeight / 2) + 150 and mouseY <= (app.screenHeight / 2) + 150 + 100:
            reset(app, player1, player2)
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
            reset(app, player1, player2)

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
                reset(app, player1, player2)
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
                reset(app, player1, player2)
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
                reset(app, player1, player2)
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
                reset(app, player1, player2)
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
                reset(app, player1, player2)
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
                reset(app, player1, player2)
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
                reset(app, player1, player2)

   
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
                    onePlayerInitializer(app, player1, player2)
                    break
        if mouseX >= ((app.screenWidth / 2) - 100) and mouseX <= (app.screenWidth / 2) - 100 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player1.playerLevel = 19
            onePlayerInitializer(app, player1, player2)
        elif mouseX >= ((app.screenWidth / 2) + 50) and mouseX <= (app.screenWidth / 2) + 50 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player1.playerLevel = 20
            onePlayerInitializer(app, player1, player2)

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
                    twoPlayerInitializer(app, player1, player2)
                    break
        if mouseX >= ((app.screenWidth / 2) - 100) and mouseX <= (app.screenWidth / 2) - 100 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player2.playerLevel = 19
            twoPlayerInitializer(app, player1, player2)
        elif mouseX >= ((app.screenWidth / 2) + 50) and mouseX <= (app.screenWidth / 2) + 50 + 75 and mouseY >= (app.screenHeight / 2) + 275 and mouseY <= (app.screenHeight / 2) + 275 + 75:
            player2.playerLevel = 20
            twoPlayerInitializer(app, player1, player2)


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


def onePlayerInitializer(app, player1, player2):
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
    reset(app, player1, player2)
    app.sound = Sound(app.backgroundurl)
    app.sound.play(loop = True)

def twoPlayerInitializer(app, player1, player2):
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
        reset(app, player1, player2)
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
        reset(app, player1, player2)
    app.sound = Sound(app.backgroundurl)
    app.sound.play(loop = True)
