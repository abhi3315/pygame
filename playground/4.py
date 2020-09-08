# pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.USEREVENT
# K_RETURN, K_SPACE, K_ESCAPE
# K_UP, K_DOWN, K_LEFT, K_RIGHT
# K_a, K_b,...
# K_0, K_1,...

import pygame

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480))
r, g, b = 0, 0, 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                if r < 255:
                    r += 1
            if event.key == pygame.K_g:
                if g < 255:
                    g += 1
            if event.key == pygame.K_b:
                if b < 255:
                    b += 1
    screen.fill((r, g, b))
    pygame.display.flip()

    clock.tick(1)
