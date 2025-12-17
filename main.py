import pygame
import sys
import math
import random
from enemy import Enemy
from bullet import Bullet

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("47 Knights - Shooting Game")
    font = pygame.font.SysFont('Arial', 24, bold=True)
    
    # Initialize pygame mixer for sounds
    pygame.mixer.init()
    
    # Load Assets
    background = pygame.image.load("asssets/image/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load multiple hero images for rotation
    hero_original = pygame.image.load("asssets/image/firing.png").convert_alpha()
    hero_original = pygame.transform.scale(hero_original, (100, 100))
    
    # Load Sounds
    try:
        shoot_sound = pygame.mixer.Sound("asssets/sounds/firing_sounds.mp3")
        background_music = pygame.mixer.Sound("asssets/sounds/Background_sound.mp3")
        death_sound = pygame.mixer.Sound("asssets/sounds/hero_died.wav")
    except:
        print("Warning: Sound files not found!")
        shoot_sound = None
        background_music = None
        death_sound = None
    
    # Game variables
    hero_x, hero_y = 180, 410
    hero_speed = 5
    hero_angle = 0  # Angle for rotation (in degrees)
    
    # Create multiple enemies
    enemies = [
        Enemy(1000, 410, enemy_type="zombie"),
        Enemy(1200, random.randint(50, 250), enemy_type="ghost"),
        Enemy(1400, random.randint(50, 250), enemy_type="ghost")
    ]
    
    bullets = []
    shoot_cooldown = 0
    score = 0
    hero_health = 100
    damage_per_frame = 100 / (2 * 60)
    game_over = False
    death_sound_played = False
    clock = pygame.time.Clock()

    # Crosshair cursor
    crosshair_size = 20
    crosshair_color = (255, 255, 255)

    # Play background music on loop
    if background_music:
        background_music.play(-1)
        background_music.set_volume(0.2)

    while True:
        if not game_over:
            screen.blit(background, (0, 0))
            
            # Get mouse position for aiming
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate angle between hero and mouse cursor
            dx = mouse_x - (hero_x + 50)  # Center of hero
            dy = mouse_y - (hero_y + 50)  # Center of hero
            hero_angle = math.degrees(math.atan2(-dy, dx))  # Negative dy because pygame y increases downward
            
            # Rotate hero image
            rotated_hero = pygame.transform.rotate(hero_original, hero_angle)
            rotated_rect = rotated_hero.get_rect(center=(hero_x + 50, hero_y + 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if background_music:
                        background_music.stop()
                    pygame.quit()
                    sys.exit()
                # Shooting with mouse click (alternative to spacebar)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and shoot_cooldown == 0:
                    # Calculate bullet angle based on mouse position
                    bullet_angle = math.atan2(-(mouse_y - (hero_y + 50)), 
                                              mouse_x - (hero_x + 50))
                    
                    # Calculate gun nozzle position (right side of hero when facing right)
                    # Base offset when facing right (0 degrees)
                    gun_offset_x = 30
                    gun_offset_y = 10
                    
                    # Rotate the gun offset based on hero angle
                    angle_rad = math.radians(hero_angle)
                    rotated_gun_x = gun_offset_x * math.cos(angle_rad) - gun_offset_y * math.sin(angle_rad)
                    rotated_gun_y = gun_offset_x * math.sin(angle_rad) + gun_offset_y * math.cos(angle_rad)
                    
                    # Bullet start position (gun nozzle)
                    bullet_start_x = hero_x + 50 + rotated_gun_x
                    bullet_start_y = hero_y + 50 + rotated_gun_y
                    
                    bullets.append(Bullet(bullet_start_x, bullet_start_y, bullet_angle))
                    shoot_cooldown = 10  # Faster shooting
                    if shoot_sound:
                        shoot_sound.play()

            # Shooting Controls with spacebar (fires in direction hero is facing)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and shoot_cooldown == 0:
                # Calculate bullet angle based on hero rotation
                bullet_angle = math.radians(hero_angle)
                
                # Calculate gun nozzle position
                gun_offset_x = 30
                gun_offset_y = 10
                
                # Rotate the gun offset based on hero angle
                angle_rad = math.radians(hero_angle)
                rotated_gun_x = gun_offset_x * math.cos(angle_rad) - gun_offset_y * math.sin(angle_rad)
                rotated_gun_y = gun_offset_x * math.sin(angle_rad) + gun_offset_y * math.cos(angle_rad)
                
                # Bullet start position (gun nozzle)
                bullet_start_x = hero_x + 50 + rotated_gun_x
                bullet_start_y = hero_y + 50 + rotated_gun_y
                
                bullets.append(Bullet(bullet_start_x, bullet_start_y, bullet_angle))
                shoot_cooldown = 10
                if shoot_sound:
                    shoot_sound.play()
            
            if shoot_cooldown > 0: 
                shoot_cooldown -= 1

            # Hero Movement
            if keys[pygame.K_LEFT] and hero_x > 0:
                hero_x -= hero_speed
            if keys[pygame.K_RIGHT] and hero_x < WIDTH - 100:
                hero_x += hero_speed
            if keys[pygame.K_UP] and hero_y > 0:
                hero_y -= hero_speed
            if keys[pygame.K_DOWN] and hero_y < HEIGHT - 100:
                hero_y += hero_speed

            # Update enemies and check for attacks
            any_attacking = False
            for enemy in enemies:
                enemy_rect = enemy.get_rect()
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                
                # Only zombies attack when touching hero
                if enemy.enemy_type == "zombie" and enemy_rect.colliderect(hero_rect):
                    enemy.is_attacking = True
                    any_attacking = True
                else:
                    enemy.is_attacking = False
                
                enemy.update(hero_rect)

            # Apply damage if any zombie is attacking
            if any_attacking:
                hero_health -= damage_per_frame
                if hero_health <= 0:
                    game_over = True
                    if background_music:
                        background_music.stop()
                    if death_sound and not death_sound_played:
                        death_sound.play()
                        death_sound_played = True

            # Update bullets and check collisions
            for bullet in bullets[:]:
                bullet.update()
                
                # Remove if off screen
                if (bullet.x < -20 or bullet.x > WIDTH + 20 or 
                    bullet.y < -20 or bullet.y > HEIGHT + 20):
                    bullets.remove(bullet)
                    continue
                
                # Check collision with enemies
                bullet_hit = False
                for enemy in enemies:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        bullets.remove(bullet)
                        enemy.health -= 1
                        if enemy.health <= 0:
                            enemy.reset()
                            # Updated scoring: 1 point for zombie, 6 points for ghost
                            if enemy.enemy_type == "ghost":
                                score += 6
                            else:
                                score += 1
                        bullet_hit = True
                        break

            # Draw Everything
            for enemy in enemies:
                enemy.draw(screen)
            
            for bullet in bullets:
                bullet.draw(screen)
            
            # Draw hero (rotated)
            screen.blit(rotated_hero, rotated_rect.topleft)
            
            # Draw crosshair at mouse position
            pygame.draw.line(screen, crosshair_color, 
                           (mouse_x - crosshair_size, mouse_y), 
                           (mouse_x + crosshair_size, mouse_y), 2)
            pygame.draw.line(screen, crosshair_color, 
                           (mouse_x, mouse_y - crosshair_size), 
                           (mouse_x, mouse_y + crosshair_size), 2)
            pygame.draw.circle(screen, crosshair_color, (mouse_x, mouse_y), 3, 2)

            # UI Rendering
            score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))
            
            # Enemy counter
            zombie_count = sum(1 for e in enemies if e.enemy_type == "zombie" and e.health > 0)
            ghost_count = sum(1 for e in enemies if e.enemy_type == "ghost" and e.health > 0)
            enemy_text = font.render(f"Zombies: {zombie_count} | Ghosts: {ghost_count}", True, (200, 200, 255))
            screen.blit(enemy_text, (20, 60))
            
            # Points info
            points_info = font.render("Zombie: 1 point | Ghost: 6 points", True, (255, 255, 0))
            screen.blit(points_info, (WIDTH - 300, 60))
            
            # Health Bar (Top Right)
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 220, 20, 200, 25), 2)
            pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 220, 20, 2 * hero_health, 25))
            
            # Instructions
            instructions = font.render("Move: Arrow Keys | Shoot: Space or Mouse Click | Aim: Mouse", 
                                      True, (200, 200, 200))
            screen.blit(instructions, (WIDTH//2 - 250, HEIGHT - 40))

        else:
            # Game Over Screen
            screen.fill((20, 20, 20))
            msg = font.render("GAME OVER - Press 'R' to Restart or 'Q' to Quit", True, (255, 255, 255))
            screen.blit(msg, (WIDTH//2 - 250, HEIGHT//2))
            
            final_score = font.render(f"Final Score: {score}", True, (255, 255, 0))
            screen.blit(final_score, (WIDTH//2 - 100, HEIGHT//2 + 50))
            
            # Score breakdown
            zombies_killed = score // 1  # Estimate
            ghosts_killed = score // 6   # Estimate
            breakdown = font.render(f"Zombies killed: {zombies_killed} | Ghosts killed: {ghosts_killed}", 
                                   True, (200, 200, 255))
            screen.blit(breakdown, (WIDTH//2 - 200, HEIGHT//2 + 100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        if death_sound:
                            death_sound.stop()
                        run_game()
                        return
                    if event.key == pygame.K_q: 
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    run_game()