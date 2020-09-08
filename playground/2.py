import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))
screen.fill((255, 0, 0))
pygame.display.update()

running = True

while running:
    print(pygame.event.get())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
