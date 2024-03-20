import pygame
import sys
import constants
from GameState import GameState
from MenuState import MenuState
from GameplayState import GameplayState
from GameOverState import GameOverState
from Stars import Star
from UserSpaceship import UserSpaceship
from EnemySpaceship import EnemySpaceship

def main():
    # Initialize Pygame, screen and clock. Screen will be passed as dependency in all render methods
    pygame.init()
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
    pygame.display.set_caption("Space Shooters")
    clock = pygame.time.Clock()

    # Initialize Pygame mixer
    pygame.mixer.init()

    # create objects to inject in state classes as needed
    stars = [Star(constants.WIDTH, constants.HEIGHT) for _ in range(constants.NUM_STARS)]

    # Create an instance of the Spaceship class
    userSpaceship = UserSpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT,
                                       size=constants.USER_SPACESHIP_SIZE,
                                       mass=constants.USER_SPACESHIP_MASS, bullet_color=constants.GREEN,
                                       friction=constants.FRICTION, image_str='Assets/spaceship.png')

    # Create an initial set of instances of the EnemySpaceship class
    enemies = [EnemySpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT,
                                   size=constants.ENEMY_SPACESHIP_SIZE,
                                   mass=constants.ENEMY_SPACESHIP_MASS, bullet_color=constants.YELLOW, friction=1,
                                   image_str='Assets/enemy.png') for _ in range(constants.NUM_ENEMIES)]

    # instantiate the state objects
    game_state = GameState()
    menu_state = MenuState(stars, game_state)  # pass the objects as dependency wherever needed
    gameplay_state = GameplayState(stars, userSpaceship, enemies, game_state)
    game_over_state = GameOverState(stars, game_state)

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Update game state
        game_state.update()

        if game_state.state == constants.MENU_STATE:
            # handle events and return current state
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
