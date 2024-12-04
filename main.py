# ## packages
# import pygame
import sys
import math
from cmu_graphics import *
import random
import copy

from generatorFile import  mapGenerator, monsterMapGenerator, chestMapGenerator, reset
from DrawFile import drawer
from KeyFile import keyPresser, keyHolder
from onStepFile import stepper
from MousePressFile import mousePresser

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
    reset(app, player1, player2)

def redrawAll(app):
    drawer(app, player1, player2)

def onKeyPress(app, key):
    keyPresser(app, key, player1, player2)

def onKeyHold(app, keys):
    keyHolder(app, keys, player1, player2)

def onStep(app):
    stepper(app, player1, player2)

def onMousePress(app, mouseX, mouseY):
    mousePresser(app, mouseX, mouseY, player1, player2)

    
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    
def newRandomDirectionProvider(app, i):
    currentDirection = app.monsters[i][2]
    newRandomDirection = currentDirection
    while newRandomDirection == currentDirection:
        randomMoveDirection = random.randint(1, 4)
        newRandomDirection = randomMoveDirection
    return newRandomDirection

def main():
    runApp(width = 900, height = 900)

main()