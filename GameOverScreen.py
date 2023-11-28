import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
class GameOverScreen:
    def __init__(self, screen, font, score):
        self.screen = screen
        self.font = font
        self.score = score
        self.running = True
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill(BLACK)
        game_over_text = self.font.render('GAME OVER', True, WHITE)
        score_text = self.font.render(f'Final Score: {self.score}', True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()

    def run(self, score):
        self.draw()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.running = False
            self.clock.tick(60)

        return 'Restart'
