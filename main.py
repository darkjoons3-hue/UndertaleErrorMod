import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

WIDTH = 640
HEIGHT = 480

fullscreen = False
show_fps = False
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UndertaleErrorMod")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)

sound_enabled = True
music_enabled = True

# --- Путь к папке с игрой ---
if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))

RESET_FLAG = os.path.join(app_dir, "reset.flag")

# --- Проверка флага сброса при запуске ---
if os.path.exists(RESET_FLAG):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            "ты не сможешь сбросит игру)",
            "UndertaleErrorMod",
            0x40
        )
    except:
        pass
    try:
        os.remove(RESET_FLAG)
    except:
        pass

# --- Загрузка изображений ---
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

try:
    textures = pygame.image.load('textures.png')
    columns_img = textures.subsurface(pygame.Rect(240, 390, 160, 140))
    blob_img = textures.subsurface(pygame.Rect(400, 350, 170, 70))
except:
    columns_img = pygame.Surface((160, 140))
    columns_img.fill(RED)
    blob_img = pygame.Surface((170, 70))
    blob_img.fill(RED)

cx = WIDTH // 2
cy = HEIGHT // 2
logo_rect = logo.get_rect(center=(cx, cy - 60))

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

# --- Звуки ---
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

logo_sound = load_sound('logo_sound.mp3')
logo_sound2 = load_sound('logo_sound2.mp3')
select_sound = load_sound('undertale-select-sound.mp3')

def play_select():
    if select_sound and sound_enabled:
        select_sound.play()

def play_music(path):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        return True
    except:
        return False

def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass

# --- Состояния ---
STATE_LOGO = 0
STATE_MENU = 1
STATE_OPTIONS = 2
state = STATE_LOGO

# --- Логотип ---
alpha = 0
fade_in = True
errmod_alpha = 0
show_press = False
press_timer = 0
logo_sound_played = False
logo_sound2_played = False
menu_music_started = False

menu_items = ["ПРОДОЛЖИТЬ", "ИСТИННЫЙ СБРОС", "ОПЦИИ"]
selected = 0  # 0 - Continue, 1 - Reset, 2 - Options
last_top = 0  # запоминаем последнюю выбранную кнопку сверху

option_items = ["Полный экран", "Звуки", "Музыка", "Показать FPS", "Сбросить настройки", "Назад"]
option_selected = 0

player_name = "CHARA"
player_lv = "LV 19"
player_time = "666:66"
status_text = "КОНЕЦ"

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

