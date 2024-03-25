import pygame
import constants


class GameOverState:
    def __init__(self, user, game_state, stars, userSpaceship, enemies):
        self.user = user
        self.game_state = game_state
        self.stars = stars
        self.userSpaceship = userSpaceship
        self.enemies = enemies

    def handle_events(self, events):
        pass

    def update(self):
        for star in self.stars:
            star.move()

    def render(self, screen):
        screen.fill(constants.BLACK)
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("Game Over", True, constants.WHITE)
        text_rect = game_over_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

        # display score down left
        # set font
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Total enemies shot: " + str(self.user.score), True, constants.PINK)
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, constants.HEIGHT - 10)  # Position the text in the bottom-left corner
        screen.blit(text_surface, text_rect)

        # draw the stars
        for star in self.stars:
            star.draw(screen, constants.WHITE)
