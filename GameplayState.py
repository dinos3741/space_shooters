import pygame
import constants
from SpaceshipFactory import SpaceshipFactory

class GameplayState:
    def __init__(self, user, game_state, stars, userspaceship, enemies):
        self.user = user
        self.game_state = game_state
        self.stars = stars
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

        # flag to run background music method only once
        self.music_has_run = False


    def handle_events(self, events):
        for event in events:
            # user spaceship shoot event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                self.userSpaceship.fire_bullet()
                self.laser_sound.play()

    def update(self):
        # Get the current state of keys to pass to the move method of user spaceship
        keys = pygame.key.get_pressed()
        self.userSpaceship.move(keys)
        # move the enemies
        for enemy in self.enemies:
            enemy.move()
            # move the stars
        for star in self.stars:
            star.move()
        # handle collisions
        self.handle_collisions()
        # check if game is over
        self.handle_game_over()
        # check if whole army is killed
        if self.army_killed():
            # Create a new set of instances of the EnemySpaceship class using factory - perhaps faster in later levels
            self.enemies = SpaceshipFactory.create_spaceship(type='enemy', number=constants.NUM_ENEMIES, max_speed=5)

        # start background music
        if not self.music_has_run:
            self.background_music(True)
            self.music_has_run = True


    def render(self, screen):
        screen.fill(constants.BLACK)
        # draw user spaceship
        self.userSpaceship.draw(screen)
        # draw the enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        # draw the stars
        for star in self.stars:
            star.draw(screen, constants.WHITE)

        # display score down left
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Enemies shot: " + str(self.user.score), True, constants.PINK)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, constants.HEIGHT - 10)  # Position the text in the bottom-left corner
        screen.blit(text_surface, text_rect)

        # display remaining lives down right
        text_surface = font.render("Lives: " + str(self.user.lives), True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (constants.WIDTH - 10, constants.HEIGHT - 10)  # Position the text at the bottom-right corner
        screen.blit(text_surface, text_rect)

        # display username up left - need to pass the user class as dependency
        name_surface = font.render("Player: " + str(self.user.name), True, constants.WHITE)
        name_rect = name_surface.get_rect()
        name_rect.topleft = (10, 10)  # Position the text at the top left corner
        screen.blit(name_surface, name_rect)


    def handle_collisions(self):
        # for each enemy:
        for enemy in self.enemies:
            # check if any of the user bullets hit any enemy
            for bullet in self.userSpaceship.bullets:
                if bullet.rect.colliderect(enemy.rect):
                    # remove the bullet from the list
                    self.userSpaceship.bullets.remove(bullet)
                    # remove enemy from the list
                    enemy.is_alive = False
                    self.enemies.remove(enemy)
                    # play sound
                    self.enemy_explode_sound.play()
                    # increase score
                    self.user.score += 1

            # check if any of the enemy bullets hit the user
            for bullet in enemy.bullets:
                # if bullet hits user spaceship
                if bullet.rect.colliderect(self.userSpaceship.rect):
                    # remove the bullet from the list
                    enemy.bullets.remove(bullet)
                    # remove one life from user
                    self.user.lives -= 1
                    # play hit sound
                    self.user_hit_sound.play()

            # check collision of user spaceship with any of the enemies
            if self.userSpaceship.rect.colliderect(enemy):
                enemy.is_alive = False
                self.enemies.remove(enemy)
                # remove one life from user
                self.user.lives -= 1
                self.user_explode_sound.play()


    def handle_game_over(self):
        if self.user.lives <= 0:
            self.userSpaceship.is_alive = False
            self.game_state.change_state(constants.GAME_OVER_STATE)
            # clear the enemy list
            for enemy in self.enemies:
                enemy.is_alive = False
                self.enemies.remove(enemy)
            # close music
            self.background_music(False)


    def background_music(self, switch):
        pygame.mixer.music.load("Assets/ethereal-ambient-music.mp3")
        pygame.mixer.music.set_volume(0.2)
        if switch == True:
            pygame.mixer.music.play(-1)  # -1 indicates loop indefinitely
        elif switch == False:
            pygame.mixer_music.stop()


    def army_killed(self):
        if len(self.enemies) == 0:
            return True
        else:
            return False
