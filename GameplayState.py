import pygame
import constants

class GameplayState:
    def __init__(self, stars, userspaceship, enemies, game_state):
        self.stars = stars
        self.userSpaceship = userspaceship
        self.enemies = enemies
        self.game_state = game_state

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

        # set font
        self.font = pygame.font.Font(None, 36)

        self.score = 0
        self.lives = constants.LIVES


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

        # display score
        text_surface = self.font.render("Enemies shot: " + str(self.score), True, constants.PINK)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, constants.HEIGHT - 10)  # Position the text in the bottom-left corner
        screen.blit(text_surface, text_rect)

        # display remaining lives
        text_surface = self.font.render("Lives: " + str(self.lives), True, constants.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (constants.WIDTH - 10, constants.HEIGHT - 10)  # Position the text at the bottom-right corner
        screen.blit(text_surface, text_rect)


    def handle_collisions(self):
        # for each enemy:
        for enemy in self.enemies:
            # check if any of the user bullets hit any enemy
            for bullet in self.userSpaceship.bullets:
                if bullet.rect.colliderect(enemy.rect):
                    # remove the bullet from the list
                    self.userSpaceship.bullets.remove(bullet)
                    # remove enemy from the list
                    self.enemies.remove(enemy)
                    # play sound
                    self.enemy_explode_sound.play()
                    # increase score
                    self.score += 1

            # check if any of the enemy bullets hit the user
            for bullet in enemy.bullets:
                # if bullet hits user spaceship
                if bullet.rect.colliderect(self.userSpaceship.rect):
                    # remove the bullet from the list
                    enemy.bullets.remove(bullet)
                    # remove one life from user
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_state.change_state(constants.GAME_OVER_STATE)
                    # play hit sound
                    self.user_hit_sound.play()

            # check collision of user spaceship with any of the enemies
            if self.userSpaceship.rect.colliderect(enemy):
                enemy.is_alive = False
                self.user_explode_sound.play()




