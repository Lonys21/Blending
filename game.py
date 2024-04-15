import pygame, random


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.actual_screen = 'menu'
        self.background_color = 'gray'


        # colors
        self.DOMINANT_VARIABLE = (150, 255)
        self.SECONDE_VARIABLE = (0, 100)
        self.SAME_VARIABLE = (50, 200)
        self.colors = []
        self.color1 = []
        self.color2 = []
        self.blend_color = []
        self.colors_blended = []
        self.modes = ('RGB', 'RGB+', 'CMY', 'CMY+')
        self.mode = ''

        # Rect
        self.rect_size1 = 200
        self.rect_size2 = 100
        self.rect_height1 = self.screen.get_height()*1/3 - self.rect_size1/2
        self.rect_height2 = self.screen.get_height()*2/3
        self.primary_rects = []
        self.rects = []

        # Life
        self.MAX_LIFE = 5
        self.life = self.MAX_LIFE
        self.heart = pygame.image.load('assets/heart.png')
        self.heart = pygame.transform.scale(self.heart, (50, 60))
        self.heart_y = 0
        self.start_heart_x = 10

        # Game
        self.start()




    def update(self):
        self.screen.fill(self.background_color)
        if self.actual_screen == 'playing':
            if len(self.color1) + len(self.color2) + len(self.blend_color) == 9:
                for r in self.primary_rects:
                    pygame.draw.rect(self.screen, 'black', r.rect_extend)
                    pygame.draw.rect(self.screen, r.color, r.rect)
                for r in self.rects:
                    pygame.draw.rect(self.screen, 'black', (r.rect.x - 5, r.rect.y - 5, r.rect.width + 10, r.rect.height + 10))
                    pygame.draw.rect(self.screen, r.color, r.rect)
                for heart in range(self.life):
                    self.screen.blit(self.heart, (heart*self.heart.get_width() + 10*heart + self.start_heart_x, self.heart_y))

        else:
            print("defeat")


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
        self.mode = random.choice(self.modes)
        if self.mode == 'RGB':
            R = 0
            G = 0
            B = 0
            color = [[R, 0], [G, 1], [B, 2]]
            color1 = []
            dominant_color = random.choice(color)
            dominant_color[0] = random.randint(self.DOMINANT_VARIABLE[0], self.DOMINANT_VARIABLE[1])
            v1 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            v2 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            color1.append(v1)
            color1.append(v2)
            color1.insert(dominant_color[1], dominant_color[0])

            del color[dominant_color[1]]
            color2 = []
            dominant_color = random.choice(color)
            dominant_color[0] = random.randint(self.DOMINANT_VARIABLE[0], self.DOMINANT_VARIABLE[1])
            v1 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            v2 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            color2.append(v1)
            color2.append(v2)
            color2.insert(dominant_color[1], dominant_color[0])
            self.colors.append(color1)
            self.colors.append(color2)
            self.color1 = color1
            self.color2 = color2
        elif self.mode == 'RGB+':
            color1 = []
            v1 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v2 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v3 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            color1.append(v1)
            color1.append(v2)
            color1.append(v3)

            color2 = []
            v1 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v2 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v3 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            color2.append(v1)
            color2.append(v2)
            color2.append(v3)
            self.colors.append(color1)
            self.colors.append(color2)
            self.color1 = color1
            self.color2 = color2
            light = random.randint(-50, 50)
            colors = [self.color1, self.color2]
            for c in colors:
                for v in c:
                    v += light
                    if v > 255:
                        v = 255
                    elif v < 0:
                        v = 0
        elif self.mode == 'CMY':
            R = 255
            G = 255
            B = 255
            color = [[R, 0], [G, 1], [B, 2]]
            color1 = []
            dominant_color = random.choice(color)
            dominant_color[0] = random.randint(self.DOMINANT_VARIABLE[0], self.DOMINANT_VARIABLE[1])
            v1 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            v2 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            dominant_color[0] = color[dominant_color[1]][0] - dominant_color[0]
            v1 = 255 - v1
            v2 = 255 - v2
            color1.append(v1)
            color1.append(v2)
            color1.insert(dominant_color[1], dominant_color[0])
            color2 = []
            dominant_color_ = random.choice(color)
            while dominant_color_ == dominant_color:
                dominant_color_ = random.choice(color)
            dominant_color = dominant_color_
            dominant_color[0] = random.randint(self.DOMINANT_VARIABLE[0], self.DOMINANT_VARIABLE[1])
            v1 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            v2 = random.randint(self.SECONDE_VARIABLE[0], self.SECONDE_VARIABLE[1])
            dominant_color[0] = color[dominant_color[1]][0] - dominant_color[0]
            v1 = 255 - v1
            v2 = 255 - v2
            color2.append(v1)
            color2.append(v2)
            color2.insert(dominant_color[1], dominant_color[0])
            self.color1 = color1
            self.color2 = color2
        elif self.mode == 'CMY+':
            color1 = []
            v1 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v2 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v3 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v1 = 255 - v1
            v2 = 255 - v2
            v3 = 255 - v3
            color1.append(v1)
            color1.append(v2)
            color1.append(v3)
            color2 = []
            v1 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v2 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v3 = random.randint(self.SAME_VARIABLE[0], self.SAME_VARIABLE[1])
            v1 = 255 - v1
            v2 = 255 - v2
            v3 = 255 - v3
            color2.append(v1)
            color2.append(v2)
            color2.append(v3)
            self.color1 = color1
            self.color2 = color2

    def blend_colors(self):
        self.colors_blended = []
        blend_color = []
        for i in range(3):
            # Average of colors
            # v = (self.color1[i] + self.color2[i])/2

            if self.mode == 'RGB' or self.mode == 'RGB+':
                # Sum of colors
                v = self.color1[i] + self.color2[i]
                if v > 255:
                    v = 255
                blend_color.append(v)
            elif self.mode == 'CMY' or self.mode == 'CMY+':
                # Average of colors
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

    def start(self):
        self.showed = False
        self.actual_screen = 'playing'
        self.create_colors()
        self.blend_colors()
        self.create_fake_colors()
        self.create_rect()
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


