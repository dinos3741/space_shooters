import pygame
from PVector import PVector
from Bullet import Bullet

MAX_SPEED = 5
KEYS_FORCE = 3
FRICTION = 0.98

GREEN = (150, 235, 8)

class UserSpaceship():
    def __init__(self, screen_width, screen_height, size, mass, image_str):
        # hardcode the size and speed for now
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.mass = mass

        # load spaceship png image (needs to be in the same folder as the code files)
        self.image = pygame.image.load(image_str)  # Replace "spaceship.png" with your image file
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.image.get_rect()
        # display spaceship in the screen center
        self.rect.center = (self.screen_width / 2, self.screen_height / 2)

        self.location = PVector(self.screen_width / 2, self.screen_height / 2) # this will be set

        self.velocity = PVector(0, 0)
        self.acceleration = PVector(0, 0)

        # array to keep the bullets visible at any time
        self.bullets = []


    # apply force to the spaceship
    def apply_force(self, force):
        f = PVector(0, 0)
        force.copy(f)  # copy force to temporary f
        f = force.divideByConstant(self.mass)
        self.acceleration.add(f)  # update the acceleration vector


    #apply force to the spaceship based on the keys pressed
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


    # boundaries method is used to avoid ecosystem boundaries and turn
    def boundaries(self):
        DISTANCE_FROM_BORDER = 50  # the distance from the borders where it starts to change direction
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


    def update_position(self):
        # add acceleration to velocity:
        self.velocity.add(self.acceleration)
        # limit maximum velocity
        self.velocity.limit(MAX_SPEED)
        # apply friction
        self.velocity.multiplyByConstant(FRICTION)
        # add velocity to position:
        self.location.add(self.velocity)
        # update position of object on screen
        self.rect.center = (self.location.x, self.location.y)
        # reset the acceleration at the end of each frame:
        self.acceleration.multiplyByConstant(0)


    def fire_bullet(self):
        # create a bullet object and add to the visible bullets array
        bullet = Bullet(self.rect.centerx, self.rect.top, GREEN, speed=7)
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


    # draw spaceship and bullets
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            bullet.draw(screen)

