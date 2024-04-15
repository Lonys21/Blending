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
            g.past_rects = []
            g.mosaic_y = g.mosaic_start_y
            g.mosaic_x = g.mosaic_start_x
            for i in range(g.NUMBER_SQUARE_ROW*100):
                g.start()
                g.add_square()



        elif ev.type == pygame.MOUSEBUTTONDOWN:
            for r in g.rects:
                if r.rect.collidepoint(ev.pos):
                    if not g.showed:
                        if r == g.blend_rect:
                            g.show_result()
                            g.add_square()
                        else:
                            g.life -= 1
                            if g.life == 1000:
                                g.actual_screen = 'loose'
                            g.rects.remove(r)
                            g.colors_blended.remove(r.color)
                            g.create_rect()
                    else:
                        if r == g.blend_rect:
                            g.start()
                        else:
                            g.colors_blended = [g.blend_color]
                            g.rects = [g.blend_rect]
                            g.create_rect()
                            g.show_result()


        elif ev.type == pygame.MOUSEMOTION:
            for r in g.rects:
                if r.rect.collidepoint(ev.pos):
                    r.extend()
                else:
                    r.set_initial_rect()
    clock.tick(FPS)

pygame.quit()
