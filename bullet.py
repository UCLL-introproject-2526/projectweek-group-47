# import pygame

# class Bullet:
#     def __init__(self, x, y):
#         self.rect = pygame.Rect(x, y, 15, 5)
#         self.speed = 7
#         self.color = (244,244,244)  # Yellow

#     def update(self):
#         # Move the bullet to the right
#         self.rect.x += self.speed

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, self.rect)


# import pygame
# import math

# class Bullet:
#     def __init__(self, x, y, dx=1, dy=0):
#         # Start position
#         self.rect = pygame.Rect(x, y, 10, 10)  # Square bullet for all directions
#         # Direction vector (normalized)
#         self.dx = dx
#         self.dy = dy
#         self.speed = 7
#         self.color = (255, 255, 0)  # Yellow

#     def update(self):
#         # Move the bullet in the direction it's facing
#         self.rect.x += self.dx * self.speed
#         self.rect.y += self.dy * self.speed

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, self.rect)
#         # Draw a small trail effect
#         trail_length = 5
#         trail_x = self.rect.x - self.dx * trail_length
#         trail_y = self.rect.y - self.dy * trail_length
#         pygame.draw.line(screen, (255, 200, 0), 
#                         (trail_x + 5, trail_y + 5), 
#                         (self.rect.x + 5, self.rect.y + 5), 2)



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
        # Draw trail
        for i in range(len(self.trail_points) - 1):
            alpha = 128 * (i / len(self.trail_points))
            trail_color = (255, 200, 0, int(alpha))
            if i > 0:
                pygame.draw.line(screen, (255, 200, 0), 
                               self.trail_points[i], 
                               self.trail_points[i-1], 2)
        
        # Draw bullet
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.radius - 1)
        
    def get_rect(self):
        # Create a small rectangle for collision detection
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)