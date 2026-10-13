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
pygame.mouse.set_visible(False)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)

sound_enabled = True
music_enabled = True

if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))

RESET_FLAG = os.path.join(app_dir, "reset.flag")

if os.path.exists(RESET_FLAG):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0, "ты не сможешь сбросит игру)",
            "UndertaleErrorMod", 0x40
        )
    except:
        pass
    try:
        os.remove(RESET_FLAG)
    except:
        pass

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
history_img = load_image('history.png', (500, 370))
sans_img = load_image('sans-error.png', (320, 320))

try:
    textures = pygame.image.load('textures.png')
    columns_img = textures.subsurface(pygame.Rect(240, 390, 160, 140))
    blob_img = textures.subsurface(pygame.Rect(400, 350, 170, 70))
except:
    columns_img = pygame.Surface((160, 140))
    columns_img.fill(RED)
    blob_img = pygame.Surface((170, 70))
    blob_img.fill(RED)

# --- Окно диалога: верхний левый из спрайт-листа ---
try:
    dialogs_sheet = pygame.image.load('undertale-dialogs.png')
    dialog_box_small = dialogs_sheet.subsurface(pygame.Rect(15, 15, 105, 75))
    dialog_box = pygame.transform.scale(dialog_box_small, (580, 130))
except Exception as e:
    print(f"Ошибка окна диалога: {e}")
    dialog_box = pygame.Surface((580, 130))
    dialog_box.fill(BLACK)
    pygame.draw.rect(dialog_box, WHITE, (0, 0, 580, 130), 3)

cx = WIDTH // 2
cy = HEIGHT // 2
logo_rect = logo.get_rect(center=(cx, cy - 60))
history_rect = history_img.get_rect(center=(cx, cy))
sans_rect = sans_img.get_rect(center=(cx, 190))
dialog_rect = dialog_box.get_rect(center=(cx, 400))

try:
    font_path = 'determinationmonorusbylyajk.otf'
    font = pygame.font.Font(font_path, 26)
    small_font = pygame.font.Font(font_path, 16)
    big_font = pygame.font.Font(font_path, 36)
except:
    font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 22)
    big_font = pygame.font.Font(None, 40)

try:
    sans_font = pygame.font.Font('ComicSans.ttf', 22)
except:
    sans_font = pygame.font.Font(None, 24)

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except:
        return None

logo_sound = load_sound('logo_sound.mp3')
logo_sound2 = load_sound('logo_sound2.mp3')
select_sound = load_sound('undertale-select-sound.mp3')
sans_dialog_sound = load_sound('sans-dialogs.mp3')

def play_select():
    if select_sound and sound_enabled:
        select_sound.play()

def play_music(path, loops=-1):
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(loops)
        return True
    except:
        return False

def stop_music():
    try:
        pygame.mixer.music.stop()
    except:
        pass

def stop_all_sounds():
    try:
        pygame.mixer.music.stop()
    except:
        pass
    try:
        pygame.mixer.stop()
    except:
        pass

STATE_LOGO = 0
STATE_MENU = 1
STATE_OPTIONS = 2
STATE_HISTORY = 3
STATE_SANS = 4
state = STATE_LOGO

alpha = 0
fade_in = True
errmod_alpha = 0
show_press = False
press_timer = 0
logo_sound_played = False
logo_sound2_played = False
menu_music_started = False

menu_items = ["ПРОДОЛЖИТЬ", "ИСТИННЫЙ СБРОС", "ОПЦИИ"]
selected = 0
last_top = 0

option_items = ["Полный экран", "Звуки", "Музыка", "Показать FPS", "Сбросить настройки", "Назад"]
option_selected = 0

player_name = "CHARA"
player_lv = "LV 19"
player_time = "666:66"
status_text = "КОНЕЦ"

footer_text = "undertaleErrorMod:Darkjoons, Smile103 year 2026"

history_start_ms = 0
history_music_started = False
bells_started = False

# Диалоги Санса (текст, скорость сек/буква, цвет)
SANS_LINES = [
    ("Вижу в тебе много зла", 0.06, WHITE),
    ("Чувак тебе надо расслабится, ведь тебе сейчас предстоит выжить в вечных муках", 0.028, WHITE),
    ("ДОБРО ПОЖАЛОВАТЬ В АД", 0.15, RED),
]

sans_start_ms = 0
sans_alpha = 0
sans_box_visible = False
sans_line_index = 0
sans_typed = 0
sans_typing_done = False
sans_last_char_ms = 0

