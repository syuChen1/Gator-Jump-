
import pygame
import sys
from pygame.locals import *
import random

pygame.init() 

class GatorJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        self.background = pygame.transform.scale(pygame.image.load("img/bg2.jpg"), (600, 800))
        self.player = pygame.transform.scale(pygame.image.load("img/gatorRight.png"), (80, 100))
        self.platformStation = pygame.transform.scale(pygame.image.load("img/platform.png"), (75, 15))
        self.platformMove = pygame.transform.scale(pygame.image.load("img/bird1.png"), (75, 15))
        self.spring = pygame.transform.scale(pygame.image.load("img/spring.png"), (15, 10))
        self.playerX = 250
        self.playerY = 600
        self.jump = 0
        self.gravity = 0
        self.platforms = [[250, 700, 0]]
        self.springs = []
        self.cameray = 0
        self.xmovement = 0
        self.directionx = 0
        self.score_value = 0
        self.font = pygame.font.Font('img/Subway-Black.ttf', 32)

    def updatePlayer(self):
        if not self.jump:
            self.playerY += self.gravity
            self.gravity += 0.5
        elif self.jump:
            self.playerY -= self.jump
            self.jump -= 1
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 10:
                self.xmovement += 1
            self.player = pygame.transform.scale(pygame.image.load("img/gatorRight.png"), (80, 100))
        elif key[K_LEFT]:
            if self.xmovement > -10:
                self.xmovement -= 1
            self.player = pygame.transform.scale(pygame.image.load("img/gatorLeft.png"), (80, 100))
        else:
            if self.xmovement > 0:
                self.xmovement -= 1
            elif self.xmovement < 0:
                self.xmovement += 1
        if self.playerX >= 525:
            self.playerX = 525
        elif self.playerX <= 0:
            self.playerX = 0
        self.playerX += self.xmovement
        if(self.playerY - self.cameray <= 300):
            self.cameray -= 8
            self.score_value += 1
        self.screen.blit(self.player, (self.playerX, self.playerY - self.cameray))
    
    def updatePlatform(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0]+10, p[1], self.platformStation.get_width()-20, self.platformStation.get_height()-5)
            player = pygame.Rect(self.playerX+10, self.playerY+70, self.player.get_width()-20, self.player.get_height()-73)
            if rect.colliderect(player) and self.gravity and self.playerY < (p[1] - self.cameray) and ((p[1] - self.cameray) < 785):
                self.jump = 20
                self.gravity = 0
            if p[2] == 1:
                if p[-1] == 1:
                    p[0] += 3
                    if p[0] > 525:
                        p[-1] = 0
                else:
                    p[0] -= 3
                    if p[0] <= 0:
                        p[-1] = 1
        for spring in self.springs:
            self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            rect = pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height())
            player = pygame.Rect(self.playerX+10, self.playerY+70, self.player.get_width()-20, self.player.get_height()-73)
            if rect.colliderect(player) and self.gravity and self.playerY < (spring[1] - self.cameray) and ((spring[1] - self.cameray) < 785):
                print("touched spring")
                r = random.randint(80,120)
                self.jump = r
                self.cameray -= r
                self.gravity = 0


    def drawPlatform(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 800:
                platform = random.randint(0, 1000)
                if platform < 850:
                    platform = 0
                elif platform <= 1000:
                    platform = 1
                self.platforms.append([random.randint(0,525), self.platforms[-1][1] - 50, platform, 0])
                
                coords = self.platforms[-1]
                r = random.randint(0, 1000)
                if r > 900 and platform == 0:
                    self.springs.append([coords[0] + random.randint(0,60), coords[1]-10, 0])
                self.platforms.pop(0)

            if p[2] == 0:
                self.screen.blit((self.platformStation), (p[0], p[1] - self.cameray))
            elif p[2] == 1:
                self.screen.blit(self.platformMove, (p[0], p[1] - self.cameray))
            
            
        

    def generatePlatform(self):
        on = 800
        while on > -100:
            x = random.randint(0,525)
            platform = random.randint(0,1000)
            if platform < 850:
                platform = 0
            elif platform <= 1000:
                platform = 1
            self.platforms.append([x,on, platform, 0])
            on -= 50

    def showScore(self):
        score = self.font.render("Score: " + str(self.score_value), True, (255, 255, 255))
        self.screen.blit(score, (10, 10))

    def die(self):
        # error: doesnt print message
        message = self.font.render("You die... \n Your Score is: " + str(self.score_value) + "\n Press Any Key to Try Again ", True, (255, 255, 255))
        print("you should print the message!")
        self.screen.blit(message, (200, 200))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    return

    def run(self):
        #Set title and icon
        pygame.display.set_caption("Gator Jump!")
        pygame.display.set_icon(pygame.image.load('img/gatorIcon.png'))
        clock = pygame.time.Clock()
        self.generatePlatform()
        #Game Loop
        while True:
            self.screen.fill((255,255,255))
            self.screen.blit(self.background, (0,0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.playerY - self.cameray > 800:
                print("die reached")
                self.die()
                self.cameray = 0
                self.score_value = 0
                self.platforms = [[250, 700, 0]]
                self.generatePlatform()
                self.playerX = 250
                self.playerY = 600
            self.drawPlatform()
            self.updatePlayer()
            self.showScore()
            self.updatePlatform()
            pygame.display.flip()

GatorJump().run()