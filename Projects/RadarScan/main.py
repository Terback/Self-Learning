from machine import Pin, SPI, PWM
import st7789
import time
import math

# =========================
# 屏幕初始化
# =========================
spi = SPI(0, baudrate=40000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19))
rst = Pin(21, Pin.OUT)
dc  = Pin(20, Pin.OUT)
cs  = Pin(17, Pin.OUT)
tft = st7789.ST7789(spi, 240, 240, rst, dc, cs)

# =========================
# Servo
# =========================
servo = PWM(Pin(15))
servo.freq(50)

def set_angle(angle):
    duty = int(1638 + (angle / 180) * 6553)
    servo.duty_u16(duty)

# =========================
# Ultrasonic
# =========================
trig = Pin(13, Pin.OUT)
echo = Pin(12, Pin.IN)

def _single_distance():
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    timeout = time.ticks_us() + 23500
    while echo.value() == 0:
        if time.ticks_us() > timeout:
            return -1
    start = time.ticks_us()
    while echo.value() == 1:
        if time.ticks_us() > timeout:
            return -1
    return time.ticks_diff(time.ticks_us(), start) * 0.034 / 2

def get_distance():
    samples = []
    for _ in range(3):
        d = _single_distance()
        if 2 < d < 400:
            samples.append(d)
        time.sleep_us(300)
    if not samples:
        return -1
    samples.sort()
    return samples[len(samples) // 2]

# =========================
# 常量
# =========================
BLACK      = 0x0000
GREEN      = 0x07E0
DARK_GREEN = 0x0320
RED        = 0xF800
DARK_RED   = 0x8000

CX, CY = 120, 125
RADIUS  = 105
MAX_CM  = 60

ANGLE_STEP   = 5
DELAY        = 6
SECTOR_WIDTH = 4
DOT_RADIUS   = 3

# =========================
# 三角函数 LUT
# =========================
_COS = [0.0] * 181
_SIN = [0.0] * 181
for _a in range(181):
    _r = math.radians(_a)
    _COS[_a] = math.cos(_r)
    _SIN[_a] = math.sin(_r)

def polar_xy(angle, radius):
    return (int(CX + radius * _COS[angle]),
            int(CY - radius * _SIN[angle]))

def map_distance(dist):
    if dist <= 0 or dist > MAX_CM:
        return 0
    return max(0, int(dist / MAX_CM * RADIUS))

# =========================
# 圆点绘制
# =========================
def draw_dot(x, y, r, color):
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(r * r - dy * dy))
        tft.line(x - dx, y + dy, x + dx, y + dy, color)
    if color == RED:
        for dy in range(-(r + 1), r + 2):
            inner = (r + 1) * (r + 1) - dy * dy
            if inner < 0:
                continue
            dx = int(math.sqrt(inner))
            tft.pixel(x - dx, y + dy, DARK_RED)
            tft.pixel(x + dx, y + dy, DARK_RED)

# =========================
# 网格
# =========================
def draw_arc(radius, color):
    last = None
    for a in range(0, 181, 3):
        p = polar_xy(a, radius)
        if last:
            tft.line(last[0], last[1], p[0], p[1], color)
        last = p

def draw_grid():
    tft.fill(BLACK)
    tft.line(CX - RADIUS, CY, CX + RADIUS, CY, DARK_GREEN)
    for r in (35, 70, 105):
        draw_arc(r, DARK_GREEN)
    for a in (0, 30, 60, 90, 120, 150, 180):
        x, y = polar_xy(a, RADIUS)
        tft.line(CX, CY, x, y, DARK_GREEN)

# =========================
# 扫描线
# =========================
def draw_scan(angle):
    x, y = polar_xy(angle, RADIUS)
    tft.line(CX, CY, x, y, GREEN)

def erase_scan(angle):
    x, y = polar_xy(angle, RADIUS)
    tft.line(CX, CY, x, y, BLACK)
    for r in (35, 70, 105):
        a0 = max(0,   angle - 2)
        a1 = min(180, angle + 2)
        x0, y0 = polar_xy(a0, r)
        x1, y1 = polar_xy(a1, r)
        tft.line(x0, y0, x1, y1, DARK_GREEN)
    if angle in (0, 30, 60, 90, 120, 150, 180):
        x, y = polar_xy(angle, RADIUS)
        tft.line(CX, CY, x, y, DARK_GREEN)

# =========================
# 检测点
# =========================
def draw_sector(angle, mapped):
    for a in range(max(0, angle - SECTOR_WIDTH),
                   min(180, angle + SECTOR_WIDTH + 1)):
        x, y = polar_xy(a, mapped)
        draw_dot(x, y, DOT_RADIUS, RED)

def erase_sector(angle, mapped):
    for a in range(max(0, angle - SECTOR_WIDTH),
                   min(180, angle + SECTOR_WIDTH + 1)):
        x, y = polar_xy(a, mapped)
        draw_dot(x, y, DOT_RADIUS, BLACK)
        for r in (35, 70, 105):
            a0 = max(0,   a - 1)
            a1 = min(180, a + 1)
            x0, y0 = polar_xy(a0, r)
            x1, y1 = polar_xy(a1, r)
            tft.line(x0, y0, x1, y1, DARK_GREEN)
    tft.line(CX - RADIUS, CY, CX + RADIUS, CY, DARK_GREEN)

# =========================
# 重绘所有缓存检测点
# =========================
detections = [0] * 181

def redraw_all_detections():
    for a in range(0, 181, ANGLE_STEP):
        if detections[a] > 5:
            draw_sector(a, detections[a])

# =========================
# 主循环
# =========================
angle      = 0
direction  = 1
prev_angle = 0

draw_grid()
set_angle(0)
time.sleep_ms(300)

while True:
    # 擦上一帧扫描线
    erase_scan(prev_angle)

    # 移动舵机
    set_angle(angle)
    time.sleep_ms(DELAY)

    # 测距
    dist   = get_distance()
    mapped = map_distance(dist)

    # 擦旧点，画新点
    old = detections[angle]
    if old > 5:
        erase_sector(angle, old)

    detections[angle] = mapped
    if mapped > 5:
        draw_sector(angle, mapped)

    # 画扫描线
    draw_scan(angle)

    prev_angle = angle

    # 步进角度
    angle += direction * ANGLE_STEP

    if angle >= 180:
        angle = 180
        direction = -1
        draw_grid()
        redraw_all_detections()
    elif angle <= 0:
        angle = 0
        direction = 1
        draw_grid()
        redraw_all_detections()
