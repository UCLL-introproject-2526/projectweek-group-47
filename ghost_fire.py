import pygame
import math
import random

class GhostFire:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        
        # Store original position for animations
        self.original_x = x
        self.original_y = y
        
        # Calculate direction toward target (hero)
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Avoid division by zero
        if distance > 0:
            self.dx = dx / distance
            self.dy = dy / distance
        else:
            self.dx = 0
            self.dy = 0
        
        # Fireball properties
        self.speed = 5
        self.radius = 10
        self.damage = 3 # 10% of hero's health
        self.animation_timer = 0
        self.colors = [
            (255, 100, 0),   
            (255, 150, 0),   
            (255, 200, 0),   
            (255, 50, 0)     
        ]
        
        # Particle trail
        self.trail_particles = []
        self.max_trail_length = 15
        
        # Rotation for spiral effect
        self.rotation_angle = 0
        self.rotation_speed = 0.1
        
    def update(self):
        """Update fireball position and animation."""
        # Move toward target
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        
        # Update animation timer
        self.animation_timer += 1
        
        # Update rotation for spiral effect
        self.rotation_angle += self.rotation_speed
        
        # Add trail particles
        self.trail_particles.append({
            'x': self.x,
            'y': self.y,
            'life': self.max_trail_length,
            'size': random.randint(3, 6)
        })
        
        # Update and remove old trail particles
        for particle in self.trail_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.trail_particles.remove(particle)
    
    def draw(self, screen):
        """Draw the fireball with glowing effect."""
        # Draw trail particles first (so they're behind)
        for i, particle in enumerate(self.trail_particles):
            # Fade out based on life
            alpha = int(255 * (particle['life'] / self.max_trail_length))
            
            # Create a surface for the particle with alpha
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            
            # Draw particle with fading color
            color_index = int((particle['life'] / self.max_trail_length) * (len(self.colors) - 1))
            color = self.colors[color_index]
            
            pygame.draw.circle(particle_surface, (*color, alpha), 
                             (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, 
                       (particle['x'] - particle['size'], particle['y'] - particle['size']))
        
        # Draw outer glow (larger, semi-transparent)
        glow_radius = self.radius + 5
        for i in range(3):
            glow_size = glow_radius + i * 2
            alpha = 100 - i * 30
            
            # Create glow surface
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            
            # Pulsing effect based on animation timer
            pulse = math.sin(self.animation_timer * 0.1) * 2
            actual_glow_size = glow_size + pulse
            
            glow_color = (255, 200, 0, alpha) 
            pygame.draw.circle(glow_surface, glow_color, 
                             (glow_size, glow_size), actual_glow_size)
            screen.blit(glow_surface, 
                       (self.x - glow_size, self.y - glow_size))
        
        current_color = self.colors[int((math.sin(self.animation_timer * 0.2) + 1) * 1.5) % len(self.colors)]
        points = []
        for i in range(8):
            angle = (i / 8) * (2 * math.pi) + self.rotation_angle
            distortion = random.uniform(0.8, 1.2) 
            radius = self.radius * distortion
            px = self.x + math.cos(angle) * radius
            py = self.y + math.sin(angle) * radius
            points.append((px, py))
        
        pygame.draw.polygon(screen, current_color, points)
        core_radius = self.radius * 0.6
        core_color = (255, 255, 200) 
        pygame.draw.circle(screen, core_color, (int(self.x), int(self.y)), int(core_radius))
        hotspot_radius = self.radius * 0.3
        hotspot_color = (255, 255, 255)  # White
        pygame.draw.circle(screen, hotspot_color, (int(self.x), int(self.y)), int(hotspot_radius))
        for i in range(3):
            start_angle = self.rotation_angle + (i * 120 * math.pi / 180)
            end_angle = start_angle + math.pi / 2
            
            start_x = self.x + math.cos(start_angle) * (self.radius + 3)
            start_y = self.y + math.sin(start_angle) * (self.radius + 3)
            end_x = self.x + math.cos(end_angle) * (self.radius + 8)
            end_y = self.y + math.sin(end_angle) * (self.radius + 8)
            
            pygame.draw.line(screen, (255, 255, 200), 
                           (int(start_x), int(start_y)), 
                           (int(end_x), int(end_y)), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)
    
    def is_off_screen(self, screen_width, screen_height):
        """Check if fireball is completely off screen."""
        return (self.x < -50 or self.x > screen_width + 50 or 
                self.y < -50 or self.y > screen_height + 50)
    
    def get_distance_traveled(self):
        
        return math.sqrt((self.x - self.original_x)**2 + (self.y - self.original_y)**2)