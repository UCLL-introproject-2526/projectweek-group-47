import pygame
import random
import math

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.collected = False
        self.animation_timer = 0
        self.float_offset = random.uniform(0, 2 * math.pi)  # Random starting point for floating
        
        # Coin colors
        self.colors = [
            (255, 215, 0),   # Gold
            (255, 223, 0),   # Yellow-gold
            (255, 235, 0),   # Bright yellow
            (218, 165, 32)   # Golden rod
        ]
        
        # Sparkle particles
        self.sparkles = []
    
    def update(self):
        """Update coin animation."""
        if not self.collected:
            self.animation_timer += 1
            
            # Create sparkle particles occasionally
            if random.random() < 0.1:  # 10% chance each frame
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(5, 15)
                sparkle_x = self.x + math.cos(angle) * distance
                sparkle_y = self.y + math.sin(angle) * distance
                
                self.sparkles.append({
                    'x': sparkle_x,
                    'y': sparkle_y,
                    'life': 20,
                    'size': random.randint(2, 4),
                    'speed_x': random.uniform(-0.5, 0.5),
                    'speed_y': random.uniform(-0.5, 0.5)
                })
            
            # Update sparkles
            for sparkle in self.sparkles[:]:
                sparkle['x'] += sparkle['speed_x']
                sparkle['y'] += sparkle['speed_y']
                sparkle['life'] -= 1
                if sparkle['life'] <= 0:
                    self.sparkles.remove(sparkle)
    
    def draw(self, screen):
        """Draw the coin with floating animation."""
        if self.collected:
            return
            
        # Draw sparkles first
        for sparkle in self.sparkles:
            alpha = int(255 * (sparkle['life'] / 20))
            sparkle_surface = pygame.Surface((sparkle['size'] * 2, sparkle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(sparkle_surface, (255, 255, 255, alpha),
                             (sparkle['size'], sparkle['size']), sparkle['size'])
            screen.blit(sparkle_surface, (sparkle['x'] - sparkle['size'], sparkle['y'] - sparkle['size']))
        
        # Floating animation
        float_height = math.sin(self.animation_timer * 0.1 + self.float_offset) * 3
        
        # Draw coin glow
        glow_radius = self.radius + 3
        for i in range(2):
            glow_size = glow_radius + i
            alpha = 150 - i * 50
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 215, 0, alpha),
                             (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, 
                       (self.x - glow_size, self.y + float_height - glow_size))
        
        # Draw coin (gold circle)
        current_color = self.colors[int((math.sin(self.animation_timer * 0.2) + 1) * 1.5) % len(self.colors)]
        pygame.draw.circle(screen, current_color, 
                         (int(self.x), int(self.y + float_height)), self.radius)
        
        # Draw coin shine (highlight)
        shine_radius = self.radius * 0.6
        shine_offset = -self.radius * 0.3
        pygame.draw.circle(screen, (255, 255, 200), 
                         (int(self.x + shine_offset), int(self.y + float_height + shine_offset)), shine_radius)
        
        # Draw coin edge (dark outline)
        pygame.draw.circle(screen, (184, 134, 11), 
                         (int(self.x), int(self.y + float_height)), self.radius, 1)
        
        # Draw "$" symbol on coin
        coin_font = pygame.font.SysFont('Arial', 12, bold=True)
        coin_text = coin_font.render("$", True, (139, 69, 19))  # Brown color
        text_rect = coin_text.get_rect(center=(self.x, self.y + float_height))
        screen.blit(coin_text, text_rect)
    
    def get_rect(self):
        """Get collision rectangle for the coin."""
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def is_off_screen(self, screen_width):
        """Check if coin is off screen (left side)."""
        return self.x < -20
    
    def collect(self):
        """Mark coin as collected."""
        self.collected = True
        return True
    
    def reset(self, x=None, y=None):
        """Reset coin position."""
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.collected = False
        self.animation_timer = 0
        self.float_offset = random.uniform(0, 2 * math.pi)
        self.sparkles = []