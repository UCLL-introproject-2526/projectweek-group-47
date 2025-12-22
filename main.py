import math
import pygame
import sys
import random
from enemy import Enemy
from bullet import Bullet
from ghost_fire import GhostFire
from coins import Coin
from health import Health


# Simple floating score popup
class ScorePopup:
    def __init__(self, x, y, text, font, color=(255, 215, 0)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.color = color
        self.vy = -1.5
        self.life = 60

    def update(self):
        self.y += self.vy
        self.vy *= 0.98
        self.life -= 1

    def draw(self, screen):
        alpha = max(0, int(255 * (self.life / 60)))
        surf = self.font.render(self.text, True, self.color)
        surf.set_alpha(alpha)
        screen.blit(surf, (self.x - surf.get_width() // 2, self.y - surf.get_height() // 2))


# Small upward star particle for ghost-kill effect
class StarParticle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.2, 1.2)
        self.vy = random.uniform(-4.0, -1.5)
        self.life = random.randint(30, 50)
        self.size = random.randint(2, 4)
        self.color = (255, 235, 180)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.12
        self.life -= 1

    def draw(self, screen):
        alpha = max(0, int(255 * (self.life / 50)))
        col = (*self.color[:3], alpha)
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (self.size, self.size), self.size)
        screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("47 Knights - Shooting Game")
    
    # Initialize fonts
    def load_font(size, bold=False):
        font_names = ['Pixelify Sans', 'Press Start 2P', 'Courier New', 'Arial']
        for font_name in font_names:
            try:
                if bold and font_name != 'Press Start 2P':  
                    return pygame.font.SysFont(font_name, size, bold=True)
                return pygame.font.SysFont(font_name, size)
            except:
                continue
        return pygame.font.Font(None, size)
    
  
    title_font = load_font(48, bold=True)       
    large_font = load_font(36, bold=True)       
    normal_font = load_font(24)                 
    small_font = load_font(18)                  
    ui_font = load_font(20)                   
    pygame.mixer.init()
    
 
    background = pygame.image.load("asssets/image/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    
    try:
       
        hero_winner_img = pygame.image.load("asssets/image/hero_winner.png").convert_alpha()
        # Scale to be large but leave room for text (about 60% of screen height)
        winner_height = int(HEIGHT * 0.6)
        winner_width = int(winner_height * (hero_winner_img.get_width() / hero_winner_img.get_height()))
        hero_winner_img = pygame.transform.scale(hero_winner_img, (winner_width, winner_height))
        
        # Load dead image and scale to fill most of screen
        hero_dead_img = pygame.image.load("asssets/image/hero_dead.png").convert_alpha()
        # Scale to be large but leave room for text (about 60% of screen height)
        dead_height = int(HEIGHT * 0.6)
        dead_width = int(dead_height * (hero_dead_img.get_width() / hero_dead_img.get_height()))
        hero_dead_img = pygame.transform.scale(hero_dead_img, (dead_width, dead_height))
    except:
        print("Warning: Win/Lose images not found! Using fallback graphics.")
        # Create fallback images
        hero_winner_img = pygame.Surface((400, 300))
        hero_winner_img.fill((0, 100, 0))
        pygame.draw.circle(hero_winner_img, (0, 255, 0), (200, 150), 100)
        
        hero_dead_img = pygame.Surface((400, 300))
        hero_dead_img.fill((100, 0, 0))
        pygame.draw.circle(hero_dead_img, (255, 0, 0), (200, 150), 100)

    # Load hero image for rotation
    hero_original = pygame.image.load("asssets/image/firing.png").convert_alpha()
    hero_original = pygame.transform.scale(hero_original, (100, 100))
    
    try:
        shoot_sound = pygame.mixer.Sound("asssets/sounds/firing_sounds.mp3")
        background_music = pygame.mixer.Sound("asssets/sounds/Background_sound.mp3")
        death_sound = pygame.mixer.Sound("asssets/sounds/hero_died.wav")
        fire_sound = pygame.mixer.Sound("asssets/sounds/fire_attack.wav")
        coin_sound = pygame.mixer.Sound("asssets/sounds/coin_collect.wav")
        health_sound = pygame.mixer.Sound("asssets/sounds/health_collect.wav")
        jump_sound = pygame.mixer.Sound("asssets/sounds/jump.wav")
    except:
        print("Warning: Sound files not found!")
        shoot_sound = None
        background_music = None
        death_sound = None
        fire_sound = None
        coin_sound = None
        health_sound = None
        jump_sound = None
    
    hero_x, hero_y = 180, 410
    hero_angle = 0
    
    is_jumping = False
    jump_velocity = 0
    jump_strength = -15
    gravity = 0.6
    hero_base_y = 410
    jump_count = 0
    max_jumps = 2
    
    enemies = [
        Enemy(1000, 410, enemy_type="zombie"),
        Enemy(1200, random.randint(50, 250), enemy_type="ghost"),
        Enemy(1400, random.randint(50, 250), enemy_type="ghost")
    ]
    
    bullets = []
    ghost_fires = []
    popups = []
    star_particles = []
    coins = []
    health_kits = []
    shoot_cooldown = 0
    score = 0
    hero_health = 100
    coins_collected = 0
    TOTAL_COINS_TO_WIN = 67
    coin_spawn_timer = 0
    COIN_SPAWN_RATE = 60
    health_spawn_timer = 0
    HEALTH_SPAWN_RATE = 300
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
            # Game running
            screen.blit(background, (0, 0))
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            dx = mouse_x - (hero_x + 50)
            dy = mouse_y - (hero_y + 50)
            
            if dx != 0 or dy != 0:
                hero_angle = math.degrees(math.atan2(-dy, dx))
            
            rotated_hero = pygame.transform.rotate(hero_original, hero_angle)
            rotated_rect = rotated_hero.get_rect(center=(hero_x + 50, hero_y + 50))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if background_music:
                        background_music.stop()
                    pygame.quit()
                    sys.exit()
                
                # Jump on key press
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and jump_count < max_jumps:
                        is_jumping = True
                        jump_velocity = jump_strength
                        jump_count += 1
                        if jump_sound:
                            jump_sound.play()
                
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
            
            # Update jump physics
            if is_jumping:
                hero_y += jump_velocity
                jump_velocity += gravity
            
            # Check if landed
            if hero_y >= hero_base_y:
                hero_y = hero_base_y
                is_jumping = False
                jump_velocity = 0
                jump_count = 0
            
            if shoot_cooldown > 0: 
                shoot_cooldown -= 1

            # Spawn coins
            coin_spawn_timer += 1
            if coin_spawn_timer >= COIN_SPAWN_RATE:
                coin_spawn_timer = 0
                coin_y = random.randint(100, 500)
                coins.append(Coin(WIDTH + 20, coin_y))
            
            # Spawn health kits
            health_spawn_timer += 1
            if health_spawn_timer >= HEALTH_SPAWN_RATE:
                health_spawn_timer = 0
                health_y = random.randint(100, 500)
                health_kits.append(Health(WIDTH + 20, health_y))
            
            # Update coins
            for coin in coins[:]:
                coin.update()
                
                if not coin.collected:
                    coin.x -= 5
                
                if coin.is_off_screen(WIDTH):
                    coins.remove(coin)
                    continue
                
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                if not coin.collected and coin.get_rect().colliderect(hero_rect):
                    coin.collect()
                    coins_collected += 1
                    if coin_sound:
                        coin_sound.play()
                    
                    if coins_collected >= TOTAL_COINS_TO_WIN:
                        victory = True
                        if background_music:
                            background_music.set_volume(0.1)
            
            # Update health kits
            for health_kit in health_kits[:]:
                health_kit.update()
                
                if health_kit.x < -50:
                    health_kits.remove(health_kit)
                    continue
                
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                if not health_kit.collected and health_kit.get_rect().colliderect(hero_rect):
                    heal_amount = health_kit.collect()
                    hero_health = min(100, hero_health + heal_amount)
                    health_kits.remove(health_kit)
                    if health_sound:
                        health_sound.play()
            
            # Update enemies
            any_attacking = False
            for enemy in enemies:
                enemy_rect = enemy.get_rect()
                hero_rect = pygame.Rect(hero_x + 20, hero_y, 60, 100)
                
                if enemy.enemy_type=="zombie" and enemy_rect.colliderect(hero_rect):
                    enemy.is_attacking = True
                    any_attacking = True
                else:
                    enemy.is_attacking = False
                
                shoot_signal = enemy.update(hero_rect, hero_x + 50, hero_y + 50)
                
                if shoot_signal == "shoot_fire" and enemy.enemy_type == "ghost":
                    ghost_fires.append(GhostFire(
                        enemy.x + 40,
                        enemy.y + 35,
                        hero_x + 50,
                        hero_y + 50
                    ))
                    if fire_sound:
                        fire_sound.play()

            if any_attacking:
                hero_health -= damage_per_frame
                if hero_health <= 0:
                    game_over = True
                    if background_music:
                        background_music.stop()
                    if death_sound and not death_sound_played:
                        death_sound.play()
                        death_sound_played = True

            # Update ghost fires
            for fire in ghost_fires[:]:
                fire.update()
                
                if fire.is_off_screen(WIDTH, HEIGHT):
                    ghost_fires.remove(fire)
                    continue
                
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

            # Update bullets
            for bullet in bullets[:]:
                bullet.update()
                
                if (bullet.x < -20 or bullet.x > WIDTH + 20 or 
                    bullet.y < -20 or bullet.y > HEIGHT + 20):
                    bullets.remove(bullet)
                    continue
                
                bullet_hit = False
                for enemy in enemies:
                    if bullet.get_rect().colliderect(enemy.get_rect()):
                        bullets.remove(bullet)
                        enemy.health -= 1
                        if enemy.health <= 0:
                            # capture death position and score value before reset
                            death_x, death_y = enemy.x + 30, enemy.y + 20
                            value = enemy.score_value
                            # spawn floating score popup
                            popups.append(ScorePopup(death_x, death_y, f"+{value}", normal_font))
                            # spawn nice star particles for ghosts
                            if enemy.enemy_type == "ghost":
                                for i in range(7):
                                    star_particles.append(StarParticle(death_x + random.uniform(-10, 10), death_y + random.uniform(-6, 6)))
                                score += 6
                            else:
                                score += 1
                            # print to console as well
                            print(f"Got +{value} points!")
                            enemy.reset()
                        bullet_hit = True
                        break

            # Draw Everything
            for coin in coins:
                coin.draw(screen)
            
            for health_kit in health_kits:
                health_kit.draw(screen)
            
            for fire in ghost_fires:
                fire.draw(screen)
            
            for enemy in enemies:
                enemy.draw(screen)
            
            # Update and draw score popups
            for popup in popups[:]:
                popup.update()
                popup.draw(screen)
                if popup.life <= 0:
                    popups.remove(popup)

            # Update and draw star particles
            for sp in star_particles[:]:
                sp.update()
                sp.draw(screen)
                if sp.life <= 0:
                    star_particles.remove(sp)

            for bullet in bullets:
                bullet.draw(screen)
            
            screen.blit(rotated_hero, rotated_rect.topleft)
            
            # Draw crosshair
            pygame.draw.line(screen, crosshair_color, 
                           (mouse_x - crosshair_size, mouse_y), 
                           (mouse_x + crosshair_size, mouse_y), 2)
            pygame.draw.line(screen, crosshair_color, 
                           (mouse_x, mouse_y - crosshair_size), 
                           (mouse_x, mouse_y + crosshair_size), 2)
            pygame.draw.circle(screen, crosshair_color, (mouse_x, mouse_y), 3, 2)

            # UI Rendering
            pygame.draw.rect(screen, (30, 30, 30, 180), (10, 10, 250, 100), border_radius=10)
            pygame.draw.rect(screen, (60, 60, 60), (10, 10, 250, 100), 2, border_radius=10)
            
            score_icon = normal_font.render("★", True, (255, 215, 0))
            screen.blit(score_icon, (20, 20))
            score_text = normal_font.render(f"{score}", True, (255, 255, 255))
            screen.blit(score_text, (45, 20))
            
            coin_icon = normal_font.render("$", True, (255, 215, 0))
            screen.blit(coin_icon, (20, 50))
            coins_text = normal_font.render(f"{coins_collected}/{TOTAL_COINS_TO_WIN}", True, (255, 215, 0))
            screen.blit(coins_text, (45, 50))
            
            pygame.draw.rect(screen, (30, 30, 30, 180), (WIDTH - 230, 10, 220, 90), border_radius=10)
            pygame.draw.rect(screen, (60, 60, 60), (WIDTH - 230, 10, 220, 90), 2, border_radius=10)
            
            health_icon = normal_font.render("❤", True, (255, 50, 50))
            screen.blit(health_icon, (WIDTH - 220, 20))
            health_text = normal_font.render(f"{int(hero_health)}%", True, (0, 255, 0))
            screen.blit(health_text, (WIDTH - 190, 20))
            
            pygame.draw.rect(screen, (50, 50, 50), (WIDTH - 220, 50, 200, 15), border_radius=5)
            pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 220, 50, 2 * hero_health, 15), border_radius=5)
            pygame.draw.rect(screen, (100, 100, 100), (WIDTH - 220, 50, 200, 15), 2, border_radius=5)
            
            jumps_icon = normal_font.render("↑", True, (100, 200, 255))
            screen.blit(jumps_icon, (WIDTH - 220, 70))
            jumps_left = max_jumps - jump_count
            jump_text = normal_font.render(f"x{jumps_left}", True, (100, 200, 255))
            screen.blit(jump_text, (WIDTH - 190, 70))
            
            # Enemy counter
            zombie_count = sum(1 for e in enemies if e.enemy_type == "zombie" and e.health > 0)
            ghost_count = sum(1 for e in enemies if e.enemy_type == "ghost" and e.health > 0)
            
            enemy_panel = pygame.Surface((200, 40), pygame.SRCALPHA)
            enemy_panel.fill((30, 30, 30, 180))
            pygame.draw.rect(enemy_panel, (60, 60, 60), (0, 0, 200, 40), 2)
            screen.blit(enemy_panel, (WIDTH // 2 - 100, 10))
            
            zombie_text = ui_font.render(f"Z: {zombie_count}", True, (255, 100, 100))
            ghost_text = ui_font.render(f"G: {ghost_count}", True, (100, 200, 255))
            screen.blit(zombie_text, (WIDTH // 2 - 80, 20))
            screen.blit(ghost_text, (WIDTH // 2 + 20, 20))
            
            if ghost_fires:
                warning_bg = pygame.Surface((250, 40), pygame.SRCALPHA)
                warning_bg.fill((255, 50, 0, 150))
                pygame.draw.rect(warning_bg, (255, 100, 0), (0, 0, 250, 40), 3)
                screen.blit(warning_bg, (WIDTH // 2 - 125, 100))
                
                warning = normal_font.render("FIRE INCOMING!", True, (255, 255, 200))
                screen.blit(warning, (WIDTH // 2 - warning.get_width() // 2, 110))
            
            instructions_bg = pygame.Surface((600, 40), pygame.SRCALPHA)
            instructions_bg.fill((0, 0, 0, 150))
            screen.blit(instructions_bg, (WIDTH // 2 - 300, HEIGHT - 50))
            
            instructions = small_font.render("AIM: MOUSE  |  SHOOT: SPACE/L-CLICK  |  JUMP: W/UP (x2)", 
                                           True, (200, 200, 200))
            screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT - 40))

        elif victory:
            # VICTORY SCREEN - Full screen with large image and bold text
            # Dark green background
            screen.fill((10, 30, 20))
            
            # Draw subtle pattern
            for i in range(0, WIDTH, 40):
                for j in range(0, HEIGHT, 40):
                    pygame.draw.rect(screen, (20, 50, 30), (i, j, 20, 20))
            
            # Draw winner image CENTERED and LARGE
            if hero_winner_img:
                img_rect = hero_winner_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                screen.blit(hero_winner_img, img_rect)
            
            # Draw victory text with shadow effect (BIG and BOLD)
            victory_shadow = title_font.render("VICTORY!", True, (0, 80, 0))
            victory_text = title_font.render("VICTORY!", True, (0, 255, 100))
            
            # Center the text
            shadow_pos = (WIDTH // 2 - victory_shadow.get_width() // 2 + 3, 
                         HEIGHT - 180 + 3)
            text_pos = (WIDTH // 2 - victory_text.get_width() // 2, 
                       HEIGHT - 180)
            
            screen.blit(victory_shadow, shadow_pos)
            screen.blit(victory_text, text_pos)
            
            # Draw stats with good spacing
            coins_text = large_font.render(f"COINS: {coins_collected}", True, (255, 215, 0))
            coins_pos = (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT - 120)
            screen.blit(coins_text, coins_pos)
            
            score_text = large_font.render(f"SCORE: {score}", True, (255, 255, 150))
            score_pos = (WIDTH // 2 - score_text.get_width() // 2, HEIGHT - 80)
            screen.blit(score_text, score_pos)
            
            # Instructions at bottom
            restart_msg = normal_font.render("PRESS 'R' TO PLAY AGAIN  |  PRESS 'Q' TO QUIT", 
                                           True, (200, 255, 200))
            restart_pos = (WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT - 30)
            screen.blit(restart_msg, restart_pos)
            
            # Draw celebration particles (optional visual effect)
            for i in range(20):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT // 2)
                pygame.draw.circle(screen, (255, 215, 0), (x, y), 3)
            
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
            # GAME OVER SCREEN - Full screen with large image and bold text
            # Dark red background
            screen.fill((30, 10, 10))
            
            # Draw subtle pattern
            for i in range(0, WIDTH, 40):
                for j in range(0, HEIGHT, 40):
                    pygame.draw.rect(screen, (50, 20, 20), (i, j, 20, 20))
            
            # Draw dead image CENTERED and LARGE
            if hero_dead_img:
                img_rect = hero_dead_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
                screen.blit(hero_dead_img, img_rect)
            
            # Draw game over text with shadow effect (BIG and BOLD)
            gameover_shadow = title_font.render("GAME OVER", True, (80, 0, 0))
            gameover_text = title_font.render("GAME OVER", True, (255, 50, 50))
            
            # Center the text
            shadow_pos = (WIDTH // 2 - gameover_shadow.get_width() // 2 + 3, 
                         HEIGHT - 180 + 3)
            text_pos = (WIDTH // 2 - gameover_text.get_width() // 2, 
                       HEIGHT - 180)
            
            screen.blit(gameover_shadow, shadow_pos)
            screen.blit(gameover_text, text_pos)
            
            # Draw stats with good spacing
            coins_text = large_font.render(f"COINS: {coins_collected}/{TOTAL_COINS_TO_WIN}", 
                                         True, (255, 215, 0))
            coins_pos = (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT - 120)
            screen.blit(coins_text, coins_pos)
            
            score_text = large_font.render(f"SCORE: {score}", True, (255, 200, 100))
            score_pos = (WIDTH // 2 - score_text.get_width() // 2, HEIGHT - 80)
            screen.blit(score_text, score_pos)
            
            # Instructions at bottom
            restart_msg = normal_font.render("PRESS 'R' TO RESTART  |  PRESS 'Q' TO QUIT", 
                                           True, (255, 200, 200))
            restart_pos = (WIDTH // 2 - restart_msg.get_width() // 2, HEIGHT - 30)
            screen.blit(restart_msg, restart_pos)
            
            # Draw some visual effects
            for i in range(15):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT // 2)
                pygame.draw.circle(screen, (255, 50, 50), (x, y), 2)
            
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