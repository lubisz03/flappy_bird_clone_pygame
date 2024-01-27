import pygame
import time
import sys
from settings import *
from obstacle import Obstacle
from plane import Plane
from ground import Ground
from background import BG


class Game:
    """Main game logic"""

    def __init__(self):
        """Initial setup for the game."""
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Flappy Bird Clone')
        self.clock = pygame.time.Clock()
        self.active = False
        self.initial_start = True

        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        bg_height = pygame.image.load(
            './graphics/environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)

        self.font = pygame.font.Font(
            './graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,
                              int(1400 * DECREASE_FACTOR**self.score))

        self.menu_surf = pygame.image.load(
            './graphics/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.bg_sound = pygame.mixer.Sound('./sounds/music.wav')
        self.bg_sound.set_volume(0.1)
        self.bg_sound.play(loops=-1)

    def collisions(self):
        """Checks if the player's plane hits an obstacle or the top of the screen. Ends the game if there is a collision."""
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)\
                or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        """Displays the current score during the game and on the game over screen."""
        if not self.initial_start:
            if self.active:
                for sprite in self.collision_sprites.sprites():
                    if sprite.sprite_type == 'obstacle':
                        if self.plane.rect.left > sprite.rect.right and not sprite.scored:
                            self.score += 1
                            sprite.scored = True
                y = WINDOW_HEIGHT / 10
            else:
                y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

            score_surf = self.font.render(f'{self.score}', True, 'black')
            score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
            self.display_surface.blit(score_surf, score_rect)

    def run(self):
        """Main game loop. Handles game updates, drawing, and player input."""
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.active:
                            self.plane.jump()
                        elif self.initial_start:
                            self.plane = Plane(
                                self.all_sprites, self.scale_factor / 1.7)
                            self.initial_start = False
                            self.active = True
                        else:
                            self.plane = Plane(
                                self.all_sprites, self.scale_factor / 1.7)
                            self.active = True
                            self.score = 0
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites],
                             self.scale_factor * 1.1)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.display_surface)
            self.display_score()
            self.all_sprites.update(dt, self.score)

            if self.active:
                self.collisions()
            elif self.initial_start:
                start_surf = self.font.render(
                    'Press SPACE to start', True, 'black')
                start_rect = start_surf.get_rect(
                    midtop=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
                self.display_surface.blit(start_surf, start_rect)
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)
