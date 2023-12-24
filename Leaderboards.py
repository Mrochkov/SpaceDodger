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
                print("Loaded leaderboard:", data)  # Debugging print
                return data
        except FileNotFoundError:
            print("Leaderboard file not found, creating a new one.")
            return []
        except json.JSONDecodeError:
            print("Error decoding JSON from leaderboard file.")
            return []

    def save_leaderboard(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.leaderboard, f, indent=4)

    def update_leaderboard(self, name, score):
        self.leaderboard.append({'name': name, 'score': score})
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x['score'], reverse=True)[:20]
        self.save_leaderboard()

    def display(self):
        self.screen.fill(BLACK)
        for i, entry in enumerate(self.leaderboard):
            entry_text = self.font.render(f'{i + 1}. {entry["name"]}: {entry["score"]}', True, WHITE)
            self.screen.blit(entry_text, (100, 50 + i * 30))

        pygame.draw.rect(self.screen, WHITE, self.back_button_rect)
        back_text = self.back_button_font.render(self.back_button_text, True, BLACK)
        back_text_rect = back_text.get_rect(center=self.back_button_rect.center)
        self.screen.blit(back_text, back_text_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False  # Only stop waiting, not quit the entire app
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                        print("Back button clicked")  # Debugging statement
                        waiting = False

        return
