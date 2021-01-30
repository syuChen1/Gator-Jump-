from io import SEEK_CUR
import pygame
import sys
from pygame.locals import *
import random

class GatorJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        self.platforms = []
        self.cameray = 0
        self.size = width, height = (75,10)
        self.surf = pygame.Surface(self.size)
        self.ymovement = 0
        self.directionx = 1
        self.directiony = 1

    def updatePlayer(self):
        self.cameray -= 0.1
    
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
        print (self.platforms)

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