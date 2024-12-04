import sys
import math
from cmu_graphics import *
import random
import copy


def drawer(app, player1, player2):

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
        darkBlue = rgb(0, 4, 253)
        lightBlue = rgb(0, 252, 246)
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