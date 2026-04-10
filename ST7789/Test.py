# Test ST7789 Without adding driver
from machine import Pin, SPI
import time

spi = SPI(
    0,
    baudrate=10000000,
    polarity=0,
    phase=0,
    sck=Pin(18),
    mosi=Pin(19)
)

cs = Pin(17, Pin.OUT)
dc = Pin(21, Pin.OUT)
rst = Pin(20, Pin.OUT)

def write_cmd(cmd):
    cs.value(0)
    dc.value(0)
    spi.write(bytearray([cmd]))
    cs.value(1)

def write_data(data):
    cs.value(0)
    dc.value(1)
    spi.write(bytearray(data))
    cs.value(1)

def reset():
    rst.value(1)
    time.sleep_ms(50)
    rst.value(0)
    time.sleep_ms(50)
    rst.value(1)
    time.sleep_ms(50)

def init():
    reset()

    write_cmd(0x01)
    time.sleep_ms(150)

    write_cmd(0x11)
    time.sleep_ms(150)

    write_cmd(0x3A)
    write_data([0x55])

    write_cmd(0x36)
    write_data([0x00])

    write_cmd(0x21)

    write_cmd(0x29)
    time.sleep_ms(100)

def set_window():
    write_cmd(0x2A)
    write_data([0, 0, 0, 239])

    write_cmd(0x2B)
    write_data([0, 0, 0, 239])

    write_cmd(0x2C)

def fill(color):
    set_window()

    hi = (color >> 8) & 0xFF
    lo = color & 0xFF
    line = bytearray([hi, lo] * 240)

    cs.value(0)
    dc.value(1)
    for _ in range(240):
        spi.write(line)
    cs.value(1)

init()

while True:
    fill(0xF800)
    time.sleep(1)
    fill(0x07E0)
    time.sleep(1)
    fill(0x001F)
    time.sleep(1)
