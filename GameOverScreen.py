import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class GameOverScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.running = True
        self.clock = pygame.time.Clock()
        self.name = ""


    def draw(self, score):
        self.screen.fill(BLACK)
        game_over_text = self.font.render('GAME OVER', True, WHITE)
        score_text = self.font.render(f'Final Score: {score}', True, WHITE)
        name_text = self.font.render(f'Enter Name: {self.name}', True, WHITE)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(name_text, name_rect)

        pygame.display.flip()

    def run(self, score):
        self.name = ""
        enter_name = True
        while enter_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        enter_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode

            self.draw(score)
            self.clock.tick(60)

        return self.name
