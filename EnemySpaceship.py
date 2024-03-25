from math import cos
from math import sin
import pygame
import random
from PVector import PVector
from Spaceship import Spaceship


class EnemySpaceship(Spaceship):
    # initialize with screen dimensions
    def __init__(self, screen_width, screen_height, size, mass, max_speed, bullet_color, friction, image_str):
        # call the constructor of the parent class, no need to initialize attributes of the parent class
        super().__init__(screen_width, screen_height, size, mass, max_speed, bullet_color, friction, image_str)

        # initialize random location, velocity and acceleration in upper half of screen
        self.location = PVector(random.randint(0, self.screen_width - self.size), random.randint(0, self.size))

        self.fire_time = 0  # count when is time to fire a bullet
        self.wander_theta = 0  # initial angle for wander method

        self.rect.center = (self.location.x, self.location.y)

    # create a wandering path for the object
    def wander(self):
        WANDER_RADIUS = 100  # radius of wander circle - smaller => more straight movement
        WANDER_DISTANCE = 100  # distance of current location to center of wander circle - larger => less jitter in move
        CHANGE_ANGLE = 0.6  # +/- angle area in radians - larger => more jitter

        # compute random theta angle
        self.wander_theta += random.uniform(-CHANGE_ANGLE, CHANGE_ANGLE)

        # calculate the new location to steer towards on the wander circle
        # copy velocity to circle center and calculate unit vector
        circle_center = PVector(self.velocity.x, self.velocity.y)
        circle_center.normalize()

        # multiply by distance
        circle_center.multiplyByConstant(WANDER_DISTANCE)
        circle_center.add(self.location)
        heading = self.velocity.heading2D()
        circle_offset = PVector(WANDER_RADIUS * cos(self.wander_theta + heading),
                                WANDER_RADIUS * sin(self.wander_theta + heading))
        circle_center.add(circle_offset)

        # now that we have the target location, seek it
        self.seek(circle_center)

    # specific move method of enemy spaceship
    def move(self):
        self.wander()
        self.boundaries()
        self.random_fire()
        self.update_position()
        # move bullets
        self.move_bullets('DOWN')

    def random_fire(self):
        # Check if it's time to fire: it starts with time = 0 then gets current time, adds random internal then fires then sets fire time to current
        current_time = pygame.time.get_ticks()
        if current_time - self.fire_time > random.randint(1000, 3000):  # Adjust firing interval
            self.fire_bullet()
            self.fire_time = current_time
