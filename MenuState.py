import pygame
import constants
from TextInputBox import TextInputBox
from User import User


class MenuState:
    def __init__(self, user, game_state, stars, userSpaceship, enemies):
        self.user = user
        self.game_state = game_state
        self.stars = stars
        self.userSpaceship = userSpaceship
        self.enemies = enemies

        # load image from file
        self.original_background_image = pygame.image.load("Assets/splash_screen_image.jpg")
        # Scale the background image to half the screen size
        self.background_image = pygame.transform.scale(self.original_background_image, (constants.WIDTH, constants.HEIGHT))
        # Set the transparency (alpha) value for the image
        self.background_image.set_alpha(128)  # 128 is the alpha value (0-255)

        # create text input box and Calculate the position of the text box to draw it in the middle of the screen
        text_box_width = 200
        text_box_height = 40
        text_box_x = (constants.WIDTH - text_box_width) // 2
        text_box_y = (constants.HEIGHT - text_box_height) // 2
        self.text_input_box = TextInputBox(text_box_x, text_box_y, text_box_width, text_box_height)


    def handle_events(self, events):
        for event in events:
            self.text_input_box.handle_event(event)


    # update is for moving game objects, handling user input and collisions, updating game state and animations, check win/loss conditions
    def update(self):
        for star in self.stars:
            star.move()
        # store text in username class
        self.user.name = self.text_input_box.text


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
        title_rect = title_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 180))
        screen.blit(title_text, title_rect)

        # draw text "press space to start"
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to start, ESC to return", True, constants.WHITE)
        text_rect = text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 + 180))
        screen.blit(text, text_rect)

        name_text = font.render("Insert your name:", True, constants.PINK)
        name_rect = name_text.get_rect(center=(constants.WIDTH // 2, constants.HEIGHT // 2 - 40))
        screen.blit(name_text, name_rect)

        # draw the stars
        for star in self.stars:
            star.draw(screen, constants.WHITE)

        self.text_input_box.draw(screen)


