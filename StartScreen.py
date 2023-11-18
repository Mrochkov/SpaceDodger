import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class StartScreen:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.running = True

    def run(self):
        self.screen.fill(BLACK)
        start_text = self.font.render('Press any key to start', True, WHITE)
        start_rect = start_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(start_text, start_rect)
        pygame.display.flip()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                if event.type == pygame.KEYUP:
                    self.running = False
            pygame.time.wait(100)
        return True