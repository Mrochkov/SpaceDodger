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
        self.leaderboard = sorted(self.leaderboard, key=lambda x: x['score'], reverse=True)[:10]  # Keep top 10 scores
        self.save_leaderboard()

    def display(self):
        self.screen.fill(BLACK)
        for i, entry in enumerate(self.leaderboard):
            entry_text = self.font.render(f'{i + 1}. {entry["name"]}: {entry["score"]}', True, WHITE)
            self.screen.blit(entry_text, (100, 50 + i * 30))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        waiting = False
