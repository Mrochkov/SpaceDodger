import pygame
import math

from SettingsScreen import SettingsScreen

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 0)
GREY = (104, 104, 104)
YELLOW = (252, 186, 3)
BLUE = (32, 3, 252)
RED = (252, 3, 3)
GREEN = (48, 242, 0)
PURPLE = (125, 0, 163)
ORANGE = (255, 98, 0)


class StartScreen:
    def __init__(self, screen, font_size, current_settings, background_image_path='DarkerBackground.png'):
        self.screen = screen
        self.font_size = font_size
        self.current_settings = current_settings
        self.font = pygame.font.Font(None, font_size)
        background_image = pygame.image.load(background_image_path)
        self.background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
        self.running = True
        self.selected = 0
        self.menu_options = ['Start Game', 'Settings', 'Leaderboards', 'Quit']
        self.menu_animation_time = 0
        self.clock = pygame.time.Clock()

    def draw_menu(self):
        screen_width, screen_height = self.screen.get_size()
        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0, 0))
        menu_start_y = 300

        for index, option in enumerate(self.menu_options):
            if index == self.selected:
                animation_scale = math.sin(self.menu_animation_time) * 10
                animated_font_size = int(self.font_size + animation_scale)
                animated_font = pygame.font.Font(None, animated_font_size)
                text = animated_font.render(option, True, HIGHLIGHT)
            else:
                text = self.font.render(option, True, GREY)

            text_rect = text.get_rect(center=(screen_width // 2, menu_start_y + index * 60))
            self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.menu_animation_time += dt * 4

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'Quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        if self.menu_options[self.selected] == 'Settings':
                            settings_screen = SettingsScreen(self.screen, self.font, self.current_settings)
                            updated_settings = settings_screen.run()
                            if updated_settings:
                                self.current_settings.update(updated_settings)
                        elif self.menu_options[self.selected] == 'Quit':
                            return 'Quit'
                        else:
                            return self.menu_options[self.selected]

            self.draw_menu()
        return 'Quit'