def toggle_fullscreen():
    global screen, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # --- ЛОГОТИП ---
            if state == STATE_LOGO:
                if event.key == pygame.K_z and show_press:
                    play_select()
                    state = STATE_MENU
            
            # --- МЕНЮ ---
            elif state == STATE_MENU:
                if event.key == pygame.K_LEFT:
                    if selected == 1:
                        play_select()
                        selected = 0
                        last_top = 0
                    elif selected == 2:
                        play_select()
                        selected = last_top
                if event.key == pygame.K_RIGHT:
                    if selected == 0:
                        play_select()
                        selected = 1
                        last_top = 1
                    elif selected == 2:
                        play_select()
                        selected = last_top
                if event.key == pygame.K_UP:
                    if selected == 2:
                        play_select()
                        selected = last_top
                if event.key == pygame.K_DOWN:
                    if selected == 0 or selected == 1:
                        play_select()
                        selected = 2
                if event.key == pygame.K_z:
                    play_select()
                    if selected == 0:
                        print("Продолжить игру")
                    elif selected == 1:
                        # Создаём флаг и выходим
                        try:
                            with open(RESET_FLAG, 'w') as f:
                                f.write("reset")
                        except:
                            pass
                        running = False
                    elif selected == 2:
                        state = STATE_OPTIONS
                        option_selected = 0
            
            # --- НАСТРОЙКИ ---
            elif state == STATE_OPTIONS:
                if event.key == pygame.K_UP:
                    play_select()
                    option_selected -= 1
                    if option_selected < 0:
                        option_selected = len(option_items) - 1
                if event.key == pygame.K_DOWN:
                    play_select()
                    option_selected += 1
                    if option_selected >= len(option_items):
                        option_selected = 0
                if event.key == pygame.K_z:
                    play_select()
                    if option_selected == 0:
                        toggle_fullscreen()
                    elif option_selected == 1:
                        sound_enabled = not sound_enabled
                    elif option_selected == 2:
                        music_enabled = not music_enabled
                        if not music_enabled:
                            stop_music()
                        else:
                            play_music('determination.mp3')
                    elif option_selected == 3:
                        show_fps = not show_fps
                    elif option_selected == 4:
                        # Сброс настроек
                        fullscreen = False
                        sound_enabled = True
                        music_enabled = True
                        show_fps = False
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        play_music('determination.mp3')
                    elif option_selected == 5:
                        state = STATE_MENU
                if event.key == pygame.K_x:
                    play_select()
                    state = STATE_MENU

    screen.fill(BLACK)
    
    # --- ЛОГОТИП ---
    if state == STATE_LOGO:
        if not logo_sound_played:
            if logo_sound and sound_enabled:
                logo_sound.play()
            logo_sound_played = True
        
        if fade_in:
            alpha += 3
            if alpha >= 255:
                alpha = 255
                fade_in = False
        elif errmod_alpha < 255:
            errmod_alpha += 5
            if errmod_alpha >= 255:
                errmod_alpha = 255
                if not logo_sound2_played:
                    if logo_sound2 and sound_enabled:
                        logo_sound2.play()
                    logo_sound2_played = True
        else:
            press_timer += 1
            if press_timer >= 30:
                press_timer = 0
            show_press = press_timer < 15
        
        logo_copy = logo.copy()
        logo_copy.set_alpha(alpha)
        screen.blit(logo_copy, logo_rect)
        
        # Надпись "Error Mod" красным
        if errmod_alpha > 0:
            errmod_text = big_font.render("Error Mod", True, RED)
            errmod_copy = errmod_text.copy()
            errmod_copy.set_alpha(errmod_alpha)
            er_rect = errmod_copy.get_rect(center=(cx, cy + 80))
            screen.blit(errmod_copy, er_rect)
        
        # Мигающая надпись "Нажмите Z"
        if errmod_alpha >= 255 and show_press:
            msg = "Нажмите Z для старта"
            text = font.render(msg, True, WHITE)
            tr = text.get_rect(center=(cx, HEIGHT - 60))
            screen.blit(text, tr)
    
    # --- МЕНЮ ---
    elif state == STATE_MENU:
        if not menu_music_started:
            if music_enabled:
                play_music('determination.mp3')
            menu_music_started = True
        
        x_btn = big_font.render("X", True, WHITE)
        screen.blit(x_btn, (20, 20))
        
        screen.blit(columns_img, (cx - 80, 20))
        
        name_text = font.render(player_name, True, WHITE)
        lv_text = font.render(player_lv, True, WHITE)
        time_text = font.render(player_time, True, WHITE)
        
        screen.blit(name_text, (150, 170))
        screen.blit(lv_text, (300, 170))
        screen.blit(time_text, (470, 170))
        
        status = font.render(status_text, True, WHITE)
        screen.blit(status, (150, 210))
        
        # Continue
        color1 = GOLD if selected == 0 else WHITE
        text1 = font.render(menu_items[0], True, color1)
        screen.blit(text1, (130, 280))
        if selected == 0:
            draw_heart(screen, 100, 290, 30)
        
        # True Reset
        color2 = GOLD if selected == 1 else WHITE
        text2 = font.render(menu_items[1], True, color2)
        screen.blit(text2, (400, 280))
        if selected == 1:
            draw_heart(screen, 370, 290, 30)
        
        # Options (по центру ниже)
        color3 = GOLD if selected == 2 else WHITE
        text3 = font.render(menu_items[2], True, color3)
        text3_rect = text3.get_rect(center=(cx, 340))
        screen.blit(text3, text3_rect)
        if selected == 2:
            draw_heart(screen, text3_rect.left - 40, 350, 30)
        
        screen.blit(blob_img, (cx - 85, 380))
        
        footer = small_font.render(footer_text, True, WHITE)
        fr = footer.get_rect(center=(cx, HEIGHT - 15))
        screen.blit(footer, fr)
    
    # --- НАСТРОЙКИ ---
    elif state == STATE_OPTIONS:
        title = big_font.render("НАСТРОЙКИ", True, WHITE)
        title_rect = title.get_rect(center=(cx, 60))
        screen.blit(title, title_rect)
        
        start_y = 140
        spacing = 50
        
        for i in range(len(option_items)):
            if i == 0:
                val = "ВКЛ" if fullscreen else "ВЫКЛ"
                label = f"{option_items[i]}: {val}"
            elif i == 1:
                val = "ВКЛ" if sound_enabled else "ВЫКЛ"
                label = f"{option_items[i]}: {val}"
            elif i == 2:
                val = "ВКЛ" if music_enabled else "ВЫКЛ"
                label = f"{option_items[i]}: {val}"
            elif i == 3:
                val = "ВКЛ" if show_fps else "ВЫКЛ"
                label = f"{option_items[i]}: {val}"
            else:
                label = option_items[i]
            
            color = GOLD if i == option_selected else WHITE
            text = font.render(label, True, color)
            ty = start_y + i * spacing
            tr = text.get_rect(center=(cx, ty))
            screen.blit(text, tr)
            
            if i == option_selected:
                draw_heart(screen, tr.left - 40, ty + 10, 30)
        
        hint = small_font.render("Z - изменить, X - назад", True, WHITE)
        hr = hint.get_rect(center=(cx, HEIGHT - 30))
        screen.blit(hint, hr)
    
    # --- FPS ---
    if show_fps:
        fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, GOLD)
        screen.blit(fps_text, (WIDTH - 100, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
