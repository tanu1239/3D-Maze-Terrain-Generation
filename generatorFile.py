import random 
import math

def reset(app, player1, player2):
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