# import pygame
# import time


# # Initialize Pygame
# pygame.init()
# later = True
# while later:
#     print("This is our introduction week")
#     time.sleep(2)
#     later= False
import pygame
import random
import math

pygame.init()

# ---------------- SETTINGS ----------------
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
WORLD_WIDTH, WORLD_HEIGHT = 2000, 2000
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GTA-1 Style Krunker (Pygame Only)")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
WHITE = (255, 255, 255)
GRAY = (40, 40, 40)
BLUE = (50, 150, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (240, 240, 0)

# ---------------- PLAYER ----------------
player = pygame.Rect(1000, 1000, 40, 40)
player_speed = 5
player_health = 100

# ---------------- BULLETS ----------------
bullets = []
bullet_speed = 12

# ---------------- ENEMIES ----------------
enemies = []
ENEMY_COUNT = 8

def spawn_enemy():
    return pygame.Rect(
        random.randint(0, WORLD_WIDTH),
        random.randint(0, WORLD_HEIGHT),
        35,
        35
    )

for _ in range(ENEMY_COUNT):
    enemies.append(spawn_enemy())

# ---------------- SCORE ----------------
score = 0
font = pygame.font.SysFont(None, 30)

# ---------------- CAMERA ----------------
def get_camera_offset():
    offset_x = player.centerx - SCREEN_WIDTH // 2
    offset_y = player.centery - SCREEN_HEIGHT // 2
    return offset_x, offset_y

# ---------------- GAME LOOP ----------------
running = True
while running:
    clock.tick(FPS)

    # -------- EVENTS --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            cam_x, cam_y = get_camera_offset()

            world_x = mx + cam_x
            world_y = my + cam_y

            angle = math.atan2(
                world_y - player.centery,
                world_x - player.centerx
            )

            bullets.append({
                "x": player.centerx,
                "y": player.centery,
                "dx": math.cos(angle) * bullet_speed,
                "dy": math.sin(angle) * bullet_speed
            })

    # -------- PLAYER MOVEMENT --------
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.y -= player_speed
    if keys[pygame.K_s]: player.y += player_speed
    if keys[pygame.K_a]: player.x -= player_speed
    if keys[pygame.K_d]: player.x += player_speed

    player.x = max(0, min(WORLD_WIDTH - player.width, player.x))
    player.y = max(0, min(WORLD_HEIGHT - player.height, player.y))

    # -------- BULLETS --------
    for bullet in bullets[:]:
        bullet["x"] += bullet["dx"]
        bullet["y"] += bullet["dy"]

        if not (0 <= bullet["x"] <= WORLD_WIDTH and 0 <= bullet["y"] <= WORLD_HEIGHT):
            bullets.remove(bullet)

    # -------- ENEMY AI --------
    for enemy in enemies:
        dx = player.centerx - enemy.centerx
        dy = player.centery - enemy.centery
        dist = math.hypot(dx, dy)

        if dist != 0:
            enemy.x += int(dx / dist * 2)
            enemy.y += int(dy / dist * 2)

        if enemy.colliderect(player):
            player_health -= 1

    # -------- COLLISIONS --------
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet["x"], bullet["y"], 6, 6)
            if enemy.colliderect(bullet_rect):
                enemies.remove(enemy)
                bullets.remove(bullet)
                enemies.append(spawn_enemy())
                score += 1
                break

    # -------- GAME OVER --------
    if player_health <= 0:
        running = False

    # -------- DRAWING --------
    cam_x, cam_y = get_camera_offset()
    screen.fill(GRAY)

    # World grid (GTA-1 feel)
    for x in range(0, WORLD_WIDTH, 100):
        pygame.draw.line(
            screen, (60, 60, 60),
            (x - cam_x, -cam_y),
            (x - cam_x, WORLD_HEIGHT - cam_y)
        )

    for y in range(0, WORLD_HEIGHT, 100):
        pygame.draw.line(
            screen, (60, 60, 60),
            (-cam_x, y - cam_y),
            (WORLD_WIDTH - cam_x, y - cam_y)
        )

    # Player
    pygame.draw.rect(
        screen,
        BLUE,
        (player.x - cam_x, player.y - cam_y, player.width, player.height)
    )

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(
            screen,
            RED,
            (enemy.x - cam_x, enemy.y - cam_y, enemy.width, enemy.height)
        )

    # Bullets
    for bullet in bullets:
        pygame.draw.circle(
            screen,
            YELLOW,
            (int(bullet["x"] - cam_x), int(bullet["y"] - cam_y)),
            4
        )

    # UI
    screen.blit(font.render(f"Health: {player_health}", True, GREEN), (10, 10))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 40))

    pygame.display.update()

pygame.quit()
