import pygame
import sys
from enemy import Enemy
from bullet import Bullet

def run_game():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont('Arial', 24, bold=True)
    
    # Load Assets
    background = pygame.image.load("asssets/image/background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    hero_img = pygame.image.load("asssets/image/firing.png")
    hero_img = pygame.transform.scale(hero_img, (100, 100))
    
   
    hero_x, hero_y = 180, 410 
    hero_rect = pygame.Rect(hero_x + 20, hero_y, 40, 100)

    
    zombie = Enemy(1000, 410)
    
   
    bullets = []
    shoot_cooldown = 0
    score = 0
    hero_health = 100
    damage_per_frame = 100 / (6 * 60) 
    game_over = False

    clock = pygame.time.Clock()

    while True:
        if not game_over:
            screen.blit(background, (0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Shooting Controls
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and shoot_cooldown == 0:
                bullets.append(Bullet(hero_x + 80, hero_y + 45))
                shoot_cooldown = 15
            if shoot_cooldown > 0: shoot_cooldown -= 1

            # Update Logic
            zombie.update(hero_rect)
            if zombie.is_attacking:
                hero_health -= damage_per_frame
                if hero_health <= 0:
                    game_over = True

            for b in bullets[:]:
                b.update()
                if b.rect.colliderect(zombie.get_rect()):
                    bullets.remove(b)
                    zombie.health -= 1
                    if zombie.health <= 0:
                        zombie.reset()
                        score += 1
                elif b.rect.x > WIDTH:
                    bullets.remove(b)

            # Draw Everything
            zombie.draw(screen)
            for b in bullets: b.draw(screen)
            screen.blit(hero_img, (hero_x, hero_y))

            # UI Rendering
            score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))
            screen.blit(score_text, (20, 20))
            
            # Health Bar (Top Right)
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH - 220, 20, 200, 25), 2) # Border
            pygame.draw.rect(screen, (0, 255, 0), (WIDTH - 220, 20, 2 * hero_health, 25))

        else:
            # Game Over Screen
            screen.fill((20, 20, 20))
            msg = font.render("GAME OVER - Press 'R' to Restart or 'Q' to Quit", True, (255, 255, 255))
            screen.blit(msg, (WIDTH//2 - 250, HEIGHT//2))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: run_game()
                    if event.key == pygame.K_q: 
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    run_game()