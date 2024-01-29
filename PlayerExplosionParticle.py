import pygame
import random

WHITE = (255, 255, 255)

class PlayerExplosionParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, xvel, yvel, radius, color, gravity=None):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.xvel = xvel
        self.yvel = yvel
        self.gravity = gravity
        self.radius = radius
        self.lifespan = random.randint(1, 3)
        self.alpha = 255

    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel
        if self.gravity is not None:
            self.yvel += self.gravity

        self.alpha = max(0, int(255 * (self.lifespan / max(1, self.lifespan))))
        self.image.set_alpha(self.alpha)

        self.lifespan -= 0.1
        if self.lifespan <= 0:
            self.kill()
