# 🎮 Tilt Ball — MicroPython Game for Raspberry Pi Pico W

A fast-paced arcade survival game running on a **Raspberry Pi Pico W** (STEPico) with a **240×240 ST7789 TFT display** and **MPU-6050 IMU**. Tilt the board to dodge red enemy balls and collect blue bonus balls — survive as long as you can as the speed ramps up every 10 points.

---

## 📸 Demo

<div align="center">
  <img src="![Image](https://github.com/user-attachments/assets/d3f99014-6508-49b1-9447-29d6f95c8707)" width="700"/>
</div>

---

## 🕹️ Gameplay

- **Tilt the board** to move the green player ball using real gyroscope/accelerometer data
- **Dodge red enemy balls** that spawn from the edges and home in on your position
- **Collect blue bonus balls** to gain +10 points instantly
- **Survive** — one hit from a red ball ends the game
- **Difficulty increases every 10 points**: enemies move faster, spawn more frequently, and in greater numbers
- **Tilt to restart** after game over

### Scoring

| Event | Points |
|---|---|
| Enemy ball exits the screen | +1 |
| Collect a blue bonus ball | +10 |

---

## 🧠 Game Design

### Architecture

The game runs a single-file `main.py` loop at ~60 fps (`16ms` sleep per frame). All rendering is done through a **framebuffer** (`framebuf.FrameBuffer`) that is flushed to the display once per frame via SPI — this avoids partial-screen tearing and keeps the render pipeline consistent.

```
IMU Read → Physics Update → Spawn Logic → Collision Detection → Render → Flush → Repeat
```

### Physics

The player ball uses simple Newtonian physics:

- Accelerometer X/Y axes map to velocity increments each frame
- A friction coefficient (`0.88`) is applied every frame to naturally decelerate
- Boundary walls provide a damped bounce (`0.5` restitution)

```python
pvx += ay * ACCEL_SCALE   # tilt → acceleration
pvx *= FRICTION            # drag
px  += pvx                 # integrate position
```

### Difficulty Scaling

Every 10 points = 1 level up. Three parameters scale with level:

| Parameter | Formula | Cap |
|---|---|---|
| Enemy speed | `1.5 × 1.4^level` (exponential) | 8.0 |
| Max enemies on screen | `4 + level × 2` | 14 |
| Spawn interval (frames) | `35 - level × 4` | min 8 |

The exponential speed formula (`×1.4 per level`) ensures players feel a clear, escalating pressure rather than a subtle linear increase.

### Enemy AI

Each red ball spawns from a random edge of the screen and is aimed at the player's current position with a small random angular offset (`±25px`), preventing perfectly predictable trajectories:

```python
dx = px - spawn_x + random.uniform(-25, 25)
dy = py - spawn_y + random.uniform(-25, 25)
speed = get_speed(score) + random.uniform(0, 0.8)
```

### Color System

The ST7789 driver and MicroPython's `framebuf` module use **different byte orders** for RGB565 colors. Mixing them causes visual corruption and potential display crashes. This project uses two explicitly separated color sets:

- `fb_*` constants — raw RGB565, used exclusively with `framebuf` drawing calls
- Direct hex values — passed directly to `tft.text()` and `tft.fill()` hardware calls

This separation is critical and must be maintained if you modify the rendering code.

### Level-Up Flash

When the player levels up, the screen flashes yellow 3× and shows the new level number. The flash is implemented entirely through the `tft` hardware interface (not framebuffer) to avoid state conflicts between the two rendering paths:

```python
for _ in range(3):
    tft.fill(0xFFE0)   # yellow
    time.sleep_ms(80)
    tft.fill(0x0000)   # black
    time.sleep_ms(80)
```

After the flash, `flush()` is called to restore the game frame before the next loop iteration.

---

## 🔧 Hardware

| Component | Details |
|---|---|
| Microcontroller | Raspberry Pi Pico W (RP2040) via STEPico |
| Display | 240×240 ST7789 TFT (SPI) |
| IMU | MPU-6050 (I2C) |

### Wiring

#### ST7789 Display (SPI0)

