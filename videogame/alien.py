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

"""Space Invaders project"""
import random
import pygame

pygame.init()
pygame.mixer.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class Alien(pygame.sprite.Sprite):
    """Alien class."""
    image = None
    shoot_sound = None

    @staticmethod
    def load_image():
        """Load the alien image"""
        return pygame.image.load(
            "videogame/data/space_invaders_assets/space_invaders_assets/alien.png"
        )

    @staticmethod
    def load_shoot_sound():
        """Load the alien fire sound"""
        return pygame.mixer.Sound(
            "videogame/data/space_invaders_assets/space_invaders_assets/alien_fire.wav"
        )

    # pylint: disable=invalid-name
    def __init__(self, x, y, velocity, bullet_group):
        """Initialize the alien"""
        super().__init__()

        if Alien.image is None:
            Alien.image = Alien.load_image()
        if Alien.shoot_sound is None:
            Alien.shoot_sound = Alien.load_shoot_sound()

        self.image = Alien.image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.starting_x = x
        self.starting_y = y

        self.direction = 1
        self.velocity = velocity
        self.bullet_group = bullet_group

    def update(self):
        """Update the alien"""
        self.rect.x += self.direction * self.velocity

        # Randomly fire a bullet
        if random.randint(0, 1000) > 999 and len(self.bullet_group) < 3:
            Alien.shoot_sound.play()
            self.fire()

    def fire(self):
        """Fire a bullet"""
        AlienBullet(self.rect.centerx, self.rect.bottom, self.bullet_group)

    def reset(self):
        """Reset the alien position"""
        self.rect.topleft = (self.starting_x, self.starting_y)
        self.direction = 1

    def __getstate__(self):
        """Return the alien state"""
        state = self.__dict__.copy()
        if "image" in state:
            del state["image"]
        if "shoot_sound" in state:
            del state["shoot_sound"]
        return state

    def __setstate__(self, state):
        """Set the alien state"""
        self.__dict__.update(state)
        self.image = Alien.load.image()
        self.shoot_sound = Alien.load.shoot_sound()


class AlienBullet(pygame.sprite.Sprite):
    """Alien Bullet class."""

    @staticmethod
    def load_image():
        """Load the bullet image"""
        return pygame.image.load(
            "videogame/data/space_invaders_assets/space_invaders_assets/red_laser.png"
        )

    # pylint: disable=invalid-name
    def __init__(self, x, y, bullet_group):
        """Initialize the bullet"""
        super().__init__()
        self.image = AlienBullet.load_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        self.velocity = 10
        bullet_group.add(self)

    def update(self):
        """Update the bullet"""
        self.rect.y += self.velocity

        # If the bullet is off the screen, kill it
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
