# Erik Williams
# CPSC 386-02
# 2023-04-20
# epwilliams@csu.fullerton.edu
# @EPW80
#
# Lab 05-00
#
# This is a pygame project!
#

"""This is my Space Invaders project!"""

import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

ASSETS_PATH = "videogame/data/space_invaders_assets/space_invaders_assets/"


class Player(pygame.sprite.Sprite):
    """Player class."""

    @staticmethod
    def load_image():
        """Load the player image"""
        return pygame.image.load(
            "videogame/data/space_invaders_assets/space_invaders_assets/player_ship.png"
        )

    @staticmethod
    def load_shoot_sound():
        """Load the shoot sound"""
        return pygame.mixer.Sound(
            "videogame/data/space_invaders_assets/space_invaders_assets/player_fire.wav"
        )

    def __init__(self, bullet_group, player_name=None, score=None):
        """Initialize the player"""
        super().__init__()
        self.image = Player.load_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 100
        self.lives = 3
        self.velocity = 8
        self.bullet_group = bullet_group
        self.player_name = player_name
        self.score = score
        self.shoot_sound = Player.load_shoot_sound()

    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.velocity

    def fire(self):
        """Fire the bullet"""
        if len(self.bullet_group) < 2:
            self.shoot_sound.play()
            PlayerBullet(self.rect.centerx, self.rect.top, self.bullet_group)

    def reset(self):
        """Reset the player"""
        self.rect.centerx = WINDOW_WIDTH // 2

    def __getstate__(self):
        """Return the player state"""
        state = self.__dict__.copy()
        if "image" in state:
            del state["image"]
        if "shoot_sound" in state:
            del state["shoot_sound"]
        return state

    def __setstate__(self, state):
        """Set the player state"""
        self.__dict__.update(state)
        self.image = pygame.image.load(ASSETS_PATH + "player_ship.png").convert_alpha()
        self.shoot_sound = Player.load_shoot_sound()


class PlayerBullet(pygame.sprite.Sprite):
    """Player Bullet class."""

    @staticmethod
    def load_image():
        """Load the bullet image"""
        return pygame.image.load(
            "videogame/data/space_invaders_assets/space_invaders_assets/green_laser.png"
        )

    # pylint: disable=invalid-name
    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()
        self.image = PlayerBullet.load_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y -= self.velocity

        if self.rect.bottom < 0:
            self.kill()
