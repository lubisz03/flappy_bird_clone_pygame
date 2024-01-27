import pygame
from settings import *


class BG(pygame.sprite.Sprite):
    """Handles the background image in the game."""

    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.bg_image = pygame.image.load(
            './graphics/environment/background.png').convert()
        full_height = self.bg_image.get_height() * scale_factor
        full_width = self.bg_image.get_width() * scale_factor
        full_sized_image = pygame.transform.scale(
            self.bg_image, (full_width, full_height))
        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt, score):
        """Updates background position for scrolling effect."""
        self.pos.x -= 300 * INCREASE_FACTOR**score * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
