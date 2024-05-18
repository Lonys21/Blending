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
            for i in range(2):
                g.start()
                g.add_square()



        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if g.actual_screen == 'menu':
                for b in g.buttons_menu:
                    if b.rect.collidepoint(ev.pos):
                        if b.name == "Life_mode":
                            g.gamemode = 'life'
                        elif b.name == 'Round_mode':
                            g.gamemode = "score"
                        g.start()
            elif g.actual_screen == 'playing':
                for r in g.rects:
                    if r.rect.collidepoint(ev.pos):
                        if not g.showed:
                            if r == g.blend_rect:
                                g.true(r)
                            else:
                                g.false(r)

                        else:
                            if r == g.blend_rect:
                                g.start()
                                if g.gamemode == 'score':
                                    g.round += 1
                            else:
                                g.colors_blended = [g.blend_color]
                                g.rects = [g.blend_rect]
                                g.create_rect()
                                g.show_result()
                if g.home_button.rect.collidepoint(ev.pos):
                    g.reset("all")
                    g.actual_screen = 'menu'
                    g.home_button.image = g.home_button.image_idle
            elif g.actual_screen == 'loose':
                """if g.arrow_rect.collidepoint(ev.pos):
                    g.loose_screen = 2"""
                if g.replay_button.rect.collidepoint(ev.pos):
                    g.restart()
                if g.home_button.rect.collidepoint(ev.pos):
                    g.reset("all")
                    g.actual_screen = 'menu'
                    g.home_button.image = g.home_button.image_idle
            elif g.actual_screen == 'end':
                if g.additional_round_button.rect.collidepoint(ev.pos):
                    g.additional_round()
                elif g.menu_button.rect.collidepoint(ev.pos):
                    g.actual_screen = 'menu'
                    g.reset("all")


        elif ev.type == pygame.MOUSEMOTION:
            if g.actual_screen == 'menu':
                for b in g.buttons_menu:
                    if b.rect.collidepoint(ev.pos):
                        b.image = b.image_mouse_on
                    else:
                        b.image = b.image_idle

            elif g.actual_screen == 'playing':
                for r in g.rects:
                    if r.rect.collidepoint(ev.pos):
                        r.extend()
                    else:
                        r.set_initial_rect()
                if g.home_button.rect.collidepoint(ev.pos):
                    g.home_button.image = g.home_button.image_mouse_on
                else:
                    g.home_button.image = g.home_button.image_idle
            elif g.actual_screen == 'loose':
                if g.replay_button.rect.collidepoint(ev.pos):
                    g.replay_button.image = g.replay_button.image_mouse_on
                else:
                    g.replay_button.image = g.replay_button.image_idle
                if g.home_button.rect.collidepoint(ev.pos):
                    g.home_button.image = g.home_button.image_mouse_on
                else:
                    g.home_button.image = g.home_button.image_idle
            elif g.actual_screen == 'end':
                if g.additional_round_button.rect.collidepoint(ev.pos):
                    g.additional_round_button.image = g.additional_round_button.image_mouse_on
                else:
                    g.additional_round_button.image = g.additional_round_button.image_idle
                if g.menu_button.rect.collidepoint(ev.pos):
                    g.menu_button.image = g.menu_button.image_mouse_on
                else:
                    g.menu_button.image = g.menu_button.image_idle





    clock.tick(FPS)

pygame.quit()
