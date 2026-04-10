from machine import Pin, SPI
import time
import st7789

# =========================
# SPI 初始化
# =========================
spi = SPI(
    0,
    baudrate=20000000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(19)
)

# =========================
# 屏幕初始化
# =========================
tft = st7789.ST7789(
    spi,
    240,
    240,
    reset=Pin(20, Pin.OUT),
    dc=Pin(21, Pin.OUT),
    cs=Pin(17, Pin.OUT)
)

tft.init()

# =========================
# 测试循环
# =========================
while True:
    print("RED")
    tft.fill(0xF800)
    time.sleep(1)

    print("GREEN")
    tft.fill(0x07E0)
    time.sleep(1)

    print("BLUE")
    tft.fill(0x001F)
    time.sleep(1)

    print("WHITE")
    tft.fill(0xFFFF)
    time.sleep(1)
