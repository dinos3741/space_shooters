import pygame
import sys

from EnemySpaceship import EnemySpaceship
from Explosion import Explosion
from UserSpaceship import UserSpaceship
from stars import Star

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()
# Load a sound file
laser_sound = pygame.mixer.Sound('laser.mp3')
laser_volume = 0.1
laser_sound.set_volume(laser_volume)

explosion_sound = pygame.mixer.Sound('user-explode.mp3')
explosion_volume = 0.3
explosion_sound.set_volume(explosion_volume)

# Constants
WIDTH = 800
HEIGHT = 600
NUM_STARS = 100
NUM_ENEMIES = 5
FPS = 60
USER_SPACESHIP_SIZE = 100
USER_SPACESHIP_MASS = 5
ENEMY_SPACESHIP_SIZE = 50
ENEMY_SPACESHIP_MASS = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (150, 235, 8)


# Load explosion frames
explosion_frames = [pygame.image.load(f"explosion{i}.png") for i in range(1, 5)]

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Destroyers")

# Initialize the clock
clock = pygame.time.Clock()

# Create a list of stars
stars = [Star(WIDTH, HEIGHT) for _ in range(NUM_STARS)]

# Create an instance of the Spaceship class
userSpaceship = UserSpaceship(WIDTH, HEIGHT, USER_SPACESHIP_SIZE, USER_SPACESHIP_MASS, GREEN, 0.98, 'spaceship.png')

# Create an initial set of instances of the EnemySpaceship class
enemies = [EnemySpaceship(WIDTH, HEIGHT, ENEMY_SPACESHIP_SIZE, ENEMY_SPACESHIP_MASS, GREEN, 1, 'enemy.png') for _ in range(NUM_ENEMIES)]


# check if a bullet collides with a spaceship
# colliderect is a method of the Rect class that checks for collision between two rectangles.
# The method is used to determine if the boundaries of two rectangles overlap or intersect.
def check_collision(bullet, spaceship):
    return bullet.rect.colliderect(spaceship.rect)

#----------------------------------------------------
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            userSpaceship.fire_bullet(GREEN)
            laser_sound.play()
        # fill up the list of enemies if right shift is pressed
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            if len(enemies) < NUM_ENEMIES:
                remaining = NUM_ENEMIES - len(enemies)
                enemies = enemies + [EnemySpaceship(WIDTH, HEIGHT, ENEMY_SPACESHIP_SIZE, ENEMY_SPACESHIP_MASS, 'enemy.png') for _ in range(remaining)]

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw and move the stars
    for star in stars:
        star.draw(screen, WHITE)
        star.move()

    # Get the current state of keys
    keys = pygame.key.get_pressed()

    # Draw and move the player and enemy spaceships
    userSpaceship.draw(screen)
    userSpaceship.move(keys)
    for enemy in enemies:
        enemy.draw(screen)
        enemy.move()


    # Check for collisions between bullets and enemy spaceship
    for enemy in enemies:
        for bullet in userSpaceship.bullets:
            if enemy.is_alive and check_collision(bullet, enemy):
                # create explosion
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery, explosion_frames)
                # draw the explosion effect
                explosion.update()
                explosion.draw(screen)
                # erase both bullet and spaceship
                enemy.is_alive = False
                bullet.is_alive = False

        for bullet in enemy.bullets:
            if userSpaceship.is_alive and check_collision(bullet, userSpaceship):
                explosion_sound.play()
                bullet.is_alive = False
                # del userSpaceship

        # check collision of user spaceship with any of the enemies
        if userSpaceship.rect.colliderect(enemy):
            enemy.is_alive = False
            explosion_sound.play()

            # update user spaceship - subtract one life
            # collision with enemy bullet: subtract one life

    # update enemies
    for enemy in enemies:
        if enemy.is_alive == False:
            enemies.remove(enemy)
            del enemy

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

#----------------------------------------------------
