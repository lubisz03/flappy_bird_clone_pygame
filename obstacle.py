import pygame
from random import choice, randint
from settings import *


class Obstacle(pygame.sprite.Sprite):
    """Handles obstacles in the game."""

    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'
        self.scored = False
        orientation = choice(('up', 'down'))
        surf = pygame.image.load(
            f'./graphics/obstacles/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(
            surf, pygame.math.Vector2(surf.get_size()) * scale_factor)
        x = WINDOW_WIDTH + randint(50, 100)
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, score):
        """Updates the obstacle's position."""
        self.pos.x -= 400 * INCREASE_FACTOR**score * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
