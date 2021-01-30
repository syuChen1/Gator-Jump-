from io import SEEK_CUR
import pygame
import sys
from pygame.locals import *
import random

class GatorJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        self.player = pygame.transform.scale(pygame.image.load("img/gatorPlayer.png"), (80, 100))
        self.playerX = 300
        self.playerY = 600
        self.jump = 0
        self.gravity = 0
        self.platforms = []
        self.cameray = 0
        self.size = width, height = (75,10)
        self.surf = pygame.Surface(self.size)
        self.xmovement = 0
        self.directionx = 0

    def updatePlayer(self):
        # if not self.jump:
        #     self.playerY += self.gravity
        #     self.gravity += 1
        # elif self.jump:
        #     self.playerY -= self.jump
        #     self.jump -= 1
        self.cameray -= 0.2
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            if self.xmovement < 1:
                self.xmovement += 0.1

        elif key[K_LEFT]:
            if self.xmovement > -1:
                self.xmovement -= 0.1
        else:
            if self.xmovement > 0:
                self.xmovement -= 0.1
            elif self.xmovement < 0:
                self.xmovement += 0.1
        self.playerX += self.xmovement
        self.screen.blit(self.player, (self.playerX, self.playerY))
    
    def updatePlatform(self):
        pass


    def drawPlatform(self):
        for p in self.platforms:
            check = self.platforms[1][1] - self.cameray
            if check > 800:
                self.platforms.append((random.randint(-0,525), self.platforms[-1][1] - 50))
                self.platforms.pop(0)
            self.screen.blit((self.surf), (p[0], p[1] - self.cameray))

    def generatePlatform(self):
        on = 800
        while on > -100:
            x = random.randint(-0,525)
            self.platforms.append((x,on))
            on -= 50

    def run(self):
        #Set title and icon
        pygame.display.set_caption("Gator Jump!")
        pygame.display.set_icon(pygame.image.load('img/gatorIcon.png'))

        clock = pygame.time.Clock()
        self.generatePlatform()
        #Game Loop
        while True:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.drawPlatform()
            self.updatePlayer()
            pygame.display.flip()

GatorJump().run()