import pygame
import random
from Bullet import Bullet
from StartScreen import StartScreen
from GameOverScreen import GameOverScreen
# Initialize Pygame
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
YELLOW = (252, 186, 3)
GREEN = (48, 242, 0)
BLUE = (32, 3, 252)
RED = (252, 3, 3)
PURPLE = (125, 0, 163)
ORANGE = (255, 98, 0)

# Font setup
score_font = pygame.font.Font(None, 36)
start_font = pygame.font.Font(None, 72)

# Spaceship settings
spaceship_speed = 5
spaceship_img = pygame.Surface((40, 40))
spaceship_img.fill(WHITE)
spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 40, 40)

# Bullet settings
bullet_group = pygame.sprite.Group()

# Clock to control frame rate
clock = pygame.time.Clock()

# Score initialization
score = 0

def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, True, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

spaceship_image_path = 'logo.png'

start_screen = StartScreen(screen, 72)
menu_selection = start_screen.run()

if not start_screen.run():
    running = False
else:
    running = True

"""
if menu_selection == 'Start Game':
    elif menu_selection == 'Settings':
    elif menu_selection == 'Leaderboards':
    elif menu_selection == 'Quit':
        running = False
"""


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

    # Check for bullets that have passed the spaceship
    for bullet in list(bullet_group):
        if bullet.is_off_screen():
            score += 1
            bullet_group.remove(bullet)

    # Generate new bullets
    if random.randint(1, 50) == 1:
        new_bullet = Bullet(random.randint(0, SCREEN_WIDTH), 0, SCREEN_HEIGHT)
        bullet_group.add(new_bullet)

    # Update and generate bullets
    bullet_group.update()

    if random.randint(1, 50) == 1:
        new_bullet = Bullet(random.randint(0, SCREEN_WIDTH), 0, SCREEN_HEIGHT)
        bullet_group.add(new_bullet)

    # Check for collisions between spaceship and bullets
    for bullet in bullet_group:
        if spaceship.colliderect(bullet.rect):
            game_over_screen = GameOverScreen(screen, start_font, score)
            game_over_screen.run()
            running = False

    # Rendering
    screen.fill(BLACK)
    screen.blit(spaceship_img, spaceship)
    for bullet in bullet_group:
        screen.blit(bullet.surf, bullet.rect)

    draw_text(f'Score: {score}', score_font, screen, 10, 10)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()