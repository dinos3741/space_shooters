import pygame
import constants

class GameState:
    def __init__(self):
        self.state = constants.MENU_STATE  # Initial state

    def change_state(self, new_state):
        self.state = new_state

    def update(self):
        # Change state if the player presses a key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.change_state(constants.GAMEPLAY_STATE)
        if keys[pygame.K_ESCAPE]:
            self.change_state(constants.MENU_STATE)
        if keys[pygame.K_r]:
            self.change_state(constants.GAMEPLAY_STATE)

