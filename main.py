import pygame
import random
from Bullet import Bullet
from Leaderboards import Leaderboards
from StartScreen import StartScreen
from GameOverScreen import GameOverScreen
from SettingsScreen import SettingsScreen
import json
import os


#TODO CLEAN CODE, WRITE DOCUMENTATION

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
        self.enemy_speed = self.settings.get('enemy_speed', 10)
        self.spaceship_speed = self.settings.get('spaceship_speed', 5)
        self.current_screen_width, self.current_screen_height = self.screen.get_size()

        # Player got hit animation
        self.player_hit = False
        self.player_hit_animation_duration = 1000
        self.player_hit_animation_start_time = 0

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

            # Loading text
            loading_text = self.score_font.render('Loading...', True, WHITE)
            text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1))
            self.screen.blit(loading_text, text_rect)

            # Loading bar background
            pygame.draw.rect(self.screen, GREY, [loading_bar_x, loading_bar_y, loading_bar_width_max, loading_bar_height])

            # Loading bar progress
            current_bar_width = (loading_bar_width_max * i) // 100
            pygame.draw.rect(self.screen, GREEN, [loading_bar_x, loading_bar_y, current_bar_width, loading_bar_height])

            pygame.display.flip()
            pygame.time.wait(20)

    def show_welcome_screen(self):
        background_image_path = 'DarkerBackground.png'
        background_image = pygame.image.load(background_image_path)
        background_image = pygame.transform.scale(background_image,
                                                  (self.current_screen_width, self.current_screen_height))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False

            self.screen.fill(BLACK)
            self.screen.blit(background_image, (0, 0))

            title_font = pygame.font.Font(None, 72)
            title_text = title_font.render('Space Dodger', True, RED)
            title_rect = title_text.get_rect(center=(self.current_screen_width // 2, self.current_screen_height // 4))
            self.screen.blit(title_text, title_rect)

            description_font = pygame.font.Font(None, 36)
            descriptions = ["This game is all about dodging the incoming bullets.",
                            "Five of the highest scores land on the leaderboard, good luck!"]
            for i, line in enumerate(descriptions):
                description_text = description_font.render(line, True, WHITE)
                description_rect = description_text.get_rect(center=(self.current_screen_width // 2,
                                                                     self.current_screen_height // 2 + i * 30))
                self.screen.blit(description_text, description_rect)

            control_instructions = "Use arrow keys to move, Enter to select"
            control_text = description_font.render(control_instructions, True, WHITE)
            control_rect = control_text.get_rect(center=(self.current_screen_width // 2, self.current_screen_height // 1.5))
            self.screen.blit(control_text, control_rect)

            continue_text = description_font.render("Press Enter to continue...", True, GREEN)
            continue_rect = continue_text.get_rect(center=(self.current_screen_width // 2, self.current_screen_height // 1.3))
            self.screen.blit(continue_text, continue_rect)

            pygame.display.flip()
            self.clock.tick(60)

    def is_first_run(self):
        return not os.path.exists('leaderboard.json')

    def reset_game(self):
        self.score = 0
        self.spaceship = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60, 50, 30)
        self.bullet_group.empty()

    def save_settings(self):
        try:
            settings_path = 'settings.json'
            with open(settings_path, 'w') as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print("Failed to save these settings:", self.settings)

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.spaceship.x -= self.spaceship_speed
        if keys[pygame.K_RIGHT]:
            self.spaceship.x += self.spaceship_speed

        self.spaceship.x = max(0, min(self.spaceship.x, self.current_screen_width - self.spaceship.width))

    def update_player_model(self):
        current_time = pygame.time.get_ticks()

        if self.player_hit:
            elapsed_time = current_time - self.player_hit_animation_start_time

            # Calculate the visibility of the player based on the elapsed time and flash interval
            self.player_visible = elapsed_time % (2 * self.player_flash_interval) < self.player_flash_interval

            # Check if the hit animation duration has passed
            if elapsed_time > self.player_hit_animation_duration:
                # End the hit animation and reset related variables
                self.player_hit = False
                self.player_visible = True

        # Draw the player only if it's visible
        if self.player_visible:
            pygame.draw.rect(self.screen, WHITE, self.spaceship)

    def game_loop(self):
        self.reset_game()
        self.apply_settings()
        running = True
        self.last_bullet_time = pygame.time.get_ticks()
        self.player_hit = False
        self.player_hit_animation_start_time = 0
        self.player_hit_duration = 1000
        self.player_visible = True
        self.player_flash_interval = 200
        self.player_last_flash_time = pygame.time.get_ticks()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_time = pygame.time.get_ticks()

            # Check if the player has been hit and handle animation
            if self.check_collisions() and not self.player_hit:
                self.player_hit = True
                self.player_hit_animation_start_time = current_time

            # Game logic
            if not self.player_hit:
                self.handle_player_input()
                self.handle_bullet_generation()

            # Update the player model and game screen
            self.update_screen()
            self.update_score()

            # Flash the player model during hit animation
            if self.player_hit:
                elapsed_time = current_time - self.player_hit_animation_start_time
                if elapsed_time > self.player_hit_duration:
                    # Delay before showing game over screen
                    pygame.time.delay(2000)
                    running = False

            self.update_player_model()

            self.clock.tick(60)

        # After the game loop ends, go to the death screen
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
        if self.is_first_run():
            self.show_welcome_screen()

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
        self.enemy_speed = self.settings.get('enemy_speed', 10)
        self.spaceship_speed = self.settings.get('spaceship_speed', 5)

        if self.settings.get('fullscreen_mode', False):
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

            # Update the current screen size
        self.current_screen_width, self.current_screen_height = self.screen.get_size()

        # Update elements' positions and sizes
        self.reposition_game_elements()
        self.redraw_screen()


    def handle_bullet_generation(self):
        time_now = pygame.time.get_ticks()
        screen_width, _ = self.screen.get_size()


        enemy_frequency = {
            'Easy': 1100,
            'Medium': 700,
            'Hard': 350
        }
        interval = enemy_frequency[self.settings['amount_of_enemies']]

        if time_now - self.last_bullet_time > interval:
            bullet_x = random.randint(0, screen_width - 20)
            new_bullet = Bullet(bullet_x, 0, 20, 10, self.enemy_speed)
            self.bullet_group.add(new_bullet)
            self.last_bullet_time = time_now

    def update_screen(self):
        self.screen.fill(BLACK)
        self.bullet_group.update()
        screen_width, screen_height = self.screen.get_size()

        for bullet in self.bullet_group:
            self.screen.blit(bullet.image, bullet.rect)

        # Only draw the player as white when it's visible during blinking animation
        if self.player_visible:
            pygame.draw.rect(self.screen, WHITE, self.spaceship)

        self.draw_text(f'Score: {self.score}', self.score_font, self.current_screen_width * 0.05,
                       self.current_screen_height * 0.05)
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

    # Reposition the spaceship and any other elements
    def reposition_game_elements(self):
        screen_width, screen_height = self.screen.get_size()

        self.spaceship.x = self.current_screen_width // 2 - self.spaceship.width // 2
        self.spaceship.y = self.current_screen_height - 60 - self.spaceship.height

    def redraw_screen(self):
        self.screen.fill(BLACK)

        pygame.draw.rect(self.screen, WHITE, self.spaceship)

        for bullet in self.bullet_group:
            self.screen.blit(bullet.image, bullet.rect)

        score_text = self.score_font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

if __name__ == '__main__':
    game = Main()
    game.run()

