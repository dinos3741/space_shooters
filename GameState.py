import pygame
import constants

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class GameState:
    def __init__(self):
        self.state = constants.MENU_STATE  # Initial state

    def change_state(self, new_state):
        if new_state not in [constants.MENU_STATE, constants.GAMEPLAY_STATE, constants.GAME_OVER_STATE]:
            raise ValueError("Invalid state")

        self.state = new_state

    def update(self):
        # Change state if the player presses a key. Handle logic for changing states: from menu with space go to gameplay,
        # from gameplay with esc go to menu. From gameover we can't go anywhere for now. Later with R we reload game.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.state == constants.MENU_STATE:
                self.change_state(constants.GAMEPLAY_STATE)
        if keys[pygame.K_ESCAPE]:
            if self.state == constants.GAMEPLAY_STATE:
                self.change_state(constants.MENU_STATE)

