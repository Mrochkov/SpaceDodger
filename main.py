import pygame
import random
from Bullet import Bullet
from Leaderboards import Leaderboards
from StartScreen import StartScreen
from GameOverScreen import GameOverScreen
from SettingsScreen import SettingsScreen
import json

#TODO FULLSCREEN MODE(idk if ill do it honestly), CLEAN CODE, WRITE DOCUMENTATION

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (252, 186, 3)
GREEN = (48, 242, 0)
BLUE = (32, 3, 252)
RED = (252, 3, 3)
PURPLE = (125, 0, 163)
ORANGE = (255, 98, 0)
GREY= (128, 128, 128)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Main:
    def __init__(self):
        pygame.init()
        self.settings = self.load_settings()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Space Dodger')
        self.clock = pygame.time.Clock()
        self.score_font = pygame.font.Font(None, 36)
        self.start_font = pygame.font.Font(None, 72)

        # Inside Main class
        self.start_screen = StartScreen(self.screen, 72, self.settings)
        self.settings_screen = SettingsScreen(self.screen, 72, self.settings)
        self.game_over_screen = GameOverScreen(self.screen, self.start_font)
        self.leaderboards = Leaderboards(self.screen, self.score_font)

        self.bullet_generation_interval = 1000
        self.last_bullet_time = 0

        self.spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 30)
        self.bullet_group = pygame.sprite.Group()

        self.running = True
        self.score = 0

    def show_loading_screen(self):
        background_image_path = 'background.jpg'
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render('Space Dodger', True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5))

        loading_bar_width_max = 400
        loading_bar_height = 20
        loading_bar_x = (SCREEN_WIDTH - loading_bar_width_max) // 2
        loading_bar_y = SCREEN_HEIGHT // 1.4 + 50

        for i in range(101):
            self.screen.blit(background_image, (0, 0))
            self.screen.blit(title_text, title_rect)

            # Draw loading text
            loading_text = self.score_font.render('Loading...', True, WHITE)
            text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1))
            self.screen.blit(loading_text, text_rect)

            # Draw loading bar background
            pygame.draw.rect(self.screen, GREY, [loading_bar_x, loading_bar_y, loading_bar_width_max, loading_bar_height])

            # Draw loading bar progress
            current_bar_width = (loading_bar_width_max * i) // 100
            pygame.draw.rect(self.screen, GREEN, [loading_bar_x, loading_bar_y, current_bar_width, loading_bar_height])

            pygame.display.flip()
            pygame.time.wait(20)

    def reset_game(self):
        self.score = 0
        self.spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 30)
        self.bullet_group.empty()

    def save_settings(self):
        try:
            settings_path = 'settings.json'
            with open(settings_path, 'w') as f:
                print("Saving these settings to file:", self.settings)
                json.dump(self.settings, f, indent=4)
            print("Settings successfully saved to:", settings_path)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.spaceship.x -= self.spaceship_speed
        if keys[pygame.K_RIGHT]:
            self.spaceship.x += self.spaceship_speed

        self.spaceship.x = max(0, min(self.spaceship.x, SCREEN_WIDTH - self.spaceship.width))

    def game_loop(self):
        self.reset_game()
        self.apply_settings()
        running = True
        self.last_bullet_time = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Game logic
            self.handle_player_input()
            self.handle_bullet_generation()
            self.update_screen()
            self.update_score()
            self.clock.tick(60)

            # Collision detection
            if self.check_collisions():
                running = False

        difficulty = self.settings['amount_of_enemies']
        player_name = self.game_over_screen.run(self.score)
        if player_name.strip():
            self.leaderboards.update_leaderboard(player_name, self.score, difficulty)
        self.leaderboards.display()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
            settings.setdefault('spaceship_speed', 5)
            settings.setdefault('enemy_speed', 10)
            settings.setdefault('amount_of_enemies', 'Easy')
            settings.setdefault('fullscreen_mode', False)
            return settings
        except FileNotFoundError:
            print("Settings file not found. Loading default settings.")
            return {'spaceship_speed': 5, 'enemy_speed': 10}
        except json.JSONDecodeError:
            print("Error decoding JSON. Loading default settings.")
            return {'spaceship_speed': 5, 'enemy_speed': 10}

    def run(self):
        self.show_loading_screen()
        menu_selection = self.start_screen.run()

        while self.running:
            if menu_selection == 'Start Game':
                self.game_loop()
                menu_selection = self.start_screen.run()
            elif menu_selection == 'Settings':
                self.settings_screen = SettingsScreen(self.screen, self.settings)
                updated_settings = self.settings_screen.run()
                if updated_settings is not None:
                    self.settings.update(updated_settings)
                    self.apply_settings()
                    self.save_settings()
                else:
                    print("No updated settings received in Main")
                menu_selection = self.start_screen.run()


            elif menu_selection == 'Leaderboards':
                self.leaderboards.display()

                menu_selection = self.start_screen.run()
            elif menu_selection == 'Quit':
                self.running = False

        pygame.quit()



    def update_score(self):
        for bullet in self.bullet_group:
            if bullet.rect.y > self.spaceship.y and not bullet.counted_for_score:
                self.score += 1
                bullet.counted_for_score = True


    def apply_settings(self):

        if self.settings.get('fullscreen_mode', False):
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.spaceship_speed = self.settings.get('spaceship_speed', 5)
        self.enemy_speed = self.settings.get('enemy_speed', 10)
        self.update_screen_references()
        self.redraw_screen()


    def handle_bullet_generation(self):
        time_now = pygame.time.get_ticks()
        enemy_frequency = {
            'Easy': 1100,
            'Medium': 700,
            'Hard': 350
        }
        interval = enemy_frequency[self.settings['amount_of_enemies']]

        if time_now - self.last_bullet_time > interval:
            bullet_x = random.randint(0, SCREEN_WIDTH - 20)
            new_bullet = Bullet(bullet_x, 0, 20, 10, self.enemy_speed)
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
                return True
        return False

    def draw_text(self, text, font, x, y):
        text_surface = font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x, y))

    def update_screen_references(self):
        self.game_over_screen.screen = self.screen
        self.leaderboards.screen = self.screen
        self.settings_screen.screen = self.screen
        self.start_screen.screen = self.screen

        self.reposition_game_elements()

    def reposition_game_elements(self):
        self.spaceship.x = self.screen.get_width() // 2 - self.spaceship.width // 2
        self.spaceship.y = self.screen.get_height() - 60 - self.spaceship.height

    def redraw_screen(self):
        # Clear the screen
        self.screen.fill(BLACK)

        # Redraw the spaceship
        pygame.draw.rect(self.screen, WHITE, self.spaceship)

        # Redraw the bullets
        for bullet in self.bullet_group:
            self.screen.blit(bullet.image, bullet.rect)

        # Redraw the score text
        score_text = self.score_font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

if __name__ == '__main__':
    game = Main()
    game.run()

