from machine import Pin
import time

class ST7789:
    def __init__(self, spi, width, height, reset, dc, cs):
        self.spi = spi
        self.width = width
        self.height = height
        self.reset = reset
        self.dc = dc
        self.cs = cs

        self.reset.init(Pin.OUT)
        self.dc.init(Pin.OUT)
        self.cs.init(Pin.OUT)

    def write_cmd(self, cmd):
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)

    def write_data(self, data):
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(data)
        self.cs.value(1)

    def init(self):
        self.reset.value(1)
        time.sleep_ms(50)
        self.reset.value(0)
        time.sleep_ms(50)
        self.reset.value(1)
        time.sleep_ms(50)

        self.write_cmd(0x01)
        time.sleep_ms(150)

        self.write_cmd(0x11)
        time.sleep_ms(150)

        self.write_cmd(0x3A)
        self.write_data(bytearray([0x55]))

        self.write_cmd(0x36)
        self.write_data(bytearray([0x00]))

        self.write_cmd(0x21)

        self.write_cmd(0x29)
        time.sleep_ms(100)

    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(0x2A)
        self.write_data(bytearray([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))

        self.write_cmd(0x2B)
        self.write_data(bytearray([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))

        self.write_cmd(0x2C)

    def fill(self, color):
        self.set_window(0, 0, self.width - 1, self.height - 1)

        hi = color >> 8
        lo = color & 0xFF
        line = bytearray([hi, lo] * self.width)

        self.dc.value(1)
        self.cs.value(0)
        for _ in range(self.height):
            self.spi.write(line)
        self.cs.value(1)

    # ✅ 关键：字体显示（匹配 vga1_16x32）
    def text(self, font, text, x, y, color=0xFFFF):
        for i, char in enumerate(text):
            self.char(font, char, x + i * font.WIDTH, y, color)

    def char(self, font, char, x, y, color):
        ascii_code = ord(char)
    
    # 小写转大写
        if 97 <= ascii_code <= 122:
            ascii_code -= 32

    # 索引映射
        if ascii_code == 32:                        # 空格
            index = 0
        elif ascii_code == 45:                      # '-'
            index = 16
        elif ascii_code == 46:                      # '.'
            index = 32
        elif 48 <= ascii_code <= 57:                # '0'~'9'
            index = 48 + (ascii_code - 48) * 16
        elif 65 <= ascii_code <= 90:                # 'A'~'Z'
            index = 208 + (ascii_code - 65) * 16
        else:
            return  # 不支持的字符直接跳过

        for row in range(font.HEIGHT):
            bits = font.FONT[index + row]
            for col in range(font.WIDTH):
                if bits & (1 << (7 - col)):
                    self.pixel(x + col, y + row, color)
    
    
    def pixel(self, x, y, color):
        scale = 1  # 👈 放大倍数

        for dx in range(scale):
            for dy in range(scale):
                self.set_window(x*scale+dx, y*scale+dy, x*scale+dx, y*scale+dy)
                self.write_data(bytearray([color >> 8, color & 0xFF]))
