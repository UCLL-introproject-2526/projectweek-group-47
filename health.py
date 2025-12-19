import pygame

class Health:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3
        self.collected = False
        self.animation_timer = 0
        
        try:
            self.image = pygame.image.load("asssets/image/health.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
        except:
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 0))
            # Draw a green cross as fallback
            pygame.draw.line(self.image, (255, 255, 255), (15, 5), (15, 25), 4)
            pygame.draw.line(self.image, (255, 255, 255), (5, 15), (25, 15), 4)
        
        self.rect = self.image.get_rect(center=(x, y))
        self.heal_amount = 20
    
    def update(self):
        if not self.collected:
            self.x -= self.speed
            self.rect.center = (self.x, self.y)
            self.animation_timer += 1
    
    def draw(self, screen):
        if not self.collected:
            # Floating animation
            float_offset = pygame.math.Vector2(0, pygame.math.lerp(-3, 3, (pygame.time.get_ticks() % 1000) / 1000))
            screen.blit(self.image, self.rect.move(float_offset))
            
            # Draw glow effect
            glow_radius = 20
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            alpha = 100 + int(50 * abs(pygame.math.lerp(-1, 1, (pygame.time.get_ticks() % 1000) / 1000)))
            pygame.draw.circle(glow_surface, (0, 255, 0, alpha), 
                             (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, 
                       (self.rect.centerx - glow_radius + float_offset.x, 
                        self.rect.centery - glow_radius + float_offset.y))
    
    def get_rect(self):
        return self.rect
    
    def collect(self):
        self.collected = True
        return self.heal_amount