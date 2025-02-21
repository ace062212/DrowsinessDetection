import pygame
from ..config.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Display:
    def __init__(self):
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Speed Control System')
        
        # Colors and fonts
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    def update_display(self, speed):
        # Clear screen
        self.screen.fill(self.black)
        
        # Render speed text
        text = self.font.render(f'Speed: {int(speed)}', True, self.white)
        text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
        self.screen.blit(text, text_rect)
        
        # Update display
        pygame.display.flip()

    def cleanup(self):
        pygame.quit()