import math
import pygame
import sys
import random
from enemy import Enemy
from bullet import Bullet
from ghost_fire import GhostFire
from coins import Coin  # Import the Coin class

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("47 Knights - Shooting Game")
    font = pygame.font.SysFont('Press Start 2P', 20)
    
    # Initialize pygame mixer for sounds
    pygame.mixer.init()
    
    # Load Assets
    background = pygame.image.load("asssets/image/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Load hero image for rotation
    hero_original = pygame.image.load("asssets/image/firing.png").convert_alpha()
    hero_original = pygame.transform.scale(hero_original, (100, 100))
    
    # Load Sounds
    try:
        shoot_sound = pygame.mixer.Sound("asssets/sounds/firing_sounds.mp3")
        background_music = pygame.mixer.Sound("asssets/sounds/Background_sound.mp3")
        death_sound = pygame.mixer.Sound("asssets/sounds/hero_died.wav")
        fire_sound = pygame.mixer.Sound("asssets/sounds/fire_attack.wav")     #fire from the ghots
        coin_sound = pygame.mixer.Sound("asssets/sounds/coin_collect.wav")  # Coin sound
    except:
        print("Warning: Sound files not found!")
        shoot_sound = None
        background_music = None
        death_sound = None
        fire_sound = None
        coin_sound = None
    
    # Game variables - Hero fixed in position
    hero_x, hero_y = 180, 410
    hero_angle = 0
    is_jumping = False
    jump_velocity = 0
    jump_strength = -16
    gravity = 0.9
    hero_base_y = 410
    
    # Create multiple enemies
    enemies = [
        Enemy(1000, 410, enemy_type="zombie"),
        Enemy(1200, random.randint(50, 250), enemy_type="ghost"),
        Enemy(1400, random.randint(50, 250), enemy_type="ghost")
    ]
    
    bullets = []
    ghost_fires = []
    coins = []  # List to store coins
    shoot_cooldown = 0
    score = 0
    hero_health = 100
    coins_collected = 0
    TOTAL_COINS_TO_WIN = 67
    coin_spawn_timer = 0
    COIN_SPAWN_RATE = 60 
    damage_per_frame = 100 / (2 * 60)
    game_over = False
    victory = False
    death_sound_played = False
    clock = pygame.time.Clock()

    
    crosshair_size = 20
    crosshair_color = (255, 255, 255)

   
    if background_music:
        background_music.play(-1)
        background_music.set_volume(0.2)

    while True:
        if not game_over and not victory:
            screen.blit(background, (0, 0))
            
            # Get mouse position for aiming
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Calculate angle between hero and mouse cursor
            dx = mouse_x - (hero_x + 50)
            dy = mouse_y - (hero_y + 50)
            
            # Update hero angle based on mouse position
            if dx != 0 or dy != 0:
                hero_angle = math.degrees(math.atan2(-dy, dx))
            
            # Rotate hero image
            rotated_hero = pygame.transform.rotate(hero_original, hero_angle)
            rotated_rect = rotated_hero.get_rect(center=(hero_x + 50, hero_y + 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if background_music:
                        background_music.stop()
                    pygame.quit()
                    sys.exit()
                
                # Shooting with mouse click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and shoot_cooldown == 0:
                    bullet_angle = math.radians(hero_angle)
                    
                    gun_offset_x = 30
                    gun_offset_y = 10
                    
                    angle_rad = math.radians(hero_angle)
                    rotated_gun_x = gun_offset_x * math.cos(angle_rad) - gun_offset_y * math.sin(angle_rad)
                    rotated_gun_y = gun_offset_x * math.sin(angle_rad) + gun_offset_y * math.cos(angle_rad)
                    
                    bullet_start_x = hero_x + 50 + rotated_gun_x
                    bullet_start_y = hero_y + 50 + rotated_gun_y
                    
                    bullets.append(Bullet(bullet_start_x, bullet_start_y, bullet_angle))
                    shoot_cooldown = 10
                    if shoot_sound:
                        shoot_sound.play()

            # Shooting Controls with spacebar
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and shoot_cooldown == 0:
                bullet_angle = math.radians(hero_angle)
                
                gun_offset_x = 30
                gun_offset_y = 10
                
                angle_rad = math.radians(hero_angle)
                rotated_gun_x = gun_offset_x * math.cos(angle_rad) - gun_offset_y * math.sin(angle_rad)
                rotated_gun_y = gun_offset_x * math.sin(angle_rad) + gun_offset_y * math.cos(angle_rad)
                
                bullet_start_x = hero_x + 50 + rotated_gun_x
                bullet_start_y = hero_y + 50 + rotated_gun_y
                
                bullets.append(Bullet(bullet_start_x, bullet_start_y, bullet_angle))
                shoot_cooldown = 10
                if shoot_sound:
                    shoot_sound.play()
            
            # Jump Controls
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                if not is_jumping and hero_y >= hero_base_y:
                    is_jumping = True
                    jump_velocity = jump_strength
            
            # Update jump physics
            if is_jumping:
                hero_y += jump_velocity
                jump_velocity += gravity
            
            # Check if landed
            if hero_y >= hero_base_y:
                hero_y = hero_base_y
                is_jumping = False
                jump_velocity = 0       
                
            if shoot_cooldown > 0: 
                shoot_cooldown -= 1

            # Spawn coins continuously (from right side, like enemies)
            coin_spawn_timer += 1
            if coin_spawn_timer >= COIN_SPAWN_RATE:
                coin_spawn_timer = 0
                # Spawn coin at random Y position on right side
                coin_y = random.randint(100, 500)  # Avoid top and bottom edges
                coins.append(Coin(WIDTH + 20, coin_y))
            
            # Update coins
            for coin in coins[:]:
                coin.update()
                
                # Move coin from right to left (like enemies)
                if not coin.collected:
                    coin.x -= 5  # Same speed as zombies
                
                # Remove if off screen (left side)
                if coin.is_off_screen(WIDTH):
                    coins.remove(coin)
                    continue
                
                # Check collision with hero
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                if not coin.collected and coin.get_rect().colliderect(hero_rect):
                    coin.collect()
                    coins_collected += 1
                    if coin_sound:
                        coin_sound.play()
                    
                    # Check win condition
                    if coins_collected >= TOTAL_COINS_TO_WIN:
                        victory = True
                        if background_music:
                            background_music.set_volume(0.1)  # Lower volume for victory
            
            # Update enemies and check for attacks
            any_attacking = False
            for enemy in enemies:
                enemy_rect = enemy.get_rect()
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                
                # Check if enemy touches hero
                if enemy.enemy_type=="zombie" and enemy_rect.colliderect(hero_rect):
                    enemy.is_attacking = True
                    any_attacking = True
                else:
                    enemy.is_attacking = False
                
                # Update enemy and check if ghost wants to shoot fire
                shoot_signal = enemy.update(hero_rect, hero_x + 50, hero_y + 50)
                
                # If ghost wants to shoot fire
                if shoot_signal == "shoot_fire" and enemy.enemy_type == "ghost":
                    ghost_fires.append(GhostFire(
                        enemy.x + 40,
                        enemy.y + 35,
                        hero_x + 50,
                        hero_y + 50
                    ))
                    if fire_sound:
                        fire_sound.play()

            # Apply damage if any enemy is attacking (touching hero)
            if any_attacking:
                hero_health -= damage_per_frame
                if hero_health <= 0:
                    game_over = True
                    if background_music:
                        background_music.stop()
                    if death_sound and not death_sound_played:
                        death_sound.play()
                        death_sound_played = True

            # Update ghost fires and check collisions
            for fire in ghost_fires[:]:
                fire.update()
                
                # Remove if off screen
                if fire.is_off_screen(WIDTH, HEIGHT):
                    ghost_fires.remove(fire)
                    continue
                
                # Check collision with hero
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                if fire.get_rect().colliderect(hero_rect):
                    ghost_fires.remove(fire)
                    hero_health -= fire.damage
                    if hero_health <= 0:
                        game_over = True
                        if background_music:
                            background_music.stop()
                        if death_sound and not death_sound_played:
                            death_sound.play()
                            death_sound_played = True

            # Update bullets and check collisions with enemies
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
                            if enemy.enemy_type == "ghost":
                                score += 6
                            else:
                                score += 1
                        bullet_hit = True
                        break

            # Draw Everything
            # Draw coins first (so they appear behind enemies)
            for coin in coins:
                coin.draw(screen)
            
            # Draw ghost fires
            for fire in ghost_fires:
                fire.draw(screen)
            
            # Draw enemies
            for enemy in enemies:
                enemy.draw(screen)
            
            # Draw bullets
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
            
            # Coin counter (most important!)
            coins_text = font.render(f"COINS: {coins_collected}/{TOTAL_COINS_TO_WIN}", True, (255, 215, 0))
            screen.blit(coins_text, (WIDTH // 2 - 100, 20))
            
            # Coin progress bar
            coin_progress_width = 200
            coin_progress = min(coins_collected / TOTAL_COINS_TO_WIN, 1.0)
            pygame.draw.rect(screen, (100, 100, 100), (WIDTH // 2 - 100, 50, coin_progress_width, 8))
            pygame.draw.rect(screen, (255, 215, 0), (WIDTH // 2 - 100, 50, coin_progress_width * coin_progress, 8))
            
            # Enemy counter
            zombie_count = sum(1 for e in enemies if e.enemy_type == "zombie" and e.health > 0)
            ghost_count = sum(1 for e in enemies if e.enemy_type == "ghost" and e.health > 0)
            enemy_text = font.render(f"Zombies: {zombie_count} | Ghosts: {ghost_count}", True, (200, 200, 255))
            screen.blit(enemy_text, (20, 60))
            
            # Points info
            points_info = font.render("Zombie: 1 | Ghost: 6", True, (255, 255, 0))
            screen.blit(points_info, (WIDTH - 200, 60))
            
            # Health Bar (Top Right)
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 220, 20, 200, 25), 2)
            pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 220, 20, 2 * hero_health, 25))
            
            # Health text
            health_text = font.render(f"HEALTH: {int(hero_health)}%", True, (0, 255, 0))
            screen.blit(health_text, (WIDTH - 220, 50))
            
            # Fire warning if any fireballs are active
            if ghost_fires:
                warning = font.render("FIRE INCOMING!", True, (255, 100, 0))
                screen.blit(warning, (WIDTH//2 - warning.get_width()//2, 100))
            
            # Instructions
            instructions = font.render("Aim: Mouse | Shoot: Space/L-Click | Jump: UP/W", 
                                      True, (200, 200, 200))
            screen.blit(instructions, (WIDTH//2 - 200, HEIGHT - 40))

        elif victory:
            # Victory Screen
            screen.fill((20, 40, 20))  # Greenish background for victory
            
            victory_text = font.render("VICTORY!", True, (0, 255, 0))
            screen.blit(victory_text, (WIDTH//2 - 80, HEIGHT//2 - 100))
            
            coins_victory = font.render(f"You collected {coins_collected} coins!", True, (255, 215, 0))
            screen.blit(coins_victory, (WIDTH//2 - 180, HEIGHT//2 - 50))
            
            goal_text = font.render("Mission Accomplished!", True, (100, 255, 100))
            screen.blit(goal_text, (WIDTH//2 - 150, HEIGHT//2))
            
            final_score = font.render(f"Final Score: {score}", True, (255, 255, 0))
            screen.blit(final_score, (WIDTH//2 - 120, HEIGHT//2 + 50))
            
            restart_msg = font.render("Press 'R' to Play Again or 'Q' to Quit", True, (255, 255, 255))
            screen.blit(restart_msg, (WIDTH//2 - 240, HEIGHT//2 + 100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if background_music:
                        background_music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        if background_music:
                            background_music.stop()
                        run_game()
                        return
                    if event.key == pygame.K_q: 
                        pygame.quit()
                        sys.exit()

        else:
            # Game Over Screen
            screen.fill((20, 20, 20))
            msg = font.render("GAME OVER", True, (255, 50, 50))
            screen.blit(msg, (WIDTH//2 - 100, HEIGHT//2 - 50))
            
            coins_final = font.render(f"Coins: {coins_collected}/{TOTAL_COINS_TO_WIN}", True, (255, 215, 0))
            screen.blit(coins_final, (WIDTH//2 - 120, HEIGHT//2))
            
            final_score = font.render(f"Final Score: {score}", True, (255, 255, 0))
            screen.blit(final_score, (WIDTH//2 - 120, HEIGHT//2 + 50))
            
            restart_msg = font.render("Press 'R' to Restart or 'Q' to Quit", True, (255, 255, 255))
            screen.blit(restart_msg, (WIDTH//2 - 220, HEIGHT//2 + 100))
            
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