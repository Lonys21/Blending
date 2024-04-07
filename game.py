import pygame, random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = 'black'

        # colors
        self.DOMINANT_VARIABLE = (150, 255)
        self.SECONDE_VARIABLE = (0, 100)
        self.colors = []
        self.color1 = []
        self.color2 = []
        self.blend_color = []

    def update(self):
        self.screen.fill(self.background_color)
        if len(self.color1) + len(self.color2) + len(self.blend_color) == 9:
            pygame.draw.rect(self.screen, self.color1, (0, 0, 100, 100))
            pygame.draw.rect(self.screen, self.color2, (300, 0, 100, 100))
            pygame.draw.rect(self.screen, self.blend_color, (150, 150, 100, 100))



    def create_colors(self):
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

    def blend_colors(self):
        blend_color = []
        for i in range(3):
            # Average of colors
            # v = (self.color1[i] + self.color2[i])/2

            # Sum of colors
            v = self.color1[i] + self.color2[i]
            if v > 255:
                v = 255
            blend_color.append(v)
        self.blend_color = blend_color


