import Parameters as par
import math
import pygame

class Linkage:
    def __init__(self, x1, y1, length, theta, color, linkages):
        self.x1 = x1
        self.y1 = y1
        self.length = length
        self.theta = theta
        self.x2 = self.x1 + self.length * math.cos((self.theta))
        self.y2 = self.y1 + self.length * math.sin((self.theta))
        self.color = color
        linkages.append(self)


    def render(self, window):
        pygame.draw.line(window, self.color, (self.x1, self.y1), (self.x2, self.y2), 5)
        pygame.draw.circle(window, par.gray, (int(self.x1 + (self.length * math.cos(self.theta) / 2)), int(self.y1 + (self.length * math.sin(self.theta) / 2))), 8)