# parent class, UserSpaceShip and EnemySpaceShip inherit from this

import pygame
from PVector import PVector
from Bullet import Bullet

MAX_SPEED = 4

class Spaceship:
    # initialize with screen dimensions
    def __init__(self, screen_width, screen_height, size, mass, max_speed, bullet_color, friction, image_str):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.mass = mass
        self.max_speed = max_speed
        self.bullet_color = bullet_color
        self.friction = friction
        self.is_alive = True  # Flag to track if the spaceship is alive

        # initialize location, velocity and acceleration
        self.location = PVector(0, 0)
        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)

        # load spaceship png image (needs to be in the same folder as the code files)
        self.image = pygame.image.load(image_str)  # Replace "spaceship.png" with your image file
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()

        # visible bullets array
        self.bullets = []


    # updates the current position based on forces applied
    def update_position(self):
        # add acceleration to velocity:
        self.velocity.add(self.acceleration)
        # limit maximum velocity
        self.velocity.limit(self.max_speed)
        # apply friction
        self.velocity.multiplyByConstant(self.friction)
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
            desired.multiplyByConstant(self.max_speed * distance / CLOSE_ENOUGH)
        else:
            # create velocity equal to the max speed of the object
            desired.multiplyByConstant(self.max_speed)

        # Subtract the desired from the current velocity to create the steering force vector:
        steering_force = desired.subtract(self.velocity)  # steering force = desired vector - current velocity

        # now apply the steering force to the object
        self.apply_force(steering_force)


    # boundaries method is used to avoid ecosystem boundaries and turn
    def boundaries(self):
        DISTANCE_FROM_BORDER = 60  # the distance from the borders where it starts to change direction
        # desired velocity is a vector from current location until target: target - location, but in this case
        # it's a vector opposite to the x-coordinate
        if self.location.x < DISTANCE_FROM_BORDER:  # close to left wall
            desired = PVector(self.max_speed, self.velocity.y)
        elif self.location.x > self.screen_width - DISTANCE_FROM_BORDER:  # close to right wall
            desired = PVector(-self.max_speed, self.velocity.y)
        elif self.location.y < DISTANCE_FROM_BORDER:  # close to ceiling
            desired = PVector(self.velocity.x, self.max_speed)
        elif self.location.y > self.screen_height - DISTANCE_FROM_BORDER:  # close to floor
            desired = PVector(self.velocity.x, -self.max_speed)
        else:
            desired = PVector(0, 0)

        if desired.get_Magnitude() != 0:  # if desired has an assigned value from above:
            # Subtract the desired from the current velocity to create the steering force vector:
            steer = desired.subtract(self.velocity)  # steer = desired - current velocity
        else:
            steer = PVector(0, 0)

        # finally apply the steering force:
        self.apply_force(steer)


    def fire_bullet(self):
        # create a bullet object and add to the visible bullets array
        bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_color, speed=5)
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
            # draw spaceship
            screen.blit(self.image, self.rect)
            # draw bullets
            for bullet in self.bullets:
                bullet.draw(screen)

