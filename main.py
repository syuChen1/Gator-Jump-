import pygame
import sys
from pygame.locals import *

class GatorJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        

    def updatePlayer(self):
        pass
    

    def run(self):
        #Set title and icon
        pygame.display.set_caption("Gator Jump!")
        pygame.display.set_icon(pygame.image.load('img/gatorIcon.png'))

        #Game Loop
        while True:
            self.screen.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            pygame.display.update()

GatorJump().run()