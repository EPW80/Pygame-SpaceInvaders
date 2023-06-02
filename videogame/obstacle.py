# Erik Williams
# CPSC 386-02
# 2023-04-20
# epwilliams@csu.fullerton.edu
# @EPW80
#
# Lab 05-00
#
# This is my Space Invaders project!
#

"""This is my Space Invaders project!"""
import random
import pygame

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800


class Obstacle(pygame.sprite.Sprite):
    """A class to represent an obstacle"""

    @staticmethod
    def load_image():
        """Load the obstacle image"""
        return pygame.image.load(
            "videogame/data/space_invaders_assets/space_invaders_assets/rock.png"
        )

    image = load_image.__func__()

    # pylint: disable=invalid-name
    def __init__(self, x, y, velocity):
        """Initialize the obstacle"""
        super().__init__()
        self.image = Obstacle.load_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.start_x = x
        self.start_y = y
        self.velocity = velocity
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.counter = 0

    def update(self):
        """Update the obstacle"""
        self.rect.x += self.direction_x * self.velocity
        self.rect.y += self.direction_y * self.velocity
        self.counter += 1

        if self.counter >= 60:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])
            self.counter = 0

        if self.rect.left < 0:
            self.rect.left = 0
            self.direction_x = 1
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.direction_x = -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.direction_y = 1
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.direction_y = -1

    def __getstate__(self):
        """Return the state of the obstacle"""
        state = self.__dict__.copy()
        if "image" in state:
            del state["image"]
        return state

    def __setstate__(self, state):
        """Set the state of the obstacle"""
        self.__dict__.update(state)
        self.image = Obstacle.load_image()

    def reset(self):
        """Reset the obstacle"""
        self.rect.topleft = (self.start_x, self.start_y)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.counter = 0
