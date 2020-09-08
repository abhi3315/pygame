import random
import sys
import pygame
from pygame.locals import *

fps = 32
screenWidth = 289
screenHeight = 511
screen = pygame.display.set_mode((screenWidth, screenHeight))
baseY = int(0.8*screenHeight)
gameSprites = {}
gameSounds = {}
player = 'images/bird.png'
background = 'images/background.png'
pipe = 'images/pipe.png'


def welcomeScreen():
    playerX = int(screenWidth/5)
    playerY = int((screenHeight-gameSprites['player'].get_height())/2)
    messageX = int((screenWidth-gameSprites['message'].get_width())/2)
    messageY = int(screenHeight*0.13)
    baseX = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                screen.blit(gameSprites['background'], (0, 0))
                screen.blit(gameSprites['player'], (playerX, playerY))
                screen.blit(gameSprites['message'], (messageX, messageY))
                screen.blit(gameSprites['base'], (baseX, baseY))
                pygame.display.update()
                clock.tick(fps)


def mainGame():
    score = 0
    playerX = int(screenWidth/5)
    playerY = int(screenWidth/2)
    baseX = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': screenWidth+200, 'y': newPipe1[0]['y']},
        {'x': screenWidth+200+int(screenWidth/2), 'y': newPipe2[0]['y']}
    ]
    lowerPipes = [
        {'x': screenWidth+200, 'y': newPipe1[1]['y']},
        {'x': screenWidth+200+int(screenWidth/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapV = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapV
                    playerFlapped = True
                    gameSounds['wing'].play()

        crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMinPos = playerX+gameSprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x']+gameSprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMinPos < pipeMidPos+4:
                score += 1
                print(f"Your score is {score}")
                gameSounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = gameSprites['player'].get_height()
        playerY = playerY+min(playerVelY, baseY - playerY-playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]['x'] < -gameSprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        screen.blit(gameSprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(gameSprites['pipe'][0],
                        (upperPipe['x'], upperPipe['y']))
            screen.blit(gameSprites['pipe'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        screen.blit(gameSprites['base'], (baseX, baseY))
        screen.blit(gameSprites['player'], (playerX, playerY))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += gameSprites['numbers'][digit].get_width()
        Xoffset = (screenWidth+width)/2

        for digit in myDigits:
            screen.blit(gameSprites['numbers'][digit],
                        (Xoffset, screenHeight*0.12))
            Xoffset += gameSprites['numbers'][digit].get_width()

        pygame.display.update()
        clock.tick(fps)


def getRandomPipe():
    pipeHeight = gameSprites['pipe'][0].get_height()
    offset = int(screenHeight/3)
    y2 = offset + random.randrange(
        0, int(screenHeight-gameSprites['base'].get_height()-1.2*offset))
    y1 = pipeHeight+offset-y2
    pipeX = screenWidth+10
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe


def isCollide(playerX, playerY, upperPipes, lowerPipes):
    if playerY > baseY-25 or playerY < 0:
        gameSounds['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = gameSprites['pipe'][0].get_height()
        pipeWidth = gameSprites['pipe'][0].get_width()
        if(playerY < pipeHeight+pipe['y'] and abs(playerX - pipe['x']) < pipeWidth):
            gameSounds['hit'].play()
            return True
    for pipe in lowerPipes:
        pipeHeight = gameSprites['pipe'][0].get_height()
        pipeWidth = gameSprites['pipe'][0].get_width()
        if(playerY+gameSprites['player'].get_height() > pipe['y'] and abs(playerX-pipe['x']) < pipeWidth):
            gameSounds['hit'].play()
            return True

    return False


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    gameSprites['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
    )
    gameSprites['message'] = pygame.image.load(
        'images/message.png').convert_alpha()
    gameSprites['base'] = pygame.image.load('images/base.png').convert_alpha()
    gameSprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )
    gameSprites['background'] = pygame.image.load(background).convert()
    gameSprites['player'] = pygame.image.load(player).convert_alpha()

    gameSounds['die'] = pygame.mixer.Sound('audio/die.wav')
    gameSounds['hit'] = pygame.mixer.Sound('audio/hit.wav')
    gameSounds['point'] = pygame.mixer.Sound('audio/point.wav')
    gameSounds['swoosh'] = pygame.mixer.Sound('audio/swoosh.wav')
    gameSounds['wing'] = pygame.mixer.Sound('audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
