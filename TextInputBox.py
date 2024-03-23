import pygame
import constants
import User

class TextInputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ''
        self.font = pygame.font.Font(None, 32)
        self.active = False


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicks on the text input box, activate it
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN and self.active:
            # If the text input box is active and a key is pressed, append the key to the text
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # maximum 15 characters for name
                if len(self.text) < 15:
                    self.text += event.unicode

    def draw(self, screen):
        # Render the text input box and text - highlight when clicked inside
        if self.active == True:
            pygame.draw.rect(screen, (212, 212, 255), self.rect, 2)
        else:
            pygame.draw.rect(screen, (123, 123, 123), self.rect, 2)
        text_surface = self.font.render(self.text, True, constants.WHITE)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

