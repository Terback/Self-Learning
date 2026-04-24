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

        self.reset.init(Pin.OUT, value=1)
        self.dc.init(Pin.OUT, value=0)
        self.cs.init(Pin.OUT, value=1)

        self.init_display()

    def write_cmd(self, cmd):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)

    def reset_display(self):
        self.reset(0)
        time.sleep_ms(100)
        self.reset(1)
        time.sleep_ms(100)

    def init_display(self):
        self.reset_display()

        self.write_cmd(0x01)
        time.sleep_ms(150)

        self.write_cmd(0x11)
        time.sleep_ms(120)

        self.write_cmd(0x36)
        self.write_data(bytearray([0x00]))

        self.write_cmd(0x3A)
        self.write_data(bytearray([0x05]))

        self.write_cmd(0x21)

        self.write_cmd(0x29)
        time.sleep_ms(50)

    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(0x2A)
        self.write_data(bytearray([
            x0 >> 8, x0 & 0xFF,
            x1 >> 8, x1 & 0xFF
        ]))

        self.write_cmd(0x2B)
        self.write_data(bytearray([
            y0 >> 8, y0 & 0xFF,
            y1 >> 8, y1 & 0xFF
        ]))

        self.write_cmd(0x2C)

    def fill(self, color):
        self.set_window(0, 0, self.width - 1, self.height - 1)

        hi = color >> 8
        lo = color & 0xFF

        line = bytearray(self.width * 2)
        for i in range(self.width):
            line[2 * i] = hi
            line[2 * i + 1] = lo

        for _ in range(self.height):
            self.write_data(line)
