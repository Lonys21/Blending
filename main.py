import pygame
from game import Game

pygame.init()
pygame.display.set_caption("Blending")
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
FPS = 60
g = Game(screen)


running = True

while running:

    # update the game
    g.update()

    # actualize the screen
    pygame.display.flip()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        elif ev.type == pygame.KEYDOWN:
            g.create_colors()
            g.blend_colors()
            g.create_rect()
    clock.tick(FPS)

pygame.quit()
