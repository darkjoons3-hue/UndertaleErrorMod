import pygame
import sys
import os

pygame.init()
WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UndertaleErrorMod")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# --- Загрузка ресурсов ---
def load_image(path, size=None):
    try:
        img = pygame.image.load(path)
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        surf = pygame.Surface(size if size else (100, 100))
        surf.fill(RED)
        return surf

logo = load_image('logo.png', (400, 200))

# Загружаем текстуры из корня проекта
try:
    textures = pygame.image.load('textures.png')
    # Вырезаем нужные кусочки (координаты подобраны под твой спрайт-лист)
    columns_img = textures.subsurface(pygame.Rect(240, 390, 160, 140))
    blob_img = textures.subsurface(pygame.Rect(400, 350, 170, 70))
except Exception as e:
    print(f"Ошибка загрузки текстур: {e}")
    columns_img = pygame.Surface((160, 140))
    columns_img.fill(RED)
    blob_img = pygame.Surface((170, 70))
    blob_img.fill(RED)

cx = WIDTH // 2
cy = HEIGHT // 2
logo_rect = logo.get_rect(center=(cx, cy))

# --- Шрифты ---
try:
    font_path = 'determinationmonorusbylyajk.otf'
    font = pygame.font.Font(font_path, 26)
    small_font = pygame.font.Font(font_path, 16)
    big_font = pygame.font.Font(font_path, 36)
except:
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 22)
    big_font = pygame.font.Font(None, 40)

clock = pygame.time.Clock()

STATE_LOGO = 0
STATE_MENU = 1
state = STATE_LOGO

alpha = 0
fade_in = True
show_press = False
press_timer = 0

# --- Данные для меню ---
player_name = "CHARA"
player_lv = "LV 19"
player_time = "666:66"
status_text = "КОНЕЦ"

menu_items = ["ПРОДОЛЖИТЬ", "ИСТИННЫЙ СБРОС"]
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
                    state = STATE_MENU
            elif state == STATE_MENU:
                if event.key == pygame.K_LEFT:
                    selected = 0
                if event.key == pygame.K_RIGHT:
                    selected = 1
                if event.key == pygame.K_z:
                    if selected == 0:
                        print("Выбрано: Продолжить")
                    elif selected == 1:
                        print("Выбрано: Истинный сброс")

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
    
    elif state == STATE_MENU:
        # 1. Кнопка выхода "X"
        x_btn = big_font.render("X", True, WHITE)
        screen.blit(x_btn, (20, 20))
        
        # 2. Колонны (из текстуры)
        screen.blit(columns_img, (cx - 80, 20))
        
        # 3. Имя, Уровень, Время
        name_text = font.render(player_name, True, WHITE)
        lv_text = font.render(player_lv, True, WHITE)
        time_text = font.render(player_time, True, WHITE)
        
        screen.blit(name_text, (150, 160))
        screen.blit(lv_text, (300, 160))
        screen.blit(time_text, (470, 160))
        
        # 4. Статус
        status = font.render(status_text, True, WHITE)
        screen.blit(status, (150, 200))
        
        # 5. Кнопки меню
        color1 = YELLOW if selected == 0 else WHITE
        text1 = font.render(menu_items[0], True, color1)
        screen.blit(text1, (150, 300))
        if selected == 0:
            draw_heart(screen, 120, 310, 30)
            
        color2 = YELLOW if selected == 1 else WHITE
        text2 = font.render(menu_items[1], True, color2)
        screen.blit(text2, (400, 300))
        if selected == 1:
            draw_heart(screen, 370, 310, 30)
            
        # 6. Пятно внизу (из текстуры)
        screen.blit(blob_img, (cx - 85, 370))
        
        # 7. Нижний колонтитул
        footer = small_font.render(footer_text, True, WHITE)
        fr = footer.get_rect(center=(cx, HEIGHT - 15))
        screen.blit(footer, fr)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
