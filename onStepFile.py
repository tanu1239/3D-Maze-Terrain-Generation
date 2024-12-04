import sys
import math
from cmu_graphics import *
import random
import copy

from generatorFile import monsterMapGenerator


def stepper(app, player1, player2):
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


def newRandomDirectionProvider(app, i):
    currentDirection = app.monsters[i][2]
    newRandomDirection = currentDirection
    while newRandomDirection == currentDirection:
        randomMoveDirection = random.randint(1, 4)
        newRandomDirection = randomMoveDirection
    return newRandomDirection