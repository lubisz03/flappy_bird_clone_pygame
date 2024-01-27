import pygame
from settings import *


class Plane(pygame.sprite.Sprite):
    """Handles the player's plane in the game."""

    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(
            midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.gravity = 600
        self.direction = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.jump_sound = pygame.mixer.Sound('./sounds/jump.wav')
        self.jump_sound.set_volume(0.3)

    def import_frames(self, scale_factor):
        """Loads and scales plane images."""
        self.frames = []
        for i in range(3):
            surf = pygame.image.load(
                f'./graphics/plane/red{i}.png').convert_alpha()
            scaled_surface = pygame.transform.scale(
                surf, pygame.math.Vector2(surf.get_size())*scale_factor)
            self.frames.append(scaled_surface)

    def apply_gravity(self, dt):
        """Applies gravity to the plane."""
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = round(self.pos.y)

    def jump(self):
        """Makes the plane jump."""
        self.jump_sound.play()
        self.direction = -350

    def animate(self, dt):
        """Animates the plane's flight."""
        self.frame_index += 10 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def rotate(self):
        """Rotates the plane based on its direction."""
        rotated_plane = pygame.transform.rotozoom(
            self.image, -self.direction * 0.075, 1)
        self.image = rotated_plane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt, score):
        """Updates the plane's position and animation."""
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()
