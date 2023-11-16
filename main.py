import pygame
import random

# Initialize Pygame
from Bullet import Bullet

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Dodger')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Spaceship settings
spaceship_speed = 5
spaceship_img = pygame.Surface((40, 40))  # Replace with your spaceship image
spaceship_img.fill(WHITE)
spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 40, 40)

# Bullet settings
bullet_group = pygame.sprite.Group()

# Clock to control frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship.left > 0:
        spaceship.x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship.right < SCREEN_WIDTH:
        spaceship.x += spaceship_speed

    # Generate bullets
    if random.randint(1, 50) == 1:
        new_bullet = Bullet(random.randint(0, SCREEN_WIDTH), 0, SCREEN_HEIGHT)
        bullet_group.add(new_bullet)

    # Update bullet positions
    bullet_group.update()

    # Check for collisions between spaceship and bullets
    for bullet in bullet_group:
        if spaceship.colliderect(bullet.rect):
            running = False  # End game

    # Rendering
    screen.fill(BLACK)
    screen.blit(spaceship_img, spaceship)
    for bullet in bullet_group:
        screen.blit(bullet.surf, bullet.rect)

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
