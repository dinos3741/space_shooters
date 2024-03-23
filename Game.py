import pygame
import sys
import constants

from EnemySpaceship import EnemySpaceship
from UserSpaceship import UserSpaceship
from Stars import Star

# Initialize Pygame
pygame.init()

# Initialize the clock
clock = pygame.time.Clock()

# Create a list of stars
stars = [Star(constants.WIDTH, constants.HEIGHT) for _ in range(constants.NUM_STARS)]

# Create an instance of the Spaceship class
userSpaceship = UserSpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT, size=constants.USER_SPACESHIP_SIZE,
                        mass=constants.USER_SPACESHIP_MASS, bullet_color=constants.GREEN, friction=constants.FRICTION, image_str='Assets/spaceship.png')

# Create an initial set of instances of the EnemySpaceship class
Enemies = [EnemySpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT, size=constants.ENEMY_SPACESHIP_SIZE, mass=constants.ENEMY_SPACESHIP_MASS,
                          bullet_color=constants.YELLOW, friction=1, image_str='Assets/enemy.png') for _ in range(constants.NUM_ENEMIES)]

# Initialize Pygame mixer
pygame.mixer.init()


# --------------------------------------------------------------
class Game:
    # inject dependencies on the spaceship objects
    def __init__(self, userspaceship, enemies):
        # Initialize the screen and caption
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        pygame.display.set_caption("Space Destroyers")

        # get dependency objects
        self.userSpaceship = userspaceship
        self.enemies = enemies

        # load user laser bullet sound
        self.laser_sound = pygame.mixer.Sound('Assets/laser.mp3')
        self.laser_sound.set_volume(0.1)

        # load user hit sound
        self.user_hit_sound = pygame.mixer.Sound('Assets/user-hit.mp3')
        self.user_hit_sound.set_volume(0.3)

        # load user explosion sound
        self.user_explode_sound = pygame.mixer.Sound('Assets/user-explode.mp3')
        self.user_explode_sound.set_volume(0.2)

        # load enemy explosion sound
        self.enemy_explode_sound = pygame.mixer.Sound('Assets/enemy-explode.mp3')
        self.enemy_explode_sound.set_volume(0.6)

        # get the starting time of the game
        self.start_time = pygame.time.get_ticks()

        self.font = pygame.font.Font(None, 36)  # Use a font and size of your choice

        self.score = 0
        self.lives = constants.LIVES

        # flag to indicate loop is running
        self.running = True

        # flag to indicate game over - user lost
        self.game_over = False


    # event handling method
    def handle_events(self):
        for event in pygame.event.get():
            # quit the app
            if event.type == pygame.QUIT:
                self.running = False

            # shoot with left shift when game is not over
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT and not self.game_over:
                self.userSpaceship.fire_bullet()
                self.laser_sound.play()

            # fill up the list of enemies if right shift is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT and not self.game_over:
                if len(self.enemies) < constants.NUM_ENEMIES:
                    remaining = constants.NUM_ENEMIES - len(self.enemies)
                    self.enemies = self.enemies + [EnemySpaceship(constants.WIDTH, constants.HEIGHT, constants.ENEMY_SPACESHIP_SIZE,
                                                constants.ENEMY_SPACESHIP_MASS, constants.YELLOW, 1, 'enemy.png') for _ in range(remaining)]


    # Draw and move the stars
    def drawStars(self):
        for star in stars:
            star.draw(self.screen, constants.WHITE)
            star.move()


    # draw and move user spaceship
    def drawUserSpaceship(self):
        # Get the current state of keys to pass to the move method
        keys = pygame.key.get_pressed()
        # Draw and move the player and enemy spaceships
        self.userSpaceship.draw(self.screen)
        self.userSpaceship.move(keys)


    # draw and move enemies
    def drawEnemies(self):
        for enemy in self.enemies:
            enemy.draw(self.screen)
            enemy.move()


    def handle_collisions(self):
        # for each enemy:
        for enemy in self.enemies:
            # check if any of the user bullets hit any enemy
            for bullet in self.userSpaceship.bullets:
                if bullet.rect.colliderect(enemy.rect):
                    # remove the bullet from the list
                    userSpaceship.bullets.remove(bullet)
                    # remove enemy from the list
                    self.enemies.remove(enemy)
                    # play sound
                    self.enemy_explode_sound.play()
                    self.update_score(1)

            # check if any of the enemy bullets hit the user
            for bullet in enemy.bullets:
                # if bullet hits user spaceship
                if bullet.rect.colliderect(userSpaceship.rect):
                    # remove the bullet from the list
                    enemy.bullets.remove(bullet)
                    # remove health from user
                    self.update_lives(-1)
                    # play hit sound
                    self.user_hit_sound.play()

            # check collision of user spaceship with any of the enemies
            if self.userSpaceship.rect.colliderect(enemy):
                enemy.is_alive = False
                self.user_explode_sound.play()


    # update list of enemies to delete dead ones
    def updateEnemies(self):
        for enemy in self.enemies:
            if enemy.is_alive == False:
                self.enemies.remove(enemy)
                del enemy

    # update the game over flag
    def handle_game_over(self):
        if self.lives <= 0:
            self.game_over = True


    # create splash screen
    def create_splash_screen(self):
        splash_screen_image = pygame.image.load("Assets/splash_screen_image.jpg")
        splash_screen_image = pygame.transform.scale(splash_screen_image, (constants.WIDTH / 2, constants.HEIGHT / 2))

        font = pygame.font.Font(None, 80)
        game_over_text = font.render("Space Shooters!", True, (123, 255, 23))

        # its own event loop before entering the game event loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if it's time to exit the splash screen
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= constants.SPLASH_SCREEN_DURATION:
                return  # Exit the method and continue with the game

            # Display the splash screen image
            self.screen.fill(constants.BLACK)  # Fill the screen with black background
            self.screen.blit(splash_screen_image, (
                (constants.WIDTH - splash_screen_image.get_width()) // 2, (constants.HEIGHT - splash_screen_image.get_height()) // 2))

            text_rect = game_over_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 200))
            self.screen.blit(game_over_text, text_rect)

            # Update the display
            pygame.display.flip()
            clock.tick(constants.FPS)


    def display_game_over_screen(self):
        self.screen.fill(constants.BLACK)
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("Game Over", True, constants.WHITE)
        text_rect = game_over_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)
        # display the score, the lives and the star effect
        self.drawStars()
        self.display_score()
        self.display_lives()

        pygame.display.flip()


    # play background music from mp3 source
    def play_background_music(self):
        pygame.mixer.music.load("Assets/ethereal-ambient-music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # -1 indicates loop indefinitely

    def update_score(self, score):
        self.score += score

    def update_lives(self, lives):
        self.lives += lives


    # display the score in the bottom left corner
    def display_score(self):
        text_surface = self.font.render("Enemies shot: " + str(self.score), True, constants.PINK)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, constants.HEIGHT - 10)  # Position the text in the bottom-left corner
        self.screen.blit(text_surface, text_rect)


    # display lives at bottom right corner
    def display_lives(self):
        text_surface = self.font.render("Lives: " + str(self.lives), True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (constants.WIDTH - 10, constants.HEIGHT - 10)  # Position the text at the bottom-right corner
        self.screen.blit(text_surface, text_rect)

    #-----------------------------------------------------------------
    # run method for main game event loop
    def run(self):
        # run those methods outside the main loop
        self.start_time = pygame.time.get_ticks()
        self.create_splash_screen()
        self.play_background_music()

        while self.running:
            self.handle_events()
            self.screen.fill(constants.BLACK)

            if not self.game_over:
                self.drawStars()
                self.drawUserSpaceship()
                self.drawEnemies()
                self.handle_collisions()
                self.updateEnemies()
                self.display_score()
                self.display_lives()

            self.handle_game_over()
            if self.game_over:
                # stop the music
                pygame.mixer_music.stop()
                self.display_game_over_screen()

            # SOS: this always at the bottom
            pygame.display.flip()
            # Cap the frame rate
            clock.tick(constants.FPS)

        pygame.quit()
        sys.exit()

# Instantiate the game object passing the dependencies and run
game = Game(userSpaceship, Enemies)
game.run()