| Pico Pin | GPIO | Display |
|---|---|---|
| GP18 | SCK | CLK / SCL |
| GP19 | MOSI | DIN / SDA |
| GP17 | CS | CS |
| GP21 | DC | DC / RS |
| GP20 | RST | RES |

#### MPU-6050 (I2C1)

| Pico Pin | GPIO | MPU-6050 |
|---|---|---|
| GP15 | SCL | SCL |
| GP14 | SDA | SDA |
| 3V3 | — | VCC |
| GND | — | GND |

---

## 📦 Dependencies

### MicroPython Libraries

These must be present on your Pico's filesystem:

| Library | Purpose | Source |
|---|---|---|
| `st7789.py` | ST7789 TFT display driver | [russhughes/st7789py_mpy](https://github.com/russhughes/st7789py_mpy) |
| `vga1_16x32.py` | 16×32 bitmap font for score display | Included with st7789py_mpy fonts |
| `framebuf` | Built-in MicroPython framebuffer | Built-in (no install needed) |
| `machine` | GPIO, SPI, I2C hardware access | Built-in |
| `math`, `random`, `time` | Standard utilities | Built-in |

### MicroPython Firmware

This project requires **MicroPython v1.20+** on the Raspberry Pi Pico W. Download from the [official MicroPython site](https://micropython.org/download/rp2-pico-w/).

---

## 🚀 Getting Started

### 1. Flash MicroPython

Hold the **BOOTSEL** button on your Pico while plugging in USB. Drag the `.uf2` firmware file onto the `RPI-RP2` drive that appears.

### 2. Install the ST7789 Driver

Download `st7789.py` and the font file `vga1_16x32.py` from [russhughes/st7789py_mpy](https://github.com/russhughes/st7789py_mpy) and copy them to the root of your Pico using [Thonny](https://thonny.org/) or `mpremote`.

```bash
# Using mpremote
mpremote connect /dev/ttyACM0 cp st7789.py :
mpremote connect /dev/ttyACM0 cp vga1_16x32.py :
```

### 3. Copy the Game

```bash
mpremote connect /dev/ttyACM0 cp main.py :
```

### 4. Run

Reset the Pico. The game starts automatically (MicroPython runs `main.py` on boot).

---

## 📁 File Structure

```
/
├── main.py          # Main game loop — all game logic and rendering
├── st7789.py        # ST7789 display driver
├── vga1_16x32.py    # Bitmap font (16×32 px per character)
└── README.md
```

---

## ⚙️ Configuration

Key constants at the top of `main.py` you can tune:

```python
PLAYER_R    = 10      # Player ball radius (px)
ENEMY_R     = 7       # Enemy ball radius (px)
BONUS_R     = 8       # Bonus ball radius (px)
FRICTION    = 0.88    # Physics drag (0=instant stop, 1=no drag)
ACCEL_SCALE = 0.00022 # IMU sensitivity → velocity mapping
```

Difficulty tuning (inside `get_speed`, `get_max_enemies`, `get_spawn_interval`):

```python
# Speed: exponential growth per level
return min(1.5 * (1.4 ** level), 8.0)

# Max enemies on screen at once
return min(4 + level * 2, 14)

# Frames between spawns
return max(8, 35 - level * 4)
```

---

## 🐛 Known Issues & Notes

- **Do not mix `tft.fill()` and `fb.fill()` in the same rendering path.** The ST7789 driver and `framebuf` use opposite RGB565 byte orders. Mixing them causes visual artifacts or display crashes, especially during transition screens.
- The MPU-6050 is read raw without calibration offset correction. If the ball drifts at rest, add a calibration step that samples 100 readings at startup and subtracts the mean.
- `vga1_16x32` font renders at 8px per character when passed to `framebuf.text()`, and at 16×32px when passed to `tft.text()` with the `font` argument. Make sure you use the right call for each context.

---

## 📄 License

MIT License. Feel free to use, modify, and share.

---

## 🙏 Acknowledgements

- [russhughes](https://github.com/russhughes) for the excellent `st7789py_mpy` driver and font collection
- The MicroPython community for `framebuf` documentation and examples
