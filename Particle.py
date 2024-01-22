import pygame
import random

WHITE = (255, 255, 255)

class Particle():
    def __init__(self, x, y, xvel, yvel, radius, color, gravity=None):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.radius = radius
        self.color = color
        self.gravity = gravity

    def render(self, win):
        self.x += self.xvel
        self.y += self.yvel
        if self.gravity is not None:
            self.yvel += self.gravity
        self.radius -= 0.1

        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), int(self.radius))