import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))

running = True

shapeIndex = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                screen.fill((255, 255, 255))
                if shapeIndex == 0:
                    pygame.draw.circle(screen, (255, 0, 0), (400, 400), 30, 2)
                elif shapeIndex == 1:
                    pygame.draw.line(screen, (255, 255, 0),
                                     (0, 0), (640, 480), 2)
                elif shapeIndex == 2:
                    pygame.draw.rect(screen, (0, 0, 255), [
                                     (10, 10), (300, 400)], 3)
                elif shapeIndex == 3:
                    pygame.draw.polygon(screen, (0, 255, 0), [
                                        (30, 30), (100, 50), (200, 300), (20, 400)])
                shapeIndex += 1
    pygame.display.flip()
