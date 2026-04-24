# 📡 RP2040 Radar Scanner (Servo + Ultrasonic + ST7789)

A real-time radar-style scanning system built with an RP2040 microcontroller, combining a servo motor, ultrasonic sensor, and SPI display to visualize distance data as a dynamic radar UI.

---

## 🚀 Project Overview

This project simulates a radar system:

- A **servo motor** sweeps from 0° to 180°
- An **ultrasonic sensor (HC-SR04)** measures distance at each angle
- A **ST7789 SPI display** renders a radar-style visualization in real time

The result is a smooth scanning radar interface that displays detected objects as highlighted points on screen.

---

## 🧠 Key Features

- ✅ Real-time radar scanning visualization  
- ✅ Smooth, non-flickering display (no full-screen refresh)  
- ✅ Bidirectional scanning with correct visual mapping  
- ✅ Optimized rendering for MicroPython + SPI display  
- ✅ Enhanced object visualization (cross + block marker)  
- ✅ Distance mapping for accurate screen representation  

---

## 🧰 Hardware Requirements

- RP2040-based board (e.g., Raspberry Pi Pico / Pico W)
- ST7789 SPI display (240x240, with CS pin)
- SG90 Servo Motor
- HC-SR04 Ultrasonic Sensor
- External 5V power supply (recommended for servo)
- Voltage divider (for HC-SR04 Echo pin)

---

## 🔌 Wiring Diagram

### 📺 ST7789 Display

| Display Pin | RP2040 Pin |
|------------|-----------|
| VCC        | 3.3V      |
| GND        | GND       |
| SCL (SCK)  | GP18      |
| SDA (MOSI) | GP19      |
| CS         | GP17      |
| DC         | GP20      |
| RES        | GP21      |
| BLK        | 3.3V      |

---

### 🔄 Servo Motor (SG90)

| Servo Wire | Connection |
|-----------|-----------|
| Red       | 5V (external recommended) |
| Brown     | GND       |
| Orange    | GP15      |

---

### 📡 Ultrasonic Sensor (HC-SR04)

| Sensor Pin | RP2040 Pin |
|-----------|-----------|
| VCC       | 5V        |
| GND       | GND       |
| TRIG      | GP13      |
| ECHO      | GP12 ⚠️ (use voltage divider) |

---

## ⚠️ Important Notes

- **Do NOT connect Echo directly to RP2040 (5V → 3.3V required)**
- Servo should be powered by **external 5V**, not 3.3V
- All grounds must be connected together

---

## 🎮 How It Works

1. Servo rotates incrementally
2. Ultrasonic sensor measures distance
3. Distance is mapped to screen radius
4. Display renders:
   - Radar grid (static)
   - Scanning line (dynamic)
   - Object markers (highlighted points)

---

## 📷 Visual Output

- Green radar sweep line
- Circular grid and angle markers
- Red detection points indicating objects
- Smooth animation without flickering

---

## ⚙️ Software Stack

- MicroPython
- Custom ST7789 driver
- Math-based polar → Cartesian conversion
- Optimized rendering loop

---

## 📦 Project Structure

├── main.py # Main radar logic
├── st7789.py # Display driver
└── README.md


---

## 🧪 Performance Optimizations

- Partial redraw (no full screen refresh)
- Lightweight object rendering (instead of heavy sector fills)
- Controlled update rate for smooth animation
- Angle-direction mapping for correct scan reversal

---

## 🔥 Future Improvements

- Radar sweep trail (afterglow effect)
- Object tracking persistence
- UI overlay (distance, angle readout)
- Kalman filter for sensor smoothing
- Data logging and PC visualization

---

## 🎯 Use Cases

- STEM education projects
- Embedded systems learning
- Sensor data visualization demos
- Kickstarter / product demos
- Microcontroller UI prototyping

---

## 👨‍💻 Author

Built as part of a hands-on electronics + embedded systems learning project.

---

## ⭐ If you like this project

Feel free to star ⭐ the repo and use it in your own projects or classrooms!
