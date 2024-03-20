import pygame
import constants

class MenuState:
    def __init__(self, stars, game_state):
        self.stars = stars
        self.game_state = game_state

        # load image from file
        self.original_background_image = pygame.image.load("Assets/splash_screen_image.jpg")
        # Scale the background image to half the screen size
        self.background_image = pygame.transform.scale(self.original_background_image, (constants.WIDTH, constants.HEIGHT))
        # Set the transparency (alpha) value for the image
        self.background_image.set_alpha(128)  # 128 is the alpha value (0-255)


    def handle_events(self, events):
        pass


    # update is for moving game objects, handling user input and collisions, updating game state and animations, check win/loss conditions
    def update(self):
        for star in self.stars:
            star.move()


    # render is for drawing graphic elements on the screen, render text and fonts
    def render(self, screen):
        screen.fill(constants.BLACK)

        # draw image
        # Get the rectangle containing the background image
        image_rect = self.background_image.get_rect()
        # Center the image rectangle on the screen rectangle
        image_rect.center = (screen.get_width() // 2, screen.get_height() // 2)
        # Blit the background image onto the screen at the centered position
        screen.blit(self.background_image, image_rect)

        # draw text "Space Shooters!"
        font = pygame.font.Font(None, 80)
        title_text = font.render("Space Shooters!", True, constants.GREEN)
        title_rect = title_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 150))
        screen.blit(title_text, title_rect)

        # draw text "press space to start"
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to start, ESC to return here", True, constants.WHITE)
        text_rect = text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 150))
        screen.blit(text, text_rect)

        # draw the stars
        for star in self.stars:
            star.draw(screen, constants.WHITE)

