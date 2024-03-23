import pygame
import sys
import constants
from SpaceshipFactory import SpaceshipFactory
from GameState import GameState
from MenuState import MenuState
from GameplayState import GameplayState
from GameOverState import GameOverState
from Stars import Star
from User import User

def main():
    # Initialize Pygame, screen and clock. Screen will be passed as dependency in all render methods
    pygame.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Space Shooters")

    # initialize clock
    clock = pygame.time.Clock()

    # Initialize Pygame mixer
    pygame.mixer.init()

    # create the user and pass as dependency to all state classes
    user = User(name='')

    # create objects to inject in state classes as needed
    stars = [Star(constants.WIDTH, constants.HEIGHT) for _ in range(constants.NUM_STARS)]

    # Create an instance of the Spaceship class using factory
    userSpaceship = SpaceshipFactory.create_spaceship(type='user', number=1, max_speed=4)

    # Create an initial set of instances of the EnemySpaceship class using factory
    enemies = SpaceshipFactory.create_spaceship(type='enemy', number=constants.NUM_ENEMIES, max_speed=5)

    # instantiate the state objects
    game_state = GameState()
    menu_state = MenuState(user, game_state, stars, userSpaceship, enemies)  # pass the objects as dependency wherever needed
    gameplay_state = GameplayState(user, game_state, stars, userSpaceship, enemies)
    game_over_state = GameOverState(user, game_state, stars, userSpaceship, enemies)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update game state
        game_state.update()

        # handle events and return current state
        if game_state.state == constants.MENU_STATE:
            menu_state.handle_events(events)
            menu_state.render(screen)
            menu_state.update()

        elif game_state.state == constants.GAMEPLAY_STATE:
            gameplay_state.handle_events(events)
            gameplay_state.render(screen)
            gameplay_state.update()

        elif game_state.state == constants.GAME_OVER_STATE:
            game_over_state.handle_events(events)
            game_over_state.render(screen)
            game_over_state.update()

        pygame.display.flip()
        clock.tick(constants.FPS)

if __name__ == "__main__":
    main()
