import pygame
from pygame.locals import *

class buttons():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self, screen, fontSize, text_color):
        pygame.draw.rect(screen, self.color, (round(self.x), round(self.y), round(self.width), round(self.height)), 0)
        
        if self.text != '':
            self.font = pygame.font.Font('img/Subway-Black.ttf', 32)
            text = self.font.render(self.text, 1, text_color)
            
        screen.blit(text, (round(self.x + (self.width / 2 - text.get_width() / 2)),
                            round(self.y + (self.height / 2 - text.get_height() / 2))))
   
    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False