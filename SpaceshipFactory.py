from EnemySpaceship import EnemySpaceship
from UserSpaceship import UserSpaceship
import constants

class SpaceshipFactory:
    @staticmethod
    def create_spaceship(type, number, max_speed):
        if type == 'enemy':
            enemies = [EnemySpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT,
                        size=constants.ENEMY_SPACESHIP_SIZE, mass=constants.ENEMY_SPACESHIP_MASS,
                        max_speed=max_speed, bullet_color=constants.YELLOW, friction=1,
                        image_str='Assets/enemy.png') for _ in range(number)]

            return enemies
        elif type == 'user':
            userSpaceship = UserSpaceship(screen_width=constants.WIDTH, screen_height=constants.HEIGHT,
                                          size=constants.USER_SPACESHIP_SIZE,
                                          mass=constants.USER_SPACESHIP_MASS, max_speed=max_speed, bullet_color=constants.GREEN,
                                          friction=constants.FRICTION, image_str='Assets/spaceship.png')
            return userSpaceship
