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
        screen_width, screen_height = self.screen.get_size()

        self.screen.fill(BLACK)

        # Make 'GAME OVER' text bigger, considering screen size
        game_over_font_size = int(screen_height * 0.15)
        game_over_font = pygame.font.Font(None, game_over_font_size)
        game_over_text = game_over_font.render('GAME OVER', True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 3))
        self.screen.blit(game_over_text, game_over_rect)

        # Make 'Final Score' and 'Enter Name' texts smaller with a margin top
        small_font_size = int(screen_height * 0.07)
        small_font = pygame.font.Font(None, small_font_size)
        score_text = small_font.render(f'Final Score: {score}', True, WHITE)
        name_text = small_font.render(f'Enter Name: {self.name}', True, WHITE)
        score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
        name_rect = name_text.get_rect(center=(screen_width // 2, screen_height // 2 + int(screen_height * 0.05)))

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
