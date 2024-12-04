import sys
import math
from cmu_graphics import *
import random
import copy

def keyPresser(app, key, player1, player2):
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


def keyHolder(app, keys, player1, player2):
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
    
    checkIfNearbyMonsters(app, player1, player2)

    if onePlayerInExit(app, player1) == True:
        player1.win = True
        player1.playerLevel = None
        player1.playerEnd = True
    if player2.playerx != None and player2.playery != None:
        if twoPlayerInExit(app, player2) == True:
            player2.win = True
            player2.playerLevel = None
            player2.playerEnd = True

def checkIfNearbyMonsters(app, player1, player2):
    for monster in app.monsters:
        if distance(monster[0], monster[1], player1.playerx, player1.playery) < 20:
            if player1.playerShield[0] == False:
                player1.playerHealth -= 10
        if player2.playerx != None and player2.playery != None:
            if distance(monster[0], monster[1], player2.playerx, player2.playery) < 20:
                if player2.playerShield[0] == False:
                    player2.playerHealth -= 10
    return True




def onePlayerInExit(app, player1):
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
    
def twoPlayerInExit(app, player2):
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