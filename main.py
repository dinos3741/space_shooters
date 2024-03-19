import pygame
import sys

# Define constants for state identifiers
MENU_STATE = 0
GAMEPLAY_STATE = 1
GAME_OVER_STATE = 2

class MenuState:
    def __init__(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return GAMEPLAY_STATE
        return MENU_STATE

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to start", True, (255, 255, 255))
        screen.blit(text, (200, 200))

class GameplayState:
    def __init__(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return MENU_STATE
        return GAMEPLAY_STATE

    def update(self):
        pass

    def render(self, screen):
        screen.fill((255, 0, 0))

class GameOverState:
    def __init__(self):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return GAMEPLAY_STATE
        return GAME_OVER_STATE

    def update(self):
        pass

    def render(self, screen):
        screen.fill((0, 0, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Press SPACE to restart", True, (255, 255, 255))
        screen.blit(text, (100, 200))

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    state = MENU_STATE
    menu_state = MenuState()
    gameplay_state = GameplayState()
    game_over_state = GameOverState()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if state == MENU_STATE:
            state = menu_state.handle_events(events)
            menu_state.render(screen)
        elif state == GAMEPLAY_STATE:
            state = gameplay_state.handle_events(events)
            gameplay_state.render(screen)
        elif state == GAME_OVER_STATE:
            state = game_over_state.handle_events(events)
            game_over_state.render(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
