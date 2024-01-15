import json
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (252, 3, 3)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Leaderboards:
    def __init__(self, screen, font, file_path='leaderboard.json'):
        self.screen = screen
        self.font = font
        self.file_path = file_path
        self.leaderboard = self.load_leaderboard()
        self.back_button_font = pygame.font.Font(None, 36)
        self.back_button_text = 'Back'
        self.back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 100, 100, 40)

        self.background_image_path = 'DarkerBackground.png'
        self.background_image = pygame.image.load(self.background_image_path)
        self.background_image = pygame.transform.scale(self.background_image, self.screen.get_size())

    def load_leaderboard(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)

            # Convert list to the new dictionary format if necessary
            if isinstance(data, list):
                data = {'Easy': data, 'Medium': [], 'Hard': []}

            # Ensure all difficulty levels are present
            for level in ['Easy', 'Medium', 'Hard']:
                data.setdefault(level, [])
            return data

        except FileNotFoundError:
            return {'Easy': [], 'Medium': [], 'Hard': []}
        except json.JSONDecodeError:
            return {'Easy': [], 'Medium': [], 'Hard': []}

    def save_leaderboard(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.leaderboard, f, indent=4)

    def update_leaderboard(self, name, score, difficulty):
        self.leaderboard[difficulty].append({'name': name, 'score': score})
        self.leaderboard[difficulty] = sorted(self.leaderboard[difficulty], key=lambda x: x['score'], reverse=True)[:20]
        self.save_leaderboard()

    def display(self):
        screen_width, screen_height = self.screen.get_size()

        # Scale the background based on current screen size
        scaled_background = pygame.transform.scale(self.background_image, (screen_width, screen_height))
        self.screen.blit(scaled_background, (0, 0))

        # three sections
        section_height = screen_height // 3
        difficulties = ['Easy', 'Medium', 'Hard']
        max_entries_per_section = 5

        for i, difficulty in enumerate(difficulties):
            y_start = section_height * i
            y_end = y_start + section_height

            # horizontal line
            if i > 0:
                pygame.draw.line(self.screen, WHITE, (0, y_start), (screen_width, y_start), 3)

            # Sections
            for j, entry in enumerate(self.leaderboard[difficulty][:max_entries_per_section]):
                entry_text = self.font.render(f'{j + 1}. {entry["name"]}: {entry["score"]}', True, WHITE)
                self.screen.blit(entry_text, (100, y_start + 30 + j * 30))

            # Titles
            difficulty_text = self.font.render(f'{difficulty} Difficulty', True, RED)
            self.screen.blit(difficulty_text, (screen_width // 2, y_start + 5))

        pygame.display.flip()


        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                        waiting = False

        return
