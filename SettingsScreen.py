import pygame



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT = (255, 255, 0)
GREY = (104, 104, 104)



class SettingsScreen:
    def __init__(self, screen, font, current_settings):
        self.screen = screen
        self.font = font
        self.settings = current_settings
        self.options = ['Spaceship Speed', 'Enemy Speed', 'Amount of Enemies', 'Fullscreen Mode', 'Save Settings']
        self.selected = 0
        self.difficulty_levels = ['Easy', 'Medium', 'Hard']

        self.background_image_path = 'DarkerBackground.png'
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())


    def draw(self):
        screen_width, screen_height = self.screen.get_size()

        self.screen.fill(BLACK)
        self.screen.blit(self.background_image, (0, 0))

        settings_title = self.font.render('Settings', True, WHITE)
        title_rect = settings_title.get_rect(center=(screen_width // 2, 50))
        self.screen.blit(settings_title, title_rect)

        for index, option in enumerate(self.options):
            text_color = HIGHLIGHT if index == self.selected else WHITE
            text = f'{option}: {self.settings.get(option.lower().replace(" ", "_"))}'
            option_text = self.font.render(text, True, text_color)
            option_rect = option_text.get_rect(center=(screen_width // 2, 150 + index * 50))
            self.screen.blit(option_text, option_rect)

        pygame.display.flip()

    def change_setting(self):
        current_option = self.options[self.selected].lower().replace(" ", "_")

        if current_option == 'fullscreen_mode':
            self.settings[current_option] = not self.settings.get(current_option, False)
        elif current_option == 'amount_of_enemies':
            current_index = self.difficulty_levels.index(self.settings[current_option])
            new_index = (current_index + 1) % len(self.difficulty_levels)
            self.settings[current_option] = self.difficulty_levels[new_index]
        elif current_option in self.settings:
            current_value = self.settings[current_option]
            new_value = current_value + 1
            if new_value > 15:
                new_value = 1
            self.settings[current_option] = new_value
            pass

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
                    print(f"Selected option: {self.options[self.selected]}")
                    if self.options[self.selected] == 'Save Settings':
                        return 'Save'
                    else:
                        self.change_setting()
        return None

    def run(self):
        result = None
        while result is None:
            self.draw()
            result = self.handle_input()

        if result == 'Save':
            print("Saving settings from SettingsScreen:", self.settings)
            return self.settings
        return None

