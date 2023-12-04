import pygame
import random
from Bullet import Bullet
from StartScreen import StartScreen
from GameOverScreen import GameOverScreen
from SettingsScreen import SettingsScreen

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (252, 186, 3)
GREEN = (48, 242, 0)
BLUE = (32, 3, 252)
RED = (252, 3, 3)
PURPLE = (125, 0, 163)
ORANGE = (255, 98, 0)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Dodger')
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 36)
        self.start_font = pygame.font.Font(None, 72)

        self.start_screen = StartScreen(self.screen, 72)
        self.settings_screen = SettingsScreen(self.screen, 72)
        self.game_over_screen = GameOverScreen(self.screen, self.start_font)

        self.spaceship_speed = 5
        self.bullet_speed = 10
        self.bullet_generation_interval = 1000  # milliseconds
        self.last_bullet_time = 0

        self.spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 30)
        self.bullet_group = pygame.sprite.Group()

        self.running = True
        self.score = 0

    def run(self):
        menu_selection = self.start_screen.run()

        while self.running:
            if menu_selection == 'Start Game':
                self.game_loop()
                menu_selection = self.start_screen.run()
            elif menu_selection == 'Settings':
                self.settings_screen.run()
                menu_selection = self.start_screen.run()
            elif menu_selection == 'Quit':
                self.running = False

        pygame.quit()

    def game_loop(self):
        running = True
        self.last_bullet_time = pygame.time.get_ticks()

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Game logic
            self.handle_player_input()
            self.handle_bullet_generation()

            # Update and draw everything
            self.update_screen()

            self.update_score()

            # Collision detection
            if self.check_collisions():
                self.game_over_screen.run(self.score)
                running = False

            self.clock.tick(60)

    def update_score(self):
        for bullet in self.bullet_group:
            if bullet.rect.y > self.spaceship.y and not bullet.counted_for_score:
                self.score += 1
                bullet.counted_for_score = True


    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.spaceship.x -= self.spaceship_speed
        if keys[pygame.K_RIGHT]:
            self.spaceship.x += self.spaceship_speed

        self.spaceship.x = max(0, min(self.spaceship.x, SCREEN_WIDTH - self.spaceship.width))

    def handle_bullet_generation(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.last_bullet_time > self.bullet_generation_interval:
            bullet_x = random.randint(0, SCREEN_WIDTH - 20)
            new_bullet = Bullet(bullet_x, 0, 20, 10, self.bullet_speed)
            self.bullet_group.add(new_bullet)
            self.last_bullet_time = time_now

    def update_screen(self):
        self.screen.fill(BLACK)
        self.bullet_group.update()
        for bullet in self.bullet_group:
            self.screen.blit(bullet.image, bullet.rect)

        pygame.draw.rect(self.screen, WHITE, self.spaceship)
        self.draw_text(f'Score: {self.score}', self.score_font, 10, 10)
        pygame.display.flip()

    def check_collisions(self):
        for bullet in self.bullet_group:
            if self.spaceship.colliderect(bullet.rect):
                self.game_over_screen.run(self.score)
                return True
        return False

    def draw_text(self, text, font, x, y):
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x, y))

if __name__ == '__main__':
    game = Main()
    game.run()
