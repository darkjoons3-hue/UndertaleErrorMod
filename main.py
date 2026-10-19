import pygame
import sys
import os
import json

pygame.init()
pygame.mixer.init()

# ==== ФУНКЦИЯ ДЛЯ ПОИСКА ФАЙЛОВ В EXE ====
def resource_path(relative_path):
    """Ищет файлы внутри .exe и в обычной папке"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

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
ORANGE = (255, 130, 0)
BLUE = (60, 60, 255)
PURPLE = (150, 0, 200)

sound_enabled = True
music_enabled = True

# ===================== СОХРАНЕНИЕ =====================
APPDATA = os.getenv('APPDATA') or os.path.expanduser('~')
SAVE_DIR = os.path.join(APPDATA, 'UndertaleErrorMod')
SAVE_FILE = os.path.join(SAVE_DIR, 'save.json')

def load_save():
    try:
        with open(SAVE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"deaths": 0}

def write_save(data):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    except:
        pass

def reset_save():
    try:
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
    except:
        pass

SAVE = load_save()

# ===================== ПУТИ =====================
if getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(sys.executable)
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))

RESET_FLAG = os.path.join(app_dir, "reset.flag")
if os.path.exists(RESET_FLAG):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, "ты не сможешь сбросит игру)", "UndertaleErrorMod", 0x40)
    except:
        pass
    try:
        os.remove(RESET_FLAG)
    except:
        pass

# ===================== ЗАГРУЗКА =====================
def load_image(path, size=None):
    try:
        img = pygame.image.load(resource_path(path))
        if size:
            img = pygame.transform.scale(img, size)
        return img
    except:
        s = pygame.Surface(size if size else (100, 100))
        s.fill(RED)
        return s

logo = load_image('logo.png', (400, 200))
history_img = load_image('history.png', (500, 370))
sans_img = load_image('sans-error.png', (320, 320))

try:
    textures = pygame.image.load(resource_path('textures.png'))
    columns_img = textures.subsurface(pygame.Rect(240, 390, 160, 140))
    blob_img = textures.subsurface(pygame.Rect(400, 350, 170, 70))
except:
    columns_img = pygame.Surface((160, 140)); columns_img.fill(RED)
    blob_img = pygame.Surface((170, 70)); blob_img.fill(RED)

try:
    dialogs_sheet = pygame.image.load(resource_path('undertale-dialogs.png'))
    dialog_box_small = dialogs_sheet.subsurface(pygame.Rect(15, 15, 105, 75))
    dialog_box = pygame.transform.scale(dialog_box_small, (580, 130))
    dialog_box_battle = pygame.transform.scale(dialog_box_small, (600, 130))
except:
    dialog_box = pygame.Surface((580, 130)); dialog_box.fill(BLACK)
    pygame.draw.rect(dialog_box, WHITE, (0, 0, 580, 130), 3)
    dialog_box_battle = pygame.Surface((600, 130)); dialog_box_battle.fill(BLACK)
    pygame.draw.rect(dialog_box_battle, WHITE, (0, 0, 600, 130), 3)

# --- Сердечки ---
HEART_SIZE = 28
HEART_COORDS = {
    "red":    (10,  20, 30, 30),
    "blue":   (10, 220, 30, 30),
    "green":  (10, 400, 30, 30),
    "purple": (10, 490, 30, 30),
    "yellow": (10, 570, 30, 30),
    "orange": (10, 720, 30, 30),
}
HEART_IMAGES = {}
try:
    hs = pygame.image.load(resource_path('hearts.png'))
    for n, r in HEART_COORDS.items():
        try:
            p = hs.subsurface(pygame.Rect(r))
            HEART_IMAGES[n] = pygame.transform.scale(p, (HEART_SIZE, HEART_SIZE))
        except: pass
except: pass
current_heart = "red"

# --- Кнопки ---
BUTTON_W = 140; BUTTON_H = 42
BUTTON_COORDS = {
    "FIGHT": (0,  55, 145, 40),
    "ACT":   (0,   0, 145, 40),
    "ITEM":  (0, 110, 145, 40),
    "MERCY": (0, 165, 145, 40),
}
BUTTON_NAMES = ["FIGHT", "ACT", "ITEM", "MERCY"]
BUTTON_IMAGES = {}
try:
    bs = pygame.image.load(resource_path('battle-buttons.png'))
    for n, r in BUTTON_COORDS.items():
        try:
            p = bs.subsurface(pygame.Rect(r))
            BUTTON_IMAGES[n] = pygame.transform.scale(p, (BUTTON_W, BUTTON_H))
        except: pass
except: pass

# --- Кости и бластеры ---
BONE_IMG = None
BLASTER_FRAMES = []
try:
    sb = pygame.image.load(resource_path('sans-battle.png'))
    try:
        BONE_IMG = sb.subsurface(pygame.Rect(270, 310, 25, 400))
    except: pass
    for i in range(6):
        try:
            f = sb.subsurface(pygame.Rect(i * 103, 935, 100, 65))
            f = pygame.transform.scale(f, (120, 80))
            BLASTER_FRAMES.append(f)
        except: pass
except Exception as e:
    print(f"Ошибка sans-battle.png: {e}")

# ===================== ПОЗИЦИИ =====================
cx = WIDTH // 2
cy = HEIGHT // 2
logo_rect = logo.get_rect(center=(cx, cy - 60))
history_rect = history_img.get_rect(center=(cx, cy))
sans_rect = sans_img.get_rect(center=(cx, 190))
dialog_rect = dialog_box.get_rect(center=(cx, 400))
battle_dialog_rect = dialog_box_battle.get_rect(center=(cx, 390))

# ===================== ШРИФТЫ =====================
try:
    fp = resource_path('determinationmonorusbylyajk.otf')
    font = pygame.font.Font(fp, 26)
    small_font = pygame.font.Font(fp, 16)
    big_font = pygame.font.Font(fp, 36)
    battle_font = pygame.font.Font(fp, 22)
except:
    font = pygame.font.Font(None, 32); small_font = pygame.font.Font(None, 22)
    big_font = pygame.font.Font(None, 40); battle_font = pygame.font.Font(None, 26)
try:
    sans_font = pygame.font.Font(resource_path('ComicSans.ttf'), 22)
except:
    sans_font = pygame.font.Font(None, 24)

# ===================== ЗВУКИ =====================
def load_sound(path):
    try: return pygame.mixer.Sound(resource_path(path))
    except: return None

snd_logo = load_sound('logo_sound.mp3')
snd_logo2 = load_sound('logo_sound2.mp3')
snd_select = load_sound('undertale-select-sound.mp3')
snd_sans = load_sound('sans-dialogs.mp3')
snd_encounter = load_sound('enemy-encounter-undertale.mp3')
snd_bone = load_sound('bone-undertale-sound-effect.mp3')
snd_ding = load_sound('undertale-ding.mp3')
snd_blaster = load_sound('gaster_blaster_sound_effect_1.mp3')
snd_damage = load_sound('undertale-damage-taken.mp3')
snd_shatter = load_sound('undertale-soul-shatter.mp3')

def play_select():
    if snd_select and sound_enabled: snd_select.play()

def play_sound(s):
    if s and sound_enabled: s.play()

def play_music(path, loops=-1):
    try:
        pygame.mixer.music.load(resource_path(path)); pygame.mixer.music.play(loops); return True
    except: return False

def stop_music():
    try: pygame.mixer.music.stop()
    except: pass

def stop_all_sounds():
    try: pygame.mixer.music.stop()
    except: pass
    try: pygame.mixer.stop()
    except: pass

# ===================== СОСТОЯНИЯ =====================
STATE_LOGO = 0
STATE_MENU = 1
STATE_OPTIONS = 2
STATE_HISTORY = 3
STATE_SANS = 4
STATE_BATTLE = 5
STATE_GAMEOVER = 6
state = STATE_LOGO

# ===================== ПЕРЕМЕННЫЕ =====================
alpha = 0; fade_in = True; errmod_alpha = 0
show_press = False; press_timer = 0
snd_logo_played = False; snd_logo2_played = False; menu_music_started = False

menu_items = ["ПРОДОЛЖИТЬ", "ИСТИННЫЙ СБРОС", "ОПЦИИ"]
selected = 0; last_top = 0

option_items = ["Полный экран", "Звуки", "Музыка", "Показать FPS", "Сбросить сохранение", "Сбросить настройки", "Назад"]
option_selected = 0

player_name = "CHARA"
player_lv = "LV 19"
player_time = "666:66"
status_text = "КОНЕЦ"
footer_text = "undertaleErrorMod:Darkjoons, Smile103 year 2026"

history_start_ms = 0; history_music_started = False; bells_started = False

# Диалоги Санса
SANS_LINES = [
    ("Вижу в тебе много зла", 0.06, WHITE),
    ("Чувак тебе надо расслабится, ведь тебе сейчас предстоит выжить в вечных муках", 0.02, WHITE),
    ("ДОБРО ПОЖАЛОВАТЬ В АД", 0.15, RED),
]
SANS_ALT = [("А я уже жду тебя тут", 0.05, WHITE)]

sans_start_ms = 0; sans_alpha = 0; sans_box_visible = False
sans_line_index = 0; sans_typed = 0; sans_typing_done = False; sans_last_char_ms = 0
sans_use_alt = False

# ===================== БОЙ =====================
BATTLE_BOX = pygame.Rect(80, 60, 480, 160)
BATTLE_BOX_WIDE = pygame.Rect(20, 90, 600, 100)
BUTTON_GAP = 13; BUTTON_Y = 260
BUTTONS = [pygame.Rect(20 + i * (BUTTON_W + BUTTON_GAP), BUTTON_Y, BUTTON_W, BUTTON_H) for i in range(4)]

# Фазы атаки
PHASE_INTRO = 0
PHASE_TRANSFORM = 1
PHASE_JUMP = 2
PHASE_WALL_RIGHT = 3
PHASE_WALL_LEFT = 4
PHASE_BLASTERS = 5
PHASE_BLUE_BONES = 6
PHASE_DIALOG = 7
PHASE_READY = 8

# Игрок
player_hp = 92
player_max_hp = 92
player_kr = 0
player_max_kr = 40
kr_timer = 0

# Сердце
heart_x = 320; heart_y = 130
heart_vx = 0; heart_vy = 0
heart_gravity = 60
heart_jump_power = 200
heart_extra_jump = 250
heart_grounded = False
heart_prev_x = 320; heart_prev_y = 130
heart_moving = False
invulnerable_until = 0

# Бой
battle_start_ms = 0; battle_alpha = 0
attack_phase = PHASE_INTRO
phase_start_ms = 0
buttons_unlocked = False
selected_btn = 0
heart_mode = "box"
battle_dialog_visible = False
battle_dialog_text = ""
gameover_start_ms = 0

# Кости (список словарей)
bones = []  # {"rect": Rect, "type": "white"/"blue"/"orange", "vx": , "vy": }
blasters = []  # {"x", "y", "angle", "frame", "timer", "fired", "target_x", "target_y"}

def reset_battle():
    global player_hp, player_kr, kr_timer, heart_x, heart_y, heart_vx, heart_vy
    global heart_grounded, heart_mode, attack_phase, phase_start_ms, bones, blasters
    global buttons_unlocked, selected_btn, battle_dialog_visible, battle_dialog_text
    global current_heart, battle_start_ms, battle_alpha, invulnerable_until
    player_hp = player_max_hp
    player_kr = 0
    kr_timer = 0
    heart_x = BATTLE_BOX.centerx
    heart_y = BATTLE_BOX.centery
    heart_vx = 0; heart_vy = 0
    heart_grounded = False
    heart_mode = "box"
    attack_phase = PHASE_INTRO
    phase_start_ms = pygame.time.get_ticks()
    bones = []; blasters = []
    buttons_unlocked = False
    selected_btn = 0
    battle_dialog_visible = False
    battle_dialog_text = ""
    current_heart = "red"
    battle_start_ms = pygame.time.get_ticks()
    battle_alpha = 0
    invulnerable_until = 0

def take_damage():
    global player_hp, player_kr
    player_hp -= 1
    player_kr = min(player_max_kr, player_kr + 3)

def draw_heart(surf, x, y, size, color=RED):
    img = HEART_IMAGES.get(current_heart)
    if img:
        surf.blit(img, img.get_rect(center=(int(x), int(y))))
    else:
        r = size // 4
        pygame.draw.circle(surf, color, (int(x - r), int(y - r)), r)
        pygame.draw.circle(surf, color, (int(x + r), int(y - r)), r)
        pygame.draw.polygon(surf, color, [(x - 2*r, y - r), (x + 2*r, y - r), (x, y + r*2)])

def draw_hp_bar():
    x0 = 30; y0 = 225; w = 140; h = 16
    pygame.draw.rect(screen, WHITE, (x0, y0, w, h), 2)
    hp_w = int(w * player_hp / player_max_hp)
    pygame.draw.rect(screen, YELLOW, (x0 + 2, y0 + 2, max(0, hp_w - 4), h - 4))
    if player_kr > 0:
        kr_w = int(w * player_kr / player_max_hp)
        kr_start = x0 + 2 + max(0, hp_w - 4)
        pygame.draw.rect(screen, PURPLE, (kr_start, y0 + 2, kr_w, h - 4))
    txt = battle_font.render(f"{player_hp}/{player_max_hp}", True, WHITE)
    screen.blit(txt, (x0 + w + 10, y0 - 2))

def option_action():
    global option_selected, state, sound_enabled, music_enabled, show_fps, fullscreen, screen
    if option_selected == 0:
        fullscreen = not fullscreen
        if fullscreen: screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else: screen = pygame.display.set_mode((WIDTH, HEIGHT))
    elif option_selected == 1: sound_enabled = not sound_enabled
    elif option_selected == 2:
        music_enabled = not music_enabled
        if not music_enabled: stop_music()
        else: play_music('determination.mp3')
    elif option_selected == 3: show_fps = not show_fps
    elif option_selected == 4:
        reset_save()
        SAVE["deaths"] = 0
    elif option_selected == 5:
        fullscreen = False; sound_enabled = True; music_enabled = True; show_fps = False
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        play_music('determination.mp3')
    elif option_selected == 6:
        state = STATE_MENU

clock = pygame.time.Clock()
running = True

# ===================== ГЛАВНЫЙ ЦИКЛ =====================
while running:
    now = pygame.time.get_ticks()
    dt = min(clock.get_time() / 1000.0, 0.05)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ---- ЛОГОТИП ----
            if state == STATE_LOGO:
                if (event.key in (pygame.K_z, pygame.K_RETURN)) and show_press:
                    play_select()
                    if SAVE.get("deaths", 0) > 0:
                        sans_use_alt = True
                        stop_all_sounds()
                        state = STATE_SANS
                        sans_start_ms = now; sans_alpha = 0
                        sans_box_visible = False; sans_line_index = 0
                        sans_typed = 0; sans_typing_done = False
                        sans_last_char_ms = 0
                        play_sound(snd_encounter)
                    else:
                        sans_use_alt = False
                        state = STATE_MENU

            # ---- МЕНЮ ----
            elif state == STATE_MENU:
                if event.key == pygame.K_LEFT:
                    if selected == 1: selected = 0; last_top = 0
                    elif selected == 2: selected = last_top
                if event.key == pygame.K_RIGHT:
                    if selected == 0: selected = 1; last_top = 1
                    elif selected == 2: selected = last_top
                if event.key == pygame.K_UP:
                    if selected == 2: selected = last_top
                if event.key == pygame.K_DOWN:
                    if selected in (0, 1): selected = 2
                if event.key in (pygame.K_z, pygame.K_RETURN):
                    play_select()
                    if selected == 0:
                        stop_all_sounds()
                        state = STATE_HISTORY
                        history_start_ms = now; history_music_started = False; bells_started = False
                        sans_use_alt = False
                    elif selected == 1:
                        try:
                            with open(RESET_FLAG, 'w') as f: f.write("reset")
                        except: pass
                        running = False
                    elif selected == 2:
                        state = STATE_OPTIONS; option_selected = 0
                if event.key in (pygame.K_x, pygame.K_ESCAPE):
                    running = False

            # ---- НАСТРОЙКИ ----
            elif state == STATE_OPTIONS:
                if event.key == pygame.K_UP:
                    option_selected = (option_selected - 1) % len(option_items)
                if event.key == pygame.K_DOWN:
                    option_selected = (option_selected + 1) % len(option_items)
                if event.key in (pygame.K_z, pygame.K_RETURN):
                    play_select(); option_action()
                if event.key in (pygame.K_x, pygame.K_ESCAPE):
                    play_select(); state = STATE_MENU

            # ---- САНС ----
            elif state == STATE_SANS:
                if sans_typing_done and (event.key in (pygame.K_z, pygame.K_RETURN)):
                    sans_line_index += 1
                    total = len(SANS_ALT) if sans_use_alt else len(SANS_LINES)
                    if sans_line_index >= total:
                        reset_battle()
                        state = STATE_BATTLE
                    else:
                        sans_typed = 0; sans_typing_done = False
                        sans_last_char_ms = now

            # ---- БОЙ ----
            elif state == STATE_BATTLE:
                if event.key in (pygame.K_z, pygame.K_RETURN):
                    if heart_mode == "buttons" and buttons_unlocked and not battle_dialog_visible:
                        battle_dialog_visible = True
                        battle_dialog_text = f"Вы выбрали: {BUTTON_NAMES[selected_btn]}"
                        play_select()
                if attack_phase == PHASE_READY:
                    if heart_mode == "box" and event.key == pygame.K_UP:
                        if heart_y <= BATTLE_BOX.top + 20:
                            heart_mode = "buttons"
                    if heart_mode == "buttons" and event.key == pygame.K_DOWN:
                        heart_mode = "box"; heart_y = BATTLE_BOX.top + 20
                        battle_dialog_visible = False

            # ---- GAME OVER ----
            elif state == STATE_GAMEOVER:
                pass

    # ===================== ОТРИСОВКА =====================
    screen.fill(BLACK)

    # ---- ЛОГОТИП ----
    if state == STATE_LOGO:
        if not snd_logo_played:
            play_sound(snd_logo); snd_logo_played = True
        if fade_in:
            alpha += 3
            if alpha >= 255: alpha = 255; fade_in = False
        elif errmod_alpha < 255:
            errmod_alpha += 5
            if errmod_alpha >= 255:
                errmod_alpha = 255
                if not snd_logo2_played:
                    try: pygame.mixer.stop()
                    except: pass
                    play_sound(snd_logo2); snd_logo2_played = True
        else:
            press_timer += 1
            if press_timer >= 30: press_timer = 0
            show_press = press_timer < 15
        lc = logo.copy(); lc.set_alpha(alpha)
        screen.blit(lc, logo_rect)
        if errmod_alpha > 0:
            et = big_font.render("Error Mod", True, RED)
            ec = et.copy(); ec.set_alpha(errmod_alpha)
            screen.blit(ec, ec.get_rect(center=(cx, cy + 80)))
        if errmod_alpha >= 255 and show_press:
            t = font.render("Нажмите Z или ENTER", True, WHITE)
            screen.blit(t, t.get_rect(center=(cx, HEIGHT - 60)))

    # ---- МЕНЮ ----
    elif state == STATE_MENU:
        if not menu_music_started:
            if music_enabled: play_music('determination.mp3')
            menu_music_started = True
        screen.blit(big_font.render("X", True, WHITE), (20, 20))
        screen.blit(columns_img, (cx - 80, 20))
        screen.blit(font.render(player_name, True, WHITE), (150, 170))
        screen.blit(font.render(player_lv, True, WHITE), (300, 170))
        screen.blit(font.render(player_time, True, WHITE), (470, 170))
        screen.blit(font.render(status_text, True, WHITE), (150, 210))
        c1 = GOLD if selected == 0 else WHITE
        t1 = font.render(menu_items[0], True, c1); r1 = t1.get_rect(topleft=(130, 280))
        screen.blit(t1, r1)
        if selected == 0: draw_heart(screen, 100, 290, 30)
        c2 = GOLD if selected == 1 else WHITE
        t2 = font.render(menu_items[1], True, c2); r2 = t2.get_rect(topleft=(400, 280))
        screen.blit(t2, r2)
        if selected == 1: draw_heart(screen, 370, 290, 30)
        c3 = GOLD if selected == 2 else WHITE
        t3 = font.render(menu_items[2], True, c3); r3 = t3.get_rect(center=(cx, 345))
        screen.blit(t3, r3)
        if selected == 2: draw_heart(screen, r3.left - 40, 355, 30)
        screen.blit(blob_img, (cx - 85, 390))
        f = small_font.render(footer_text, True, WHITE)
        screen.blit(f, f.get_rect(center=(cx, HEIGHT - 15)))

    # ---- НАСТРОЙКИ ----
    elif state == STATE_OPTIONS:
        screen.blit(big_font.render("НАСТРОЙКИ", True, WHITE), big_font.render("НАСТРОЙКИ", True, WHITE).get_rect(center=(cx, 50)))
        start_y = 120; spacing = 42
        for i in range(len(option_items)):
            if i == 0: val = "ВКЛ" if fullscreen else "ВЫКЛ"
            elif i == 1: val = "ВКЛ" if sound_enabled else "ВЫКЛ"
            elif i == 2: val = "ВКЛ" if music_enabled else "ВЫКЛ"
            elif i == 3: val = "ВКЛ" if show_fps else "ВЫКЛ"
            else: val = None
            label = f"{option_items[i]}: {val}" if val else option_items[i]
            col = GOLD if i == option_selected else WHITE
            t = font.render(label, True, col)
            ty = start_y + i * spacing
            tr = t.get_rect(center=(cx, ty))
            screen.blit(t, tr)
            if i == option_selected: draw_heart(screen, tr.left - 40, ty + 10, 26)
        h = small_font.render("Стрелки - выбор, Z/ENTER - изменить, X/ESC - назад", True, WHITE)
        screen.blit(h, h.get_rect(center=(cx, HEIGHT - 25)))

    # ---- ИСТОРИЯ ----
    elif state == STATE_HISTORY:
        el = (now - history_start_ms) / 1000.0
        if el < 3.0: pass
        elif el < 21.0:
            if not history_music_started:
                stop_all_sounds()
                if music_enabled: play_music('undertale-history.mp3', loops=0)
                history_music_started = True
            loc = el - 3.0
            seg = int(loc // 3)
            if seg % 2 == 0: screen.blit(history_img, history_rect)
        elif el < 28.0:
            if not bells_started:
                stop_all_sounds()
                if music_enabled: play_music('undertale-bells.mp3', loops=0)
                bells_started = True
        else:
            stop_all_sounds()
            state = STATE_SANS
            sans_start_ms = now; sans_alpha = 0
            sans_box_visible = False; sans_line_index = 0
            sans_typed = 0; sans_typing_done = False
            sans_last_char_ms = 0
            play_sound(snd_encounter)

    # ---- САНС ----
    elif state == STATE_SANS:
        el = (now - sans_start_ms) / 1000.0
        if sans_alpha < 255:
            sans_alpha += 5
            if sans_alpha > 255: sans_alpha = 255
        if el >= 3.0 and not sans_box_visible:
            sans_box_visible = True
            sans_last_char_ms = now
        lines = SANS_ALT if sans_use_alt else SANS_LINES
        if sans_box_visible and not sans_typing_done and sans_line_index < len(lines):
            lt, spd, _ = lines[sans_line_index]
            if now - sans_last_char_ms >= spd * 1000:
                if sans_typed < len(lt):
                    sans_typed += 1
                    sans_last_char_ms = now
                    play_sound(snd_sans)
                else:
                    sans_typing_done = True
        sc = sans_img.copy(); sc.set_alpha(sans_alpha)
        screen.blit(sc, sans_rect)
        if sans_box_visible and sans_line_index < len(lines):
            screen.blit(dialog_box, dialog_rect)
            lt, _, col = lines[sans_line_index]
            txt = sans_font.render(lt[:sans_typed], True, col)
            screen.blit(txt, (dialog_rect.left + 30, dialog_rect.top + 45))

    # ---- БОЙ ----
    elif state == STATE_BATTLE:
        if player_kr > 0:
            kr_timer += 1
            if player_kr >= 40: interval = 1
            elif player_kr >= 30: interval = 2
            elif player_kr >= 20: interval = 5
            elif player_kr >= 10: interval = 15
            else: interval = 30
            if kr_timer >= interval:
                kr_timer = 0
                player_kr -= 1
                player_hp -= 1

        if player_hp <= 0 and state != STATE_GAMEOVER:
            play_sound(snd_shatter)
            stop_all_sounds()
            SAVE["deaths"] = SAVE.get("deaths", 0) + 1
            write_save(SAVE)
            state = STATE_GAMEOVER
            gameover_start_ms = now
        else:
            el_phase = (now - phase_start_ms) / 1000.0

            # === Фаза 0: Вступление ===
            if attack_phase == PHASE_INTRO:
                if el_phase >= 1.0:
                    attack_phase = PHASE_TRANSFORM; phase_start_ms = now
                    current_heart = "blue"
                    play_sound(snd_ding)

            # === Фаза 1: Превращение + падение ===
            elif attack_phase == PHASE_TRANSFORM:
                heart_vy += heart_gravity * dt
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and heart_grounded:
                    heart_vy = -heart_jump_power
                    heart_grounded = False
                elif keys[pygame.K_UP] and heart_vy < 0:
                    heart_vy -= heart_extra_jump * dt
                heart_y += heart_vy * dt
                if heart_y >= BATTLE_BOX.bottom - 20:
                    heart_y = BATTLE_BOX.bottom - 20
                    heart_vy = 0; heart_grounded = True
                if heart_y <= BATTLE_BOX.top + 12:
                    heart_y = BATTLE_BOX.top + 12
                    if heart_vy < 0: heart_vy = 0
                if el_phase >= 1.5:
                    attack_phase = PHASE_JUMP; phase_start_ms = now
                    bones.clear()
                    for i in range(3):
                        b = pygame.Rect(BATTLE_BOX.left + 60 + i * 150, BATTLE_BOX.bottom + 30, 20, 400)
                        bones.append({"rect": b, "type": "white", "vx": 0, "vy": -120})
                    play_sound(snd_bone)

            # === Фаза 2: Прыжки через кости (3 сек) ===
            elif attack_phase == PHASE_JUMP:
                heart_vy += heart_gravity * dt
                keys = pygame.key.get_pressed()
                if keys[pygame.K_UP] and heart_grounded:
                    heart_vy = -heart_jump_power
                    heart_grounded = False
                elif keys[pygame.K_UP] and heart_vy < 0:
                    heart_vy -= heart_extra_jump * dt
                heart_y += heart_vy * dt
                if heart_y >= BATTLE_BOX.bottom - 20:
                    heart_y = BATTLE_BOX.bottom - 20
                    heart_vy = 0; heart_grounded = True
                if heart_y <= BATTLE_BOX.top + 12:
                    heart_y = BATTLE_BOX.top + 12
                    if heart_vy < 0: heart_vy = 0
                for b in bones:
                    b["rect"].y += b["vy"] * dt
                hh = pygame.Rect(heart_x - 8, heart_y - 8, 16, 16)
                inv = now < invulnerable_until
                for b in bones:
                    if hh.colliderect(b["rect"]) and not inv:
                        take_damage()
                        play_sound(snd_damage)
                        invulnerable_until = now + 300
                        break
                if el_phase >= 3.0:
                    bones.clear()
                    attack_phase = PHASE_WALL_RIGHT; phase_start_ms = now
                    for i in range(4):
                        b = pygame.Rect(BATTLE_BOX_WIDE.left - 100 - i * 200, BATTLE_BOX_WIDE.top + 5, 180, 40)
                        bones.append({"rect": b, "type": "white", "vx": 300, "vy": 0})
                    play_sound(snd_bone)
                    heart_x = BATTLE_BOX_WIDE.centerx
                    heart_y = BATTLE_BOX_WIDE.centery

            # === Фаза 3: Стена костей вправо ===
            elif attack_phase == PHASE_WALL_RIGHT:
                heart_x += 180 * dt
                heart_x = min(heart_x, BATTLE_BOX_WIDE.right - 15)
                for b in bones:
                    b["rect"].x += b["vx"] * dt
                hh = pygame.Rect(heart_x - 8, heart_y - 8, 16, 16)
                inv = now < invulnerable_until
                for b in bones:
                    if hh.colliderect(b["rect"]) and not inv:
                        take_damage(); play_sound(snd_damage)
                        invulnerable_until = now + 300
                        break
                if el_phase >= 3.0:
                    bones.clear()
                    attack_phase = PHASE_WALL_LEFT; phase_start_ms = now
                    for i in range(4):
                        b = pygame.Rect(BATTLE_BOX_WIDE.right + i * 200, BATTLE_BOX_WIDE.top + 5, 180, 40)
                        bones.append({"rect": b, "type": "white", "vx": -300, "vy": 0})
                    play_sound(snd_bone)
                    heart_x = BATTLE_BOX_WIDE.centerx

            # === Фаза 4: Стена костей влево ===
            elif attack_phase == PHASE_WALL_LEFT:
                heart_x -= 180 * dt
                heart_x = max(heart_x, BATTLE_BOX_WIDE.left + 15)
                for b in bones:
                    b["rect"].x += b["vx"] * dt
                hh = pygame.Rect(heart_x - 8, heart_y - 8, 16, 16)
                inv = now < invulnerable_until
                for b in bones:
                    if hh.colliderect(b["rect"]) and not inv:
                        take_damage(); play_sound(snd_damage)
                        invulnerable_until = now + 300
                        break
                if el_phase >= 3.0:
                    bones.clear(); blasters.clear()
                    attack_phase = PHASE_BLASTERS; phase_start_ms = now
                    current_heart = "red"
                    heart_x = BATTLE_BOX.centerx; heart_y = BATTLE_BOX.centery
                    play_sound(snd_ding)
                    blasters.append({"x": BATTLE_BOX.left + 60, "y": BATTLE_BOX.top - 60, "frame": 0, "timer": 0, "fired": False, "vx": 0, "vy": 200})
                    blasters.append({"x": BATTLE_BOX.right - 60, "y": BATTLE_BOX.top - 60, "frame": 0, "timer": 0, "fired": False, "vx": 0, "vy": 200})
                    play_sound(snd_blaster)

            # === Фаза 5: Гастер-бластеры ===
            elif attack_phase == PHASE_BLASTERS:
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_LEFT]: dx -= 1
                if keys[pygame.K_RIGHT]: dx += 1
                if keys[pygame.K_UP]: dy -= 1
                if keys[pygame.K_DOWN]: dy += 1
                if dx and dy:
                    l = (dx*dx+dy*dy) ** 0.5
                    dx /= l; dy /= l
                heart_x += dx * 180 * dt
                heart_y += dy * 180 * dt
                heart_x = max(BATTLE_BOX.left + 12, min(BATTLE_BOX.right - 12, heart_x))
                heart_y = max(BATTLE_BOX.top + 12, min(BATTLE_BOX.bottom - 12, heart_y))
                hh = pygame.Rect(heart_x - 8, heart_y - 8, 16, 16)
                inv = now < invulnerable_until
                for bl in blasters:
                    bl["timer"] += 1
                    if bl["frame"] < 5 and bl["timer"] % 4 == 0:
                        bl["frame"] += 1
                    if bl["frame"] >= 5 and not bl["fired"]:
                        bl["fired"] = True
                        play_sound(snd_blaster)
                for bl in blasters:
                    if bl["fired"]:
                        laser_rect = pygame.Rect(bl["x"] - 15, bl["y"], 30, BATTLE_BOX.height + 100)
                        if hh.colliderect(laser_rect) and not inv:
                            take_damage(); play_sound(snd_damage)
                            invulnerable_until = now + 300
                            break
                if el_phase >= 4.5:
                    blasters.clear()
                    attack_phase = PHASE_BLUE_BONES; phase_start_ms = now
                    bones.append({"rect": pygame.Rect(BATTLE_BOX.left - 200, heart_y - 15, 200, 30), "type": "blue", "vx": 250, "vy": 0})
                    bones.append({"rect": pygame.Rect(BATTLE_BOX.right, heart_y - 15, 200, 30), "type": "blue", "vx": -250, "vy": 0})
                    play_sound(snd_bone)

            # === Фаза 6: Синие кости ===
            elif attack_phase == PHASE_BLUE_BONES:
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_LEFT]: dx -= 1
                if keys[pygame.K_RIGHT]: dx += 1
                if keys[pygame.K_UP]: dy -= 1
                if keys[pygame.K_DOWN]: dy += 1
                heart_moving = (dx != 0 or dy != 0)
                if dx and dy:
                    l = (dx*dx+dy*dy) ** 0.5
                    dx /= l; dy /= l
                heart_x += dx * 180 * dt
                heart_y += dy * 180 * dt
                heart_x = max(BATTLE_BOX.left + 12, min(BATTLE_BOX.right - 12, heart_x))
                heart_y = max(BATTLE_BOX.top + 12, min(BATTLE_BOX.bottom - 12, heart_y))
                for b in bones:
                    b["rect"].x += b["vx"] * dt
                hh = pygame.Rect(heart_x - 8, heart_y - 8, 16, 16)
                inv = now < invulnerable_until
                for b in bones:
                    if hh.colliderect(b["rect"]) and heart_moving and not inv:
                        take_damage(); play_sound(snd_damage)
                        invulnerable_until = now + 300
                        break
                if el_phase >= 3.0:
                    bones.clear()
                    attack_phase = PHASE_DIALOG; phase_start_ms = now
                    battle_dialog_visible = True
                    battle_dialog_text = "ты жив?"
                    sans_typed = 0; sans_typing_done = False
                    sans_last_char_ms = now

            # === Фаза 7: Диалог «ты жив?» ===
            elif attack_phase == PHASE_DIALOG:
                if battle_dialog_visible:
                    if not sans_typing_done:
                        if now - sans_last_char_ms >= 50:
                            if sans_typed < len(battle_dialog_text):
                                sans_typed += 1; sans_last_char_ms = now
                                play_sound(snd_sans)
                            else:
                                sans_typing_done = True
                    else:
                        if pygame.key.get_pressed()[pygame.K_z] or pygame.key.get_pressed()[pygame.K_RETURN]:
                            battle_dialog_visible = False
                            attack_phase = PHASE_READY; phase_start_ms = now
                            buttons_unlocked = True
                            heart_mode = "box"
                            heart_x = BATTLE_BOX.centerx; heart_y = BATTLE_BOX.centery
                            if music_enabled: play_music('megalovania.mp3')

            # === Фаза 8: Кнопки доступны ===
            elif attack_phase == PHASE_READY:
                keys = pygame.key.get_pressed()
                if heart_mode == "box":
                    dx, dy = 0, 0
                    if keys[pygame.K_LEFT]: dx -= 1
                    if keys[pygame.K_RIGHT]: dx += 1
                    if keys[pygame.K_UP]: dy -= 1
                    if keys[pygame.K_DOWN]: dy += 1
                    if dx and dy:
                        l = (dx*dx+dy*dy) ** 0.5
                        dx /= l; dy /= l
                    heart_x += dx * 180 * dt
                    heart_y += dy * 180 * dt
                    heart_x = max(BATTLE_BOX.left + 12, min(BATTLE_BOX.right - 12, heart_x))
                    heart_y = max(BATTLE_BOX.top + 12, min(BATTLE_BOX.bottom - 12, heart_y))
                elif heart_mode == "buttons":
                    if keys[pygame.K_LEFT]: selected_btn = max(0, selected_btn - 1)
                    if keys[pygame.K_RIGHT]: selected_btn = min(len(BUTTONS) - 1, selected_btn + 1)

        # ---- Отрисовка боя ----
        cur_box = BATTLE_BOX_WIDE if attack_phase in (PHASE_WALL_RIGHT, PHASE_WALL_LEFT) else BATTLE_BOX
        pygame.draw.rect(screen, WHITE, cur_box, 3)

        screen.set_clip(cur_box)
        for b in bones:
            col = WHITE if b["type"] == "white" else (BLUE if b["type"] == "blue" else ORANGE)
            if BONE_IMG:
                img = BONE_IMG.copy()
                img = pygame.transform.scale(img, (b["rect"].width, b["rect"].height))
                if b["type"] != "white":
                    tint = pygame.Surface(img.get_size())
                    tint.fill(col)
                    img.blit(tint, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
                screen.blit(img, b["rect"])
            else:
                pygame.draw.rect(screen, col, b["rect"])
        screen.set_clip(None)

        for bl in blasters:
            if BLASTER_FRAMES:
                fi = min(bl["frame"], len(BLASTER_FRAMES) - 1)
                screen.blit(BLASTER_FRAMES[fi], BLASTER_FRAMES[fi].get_rect(center=(bl["x"], bl["y"])))
            else:
                pygame.draw.circle(screen, WHITE, (int(bl["x"]), int(bl["y"])), 25)
            if bl["fired"]:
                pygame.draw.rect(screen, (255, 255, 200), (bl["x"] - 15, bl["y"], 30, BATTLE_BOX.height + 100))

        blink = (now < invulnerable_until) and ((now // 60) % 2 == 0)
        if not blink:
            if heart_mode == "box":
                draw_heart(screen, int(heart_x), int(heart_y), HEART_SIZE)
            else:
                btn = BUTTONS[selected_btn]
                draw_heart(screen, btn.centerx, btn.top - 22, HEART_SIZE)

        for i, br in enumerate(BUTTONS):
            hov = (heart_mode == "buttons" and selected_btn == i and buttons_unlocked)
            img = BUTTON_IMAGES.get(BUTTON_NAMES[i])
            if img:
                screen.blit(img, img.get_rect(center=br.center))
                if hov: pygame.draw.rect(screen, YELLOW, br, 3)
            else:
                col = YELLOW if hov else ORANGE
                pygame.draw.rect(screen, col, br, 3)
                t = battle_font.render(BUTTON_NAMES[i], True, col)
                screen.blit(t, t.get_rect(center=br.center))

        screen.blit(battle_font.render(player_name, True, WHITE), (30, 200))
        screen.blit(battle_font.render(player_lv, True, WHITE), (120, 200))
        draw_hp_bar()

        if battle_dialog_visible:
            screen.blit(dialog_box_battle, battle_dialog_rect)
            if attack_phase == PHASE_DIALOG:
                txt = sans_font.render(battle_dialog_text[:sans_typed], True, WHITE)
            else:
                txt = battle_font.render(battle_dialog_text, True, WHITE)
            screen.blit(txt, (battle_dialog_rect.left + 30, battle_dialog_rect.top + 50))

        if attack_phase == PHASE_READY and heart_mode == "box" and not battle_dialog_visible:
            h = small_font.render("↑ - к кнопкам", True, (150, 150, 150))
            screen.blit(h, (cx - 60, BATTLE_BOX.bottom + 5))

        if battle_alpha < 255:
            battle_alpha += 5
            if battle_alpha > 255: battle_alpha = 255
            ov = pygame.Surface((WIDTH, HEIGHT)); ov.fill(BLACK)
            ov.set_alpha(255 - battle_alpha)
            screen.blit(ov, (0, 0))

    # ---- GAME OVER ----
    elif state == STATE_GAMEOVER:
        el = (now - gameover_start_ms) / 1000.0
        if el >= 2.0:
            reset_battle()
            sans_use_alt = True
            state = STATE_SANS
            sans_start_ms = now; sans_alpha = 0
            sans_box_visible = False; sans_line_index = 0
            sans_typed = 0; sans_typing_done = False
            sans_last_char_ms = 0
            play_sound(snd_encounter)

    if show_fps:
        f = small_font.render(f"FPS: {int(clock.get_fps())}", True, GOLD)
        screen.blit(f, (WIDTH - 100, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
