from machine import Pin, SPI, I2C
import time
import math
import random
import framebuf
import st7789
import vga1_16x32 as font

# =========================
# 初始化
# =========================
spi = SPI(0, baudrate=40_000_000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(19))
tft = st7789.ST7789(spi, 240, 240, reset=Pin(20), dc=Pin(21), cs=Pin(17))
tft.init()
tft.fill(0)

i2c = I2C(1, scl=Pin(15), sda=Pin(14))
MPU = 0x68
i2c.writeto_mem(MPU, 0x6B, b'\x00')

def read_word(reg):
    h = i2c.readfrom_mem(MPU, reg, 1)[0]
    l = i2c.readfrom_mem(MPU, reg+1, 1)[0]
    v = (h << 8) | l
    return v - 65536 if v > 32767 else v

# =========================
# Framebuffer
# =========================
fb_data = bytearray(240 * 240 * 2)
fb = framebuf.FrameBuffer(fb_data, 240, 240, framebuf.RGB565)

def flush():
    tft.set_window(0, 0, 239, 239)
    tft.write_data(fb_data)

# =========================
# 颜色
# =========================
def sc(c):
    return ((c & 0xFF) << 8) | (c >> 8)

BLACK  = sc(0x0000)
WHITE  = sc(0xFFFF)
GREEN  = sc(0x07E0)
RED    = sc(0xF800)
BLUE   = sc(0x001F)
CYAN   = sc(0x07FF)
YELLOW = sc(0xFFE0)
GRAY   = sc(0x4208)
BG     = sc(0x0841)
ORANGE = sc(0xFD20)

# =========================
# 画实心圆
# =========================
def fb_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(r * r - dy * dy))
        y = cy + dy
        if 0 <= y < 240:
            x0 = max(0, cx - dx)
            x1 = min(239, cx + dx)
            fb.hline(x0, y, x1 - x0 + 1, color)

# =========================
# 游戏常量
# =========================
PLAYER_R    = 10
ENEMY_R     = 7
BONUS_R     = 8
FRICTION    = 0.88
ACCEL_SCALE = 0.00022

# =========================
# 难度计算
# =========================
def get_level(score):
    return score // 10

def get_speed(score):
    level = get_level(score)
    # 每级 +0.7，感觉更明显（原来 +0.4）
    return min(1.5 + level * 0.7, 7.5)

def get_max_enemies(score):
    level = get_level(score)
    return min(4 + level * 2, 14)

def get_spawn_interval(score):
    level = get_level(score)
    return max(10, 35 - level * 4)

# =========================
# 生成红色敌球
# =========================
def spawn_enemy(px, py, score):
    side = random.randint(0, 3)
    if side == 0:   x, y = float(random.randint(10, 230)), -12.0
    elif side == 1: x, y = float(random.randint(10, 230)), 252.0
    elif side == 2: x, y = -12.0, float(random.randint(10, 230))
    else:           x, y = 252.0, float(random.randint(10, 230))

    dx = px - x + random.uniform(-25, 25)
    dy = py - y + random.uniform(-25, 25)
    dist = math.sqrt(dx*dx + dy*dy) or 1
    speed = get_speed(score) + random.uniform(0, 0.8)
    return {'x': x, 'y': y,
            'vx': dx/dist*speed, 'vy': dy/dist*speed,
            'type': 'enemy'}

# =========================
# 生成蓝色奖励球
# =========================
def spawn_bonus():
    margin = 30
    return {'x': float(random.randint(margin, 240-margin)),
            'y': float(random.randint(margin, 240-margin)),
            'vx': 0.0, 'vy': 0.0,
            'type': 'bonus',
            'life': 180}

# =========================
# 碰撞检测
# =========================
def collide(px, py, ex, ey, pr, er):
    dx = px - ex
    dy = py - ey
    return (dx*dx + dy*dy) < (pr + er) ** 2

