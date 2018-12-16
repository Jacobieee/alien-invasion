import pygame.font

class Button():
    def __init__(self, ai_settings, screen, msg):
        # initialization.
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # dimension of the button.
        