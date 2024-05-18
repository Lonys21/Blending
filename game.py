import pygame, random


class Game:
    def __init__(self, screen):
        # screen
        self.screen = screen
        self.actual_screen = 'welcome_screen'
        self.background_color = 'beige' # #f4f6e3

        # Welcome_screen
        self.welclome_sceen = pygame.image.load("assets/Welcome_screen.png")
        self.play_button = Button("Play", 238, 594, self, width=324, height=147)


        # Button
        self.button_width = self.screen.get_width()/2
        self.button_height = self.button_width*17/25
        self.button_width_horizontal = self.button_width - 60
        self.button_height_horizontal = self.button_width_horizontal*20/50
        self.button_x = self.screen.get_width()/2 - self.button_width/2
        self.button_y_menu = self.screen.get_height()/4 - self.button_height/2
        self.button_y_replay = 20
        self.button_y_additional_round = 300
        self.button_home_size = 100
        self.button_x_home_life = self.screen.get_width() - 15 - self.button_home_size
        self.button_x_home_score = 15
        self.button_y_home = 15
        self.buttons_menu = pygame.sprite.Group()
        self.buttons_menu.add(Button("Life_mode", self.button_x, self.button_y_menu, self),
                              Button("Round_mode", self.button_x, self.button_y_menu + self.screen.get_width()/2, self))
        self.additional_round_button = Button("Additional_round", self.button_x, self.button_y_additional_round, self, height=self.button_height_horizontal)
        self.replay_button = Button("Replay_horizontal", self.button_x, self.button_y_replay, self, height=self.button_height_horizontal)
        self.arrow_image = pygame.image.load("assets/arrow.png")
        self.menu_button = Button("Menu", self.button_x, self.button_y_additional_round - self.button_height_horizontal - 20, self, height=self.button_height_horizontal)
        self.home_button = Button("Home", self.button_x_home_score, self.button_y_home, self, width=self.button_home_size, height=self.button_home_size)

        # Gamemode
        self.gamemode = '' # Life Mode, Score Mode, Party

        # colors
        self.DOMINANT_VARIABLE = (150, 255)
        self.SECONDE_VARIABLE = (0, 100)
        self.SAME_VARIABLE = (25, 215)
        self.colors = []
        self.color1 = []
        self.color2 = []
        self.blend_color = []
        self.colors_blended = []
        self.modes = ('RGB', 'RGB+', 'RGB++', 'CMY', 'CMY+', 'CMY++')
        self.mode = ''

        # Rect
        self.rect_size1 = 200
        self.rect_size2 = 100
        self.rect_height1 = self.screen.get_height()*1/3 - self.rect_size1/2
        self.rect_height2 = self.screen.get_height()*2/3
        self.primary_rects = []
        self.rects = []

        # Past_rect
        self.NUMBER_SQUARE_ROW = 10  # 25 for life mode
        self.SQUARE_EDGE_SIZE = int(self.screen.get_width()/self.NUMBER_SQUARE_ROW * 0.05)
        self.SQUARE_SIZE = self.screen.get_width()/self.NUMBER_SQUARE_ROW - self.SQUARE_EDGE_SIZE*2
        self.past_rects = []
        self.previous_round_rects = self.past_rects
        self.mosaic_start_x = self.SQUARE_EDGE_SIZE
        self.mosaic_x = self.mosaic_start_x
        self.mosaic_start_y = self.screen.get_height() - self.SQUARE_SIZE - self.SQUARE_EDGE_SIZE
        self.mosaic_y = self.mosaic_start_y

        # Lifemode
        self.MAX_LIFE = 10
        self.life = self.MAX_LIFE
        self.heart = pygame.image.load('assets/heart.png')
        self.heart = pygame.transform.scale(self.heart, (50, 60))
        self.heart_y = 0
        self.start_heart_x = 10

        # Score mode
        self.NUMBER_ROUNDS = 10
        self.max_round = self.NUMBER_ROUNDS
        self.round = 1
        self.rounds_did = 0
        self.square_size = 0
        self.previous_square_size = 0
        self.score_font = pygame.font.SysFont('Arial', 60)
        self.score_font_color = 'black'
        self.round_font_x = 650
        self.round_font_y = 25
        self.score_font_x = 100
        self.score_font_y = 50
        self.point = 0


    def update(self):
        self.screen.fill(self.background_color)
        if self.actual_screen == 'welcome_screen':
            self.screen.blit(self.welclome_sceen, (0, 0))
            self.screen.blit(self.play_button.image, (self.play_button.rect.x, self.play_button.rect.y))
        elif self.actual_screen == 'menu':
            for b in self.buttons_menu:
                self.screen.blit(b.image, (b.rect.x, b.rect.y))
        elif self.actual_screen == 'playing':
            if self.gamemode == 'life':
                self.update_life_mode()
            elif self.gamemode == 'score':
                self.update_score_mode()
            if len(self.color1) + len(self.color2) + len(self.blend_color) == 9:
                for r in self.past_rects:
                    pygame.draw.rect(self.screen, 'black',
                                     (r.rect.x - self.SQUARE_EDGE_SIZE, r.rect.y - self.SQUARE_EDGE_SIZE,
                                      r.rect.width + self.SQUARE_EDGE_SIZE * 2,
                                      r.rect.height + self.SQUARE_EDGE_SIZE * 2))
                    pygame.draw.rect(self.screen, r.color, r.rect)
                for r in self.primary_rects:
                    pygame.draw.rect(self.screen, 'black', r.rect_extend)
                    pygame.draw.rect(self.screen, r.color, r.rect)
                for r in self.rects:
                    pygame.draw.rect(self.screen, 'black', (r.rect.x - 5, r.rect.y - 5, r.rect.width + 10, r.rect.height + 10))
                    pygame.draw.rect(self.screen, r.color, r.rect)
            self.screen.blit(self.home_button.image, (self.home_button.rect.x, self.home_button.rect.y))

        elif self.actual_screen == 'loose': # when the player lost the life mode
            self.loose_life_mode()

        elif self.actual_screen == 'end': # when all rounds have been made
            self.end_score_mode()

    def reset(self, mode):
        # reset all variables
        self.past_rects = []
        # life mode
        self.mosaic_x = self.mosaic_start_x
        self.mosaic_y = self.mosaic_start_y
        self.life = self.MAX_LIFE
        # Score mode
        if mode == 'all':
            self.round = 1
            self.rounds_did = 0
            self.max_round = self.NUMBER_ROUNDS
            self.previous_round_rects = []
            self.square_size = 0
            self.previous_square_size = 0
            self.point = 0

    def start(self):
        self.showed = False
        self.actual_screen = 'playing'
        self.create_colors()
        self.blend_colors()
        self.create_fake_colors()
        self.create_rect()

    def restart(self, mode='all'):
        self.reset(mode)
        self.start()

    def true(self, rect):
        # manage a good answer in fonction of the mode
        self.show_result()
        if self.gamemode == 'life':
            self.add_square()
        elif self.gamemode == 'score':
            self.add_square('green')
            self.point += 1

    def false(self, rect):
        # manage a bad answer in fonction of the mode

        # Life Mode
        if self.gamemode == 'life':
            self.life -= 1
            if self.life == 0:
                self.actual_screen = 'loose'
            self.rects.remove(rect) # delete the fake rect of the list
            self.colors_blended.remove(rect.color) # delete fake color of the list
            self.create_rect() # actualise rectangles

        # Score mode
        elif self.gamemode == 'score':
            self.add_square('red') # add a red square --> Bad answer
            self.show_result()

    def update_life_mode(self):
        # display heart on the screen
        for heart in range(self.life):
            self.screen.blit(self.heart,
                             (heart * self.heart.get_width() + 10 * heart + self.start_heart_x, self.heart_y))
        self.home_button.rect.x = self.button_x_home_life

    def loose_life_mode(self):
        start_x = 100
        start_y = 100
        if self.past_rects != self.previous_round_rects:
            self.past_rects = self.previous_round_rects + self.past_rects
            self.previous_round_rects = self.past_rects

        # square_root of number of square then round it to the upper number
        square_in_a_row = len(self.past_rects) ** (1 / 2)
        e = round(square_in_a_row, 1)
        if 0 < e - int(e) < 0.5:
            square_in_a_row = square_in_a_row - (square_in_a_row - round(square_in_a_row))
            square_in_a_row += 1
        else:
            square_in_a_row = round(square_in_a_row)
        if square_in_a_row == 0:
            square_in_a_row = 1


        # Square size in fonction of the number of square in one row
        square_size = (self.screen.get_width() - start_x*2)/square_in_a_row
        if int(len(self.past_rects))/square_in_a_row * square_size > self.screen.get_height()/2 - start_y:
            square_size = (self.screen.get_height()/2 - start_y)/square_in_a_row

        # call print mosaic function
        start_x = self.screen.get_width()/2 - square_in_a_row*square_size/2
        start_y = self.screen.get_height()/2 - int(len(self.past_rects))/square_in_a_row * square_size/2
        self.print_mosaic(start_x, start_y, square_in_a_row, square_size)

        self.screen.blit(self.replay_button.image, (self.replay_button.rect.x, self.replay_button.rect.y))
        self.screen.blit(self.home_button.image, (self.home_button.rect.x, self.home_button.rect.y))

    def print_mosaic(self, start_x, start_y, square_in_a_row, square_size, rects=0):
        if rects == 0:
            rects = self.past_rects
        x = start_x
        y = start_y
        i = 0
        square_edge_size = int(square_size/50)
        if square_edge_size < 1:
            square_edge_size = 1
        for r in rects:
            pygame.draw.rect(self.screen, 'black', (x - square_edge_size, y - square_edge_size,
                                                    square_size + square_edge_size * 2,
                                                    square_size + square_edge_size * 2))
            pygame.draw.rect(self.screen, r.color, (x, y, square_size, square_size))
            x += square_size + square_edge_size*2
            i += 1
            if i == square_in_a_row:
                y += square_size + square_edge_size*2
                x = start_x
                i = 0

    def update_score_mode(self):
        self.screen.blit(self.score_font.render(str(self.round)+'/'+str(self.max_round), True, self.score_font_color), (self.round_font_x, self.round_font_y))
        if self.round == self.max_round + 1:
            self.actual_screen = 'end'
            self.rounds_did += 1
        self.home_button.rect.x = self.button_x_home_score

    def end_score_mode(self):
        start_x = 100
        start_y = 500
        square_area_width = self.screen.get_width() - start_x*2
        square_area_height = self.screen.get_height() - start_y - start_x/2
        
        # To rectify
        if self.rounds_did == 1:
            square_in_a_row = 5
            self.square_size = square_area_width/square_in_a_row
        elif self.rounds_did % 3 == 0:
            square_in_a_row = 15
            self.square_size = (square_area_width / square_in_a_row)
            if self.square_size * (self.rounds_did * 10 / square_in_a_row) > square_area_height:
                self.square_size * 3 / self.rounds_did
        elif self.rounds_did % 2 == 0:
            square_in_a_row = 10
            self.square_size = square_area_width/square_in_a_row
            if self.square_size * (self.rounds_did * 10 / square_in_a_row) > square_area_height:
                if self.rounds_did % 4 == 0:
                    square_in_a_row = 20
                    self.square_size = square_area_width/square_in_a_row
        elif self.rounds_did % 5 == 0:
            square_in_a_row = 10
            self.square_size = square_area_height/self.rounds_did
            #  start_x += (square_area_width-square_in_a_row*self.square_size)/2
        elif self.rounds_did % 7 == 0:
            square_in_a_row = 14
            self.square_size = (square_area_width / square_in_a_row)
            if self.square_size * (self.rounds_did * 10 / square_in_a_row) > square_area_height:
                self.square_size * 7 / self.rounds_did

        if self.rounds_did > 2:
            square_in_a_row = 10
            if self.rounds_did*10/square_in_a_row*self.previous_square_size > square_area_height:
                self.square_size = square_area_height / self.rounds_did
                start_x += (square_area_width - square_in_a_row * self.square_size) / 2
            else:
                self.square_size = self.previous_square_size





        if self.previous_round_rects != self.past_rects:
            self.previous_round_rects += self.past_rects
            self.past_rects = self.previous_round_rects.copy()

        self.print_mosaic(start_x, start_y, square_in_a_row, self.square_size, self.previous_round_rects)
        self.screen.blit(self.score_font.render(f'Well, your score is : {self.point}/{self.max_round}',True, self.score_font_color),
                         (self.score_font_x, self.score_font_y))
        self.screen.blit(self.additional_round_button.image, (self.additional_round_button.rect.x, self.additional_round_button.rect.y))
        self.screen.blit(self.menu_button.image, (self.menu_button.rect.x, self.menu_button.rect.y))

    def additional_round(self):
        self.max_round += self.NUMBER_ROUNDS
        self.previous_square_size = self.square_size
        self.restart("partial")



    def create_rect(self):
        self.primary_rects = []
        self.rects = []
        self.primary_rects.append(Rectangle(self.screen.get_width()*1/3-self.rect_size1/2, self.rect_height1, self.rect_size1, self.rect_size1, self.color1))
        self.primary_rects.append(Rectangle(self.screen.get_width() * 2 / 3 - self.rect_size1/2, self.rect_height1,
                                      self.rect_size1, self.rect_size1, self.color2))
        if len(self.colors_blended) > 2:
            a = self.screen.get_width() * 1/len(self.colors_blended)**2
        elif len(self.colors_blended) == 2:
            a = self.screen.get_width() * 1/3 - self.rect_size2/2
        else:
            a = self.screen.get_width()/2 - self.rect_size2/2
        for c in self.colors_blended:
            if c == self.blend_color:
                self.blend_rect = Rectangle(a, self.rect_height2, self.rect_size2, self.rect_size2, c)
                self.rects.append(self.blend_rect)
            else:
                self.rects.append(Rectangle(a, self.rect_height2, self.rect_size2, self.rect_size2, c))
            a += self.screen.get_width() * 1/len(self.colors_blended)
            if len(self.colors_blended) == 2:
                a = self.screen.get_width() * 2/3 - self.rect_size2/2



    def create_colors(self):
        # RGB --> random variables = 0 + random number
        # RGB+ --> 1 dominant variable = 0 + high random number; 2 second variables = 0 + low random number
        # RGB++ --> 1 dominant variable = 255; 2 zero variable = 0
        # CMY --> random variables = 255 - random number
        # CMY+ --> 1 dominant varaible 255 - high random number; 2 second variables = 255 - low random number
        # CMY++ --> 1 variable = 0; 2 variables = 255
        colors = []
        for i in range(2):
            self.mode = random.choice(self.modes)
            if self.mode == 'RGB+':
                R = 0
                G = 0
                B = 0
                color_ = [[R, 0], [G, 1], [B, 2]]
                color = []
                dominant_color = random.choice(color_)
                dominant_color[0] = random.randint(self.DOMINANT_VARIABLE[0], self.DOMINANT_VARIABLE[1])
                v1 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
                v2 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
                color.append(v1)
                color.append(v2)
                color.insert(dominant_color[1], dominant_color[0])
                colors.append(color)

            elif self.mode == 'RGB':
                color = []
                v1 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
                v2 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
                v3 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
                color.append(v1)
                color.append(v2)
                color.append(v3)
                colors.append(color)
            elif self.mode == 'RGB++':
                R = 0
                G = 0
                B = 0
                color_ = [[R, 0], [G, 1], [B, 2]]
                color = []
                dominant_color = random.choice(color_)
                dominant_color[0] = 255
                v1 = 0
                v2 = 0
                color.append(v1)
                color.append(v2)
                color.insert(dominant_color[1], dominant_color[0])
                colors.append(color)

            elif self.mode == 'CMY+':
                R = 255
                G = 255
                B = 255
                color_ = [[R, 0], [G, 1], [B, 2]]
                color = []
                dominant_color = random.choice(color_)
                dominant_color[0] = random.randint(self.DOMINANT_VARIABLE[0], self.DOMINANT_VARIABLE[1])
                v1 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
                v2 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
                dominant_color[0] = color_[dominant_color[1]][0] - dominant_color[0]
                v1 = 255 - v1
                v2 = 255 - v2
                color.append(v1)
                color.append(v2)
                color.insert(dominant_color[1], dominant_color[0])
                colors.append(color)
            elif self.mode == 'CMY':
                color = []
                v1 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
                v2 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
                v3 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
                v1 = 255 - v1
                v2 = 255 - v2
                v3 = 255 - v3
                color.append(v1)
                color.append(v2)
                color.append(v3)
                colors.append(color)
            elif self.mode == 'CMY++':
                R = 255
                G = 255
                B = 255
                color_ = [[R, 0], [G, 1], [B, 2]]
                color = []
                dominant_color = random.choice(color_)
                dominant_color[0] = 0
                v1 = 255
                v2 = 255
                dominant_color[0] = color_[dominant_color[1]][0] - dominant_color[0]
                color.append(v1)
                color.append(v2)
                color.insert(dominant_color[1], dominant_color[0])
                colors.append(color)
        self.color1 = colors[0]
        self.color2 = colors[1]
    def blend_colors(self):
        self.colors_blended = []
        blend_color = []
        for i in range(3):
            v = (self.color1[i] + self.color2[i]) / 2
            blend_color.append(v)
        self.blend_color = blend_color


    def create_fake_colors(self):
        m = random.randint(-50, 75)
        for i in range(3):
            fake_color = []
            for color in self.blend_color:
                n = random.randint(0, 1)
                if n == 0:
                    color *= 1/random.randint(2, 8)
                else:
                    color *= random.randint(2, 4)
                color += m
                if color > 255:
                    color = 255
                elif color < 0:
                    color = 1
                fake_color.append(color)
            self.colors_blended.append(fake_color)
        self.colors_blended.insert(random.randint(0, 2), self.blend_color)

    def show_result(self):
        self.primary_rects = [Rectangle(self.screen.get_width()/2-self.rect_size1/2, self.rect_height1, self.rect_size1, self.rect_size1, self.blend_color)]
        self.showed = True


    def add_square(self, color=''):
        if color == '':
            color = self.blend_color
        self.past_rects.append(Rectangle(self.mosaic_x, self.mosaic_y, self.SQUARE_SIZE, self.SQUARE_SIZE, color))
        self.mosaic_x += self.SQUARE_SIZE + self.SQUARE_EDGE_SIZE*2
        if self.gamemode == 'life':
            if len(self.past_rects) == self.NUMBER_SQUARE_ROW:
                self.life = self.MAX_LIFE
                self.mosaic_y = self.mosaic_start_y
                self.mosaic_x = self.mosaic_start_x
                self.previous_round_rects = self.past_rects.copy()
            if len(self.past_rects) == self.NUMBER_SQUARE_ROW + 1:
                self.past_rects = []
                self.past_rects.append(
                    Rectangle(self.mosaic_start_x, self.mosaic_start_y, self.SQUARE_SIZE, self.SQUARE_SIZE, color))




