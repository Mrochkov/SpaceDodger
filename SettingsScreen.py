import pygame
import math

# Define colors
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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class SettingsScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.clock = pygame.time.Clock()
        self.options = ['Difficulty', 'Game Speed', 'Change Colors', 'Back']
        self.selected = 0
        self.difficulty = 'Normal'
        self.game_speed = 'Normal'
        self.color = WHITE

    def draw(self):
        self.screen.fill(BLACK)
        settings_title = self.font.render('Settings', True, WHITE)
        title_rect = settings_title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(settings_title, title_rect)

        for index, option in enumerate(self.options):
            text_color = HIGHLIGHT if index == self.selected else GREY
            if option == 'Change Colors':
                option_text = self.font.render('Change Colors', True, text_color)
            else:
                attribute_value = getattr(self, option.lower().replace(" ", "_"), 'Not Set')
                option_text = self.font.render(f'{option}: {attribute_value}', True, text_color)

            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 150 + index * 50))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected] == 'Back':
                            running = False
                        # changing difficulty, game speed, and color

            self.draw()
            self.clock.tick(60)
