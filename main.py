import pygame
import sys

pygame.init()
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UndertaleErrorMod")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

try:
    logo = pygame.image.load('logo.png')
    logo = pygame.transform.scale(logo, (400, 200))
except:
    logo = pygame.Surface((400, 200))
    logo.fill(RED)

cx = WIDTH // 2
cy = HEIGHT // 2
logo_rect = logo.get_rect(center=(cx, cy))

# --- Подключение шрифта Undertale ---
try:
    font_path = 'determinationmonorusbylyajk.otf'
    font = pygame.font.Font(font_path, 26)
    small_font = pygame.font.Font(font_path, 16)
except:
    # Если шрифт не найден, используем стандартный
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 22)

clock = pygame.time.Clock()

STATE_LOGO = 0
STATE_INSTRUCTION = 1
state = STATE_LOGO

alpha = 0
fade_in = True
show_press = False
press_timer = 0

instruction_lines = [
    "--- Инструкция ---",
    "",
    "[Z или ENTER] - Подтвердить",
    "[X или SHIFT] - Отмена",
    "[C или CTRL] - Меню (В игре)",
    "[F4] - Полный экран",
    "[Удерживайте ESC] - Выход",
    "Когда HP равен 0, вы проигрываете.",
]

menu_items = ["Начать игру", "Настройки"]
selected = 0
footer_text = "undertaleErrorMod:Darkjoons, Smile103 year 2026"

def draw_heart(surf, x, y, size):
    r = size // 4
    c1 = (x - r, y - r)
    c2 = (x + r, y - r)
    pygame.draw.circle(surf, RED, c1, r)
    pygame.draw.circle(surf, RED, c2, r)
    p1 = (x - 2 * r, y - r)
    p2 = (x + 2 * r, y - r)
    p3 = (x, y + r * 2)
    pygame.draw.polygon(surf, RED, [p1, p2, p3])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if state == STATE_LOGO:
                if event.key == pygame.K_z and show_press:
                    state = STATE_INSTRUCTION
            elif state == STATE_INSTRUCTION:
                if event.key == pygame.K_UP:
                    selected = selected - 1
                    if selected < 0:
                        selected = len(menu_items) - 1
                if event.key == pygame.K_DOWN:
                    selected = selected + 1
                    if selected >= len(menu_items):
                        selected = 0
                if event.key == pygame.K_z:
                    if selected == 0:
                        print("Начать игру")
                    elif selected == 1:
                        print("Настройки")

    screen.fill(BLACK)
    
    if state == STATE_LOGO:
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
                show_press = not show_press
        
        logo_copy = logo.copy()
        logo_copy.set_alpha(alpha)
        screen.blit(logo_copy, logo_rect)
        
        if show_press:
            msg = "Нажмите Z для старта"
            text = font.render(msg, True, WHITE)
            tx = cx
            ty = HEIGHT - 80
            tr = text.get_rect(center=(tx, ty))
            screen.blit(text, tr)
    
    elif state == STATE_INSTRUCTION:
        start_y = 40
        line_spacing = 26
        for i in range(len(instruction_lines)):
            text = font.render(instruction_lines[i], True, WHITE)
            tx = cx
            ty = start_y + i * line_spacing
            tr = text.get_rect(center=(tx, ty))
            screen.blit(text, tr)
        
        menu_start_y = 300
        for i in range(len(menu_items)):
            color = YELLOW if i == selected else WHITE
            text = font.render(menu_items[i], True, color)
            tx = cx - 50
            ty = menu_start_y + i * 50
            tr = text.get_rect(center=(tx, ty))
            screen.blit(text, tr)
            
            if i == selected:
                hx = tr.left - 40
                hy = ty
                draw_heart(screen, hx, hy, 30)
        
        footer = small_font.render(footer_text, True, WHITE)
        fr = footer.get_rect(center=(cx, HEIGHT - 20))
        screen.blit(footer, fr)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
