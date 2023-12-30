import json
import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

    def load_leaderboard(self):
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)

            # Convert list to the new dictionary format if necessary
            if isinstance(data, list):
                # Assuming the existing list is for one of the difficulties, e.g., 'Easy'
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
        # Use 'leaderboard' instead of 'leaderboards'
        self.leaderboard[difficulty].append({'name': name, 'score': score})
        self.leaderboard[difficulty] = sorted(self.leaderboard[difficulty], key=lambda x: x['score'], reverse=True)[:20]
        self.save_leaderboard()

    def display(self):
        self.screen.fill(BLACK)

        # Screen divided into three sections
        section_height = SCREEN_HEIGHT // 3
        difficulties = ['Easy', 'Medium', 'Hard']
        max_entries_per_section = 5  # Limit to 5 entries per difficulty

        for i, difficulty in enumerate(difficulties):
            y_start = section_height * i
            y_end = y_start + section_height

            # Draw a horizontal line to separate the sections
            if i > 0:
                pygame.draw.line(self.screen, WHITE, (0, y_start), (SCREEN_WIDTH, y_start), 3)

            # Display each leaderboard in its section
            for j, entry in enumerate(self.leaderboard[difficulty][:max_entries_per_section]):
                entry_text = self.font.render(f'{j + 1}. {entry["name"]}: {entry["score"]}', True, WHITE)
                self.screen.blit(entry_text, (100, y_start + 30 + j * 30))

            # Display the difficulty level title
            difficulty_text = self.font.render(f'{difficulty} Difficulty', True, WHITE)
            self.screen.blit(difficulty_text, (SCREEN_WIDTH // 2, y_start + 5))

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
                        print("Back button clicked")
                        waiting = False

        return
