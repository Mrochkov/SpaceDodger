import pygame

WHITE = (255, 255, 255)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, screen_height):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill(WHITE)
        self.rect = self.surf.get_rect(center=(x, y))
        self.screen_height = screen_height

    def update(self):
        self.rect.move_ip(0, 5)  # Move the bullet down
        if self.rect.top > self.screen_height:
            self.kill()  # Remove the bullet if it goes off-screen
