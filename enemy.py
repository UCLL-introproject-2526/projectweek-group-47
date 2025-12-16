import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        try:
            self.frames = [
                pygame.image.load("asssets/image/zombie_3.png"),
                pygame.image.load("asssets/image/zombie_4.png")
            ]
            self.frames = [pygame.transform.scale(f, (80, 100)) for f in self.frames]
        except:
            self.frames = [pygame.Surface((80, 100))] # Fallback

        self.frame_index = 0
        self.health = 3
        self.max_health = 3
        self.speed = 3
        self.is_attacking = False

    def update(self, hero_rect):
        enemy_rect = self.get_rect()
        
        # Check if touching hero
        if enemy_rect.colliderect(hero_rect):
            self.is_attacking = True
        else:
            self.is_attacking = False
            self.x -= self.speed

        # Animation
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
            
        if self.x < -80:
            self.reset()

    def reset(self):
        self.x = 800
        self.health = 3

    def draw(self, screen):
        current_frame = self.frames[int(self.frame_index)]
        screen.blit(current_frame, (self.x, self.y))
        
        # Draw Enemy Health Bar over head
        bar_width = 50
        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x + 15, self.y - 10, bar_width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (self.x + 15, self.y - 10, bar_width * health_ratio, 5))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 80, 100)