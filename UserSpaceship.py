import pygame
from PVector import PVector
from Spaceship import Spaceship

KEYS_FORCE = 3

class UserSpaceship(Spaceship):
    def __init__(self, screen_width, screen_height, size, mass, bullet_color, friction, image_str):
        # call the constructor of the parent class, no need to initialize attributes of the parent class
        super().__init__(screen_width, screen_height, size, mass, bullet_color, friction, image_str)

        # display spaceship in the screen center
        self.rect.center = (self.screen_width / 2, self.screen_height / 2)
        # set initial location of the user spaceship in the bottom center
        self.location = PVector(self.screen_width / 2, self.screen_height - self.size)


    # the specific move method of the user spaceship
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.apply_force(PVector(-KEYS_FORCE, 0))
        if keys[pygame.K_RIGHT] and self.rect.x < self.screen_width - self.size:
            self.apply_force(PVector(KEYS_FORCE, 0))
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.apply_force(PVector(0, -KEYS_FORCE))
        if keys[pygame.K_DOWN] and self.rect.y < self.screen_height - self.size:
            self.apply_force(PVector(0, KEYS_FORCE))

        self.boundaries()
        self.update_position()

        # move bullets
        self.move_bullets('UP')

