import pygame
import random

STAR_RADIUS = 1

# Define a Star class
class Star:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height)
        self.width = width
        self.height = height
        self.speed = random.uniform(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > self.height:
            self.y = 0
            self.x = random.randint(0, self.width)

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), STAR_RADIUS)

