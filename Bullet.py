import pygame

BULLET_SPEED = 7

class Bullet:
    def __init__(self, x, y, color, speed):
        self.rect = pygame.Rect(x - 2, y - 10, 4, 10)
        self.color = color
        self.speed = speed
        self.is_alive = True  # Flag to track if the bullet is active

    def move(self, direction):
        if direction == 'UP':
            self.rect.y -= self.speed
        elif direction == 'DOWN':
            self.rect.y += self.speed

    def draw(self, screen):
        if self.is_alive:
            pygame.draw.rect(screen, self.color, self.rect)
