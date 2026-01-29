import pygame
import math
import sys
import os
import random

# --- BAŞLATMA ---
pygame.init()
pygame.mixer.init()

bilgi = pygame.display.Info()
WIDTH, HEIGHT = bilgi.current_w, bilgi.current_h
HALF_WIDTH, HALF_HEIGHT = WIDTH // 2, HEIGHT // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.event.set_grab(True)
pygame.mouse.set_visible(False)

display_surf = pygame.Surface((WIDTH, HEIGHT))
font = pygame.font.SysFont("Courier", 20, bold=True)

# --- CHAT VE DIYALOG SISTEMI ---
chat_active = False
chat_input = ""
chat_log = [] 
MAX_MESSAGES = 10
com_state = "START" 
door_hint_given = False

# --- SES ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    brown_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "brown.mp3"))
    pygame.mixer.Channel(0).play(brown_sound, -1)
    pygame.mixer.Channel(0).set_volume(0.3)
except:
    pass

# --- OYUN DEĞİŞKENLERİ ---
player_x, player_y = 150, 150
player_angle, player_pitch = 0, 0
TILE = 100
bob_angle, bob_speed, bob_intensity = 0, 0.15, 12

world_map = [
    "1111111111111111",
    "1000000000000001",
    "1011111911111001",
    "1010000000001001",
    "1010000000001001",
    "1011191110001001",
    "1000000000000001",
    "1111111111111111",
]

doors = {(c, r): 0 for r, row in enumerate(world_map) for c, char in enumerate(row) if char == "9"}
door_states = {pos: False for pos in doors}
door_timers = {pos: 0 for pos in doors}

FOV, NUM_RAYS = math.pi / 3, 120
SCALE = WIDTH // NUM_RAYS
clock = pygame.time.Clock()

# ---------------- NOISE AYARLARI ----------------
NOISE_CHANCE = 0.07
NOISE_STRENGTH = 35