def draw_heart(surf, x, y, size, color=RED):
    r = size // 4
    c1 = (x - r, y - r)
    c2 = (x + r, y - r)
    pygame.draw.circle(surf, color, c1, r)
    pygame.draw.circle(surf, color, c2, r)
    p1 = (x - 2 * r, y - r)
    p2 = (x + 2 * r, y - r)
    p3 = (x, y + r * 2)
    pygame.draw.polygon(surf, color, [p1, p2, p3])

def option_action():
    global option_selected, state, sound_enabled, music_enabled, show_fps, fullscreen, screen
    if option_selected == 0:
        fullscreen = not fullscreen
        if fullscreen:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
        fullscreen = False
        sound_enabled = True
        music_enabled = True
        show_fps = False
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        play_music('determination.mp3')
    elif option_selected == 5:
        state = STATE_MENU

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if state == STATE_LOGO:
                if (event.key == pygame.K_z or event.key == pygame.K_RETURN) and show_press:
                    play_select()
                    state = STATE_MENU
            
            elif state == STATE_MENU:
                if event.key == pygame.K_LEFT:
                    if selected == 1:
                        selected = 0; last_top = 0
                    elif selected == 2:
                        selected = last_top
                if event.key == pygame.K_RIGHT:
                    if selected == 0:
                        selected = 1; last_top = 1
                    elif selected == 2:
                        selected = last_top
                if event.key == pygame.K_UP:
                    if selected == 2:
                        selected = last_top
                if event.key == pygame.K_DOWN:
                    if selected == 0 or selected == 1:
                        selected = 2
                
                if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                    play_select()
                    if selected == 0:
                        stop_all_sounds()
                        state = STATE_HISTORY
                        history_start_ms = pygame.time.get_ticks()
                        history_music_started = False
                        bells_started = False
                    elif selected == 1:
                        try:
                            with open(RESET_FLAG, 'w') as f:
                                f.write("reset")
                        except:
                            pass
                        running = False
                    elif selected == 2:
                        state = STATE_OPTIONS
                        option_selected = 0
                
                if event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                    running = False
            
            elif state == STATE_OPTIONS:
                if event.key == pygame.K_UP:
                    option_selected -= 1
                    if option_selected < 0:
                        option_selected = len(option_items) - 1
                if event.key == pygame.K_DOWN:
                    option_selected += 1
                    if option_selected >= len(option_items):
                        option_selected = 0
                if event.key == pygame.K_z or event.key == pygame.K_RETURN:
                    play_select()
                    option_action()
                if event.key == pygame.K_x or event.key == pygame.K_ESCAPE:
                    play_select()
                    state = STATE_MENU
            
            elif state == STATE_SANS:
                if sans_typing_done and (event.key == pygame.K_z or event.key == pygame.K_RETURN):
                    sans_line_index += 1
                    if sans_line_index < len(SANS_LINES):
                        sans_typed = 0
                        sans_typing_done = False
                        sans_last_char_ms = pygame.time.get_ticks()

    screen.fill(BLACK)
    
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
                    if sound_enabled:
                        try:
                            pygame.mixer.stop()
                        except:
                            pass
                        if logo_sound2:
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
        
        if errmod_alpha > 0:
            errmod_text = big_font.render("Error Mod", True, RED)
            errmod_copy = errmod_text.copy()
            errmod_copy.set_alpha(errmod_alpha)
            er_rect = errmod_copy.get_rect(center=(cx, cy + 80))
            screen.blit(errmod_copy, er_rect)
        
        if errmod_alpha >= 255 and show_press:
            msg = "Нажмите Z или ENTER"
            text = font.render(msg, True, WHITE)
            tr = text.get_rect(center=(cx, HEIGHT - 60))
            screen.blit(text, tr)
    
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
        
        color1 = GOLD if selected == 0 else WHITE
        text1 = font.render(menu_items[0], True, color1)
        rect1 = text1.get_rect(topleft=(130, 280))
        screen.blit(text1, rect1)
        if selected == 0:
            draw_heart(screen, 100, 290, 30)
        
        color2 = GOLD if selected == 1 else WHITE
        text2 = font.render(menu_items[1], True, color2)
        rect2 = text2.get_rect(topleft=(400, 280))
        screen.blit(text2, rect2)
        if selected == 1:
            draw_heart(screen, 370, 290, 30)
        
        color3 = GOLD if selected == 2 else WHITE
        text3 = font.render(menu_items[2], True, color3)
        rect3 = text3.get_rect(center=(cx, 345))
        screen.blit(text3, rect3)
        if selected == 2:
            draw_heart(screen, rect3.left - 40, 355, 30)
        
        screen.blit(blob_img, (cx - 85, 390))
        
        footer = small_font.render(footer_text, True, WHITE)
        fr = footer.get_rect(center=(cx, HEIGHT - 15))
        screen.blit(footer, fr)
    
    elif state == STATE_OPTIONS:
        title = big_font.render("НАСТРОЙКИ", True, WHITE)
        title_rect = title.get_rect(center=(cx, 60))
        screen.blit(title, title_rect)
        
        start_y = 140
        spacing = 50
        
        for i in range(len(option_items)):
            if i == 0:
                val = "ВКЛ" if fullscreen else "ВЫКЛ"
            elif i == 1:
                val = "ВКЛ" if sound_enabled else "ВЫКЛ"
            elif i == 2:
                val = "ВКЛ" if music_enabled else "ВЫКЛ"
            elif i == 3:
                val = "ВКЛ" if show_fps else "ВЫКЛ"
            else:
                val = None
            
            label = f"{option_items[i]}: {val}" if val else option_items[i]
            color = GOLD if i == option_selected else WHITE
            text = font.render(label, True, color)
            ty = start_y + i * spacing
            tr = text.get_rect(center=(cx, ty))
            screen.blit(text, tr)
            
            if i == option_selected:
                draw_heart(screen, tr.left - 40, ty + 10, 30)
        
        hint = small_font.render("Стрелки - выбор, Z/ENTER - изменить, X/ESC - назад", True, WHITE)
        hr = hint.get_rect(center=(cx, HEIGHT - 30))
        screen.blit(hint, hr)
    
    elif state == STATE_HISTORY:
        elapsed = (pygame.time.get_ticks() - history_start_ms) / 1000.0
        
        if elapsed < 3.0:
            pass
        elif elapsed < 21.0:
            if not history_music_started:
                stop_all_sounds()
                if music_enabled:
                    play_music('undertale-history.mp3', loops=0)
                history_music_started = True
            
            local = elapsed - 3.0
            segment = int(local // 3)
            if segment % 2 == 0:
                screen.blit(history_img, history_rect)
        elif elapsed < 28.0:
            if not bells_started:
                stop_all_sounds()
                if music_enabled:
                    play_music('undertale-bells.mp3', loops=0)
                bells_started = True
        else:
            stop_all_sounds()
            state = STATE_SANS
            sans_start_ms = pygame.time.get_ticks()
            sans_alpha = 0
            sans_box_visible = False
            sans_line_index = 0
            sans_typed = 0
            sans_typing_done = False
            sans_last_char_ms = 0
    
    elif state == STATE_SANS:
        sans_elapsed = (pygame.time.get_ticks() - sans_start_ms) / 1000.0
        
        if sans_alpha < 255:
            sans_alpha += 5
            if sans_alpha > 255:
                sans_alpha = 255
        
        if sans_elapsed >= 3.0 and not sans_box_visible:
            sans_box_visible = True
            sans_last_char_ms = pygame.time.get_ticks()
        
        if sans_box_visible and not sans_typing_done and sans_line_index < len(SANS_LINES):
            now = pygame.time.get_ticks()
            line_text = SANS_LINES[sans_line_index][0]
            char_time_ms = SANS_LINES[sans_line_index][1] * 1000
            if now - sans_last_char_ms >= char_time_ms:
                if sans_typed < len(line_text):
                    sans_typed += 1
                    sans_last_char_ms = now
                    if sans_dialog_sound and sound_enabled:
                        sans_dialog_sound.play()
                else:
                    sans_typing_done = True
        
        sans_copy = sans_img.copy()
        sans_copy.set_alpha(sans_alpha)
        screen.blit(sans_copy, sans_rect)
        
        if sans_box_visible and sans_line_index < len(SANS_LINES):
            screen.blit(dialog_box, dialog_rect)
            line_text = SANS_LINES[sans_line_index][0]
            color = SANS_LINES[sans_line_index][2]
            visible_text = line_text[:sans_typed]
            text_surface = sans_font.render(visible_text, True, color)
            screen.blit(text_surface, (dialog_rect.left + 30, dialog_rect.top + 45))
    
    if show_fps:
        fps_text = small_font.render(f"FPS: {int(clock.get_fps())}", True, GOLD)
        screen.blit(fps_text, (WIDTH - 100, 10))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