# =========================
# 难度升级闪屏提示
# ✅ 全部通过 framebuffer，不再混用 tft.fill()
# =========================
def level_up_flash(level):
    # 闪3次黄色
    for _ in range(3):
        fb.fill(YELLOW)
        flush()
        time.sleep_ms(80)
        fb.fill(BLACK)
        flush()
        time.sleep_ms(80)

    # 显示 LEVEL + 数字
    fb.fill(BLACK)
    # 手动用 fb.text() 写字（framebuf 内置小字体）
    lv_str = "LEVEL " + str(level)
    lx = max(0, (240 - len(lv_str) * 8) // 2)
    fb.text(lv_str, lx, 108, YELLOW)
    flush()
    time.sleep_ms(900)
    # 闪屏结束，framebuffer 留着，下一帧正常渲染会覆盖

# =========================
# 计算某类球的数量
# =========================
def count_type(balls, t):
    return sum(1 for b in balls if b['type'] == t)

# =========================
# 游戏结束画面
# ✅ 同样全部用 framebuffer
# =========================
def game_over_screen(score):
    fb.fill(BLACK)

    # 用 framebuf 内置 8px 字体居中显示
    fb.text("GAME OVER", 60, 70, RED)
    fb.text("SCORE: " + str(score), 60, 100, WHITE)
    fb.text("LV " + str(get_level(score)), 88, 125, CYAN)
    fb.text("TILT to restart", 28, 160, GRAY)
    flush()

    time.sleep_ms(1500)
    while True:
        if abs(read_word(0x3B)) > 6000 or abs(read_word(0x3D)) > 6000:
            break
        time.sleep_ms(100)
    time.sleep_ms(500)

# =========================
# 重置
# =========================
def reset_game():
    return {
        'px': 120.0, 'py': 120.0,
        'pvx': 0.0,  'pvy': 0.0,
        'balls': [],
        'score': 0,
        'prev_level': 0,
        'spawn_timer': 0,
        'bonus_timer': 0,
        'frame': 0,
    }

# =========================
# 浮动 +10 文字
# =========================
float_texts = []  # [x, y, frames_left]

# =========================
# 主循环
# =========================
g = reset_game()

while True:
    g['frame'] += 1

    # IMU 读取
    ax = read_word(0x3B)
    ay = read_word(0x3D)

    # 玩家物理
    g['pvx'] += ay * ACCEL_SCALE
    g['pvy'] += ax * ACCEL_SCALE
    g['pvx'] *= FRICTION
    g['pvy'] *= FRICTION
    g['px']  += g['pvx']
    g['py']  += g['pvy']

    # 边界反弹
    if g['px'] < PLAYER_R:       g['px'] = PLAYER_R;       g['pvx'] =  abs(g['pvx']) * 0.5
    if g['px'] > 239 - PLAYER_R: g['px'] = 239 - PLAYER_R; g['pvx'] = -abs(g['pvx']) * 0.5
    if g['py'] < PLAYER_R:       g['py'] = PLAYER_R;        g['pvy'] =  abs(g['pvy']) * 0.5
    if g['py'] > 239 - PLAYER_R: g['py'] = 239 - PLAYER_R; g['pvy'] = -abs(g['pvy']) * 0.5

    # 生成红球
    g['spawn_timer'] += 1
    if (g['spawn_timer'] >= get_spawn_interval(g['score']) and
            count_type(g['balls'], 'enemy') < get_max_enemies(g['score'])):
        g['balls'].append(spawn_enemy(g['px'], g['py'], g['score']))
        g['spawn_timer'] = 0

    # 生成蓝球
    g['bonus_timer'] += 1
    if (g['bonus_timer'] >= 120 and
            count_type(g['balls'], 'bonus') < 2):
        g['balls'].append(spawn_bonus())
        g['bonus_timer'] = 0

    # 更新所有球 + 碰撞检测
    hit = False
    survivors = []
    for b in g['balls']:
        b['x'] += b['vx']
        b['y'] += b['vy']

        if b['type'] == 'enemy':
            if collide(g['px'], g['py'], b['x'], b['y'], PLAYER_R, ENEMY_R):
                hit = True
                break
            if -20 < b['x'] < 260 and -20 < b['y'] < 260:
                survivors.append(b)
            else:
                g['score'] += 1

        elif b['type'] == 'bonus':
            if collide(g['px'], g['py'], b['x'], b['y'], PLAYER_R, BONUS_R):
                g['score'] += 10
                # ✅ 吃蓝球后立即同步 prev_level，防止触发升级闪屏
                g['prev_level'] = get_level(g['score'])
                float_texts.append([int(g['px']), int(g['py']) - 15, 40])
            else:
                b['life'] -= 1
                if b['life'] > 0:
                    survivors.append(b)

    g['balls'] = survivors

    # 难度升级检测
    cur_level = get_level(g['score'])
    if cur_level > g['prev_level']:
        g['prev_level'] = cur_level
        level_up_flash(cur_level)

    # 游戏结束
    if hit:
        game_over_screen(g['score'])
        g = reset_game()
        float_texts.clear()
        continue

    # =========================
    # 渲染
    # =========================
    fb.fill(BG)

    # 边框颜色随等级变化
    border_colors = [CYAN, YELLOW, ORANGE, RED, sc(0xF81F)]
    bc = border_colors[min(get_level(g['score']), len(border_colors)-1)]
    fb.rect(0, 0, 240, 240, bc)
    fb.rect(1, 1, 238, 238, bc)

    # 蓝色奖励球
    for b in g['balls']:
        if b['type'] == 'bonus':
            fb_circle(int(b['x']), int(b['y']), BONUS_R + 1, WHITE)
            fb_circle(int(b['x']), int(b['y']), BONUS_R,     BLUE)
            if b['life'] < 60 and (g['frame'] % 6 < 3):
                fb_circle(int(b['x']), int(b['y']), BONUS_R, BG)

    # 红色敌球
    for b in g['balls']:
        if b['type'] == 'enemy':
            fb_circle(int(b['x']), int(b['y']), ENEMY_R, RED)

    # 玩家
    fb_circle(int(g['px']), int(g['py']), PLAYER_R + 1, WHITE)
    fb_circle(int(g['px']), int(g['py']), PLAYER_R,     GREEN)

    flush()

    # 分数 + 等级（framebuf 原生字体叠加）
    tft.text(font, str(g['score']), 6, 6, 0xFFE0)
    lv = "LV" + str(get_level(g['score']))
    tft.text(font, lv, 240 - len(lv)*8 - 4, 6, 0x07FF)

    # +10 浮动文字
    still_alive = []
    for ft in float_texts:
        if ft[2] > 0:
            tft.text(font, "+10", ft[0], ft[1], 0x07FF)
            ft[1] -= 1
            ft[2] -= 1
            still_alive.append(ft)
    float_texts[:] = still_alive

    time.sleep_ms(16)
