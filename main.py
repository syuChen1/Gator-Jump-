import pygame

pygame.init()

# Create the screen
screen = pygame.display.set_mode((1200, 900))

pygame.display.set_caption("Gator Jump!")
pygame.display.set_icon(pygame.image.load('img/gatorIcon.png'))



# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False