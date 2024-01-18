import pygame
from settings import *


class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_vector):
        super().__init__(groups)
        self.bg_image = pygame.image.load(
            './graphics/environment/background.png').convert()

        full_height = self.bg_image.get_height() * scale_vector
        full_width = self.bg_image.get_width() * scale_vector
        full_sized_image = pygame.transform.scale(
            self.bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_sized_image, (0, 0))
        self.image.blit(full_sized_image, (full_width, 0))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)


class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scale_vector):
        super().__init__(groups)

        # image
        ground_surf = pygame.image.load(
            './graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(
            ground_surf, pygame.math.Vector2(ground_surf.get_size()) * scale_vector)

        # position
        self.rect = self.image.get_rect(
            bottomleft=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
