import pygame
import math

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle  # Angle in radians
        self.speed = 10
        self.radius = 4  # Smaller bullet for better accuracy
        self.color = (255, 255, 0)  # Yellow
        self.trail_points = []  # For trail effect
        
    def update(self):
        # Move in the direction of the angle
        self.x += math.cos(self.angle) * self.speed
        self.y += -math.sin(self.angle) * self.speed  # Negative because pygame y increases downward
        
        # Add current position to trail (keep last 3 positions)
        self.trail_points.append((self.x, self.y))
        if len(self.trail_points) > 3:
            self.trail_points.pop(0)
            
    def draw(self, screen):
        for i in range(len(self.trail_points) - 1):
            alpha = 128 * (i / len(self.trail_points))
            trail_color = (255, 200, 0, int(alpha))
            if i > 0:
                pygame.draw.line(screen, (255, 200, 0), 
                               self.trail_points[i], 
                               self.trail_points[i-1], 2)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.radius - 1)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)