def raycasting(surf, current_bob):
    start_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * (FOV / NUM_RAYS)
        sin_a, cos_a = math.sin(angle), math.cos(angle)
        for depth in range(1, 1500, 4):
            x, y = player_x + depth * cos_a, player_y + depth * sin_a
            mx, my = int(x // TILE), int(y // TILE)
            if not (0 <= mx < 16 and 0 <= my < 8): break
            tile = world_map[my][mx]
            if tile in ("1", "9"):
                hit_pos = (y % TILE if abs(cos_a) > abs(sin_a) else x % TILE)
                if tile == "9" and hit_pos <= doors.get((mx, my), 0): continue
                dist = depth * math.cos(player_angle - angle)
                shade = 255 / (1 + dist * dist * 0.00002)
                c_val = max(10, min(160, shade))

                base_color = (c_val, c_val, c_val) if tile == "1" else (c_val*0.7, c_val*0.4, c_val*0.2)

                if random.random() < NOISE_CHANCE:
                    n = random.randint(-NOISE_STRENGTH, NOISE_STRENGTH)
                    base_color = (
                        max(0, min(255, base_color[0] + n)),
                        max(0, min(255, base_color[1] + n)),
                        max(0, min(255, base_color[2] + n))
                    )

                proj_h = (TILE * 500) / (dist + 0.0001)
                pygame.draw.rect(
                    surf,
                    base_color,
                    (ray * SCALE,
                     HALF_HEIGHT - proj_h // 2 + player_pitch + current_bob,
                     SCALE,
                     proj_h)
                )
                break

def apply_distortion():
    for i in range(0, HEIGHT, 4):
        offset = random.randint(-2, 2)
        screen.blit(display_surf, (offset, i), (0, i, WIDTH, 4))

def draw_ui():
    M_TILE = 10
    pygame.draw.rect(screen, (0, 0, 0), (15, 15, 16 * M_TILE + 10, 8 * M_TILE + 10))
    for r, row in enumerate(world_map):
        for c, char in enumerate(row):
            if char == "1":
                pygame.draw.rect(screen, (70, 70, 70), (c * M_TILE + 20, r * M_TILE + 20, M_TILE - 1, M_TILE - 1))
            elif char == "9":
                pygame.draw.rect(screen, (120, 60, 30), (c * M_TILE + 20, r * M_TILE + 20, M_TILE - 1, M_TILE - 1))

    # --- YEŞİL ÜÇGEN ---
    px = (player_x / TILE) * M_TILE + 20
    py = (player_y / TILE) * M_TILE + 20
    ang = player_angle
    size = 6

    p1 = (px + math.cos(ang) * size * 2, py + math.sin(ang) * size * 2)
    p2 = (px + math.cos(ang + 2.5) * size, py + math.sin(ang + 2.5) * size)
    p3 = (px + math.cos(ang - 2.5) * size, py + math.sin(ang - 2.5) * size)

    pygame.draw.polygon(screen, (0, 255, 0), [p1, p2, p3])

    chat_y = HEIGHT - 50
    for i, msg in enumerate(reversed(chat_log)):
        if msg.startswith("Com:"): color = (255, 50, 50)
        elif msg.startswith("Sys:"): color = (255, 255, 0)
        else: color = (0, 255, 0)
        msg_surf = font.render(msg, True, color)
        screen.blit(msg_surf, (20, chat_y - 30 - (i * 25)))
    
    input_prefix = "> " if chat_active else "[T] to chat"
    color = (0, 255, 0) if chat_active else (100, 100, 100)
    input_surf = font.render(input_prefix + chat_input, True, color)
    screen.blit(input_surf, (20, chat_y))

# --- SCREENSHOT KLASÖRÜ ---
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
screenshot_count = 0

# --- ANA DÖNGÜ ---
while True:
    dt_ms = clock.tick(60)
    dt = dt_ms / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit(); sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # 📸 SCREENSHOT — P TUŞU
            if event.key == pygame.K_p:
                filename = f"screenshot_{screenshot_count}.png"
                pygame.image.save(screen, os.path.join(SCREENSHOT_DIR, filename))
                screenshot_count += 1

            if event.key == pygame.K_t and not chat_active:
                chat_active = True
            elif chat_active:
                if event.key == pygame.K_RETURN:
                    user_msg = chat_input.strip().lower()
                    if user_msg:
                        chat_log.append("You: " + chat_input)
                        
                        if com_state == "START":
                            chat_log.append("Com: merhaba beni duyuyor musun?")
                            chat_log.append("Sys: evet için e hayır için h yazınız.")
                            com_state = "ASKING"
                        
                        elif com_state == "ASKING":
                            if user_msg == "e":
                                chat_log.append("Com: bunu duyduguma sevindim.")
                                com_state = "FINISHED"
                            elif user_msg == "h":
                                chat_log.append("Com: peki simdi beni duyabiliyor musun?")
                            else:
                                chat_log.append("Com: (cevap gelmedi...) duyuyor musun?")

                        while len(chat_log) > MAX_MESSAGES: chat_log.pop(0)
                        
                    chat_input = ""
                    chat_active = False
                elif event.key == pygame.K_BACKSPACE:
                    chat_input = chat_input[:-1]
                else:
                    chat_input += event.unicode
            
            if not chat_active and event.key == pygame.K_e:
                cx, cy = player_x + math.cos(player_angle) * 150, player_y + math.sin(player_angle) * 150
                pos = (int(cx // TILE), int(cy // TILE))
                if pos in door_states:
                    door_states[pos] = not door_states[pos]
                    if door_states[pos]: door_timers[pos] = 3000

    # --- HAREKET ---
    current_bob = 0
    if not chat_active:
        keys = pygame.key.get_pressed()
        is_moving, dx, dy = False, 0, 0
        speed = 250 * dt
        cos_a, sin_a = math.cos(player_angle), math.sin(player_angle)

        if keys[pygame.K_w]: dx += cos_a * speed; dy += sin_a * speed; is_moving = True
        if keys[pygame.K_s]: dx -= cos_a * speed; dy -= sin_a * speed; is_moving = True
        if keys[pygame.K_a]: dx += sin_a * speed; dy -= cos_a * speed; is_moving = True
        if keys[pygame.K_d]: dx -= sin_a * speed; dy += cos_a * speed; is_moving = True

        if is_moving:
            bob_angle += bob_speed
            current_bob = math.sin(bob_angle) * bob_intensity
        
        def can_move(nx, ny):
            tx, ty = int(nx // TILE), int(ny // TILE)
            if 0 <= tx < 16 and 0 <= ty < 8:
                if world_map[ty][tx] == '1': return False
                if world_map[ty][tx] == '9' and doors.get((tx, ty), 0) < 80: return False
                return True
            return False
        
        if can_move(player_x + dx * 2.5, player_y): player_x += dx
        if can_move(player_x, player_y + dy * 2.5): player_y += dy

        mouse_rel = pygame.mouse.get_rel()
        player_angle += mouse_rel[0] * 0.002
        player_pitch = max(-350, min(350, player_pitch - mouse_rel[1] * 1.5))

    # --- KAPI ---
    px, py = int(player_x // TILE), int(player_y // TILE)
    for pos in doors:
        dist_to_door = math.sqrt((player_x - (pos[0]*TILE + 50))**2 + (player_y - (pos[1]*TILE + 50))**2)
        if dist_to_door < 150 and not door_hint_given:
            chat_log.append("Sys: kapıyı açmak için [e] ye basınız.")
            door_hint_given = True

        if door_states[pos] and doors[pos] < TILE: doors[pos] += 5
        elif not door_states[pos] and doors[pos] > 0:
            if (px, py) != pos: doors[pos] -= 5
            else: door_timers[pos] = 500 
        if door_states[pos] and doors[pos] >= TILE:
            if (px, py) != pos:
                door_timers[pos] -= dt_ms
                if door_timers[pos] <= 0: door_states[pos] = False

    # --- RENDER ---
    display_surf.fill((0, 0, 0))
    pygame.draw.rect(display_surf, (10, 10, 25), (0, 0, WIDTH, HALF_HEIGHT + player_pitch + current_bob))
    pygame.draw.rect(display_surf, (15, 15, 15), (0, HALF_HEIGHT + player_pitch + current_bob, WIDTH, HEIGHT))
    raycasting(display_surf, current_bob)

    apply_distortion()
    for _ in range(300):
        rx, ry = random.randint(0, WIDTH-1), random.randint(0, HEIGHT-1)
        screen.set_at((rx, ry), (40, 40, 40))
    
    draw_ui()
    pygame.display.flip()
