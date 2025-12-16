import pygame
import sys
from main import run_game  # Your game loop from main.py

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("47 Knights - Menu")

# Load menu background (using the clean version without the cursor/button)
try:
    menu_bg = pygame.image.load("asssets/image/manu_background.png")
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))
except:
    # Fallback if image path is wrong
    menu_bg = pygame.Surface((WIDTH, HEIGHT))
    menu_bg.fill((50, 50, 50))

# Using Arial font - bold for a more premium look
font = pygame.font.SysFont('Arial', 45, bold=True)
small_font = pygame.font.SysFont('Arial', 35, bold=True)

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (231, 76, 60)        # A modern "Flat" Red
GREEN = (46, 204, 113)     # A modern "Flat" Green
RED_HOVER = (192, 57, 43)
GREEN_HOVER = (39, 174, 96)
SHADOW = (40, 40, 40)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def menu_loop():
    while True:
        screen.blit(menu_bg, (0, 0))

        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True  

        # --- Button Positioning (Aligned inside the white box) ---
        # The white box center is roughly WIDTH//2 and HEIGHT//2
        button_width = 180
        button_height = 55
        
        # We place them lower in the box to clear the "47 Knights" title
        start_button = pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 30, button_width, button_height)
        exit_button = pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 30, button_width, button_height)

        # Logic for colors
        is_hover_start = start_button.collidepoint((mx, my))
        is_hover_exit = exit_button.collidepoint((mx, my))
        
        start_color = RED_HOVER if is_hover_start else RED
        exit_color = GREEN_HOVER if is_hover_exit else GREEN

        # Draw Shadow first for "Pop" effect
        pygame.draw.rect(screen, SHADOW, (start_button.x + 4, start_button.y + 4, button_width, button_height), border_radius=8)
        pygame.draw.rect(screen, SHADOW, (exit_button.x + 4, exit_button.y + 4, button_width, button_height), border_radius=8)

        # Draw Actual Buttons with rounded corners
        pygame.draw.rect(screen, start_color, start_button, border_radius=8)
        pygame.draw.rect(screen, exit_color, exit_button, border_radius=8)

        # Draw Button Text
        draw_text("START", small_font, WHITE, screen, start_button.centerx, start_button.centery)
        draw_text("EXIT", small_font, WHITE, screen, exit_button.centerx, exit_button.centery)

        # Check clicks
        if is_hover_start and click:
            run_game()
        if is_hover_exit and click:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    menu_loop()