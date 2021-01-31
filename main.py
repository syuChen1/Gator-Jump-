import pygame
import sys
from pygame.locals import *
import random
import buttons
from pygame import mixer 

pygame.init() 

class GatorJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 800))
        self.screen_length = 600
        self.screen_width = 800
        self.background = pygame.transform.scale(pygame.image.load("img/bg2.jpg"), (600, 800))
        self.player = pygame.transform.scale(pygame.image.load("img/gatorRight.png"), (80, 100))
        self.platformStation = pygame.transform.scale(pygame.image.load("img/platform.png"), (75, 15))
        self.plane = pygame.transform.scale(pygame.image.load("img/plane-left.png"), (75, 15))
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
        self.player_died = False
        self.in_main_menu = True
        self.play_button = buttons.buttons((255, 255, 255), self.screen_width/2 - 200, (self.screen_length*0.8), 200, 100, "Play!")

    def updatePlayer(self):
        if not self.jump:
            self.playerY += self.gravity
            if(self.gravity < 10):
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
                mixer.music.load('img/spring.wav')
                mixer.music.set_volume(0.17)
                mixer.music.play(0)
                self.jump = 20
                self.gravity = 0
            if p[2] == 1:
                if p[-1] == 1:
                    self.plane = pygame.transform.scale(pygame.image.load("img/plane-right.png"), (75, 15))
                    p[0] += 3
                    if p[0] > 525:
                        p[-1] = 0
                else:
                    self.plane = pygame.transform.scale(pygame.image.load("img/plane-left.png"), (75, 15))
                    p[0] -= 3
                    if p[0] <= 0:
                        p[-1] = 1
                self.screen.blit(self.plane, (p[0], p[1] - self.cameray)) 

        for spring in self.springs:
            self.screen.blit(self.spring, (spring[0], spring[1] - self.cameray))
            rect = pygame.Rect(spring[0], spring[1], self.spring.get_width(), self.spring.get_height())
            player = pygame.Rect(self.playerX+10, self.playerY+70, self.player.get_width()-20, self.player.get_height()-73)
            if rect.colliderect(player) and self.gravity and self.playerY < (spring[1] - self.cameray) and ((spring[1] - self.cameray) < 785):
                print("touched spring")
                r = random.randint(40,60)
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
                if r > 960 and platform == 0:
                    self.springs.append([coords[0] + random.randint(0,60), coords[1]-10, 0])
                self.platforms.pop(0)

            if p[2] == 0:
                self.screen.blit((self.platformStation), (p[0], p[1] - self.cameray))
            

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
        # error: doesnt print message - fixed
        self.player_died = True
        message = self.font.render("You died...", True, (255, 255, 255))
        message2 = self.font.render("Your Score is: " + str(self.score_value), True, (255, 255, 255))
        message3 = self.font.render("Press ESC to go back to Main Menu", True, (255, 255, 255))
        message4 = self.font.render("Or Press Any Key to Play Again!", True, (255, 255, 255))
        self.screen.blit(message, (self.screen_length*0.35, self.screen_width*0.35))
        self.screen.blit(message2, (self.screen_length*0.27, self.screen_width*0.4))
        self.screen.blit(message3, (self.screen_length*0.01, self.screen_width*0.45))
        self.screen.blit(message4, (self.screen_length*0.04, self.screen_width*0.50))
        pygame.display.update()     #adding this prints message!!!
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                key = pygame.key.get_pressed()
                if key[K_ESCAPE]:
                    self.main_menu()
                else:
                    return

    def draw_menu(self):
        self.screen.fill((64, 174, 118))
        title = self.font.render("Welcome to Gator Jump!", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_length*0.11, self.screen_width*0.35))
        self.play_button.draw_button(self.screen, 40, (0,0,0))
        pygame.display.update()
        #pygame.draw.rect(self.screen, (0,0,0), (round(self.screen_width - 2, self.screen_length - 2), 
         #   round(self.screen_width + 4, self.screen_length + 4)), 0)
        #play_button = self.font.render("Play!", 1, (255, 255, 255))
        #self.screen.blit(play_button, (round(self.screen_width - 2, self.screen_length - 2), 
         #   round(self.screen_width + 4, self.screen_length + 4)))

    def main_menu(self):
        self.draw_menu()
        while True:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_button.is_over(mouse_pos):
                        return
        
    def run(self):
        #Set title and icon
        pygame.display.set_caption("Gator Jump!")
        pygame.display.set_icon(pygame.image.load('img/gatorIcon.png'))

        self.main_menu()

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
                self.player_died = True
                self.die()
            if self.player_died:
                self.cameray = 0
                self.score_value = 0
                self.platforms = [[250, 700, 0]]
                self.playerX = 250
                self.playerY = 600
                self.generatePlatform()
                self.player_died = False
            self.drawPlatform()
            self.updatePlayer()
            self.showScore()
            self.updatePlatform()
            pygame.display.flip()

GatorJump().run()
