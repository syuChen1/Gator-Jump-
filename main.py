import pygame
import sys
from pygame.locals import *
import random
import buttons
import FaceRec
from pygame import mixer 
import cv2

pygame.init() 
face = cv2.CascadeClassifier('img/frontface.xml')
eye = cv2.CascadeClassifier('img/eye.xml')
smile = cv2.CascadeClassifier('img/smile.xml')
class GatorJump:
    def __init__(self):
        self.screen = pygame.display.set_mode((560, 720))
        self.screen_length = 560
        self.screen_width = 720
        self.background = pygame.transform.scale(pygame.image.load("img/bg2.jpg"), (560, 720))
        self.player = pygame.transform.scale(pygame.image.load("img/gatorRight.png"), (80, 100))
        self.platformStation = pygame.transform.scale(pygame.image.load("img/platform.png"), (75, 15))
        self.plane = pygame.transform.scale(pygame.image.load("img/plane-left.png"), (75, 15))
        self.spring = pygame.transform.scale(pygame.image.load("img/spring.png"), (15, 10))
        self.playK = False
        self.playF = False
        self.playerX = 200
        self.playerY = 430
        self.faceX = 0
        self.jump = 0
        self.gravity = 0
        self.platforms = [[200, 620, 0]]
        self.springs = []
        self.cameray = 0
        self.xmovement = 0
        self.directionx = 0
        self.score_value = 0
        self.font = pygame.font.Font('img/Subway-Black.ttf', 32)
        self.title_font = pygame.font.Font('img/Subway-Black.ttf', 80)
        self.player_died = False
        self.in_main_menu = True
        self.in_settings = False
        self.playK_button = buttons.buttons((255, 255, 255), self.screen_width/2 - 290, (self.screen_length*0.625), 420, 80, "Play with Keyboard")
        self.playF_button = buttons.buttons((255, 255, 255), self.screen_width/2 - 290, (self.screen_length*0.8), 420, 80, "Play with Face")
        self.menuMusic = mixer.Sound('img/menuMusic.wav')
        self.return_to_menu = buttons.buttons((255, 255, 255), self.screen_width/2 - 250, (self.screen_length*0.7), 350, 100, "Back to Main Menu")
        self.exit_game = buttons.buttons((255, 255, 255), self.screen_width / 2 - 290, (self.screen_length * 0.975), 420, 80, "Exit Game")
        #self.change_background = buttons.buttons((255, 255, 255), self.screen_width/2 - 290, (self.screen_length*0.975), 420, 80, "Change Background")


    def updatePlayer_Face(self):
        self.player = pygame.transform.scale(pygame.image.load("img/gatorRight.png"), (80, 100))
        if not self.jump:
            self.playerY += self.gravity
            if(self.gravity < 10):
                self.gravity += 0.5
        elif self.jump:
            self.playerY -= self.jump
            self.jump -= 1
        self.playerX = self.faceX
        if self.playerX >= 480:
            self.playerX = 480
        elif self.playerX <= 0:
            self.playerX = 0
        if(self.playerY - self.cameray <= 275):
            self.cameray -= 8
            self.score_value += 1
        
        self.screen.blit(self.player, (self.playerX, self.playerY - self.cameray))

    def updatePlayer_key(self):
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
        if self.playerX >= 480:
            self.playerX = 480
        elif self.playerX <= 0:
            self.playerX = 0
        self.playerX += self.xmovement
        if(self.playerY - self.cameray <= 275):
            self.cameray -= 8
            self.score_value += 1
        self.screen.blit(self.player, (self.playerX, self.playerY - self.cameray))
    
    def updatePlatform(self):
        for p in self.platforms:
            rect = pygame.Rect(p[0]+10, p[1], self.platformStation.get_width()-20, self.platformStation.get_height()-5)
            player = pygame.Rect(self.playerX+10, self.playerY+70, self.player.get_width()-20, self.player.get_height()-73)
            if rect.colliderect(player) and self.gravity and self.playerY < (p[1] - self.cameray) and ((p[1] - self.cameray) < 705):
                jumpSound = mixer.Sound('img/jump.wav')
                jumpSound.set_volume(0.12)
                jumpSound.play(0)
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
                springSound = mixer.Sound('img/jump.wav') #boing.wav but crashes code
                springSound.set_volume(0.4)
                springSound.play(0)
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
                self.platforms.append([random.randint(0,485), self.platforms[-1][1] - 50, platform, 0])
                
                coords = self.platforms[-1]
                r = random.randint(0, 1000)
                if r > 960 and platform == 0:
                    self.springs.append([coords[0] + random.randint(0,60), coords[1]-10, 0])
                self.platforms.pop(0)

            if p[2] == 0:
                self.screen.blit((self.platformStation), (p[0], p[1] - self.cameray))
            

    def generatePlatform(self):
        on = 700
        while on > -150:
            x = random.randint(0,485)
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
        message = self.font.render("You Died...", True, (255, 255, 255))
        message2 = self.font.render("Your Score is: " + str(self.score_value), True, (255, 255, 255))
        #message3 = self.font.render("Press ESC to go back to Main Menu", True, (255, 255, 255))
        message4 = self.font.render("Press Any Key to Play Again!", True, (255, 255, 255))
        self.screen.blit(message, (self.screen_length*0.33, self.screen_width*0.35))
        self.screen.blit(message2, (self.screen_length*0.25, self.screen_width*0.4))
        #self.screen.blit(message3, (self.screen_length*0.01, self.screen_width*0.45))
        self.screen.blit(message4, (self.screen_length*0.07, self.screen_width*0.45))
        self.return_to_menu.draw_button(self.screen, 40, (0,0,0))
        pygame.display.update()     #adding this prints message!!!
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #pygame.quit()
                    sys.exit()
                #key = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_to_menu.is_over(mouse_pos):
                        self.playK = False
                        self.playF = False
                        self.in_main_menu = True
                        return
                if event.type == pygame.KEYDOWN:
                    return

    '''
    def settings_menu(self):
        self.screen.fill((64, 173, 174))
        title = self.font.render("Background Settings", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width*0.15, self.screen_length*0.35))
        self.return_to_menu.draw_button(self.screen, 40, (0,0,0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.return_to_menu.is_over(mouse_pos):
                        self.in_settings = False
                        self.in_main_menu = True
                        self.main_menu()
                        return
    '''

    def draw_menu(self):
        self.screen.fill([54,42,72])
        self.screen.blit(self.background, (0, 0))
        intro_title = self.font.render("WELCOME TO", True, (255, 255, 255))
        title = self.title_font.render("Gator Jump!", True, (255, 255, 255))
        self.screen.blit(intro_title, (self.screen_width * 0.22, self.screen_length * 0.15))
        self.screen.blit(title, (self.screen_width*0.02, self.screen_length*0.25))
        self.screen.blit(pygame.transform.scale(pygame.image.load("img/gatorRight.png"), (80, 100)), (self.screen_width*.09, self.screen_length*0.42))
        self.screen.blit(pygame.transform.scale(pygame.image.load("img/gatorLeft.png"), (80, 100)), (self.screen_width*.575, self.screen_length*0.42))
        self.playK_button.draw_button(self.screen, 40, (0,0,0))
        self.playF_button.draw_button(self.screen, 40, (0,0,0))
        self.exit_game.draw_button(self.screen, 40, (0,0,0))
        #self.change_background.draw_button(self.screen, 40, (0,0,0))
        pygame.display.update()
        #pygame.draw.rect(self.screen, (0,0,0), (round(self.screen_width - 2, self.screen_length - 2), 
         #   round(self.screen_width + 4, self.screen_length + 4)), 0)
        #play_button = self.font.render("Play!", 1, (255, 255, 255))
        #self.screen.blit(play_button, (round(self.screen_width - 2, self.screen_length - 2), 
         #   round(self.screen_width + 4, self.screen_length + 4)))

    def main_menu(self):
        if mixer.music.get_busy():
            mixer.music.stop()
        self.draw_menu()
        while True: 
            self.menuMusic.set_volume(0.1)
            self.menuMusic.play(-1)
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.playK_button.is_over(mouse_pos):
                        self.in_main_menu = False
                        self.playK = True
                        self.menuMusic.stop()
                        mixer.music.load('img/music1.wav')
                        mixer.music.set_volume(0.3)
                        mixer.music.play(-1)
                        return  
                    if self.playF_button.is_over(mouse_pos):
                        self.in_main_menu = False
                        self.playF = True
                        self.menuMusic.stop()
                        mixer.music.load('img/music1.wav')
                        mixer.music.set_volume(0.3)
                        mixer.music.play(-1)
                        return 
                    if self.exit_game.is_over(mouse_pos):
                        sys.exit()
                        #self.in_settings = True
                        #self.settings_menu()
                        return
        pass

    def runF_Func(self, camera):
        ret, img = camera.read()
        img = cv2.rotate(img,cv2.ROTATE_90_COUNTERCLOCKWISE)
        roi = img[320:880, 0:720]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        for angle in [0, -25, 25]:
            rimg = FaceRec.rotate_image(roi, angle-90)
            detected = face.detectMultiScale(rimg, **FaceRec.settings)
            if len(detected):
                detected = [FaceRec.rotate_point(detected[-1], roi, -angle+90)]
                break
        for x, y, w, h in detected[-1:]:
            cv2.rectangle(roi, (x, y), (x+w, y+h), (255,255,0), 2)
            self.faceX = y+int(h/2)

        pygame.surfarray.blit_array(self.screen,roi)

    def runK_Func(self):
        self.screen.fill((255,255,255))
        self.screen.blit(self.background, (0,0))
        
    def run(self):
        #Set title and icon
        pygame.display.set_caption("Gator Jump!")
        pygame.display.set_icon(pygame.image.load('img/gatorIcon.png'))

        self.main_menu()
        camera =  cv2.VideoCapture(0)
        camera.set(3, 1280)
        camera.set(4, 720)
        
        clock = pygame.time.Clock()
        self.generatePlatform()
        #Game Loop
        while True:
            if(self.playF):
                self.runF_Func(camera)
                clock.tick(80)
            elif(self.playK):
                self.runK_Func()
                clock.tick(50)
           
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if self.playerY - self.cameray > 720:
                self.player_died = True
                self.die()
            if self.player_died:
                self.cameray = 0
                self.score_value = 0
                self.platforms = [[200, 620, 0]]
                self.playerX = 200
                self.playerY = 520
                self.generatePlatform()
                self.player_died = False
            if self.in_main_menu:
                self.main_menu()
            self.drawPlatform()
            if(self.playK):
                self.updatePlayer_key()
            if(self.playF):
                self.updatePlayer_Face()
            self.showScore()
            self.updatePlatform()
            pygame.display.flip()

GatorJump().run()