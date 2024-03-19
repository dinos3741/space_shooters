from math import cos
from math import sin
import pygame
import random
from PVector import PVector
from Bullet import Bullet

BULLET_SPEED = 5
MAX_SPEED = 4
YELLOW = (134, 123, 23)

class EnemySpaceship:
    # initialize with screen dimensions
    def __init__(self, screen_width, screen_height, size, mass):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.mass = mass
        self.is_alive = True  # Flag to track if the enemy spaceship is alive

        # initialize random location, velocity and acceleration
        self.location = PVector( random.randint(0, self.screen_width - self.size), random.randint(0, self.screen_height // 2 - self.size) )
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)

        self.fire_time = 0  # count when is time to fire a bullet

        self.wander_theta = 0  # initial angle for wander method

        # load spaceship png image (needs to be in the same folder as the code files)
        self.image = pygame.image.load("enemy.png")  # Replace "spaceship.png" with your image file
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

        self.rect = self.image.get_rect()
        self.rect.center = (self.location.x, self.location.y)

        # visible bullets array
        self.bullets = []


    # updates the current position based on forces applied
    def update_position(self):
        # add acceleration to velocity:
        self.velocity.add(self.acceleration)

        # limit maximum velocity
        self.velocity.limit(MAX_SPEED)

        # add velocity to position:
        self.location.add(self.velocity)

        # update position of object on screen
        self.rect.center = (self.location.x, self.location.y)

        # reset the acceleration at the end of each frame:
        self.acceleration.multiplyByConstant(0)


    # apply force to the spaceship
    def apply_force(self, force):
        f = PVector(0, 0)
        force.copy(f)  # copy force to temporary f
        f = force.divideByConstant(self.mass)
        self.acceleration.add(f)  # update the acceleration vector


    # calculate and apply steering force towards a target
    def seek(self, target):
        CLOSE_ENOUGH = 50  # distance from target in order to detect arriving and stop - more than 30 looks unnatural

        # subtract the current location from the target location vector to find the desired direction vector:
        desired = target.subtract(self.location)  # desired velocity = target position - current position

        distance = desired.get_Magnitude()  # this is how far the target is

        # get the unit vector in the direction of the desired vector
        desired.normalize()

        if distance < CLOSE_ENOUGH:  # if we arrive close to the target
            # limit with the max speed of the vehicle (if instead -max_speed, we have fleeing behaviour)
            desired.multiplyByConstant(MAX_SPEED * distance / CLOSE_ENOUGH)
        else:
            # create velocity equal to the max speed of the object
            desired.multiplyByConstant(MAX_SPEED)

        # Subtract the desired from the current velocity to create the steering force vector:
        steering_force = desired.subtract(self.velocity)  # steering force = desired vector - current velocity

        # now apply the steering force to the object
        self.apply_force(steering_force)


    # create a wandering path for the object
    def wander(self):
        WANDER_RADIUS = 50  # radius of wander circle - smaller => more straight movement
        WANDER_DISTANCE = 100  # distance of current location to center of wander circle - larger => less jitter in move
        CHANGE_ANGLE = 0.3  # +/- angle area in radians - larger => more jitter

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
        circle_offset = PVector(WANDER_RADIUS * cos(self.wander_theta + heading), WANDER_RADIUS * sin(self.wander_theta + heading))
        circle_center.add(circle_offset)

        # now that we have the target location, seek it
        self.seek(circle_center)


    # boundaries method is used to avoid ecosystem boundaries and turn
    def boundaries(self):
        DISTANCE_FROM_BORDER = 60  # the distance from the borders where it starts to change direction
        # desired velocity is a vector from current location until target: target - location, but in this case
        # it's a vector opposite to the x-coordinate
        if self.location.x < DISTANCE_FROM_BORDER:  # close to left wall
            desired = PVector(MAX_SPEED, self.velocity.y)
        elif self.location.x > self.screen_width - DISTANCE_FROM_BORDER:  # close to right wall
            desired = PVector(-MAX_SPEED, self.velocity.y)
        elif self.location.y < DISTANCE_FROM_BORDER:  # close to ceiling
            desired = PVector(self.velocity.x, MAX_SPEED)
        elif self.location.y > self.screen_height - DISTANCE_FROM_BORDER:  # close to floor
            desired = PVector(self.velocity.x, -MAX_SPEED)
        else:
            desired = PVector(0, 0)

        if desired.get_Magnitude() != 0:  # if desired has an assigned value from above:
            # Subtract the desired from the current velocity to create the steering force vector:
            steer = desired.subtract(self.velocity)  # steer = desired - current velocity
        else:
            steer = PVector(0, 0)

        # finally apply the steering force:
        self.apply_force(steer)


    # control the move of the object
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

    def fire_bullet(self):
        # create a bullet object and add to the visible bullets array
        bullet = Bullet(self.rect.centerx, self.rect.top, YELLOW, speed=5)
        self.bullets.append(bullet)


    def move_bullets(self, direction):
        for bullet in self.bullets:
            bullet.move(direction)
            if direction == 'UP':
            # if bullet out of top border, remove from visible array amd delete instance
                if bullet.rect.bottom < 0:
                    self.bullets.remove(bullet)
            elif direction == 'DOWN':
                if bullet.rect.bottom > self.screen_height:
                    self.bullets.remove(bullet)
            del bullet


    # redraws the image on the screen in the current position x,y of self.rect
    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.image, self.rect)
            for bullet in self.bullets:
                bullet.draw(screen)

