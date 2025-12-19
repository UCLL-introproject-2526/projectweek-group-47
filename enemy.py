# import pygame
# import random
# import math

# class Enemy:
#     def __init__(self, x, y, enemy_type="zombie"):
#         self.x = x
#         self.y = y
#         self.enemy_type = enemy_type  # "zombie" or "ghost"
        
#         try:
#             if self.enemy_type == "ghost":
#                 # Ghost uses different image
#                 self.frames = [
#                     pygame.image.load("asssets/image/ghost_the_second_enemy.png")
#                 ]
#                 self.frames = [pygame.transform.scale(f, (60, 70)) for f in self.frames]
#                 # Ghost starts with random Y position (top area)
#                 self.y = random.randint(50, 250)
#                 self.glow_color = (100, 200, 255)  # Blue glow for ghost
#             else:
#                 # Regular zombie
#                 self.frames = [
#                     pygame.image.load("asssets/image/zombie_3.png"),
#                     pygame.image.load("asssets/image/zombie_4.png")
#                 ]
#                 self.frames = [pygame.transform.scale(f, (80, 100)) for f in self.frames]
#                 self.y = 410
#                 self.glow_color = (255, 100, 100)  # Red glow for zombie
#         except:
#             self.frames = [pygame.Surface((80, 100))]
#             self.glow_color = (150, 150, 150)

#         self.frame_index = 0
#         self.health = 3 if enemy_type == "ghost" else 4
#         self.max_health = self.health
#         self.speed = random.randint(2,4) if enemy_type == "ghost" else 6
#         self.is_attacking = False
#         self.score_value = 6 if enemy_type == "ghost" else 1
        
#         # Fire shooting variables (for ghosts only)
#         self.fire_cooldown = 0
#         self.fire_rate = random.randint(120, 240)  # 2-4 seconds at 60 FPS
#         self.can_shoot_fire = random.random() < 0.1  # 1 in 6 chance (16.6%)

#     def update(self, hero_rect, hero_x=None, hero_y=None):
#         enemy_rect = self.get_rect()
        
#         # Check if touching hero (both zombies and ghosts can attack by touching)
#         if enemy_rect.colliderect(hero_rect):
#             self.is_attacking = True
#         else:
#             self.is_attacking = False
#             self.x -= self.speed
#         if self.enemy_type == "zombie":
#             self.frame_index += 0.1
#             if self.frame_index >= len(self.frames):
#                 self.frame_index = 0
#         if self.x < -100:
#             self.reset()
#             return None
#         shoot_signal = None
#         if (self.enemy_type == "ghost" and self.can_shoot_fire and 
#             self.fire_cooldown <= 0 and hero_x is not None and hero_y is not None):
#             distance_to_hero = math.sqrt((hero_x - self.x)**2 + (hero_y - self.y)**2)
            
            
#             if 200 < distance_to_hero < 500:
#                 self.fire_cooldown = self.fire_rate
#                 shoot_signal = "shoot_fire"  
        
#         # Update fire cooldown
#         if self.fire_cooldown > 0:
#             self.fire_cooldown -= 1
        
#         return shoot_signal

#     def reset(self):
#         self.x = random.randint(800, 1000)
        
#         if self.enemy_type == "ghost":
#             # Reset ghost to random Y position
#             self.y = random.randint(50, 350)
#             self.health = 3
#             self.speed = random.randint(4,6)
#             # Keep fire shooting ability
#             if not self.can_shoot_fire:
#                 # Small chance to gain fire ability when reset
#                 self.can_shoot_fire = random.random() < 0.1  # 10% chance
#         else:
#             # Reset zombie to ground position
#             self.y = 410
#             self.health = 4
#             self.speed = 4

#     def draw(self, screen):
#         # Draw glow effect for ghost
#         if self.enemy_type == "ghost":
#             glow_radius = 35
#             glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
#             pygame.draw.circle(glow_surface, (*self.glow_color, 100), 
#                              (glow_radius, glow_radius), glow_radius)
#             screen.blit(glow_surface, 
#                        (self.x + 30 - glow_radius, self.y + 35 - glow_radius), 
#                        special_flags=pygame.BLEND_ALPHA_SDL2)
        
#         if self.enemy_type == "ghost":
#             current_frame = self.frames[0]
#         else:
#             current_frame = self.frames[int(self.frame_index)]
            
#         screen.blit(current_frame, (self.x, self.y))
        
#         # Draw Enemy Health Bar over head
#         bar_width = 40 if self.enemy_type == "ghost" else 50
#         health_ratio = self.health / self.max_health
#         health_bar_x = self.x + (10 if self.enemy_type == "ghost" else 15)
        
#         # Health bar background
#         pygame.draw.rect(screen, (100, 100, 100), (health_bar_x, self.y - 10, bar_width, 5))
#         # Health bar
#         pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, self.y - 10, bar_width * health_ratio, 5))
#         # Health bar border
#         pygame.draw.rect(screen, (255, 255, 255), (health_bar_x, self.y - 10, bar_width, 5), 1)
        