class Rectangle:
    def __init__(self, left, top, width, height, color):
        self.rect_initial = pygame.rect.Rect(left, top, width, height)
        self.rect_extend = pygame.rect.Rect(left-5, top-5, width+10, height+10)
        self.rect = self.rect_initial.copy()
        self.color = color

    def extend(self):
        self.rect = self.rect_extend.copy()

    def set_initial_rect(self):
        self.rect = self.rect_initial.copy()



class Button(pygame.sprite.Sprite):
    def __init__(self, name, x, y, game, width=0, height=0):
        super().__init__()
        self.name = name
        self.width = width
        self.height = height
        if self.width == 0:
            self.original_width = game.button_width
            self.width = self.original_width
        if self.height == 0:
            self.original_height = game.button_height
            self.height = self.original_height
        self.image_idle = pygame.transform.scale(pygame.image.load("assets/" + name + "_button.png"), (self.width, self.height))
        self.image_mouse_on = pygame.transform.scale(pygame.image.load("assets/" + name + "_button_mouse_on.png"), (self.width, self.height))
        self.image = self.image_idle
        self.rect = self.image.get_rect()
        self.original_x = x
        self.original_y = y
        self.rect.x = self.original_x
        self.rect.y = self.original_y

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.image_idle = pygame.transform.scale(self.image_idle, (self.width, self.height))
        self.image_mouse_on = pygame.transform.scale(self.image_mouse_on, (self.width, self.height))

    def reset_size(self):
        self.width = self.original_width
        self.height = self.original_height
        self.image_idle = pygame.transform.scale(self.image_idle, (self.width, self.height))
        self.image_mouse_on = pygame.transform.scale(self.image_mouse_on, (self.width, self.height))

    def replace(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def reset_position(self):
        self.rect.x = self.original_x
        self.rect.y = self.original_y