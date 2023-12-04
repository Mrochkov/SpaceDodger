import pygame

WHITE = (255, 255, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.counted_for_score = False


    def update(self):
        self.rect.y += self.speed