#         # Draw score value above enemy
#         score_font = pygame.font.SysFont('Arial', 12, bold=True)
#         score_text = score_font.render(f"+{self.score_value}", True, (255, 255, 0))
#         screen.blit(score_text, (self.x + 20, self.y - 25))
        
#         # Draw fire ability indicator for ghosts that can shoot
#         if self.enemy_type == "ghost" and self.can_shoot_fire:
#             # Draw small fire icon near ghost
#             fire_radius = 4
#             fire_color = (255, 100, 0)  # Orange
#             pygame.draw.circle(screen, fire_color, 
#                              (int(self.x + 50), int(self.y - 15)), fire_radius)
#             pygame.draw.circle(screen, (255, 200, 0), 
#                              (int(self.x + 50), int(self.y - 15)), fire_radius - 2)

#     def get_rect(self):
#         if self.enemy_type == "ghost":
#             return pygame.Rect(self.x + 10, self.y + 10, 40, 50)
#         return pygame.Rect(self.x + 20, self.y, 40, 100)



import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type="zombie"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        
        try:
            if self.enemy_type == "ghost":
                self.frames = [
                    pygame.image.load("asssets/image/ghost_the_second_enemy.png")
                ]
                self.frames = [pygame.transform.scale(f, (60, 70)) for f in self.frames]
                self.y = random.randint(50, 250)
                self.glow_color = (100, 200, 255)
            else:
                self.frames = [
                    pygame.image.load("asssets/image/zombie_3.png"),
                    pygame.image.load("asssets/image/zombie_4.png")
                ]
                self.frames = [pygame.transform.scale(f, (80, 100)) for f in self.frames]
                self.y = 410
                self.glow_color = (255, 100, 100)
        except:
            self.frames = [pygame.Surface((80, 100))]
            self.glow_color = (150, 150, 150)

        self.frame_index = 0
        self.health = 3 if enemy_type == "ghost" else 4
        self.max_health = self.health
        self.speed = random.randint(2, 4) if enemy_type == "ghost" else 6
        self.is_attacking = False
        self.score_value = 6 if enemy_type == "ghost" else 1
        
        # Fire shooting variables
        self.fire_cooldown = 0
        self.fire_rate = random.randint(120, 240)
        self.can_shoot_fire = random.random() < 0.1

    def update(self, hero_rect, hero_x=None, hero_y=None):
        enemy_rect = self.get_rect()
        
        # Check if touching hero
        if enemy_rect.colliderect(hero_rect):
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
            return None
        
        shoot_signal = None
        if (self.enemy_type == "ghost" and self.can_shoot_fire and 
            self.fire_cooldown <= 0 and hero_x is not None and hero_y is not None):
            
            # Calculate distance to hero
            distance_to_hero = math.sqrt((hero_x - self.x)**2 + (hero_y - self.y)**2)
            
            # FIXED: Only shoot if ghost is in FRONT of hero (to the right)
            # AND within reasonable vertical range (so you can jump to dodge)
            # AND not too far horizontally
            is_in_front = self.x > hero_x  # Ghost is to the right of hero
            vertical_distance = abs(self.y - hero_y)
            
            # Only shoot if:
            # 1. Ghost is in front of hero (to the right)
            # 2. Within 300-500 pixels horizontally
            # 3. Within 150 pixels vertically (so you can jump to dodge)
            if (is_in_front and 
                300 < distance_to_hero < 500 and 
                vertical_distance < 150):
                self.fire_cooldown = self.fire_rate
                shoot_signal = "shoot_fire"
        
        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1
        
        return shoot_signal

    def reset(self):
        self.x = random.randint(800, 1000)
        
        if self.enemy_type == "ghost":
            self.y = random.randint(50, 350)
            self.health = 3
            self.speed = random.randint(4, 6)
            if not self.can_shoot_fire:
                self.can_shoot_fire = random.random() < 0.6
        else:
            self.y = 410
            self.health = 4
            self.speed = 4

    def draw(self, screen):
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
        
        bar_width = 40 if self.enemy_type == "ghost" else 50
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (10 if self.enemy_type == "ghost" else 15)
        
        pygame.draw.rect(screen, (100, 100, 100), (health_bar_x, self.y - 10, bar_width, 5))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, self.y - 10, bar_width * health_ratio, 5))
        pygame.draw.rect(screen, (255, 255, 255), (health_bar_x, self.y - 10, bar_width, 5), 1)
        
        score_font = pygame.font.SysFont('Arial', 12, bold=True)
        score_text = score_font.render(f"+{self.score_value}", True, (255, 255, 0))
        screen.blit(score_text, (self.x + 20, self.y - 25))
        
        if self.enemy_type == "ghost" and self.can_shoot_fire:
            fire_radius = 4
            fire_color = (255, 100, 0)
            pygame.draw.circle(screen, fire_color, 
                             (int(self.x + 50), int(self.y - 15)), fire_radius)
            pygame.draw.circle(screen, (255, 200, 0), 
                             (int(self.x + 50), int(self.y - 15)), fire_radius - 2)

    def get_rect(self):
        if self.enemy_type == "ghost":
            return pygame.Rect(self.x + 10, self.y + 10, 40, 50)
        return pygame.Rect(self.x + 20, self.y, 40, 100)