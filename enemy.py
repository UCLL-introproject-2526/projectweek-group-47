import pygame
import random

class Enemy:
    def __init__(self, x, y, enemy_type="zombie"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type  # "zombie" or "ghost"
        
        try:
            if self.enemy_type == "ghost":
                # Ghost uses different image
                self.frames = [
                    pygame.image.load("asssets/image/ghost_the_second_enemy.png")
                ]
                self.frames = [pygame.transform.scale(f, (60, 70)) for f in self.frames]
                # Ghost starts with random Y position (top area)
                self.y = random.randint(50, 250)
                self.glow_color = (100, 200, 255)  # Blue glow for ghost
            else:
                # Regular zombie
                self.frames = [
                    pygame.image.load("asssets/image/zombie_3.png"),
                    pygame.image.load("asssets/image/zombie_4.png")
                ]
                self.frames = [pygame.transform.scale(f, (80, 100)) for f in self.frames]
                self.y = 410
                self.glow_color = (255, 100, 100)  # Red glow for zombie
        except:
            self.frames = [pygame.Surface((80, 100))]
            self.glow_color = (150, 150, 150)

        self.frame_index = 0
        self.health = 3 if enemy_type == "ghost" else 4
        self.max_health = self.health
        self.speed = random.randint(5, 10) if enemy_type == "ghost" else 8
        self.is_attacking = False
        self.score_value = 6 if enemy_type == "ghost" else 1

    def update(self, hero_rect):
        enemy_rect = self.get_rect()
        
        if self.enemy_type == "zombie" and enemy_rect.colliderect(hero_rect):
            self.is_attacking = True
        else:
            self.is_attacking = False
            self.x -= self.speed

        if self.enemy_type == "zombie":
            self.frame_index += 0.1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            
        if self.x < -100:
            self.reset()

    def reset(self):
        self.x = random.randint(800, 1000)
        
        if self.enemy_type == "ghost":
            self.y = random.randint(50, 350)
            self.health = 3
            self.speed = random.randint(5, 10)
        else:
            self.y = 410
            self.health = 3
            self.speed = 4

    def draw(self, screen):
        # Draw glow effect for ghost
        if self.enemy_type == "ghost":
            glow_radius = 35
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.glow_color, 100), 
                             (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, 
                       (self.x + 30 - glow_radius, self.y + 35 - glow_radius), 
                       special_flags=pygame.BLEND_ALPHA_SDL2)
        
        if self.enemy_type == "ghost":
            current_frame = self.frames[0]
        else:
            current_frame = self.frames[int(self.frame_index)]
            
        screen.blit(current_frame, (self.x, self.y))
        
        # Draw Enemy Health Bar over head
        bar_width = 40 if self.enemy_type == "ghost" else 50
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (10 if self.enemy_type == "ghost" else 15)
        
        # Health bar background
        pygame.draw.rect(screen, (100, 100, 100), (health_bar_x, self.y - 10, bar_width, 5))
        # Health bar
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, self.y - 10, bar_width * health_ratio, 5))
        # Health bar border
        pygame.draw.rect(screen, (255, 255, 255), (health_bar_x, self.y - 10, bar_width, 5), 1)
        
        # Draw score value above enemy
        score_font = pygame.font.SysFont('Arial', 12, bold=True)
        score_text = score_font.render(f"+{self.score_value}", True, (255, 255, 0))
        screen.blit(score_text, (self.x + 20, self.y - 25))

    def get_rect(self):
        if self.enemy_type == "ghost":
            return pygame.Rect(self.x + 10, self.y + 10, 40, 50)
        return pygame.Rect(self.x + 20, self.y, 40, 100)