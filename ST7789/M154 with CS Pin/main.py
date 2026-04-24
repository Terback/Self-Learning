from machine import Pin, SPI
import time
import st7789

spi = SPI(
    0,
    baudrate=10000000,
    polarity=1,
    phase=1,
    sck=Pin(18),
    mosi=Pin(19)
)

rst = Pin(21, Pin.OUT)
dc = Pin(20, Pin.OUT)
cs = Pin(17, Pin.OUT)

tft = st7789.ST7789(spi, 240, 240, rst, dc, cs)

RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
WHITE = 0xFFFF
BLACK = 0x0000

print("ST7789 test start")

while True:
    tft.fill(RED)
    time.sleep(1)
    tft.fill(GREEN)
    time.sleep(1)
    tft.fill(BLUE)
    time.sleep(1)
    tft.fill(WHITE)
    time.sleep(1)
    tft.fill(BLACK)
    time.sleep(1)
