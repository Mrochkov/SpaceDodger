import pygame
import random

# Initialize Pygame
from Bullet import Bullet

pygame.init()

score = 0
score_font = pygame.font.SysFont("Arial", 24)  # Create a font object

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Dodger')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

score_font = pygame.font.Font(None, 36)  # Create a font object with a size of 36

# Spaceship settings
spaceship_speed = 5
spaceship_img = pygame.Surface((40, 40))  # Replace with your spaceship image
spaceship_img.fill(WHITE)
spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 40, 40)

# Bullet settings
bullet_group = pygame.sprite.Group()

# Clock to control frame rate
clock = pygame.time.Clock()

def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

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

    bullet_group.update()  # This calls the update method of all Bullet instances

    # Generate bullets
    if random.randint(1, 50) == 1:
        new_bullet = Bullet(random.randint(0, SCREEN_WIDTH), 0, SCREEN_HEIGHT)
        bullet_group.add(new_bullet)

    for bullet in list(bullet_group):
        if bullet.is_off_screen():
            print("Bullet off screen, incrementing score")  # Debug print
            score += 1
            bullet_group.remove(bullet)

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
        score_text = score_font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

    draw_text(f'Score: {score}', score_font, screen, 10, 10)  # Draw the score at the top-left corner

pygame.quit()
