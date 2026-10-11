import pygame
import sys

pygame.init()

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale Fan Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

try:
    logo = pygame.image.load('logo.png')
    logo = pygame.transform.scale(logo, (400, 200))
except:
    logo = pygame.Surface((400, 200))
    logo.fill((255, 0, 0))

cx = WIDTH // 2
cy = HEIGHT // 2
logo_rect = logo.get_rect(center=(cx, cy))

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

alpha = 0
fade_in = True
show_press = False
press_timer = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if show_press:
                    running = False

    if fade_in:
        alpha += 3
        if alpha >= 255:
            alpha = 255
            fade_in = False
            show_press = True
    else:
        press_timer += 1
        if press_timer >= 30:
            press_timer = 0
            # Теперь эта строка короткая, IDE её не тронет:
            if show_press:
                show_press = False
            else:
                show_press = True

    screen.fill(BLACK)
    
    logo_copy = logo.copy()
    logo_copy.set_alpha(alpha)
    screen.blit(logo_copy, logo_rect)
    
    if show_press:
        msg = "Press Z to start"
        text = font.render(msg, True, WHITE)
        tx = WIDTH // 2
        ty = HEIGHT - 80
        text_rect = text.get_rect(center=(tx, ty))
        screen.blit(text, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
