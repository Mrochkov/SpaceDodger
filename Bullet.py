import pygame
from Particle import Particle
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
colors = [(255, 0, 0), (255, 215, 0), (255, 69, 0)]

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.counted_for_score = False
        self.particles = []

    def update(self):
        self.rect.y += self.speed
        self.generate_particles()

    def generate_particles(self):
        particle_count = 5
        for _ in range(particle_count):
            particle = Particle(
                self.rect.centerx,
                self.rect.centery,
                random.uniform(-2, 2),
                random.uniform(-2, 2),
                random.uniform(2, 5),
                random.choice(colors),
                gravity=0.1
            )
            self.particles.append(particle)

    def render_particles(self, win):
        for particle in self.particles:
            particle.render(win)
            if particle.radius <= 0:
                self.particles.remove(particle)