import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 0)
GREY = (104, 104, 104)

DIFFICULTY_LEVELS = ['Easy', 'Normal', 'Hard']
GAME_SPEEDS = ['Slow', 'Normal', 'Fast']

class SettingsScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ['Difficulty', 'Game Speed', 'Back']
        self.selected = 0
        self.settings = {
            'difficulty': 'Normal',
            'game_speed': 'Normal',
        }

    def draw(self):
        self.screen.fill(BLACK)
        settings_title = self.font.render('Settings', True, WHITE)
        title_rect = settings_title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(settings_title, title_rect)

        for index, option in enumerate(self.options):
            text_color = HIGHLIGHT if index == self.selected else GREY
            setting_value = self.settings.get(option.lower().replace(" ", "_"), 'Not Set')
            option_text = self.font.render(f'{option}: {setting_value}', True, text_color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 150 + index * 60))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()

    def change_setting(self):
        current_option = self.options[self.selected].lower().replace(" ", "_")
        if current_option in ['difficulty', 'game_speed']:
            current_setting = self.settings[current_option]
            options_list = DIFFICULTY_LEVELS if current_option == 'difficulty' else GAME_SPEEDS
            current_index = options_list.index(current_setting)
            next_index = (current_index + 1) % len(options_list)
            self.settings[current_option] = options_list[next_index]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return self.settings
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected] == 'Back':
                            running = False
                        else:
                            self.change_setting()

            self.draw()

        return self.settings  # Return the updated settings

