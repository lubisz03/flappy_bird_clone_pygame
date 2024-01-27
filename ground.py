import pygame
from settings import *


class Ground(pygame.sprite.Sprite):
    """Handles the ground image in the game."""

    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'ground'
        ground_surf = pygame.image.load(
            './graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(
            ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_factor)
        self.rect = self.image.get_rect(bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, score):
        """Updates ground position for scrolling effect."""
        self.pos.x -= 360 * INCREASE_FACTOR**score * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
