import pygame

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 5)
        self.speed = 7
        self.color = (244,244,244)  # Yellow

    def update(self):
        # Move the bullet to the right
        self.rect.x += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)