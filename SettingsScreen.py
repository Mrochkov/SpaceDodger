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
            'difficulty': 'Normal',  # This could be 'Easy', 'Normal', or 'Hard'
            'game_speed': 'Normal',  # This could be 'Slow', 'Normal', or 'Fast'
        }

    def draw(self):
        self.screen.fill(BLACK)
        settings_title = self.font.render('Settings', True, WHITE)
        title_rect = settings_title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(settings_title, title_rect)

        for index, option in enumerate(self.options):
            text_color = HIGHLIGHT if index == self.selected else GREY
            text = f'{option}: {self.settings.get(option.lower().replace(" ", "_"), "Not Set")}'
            option_text = self.font.render(text, True, text_color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, 150 + index * 50))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()

    def change_setting(self):
        current_option = self.options[self.selected].lower().replace(" ", "_")
        if current_option in self.settings:
            self.cycle_setting(current_option)

    def cycle_setting(self, setting):
        options_list = DIFFICULTY_LEVELS if setting == 'difficulty' else GAME_SPEEDS
        current_index = options_list.index(self.settings[setting])
        next_index = (current_index + 1) % len(options_list)
        self.settings[setting] = options_list[next_index]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'Quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == 'Back':
                        return 'Back'
                    else:
                        self.change_setting()
        return None

    def run(self):
        result = None
        while result is None:
            self.draw()
            result = self.handle_input()

        return self.settings if result != 'Quit' else None
