import pygame
import constants
from EnemySpaceship import EnemySpaceship


class GameOverState:
    def __init__(self, stars, game_state):
        self.stars = stars
        self.game_state = game_state


    def handle_events(self, events):
        for event in events:
            # user spaceship shoot event
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # reload the enemy list
                # Create an initial set of instances of the EnemySpaceship class
                enemies = [EnemySpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT,
                                          size=constants.ENEMY_SPACESHIP_SIZE,
                                          mass=constants.ENEMY_SPACESHIP_MASS, bullet_color=constants.YELLOW,
                                          friction=1,
                                          image_str='Assets/enemy.png') for _ in range(constants.NUM_ENEMIES)]

    def update(self):
        for star in self.stars:
            star.move()


    def render(self, screen):
        screen.fill(constants.BLACK)
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("Game Over", True, constants.WHITE)
        text_rect = game_over_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

        # draw the stars
        for star in self.stars:
            star.draw(screen, constants.WHITE)
