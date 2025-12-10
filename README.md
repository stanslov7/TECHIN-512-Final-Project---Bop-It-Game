
<<<<<<< HEAD
# 80s Bop-It–Style Motion Game (CircuitPython)

## Overview

This project is an **interactive, motion-controlled game inspired by the classic 1980s “Bop-It” concept**, built using **CircuitPython** and physical hardware inputs. Players must perform the **correct directional movement** (detected via an accelerometer) within a **shrinking time window** as difficulty increases.

The game combines **embedded systems**, **sensor signal processing**, and **human–computer interaction** into a single interactive experience.

---

## Features

- ✅ Three difficulty modes (Easy / Normal / Hard)
- ✅ Rotary encoder for difficulty selection
- ✅ Ten progressively harder levels
- ✅ Directional motion detection using ADXL345
- ✅ OLED display for all game text
- ✅ NeoPixel visual feedback
- ✅ Lives system and replay button
- ✅ Dynamic timing and sensitivity scaling

---

## Hardware Requirements

| Component | Purpose |
|---------|--------|
| ESP32 / CircuitPython-compatible board | Main controller |
| ADXL345 Accelerometer | Detects directional motion |
| SSD1306 OLED (128×64) | Displays game text |
| Rotary Encoder | Difficulty selection |
| NeoPixel (1 LED) | Visual feedback |
| Push Button | Start / Play again |
| I2C Bus | OLED + Accelerometer communication |

---

## Pin Connections

| Device | Pin |
|------|----|
| Rotary Encoder A | D3 |
| Rotary Encoder B | D2 |
| NeoPixel Data | D10 |
| Button Input | D9 |
| OLED SDA / SCL | I2C (SDA, SCL) |
| ADXL345 | I2C (Address 0x53) |

---

## Gameplay Instructions

1. Power on the device
2. Rotate the encoder to select difficulty:
   - **Easy** (5 lives)
   - **Normal** (3 lives)
   - **Hard** (1 life)
3. Press the button to confirm selection
4. Follow the OLED prompts:
   - `UP`, `DOWN`, `LEFT`, `RIGHT`, `FORWARD`, `BACK`
5. Perform the correct motion before time runs out
6. Progress through 10 levels with decreasing reaction time
7. Game ends when lives reach zero or all levels are completed
8. Press the button to play again

---

## Difficulty Scaling

| Level | Time per Move |
|------|--------------|
| 1 | ~6.0 seconds |
| 5 | ~4.2 seconds |
| 10 | ~2.0 seconds |

Difficulty also affects:
- Motion detection threshold
- Accuracy tolerance
- Number of starting lives

---

## Motion Detection Method

The game uses an **Improved Direction Detection algorithm** featuring:

- Exponential Moving Average (EMA) filtering
- Gravity compensation on the Z-axis
- Dominant-axis selection
- Persistence requirement (consistent readings)
- Dynamic thresholds based on level

### Supported Directions

| Axis | Direction |
|----|----------|
| +X | Right |
| −X | Left |
| +Y | Forward |
| −Y | Back |
| +Z | Up |
| −Z | Down |

---

## Visual Feedback

### OLED Display
- Current difficulty, level, and lives
- Prompted movement direction
- Game status messages (Correct / Wrong / Too Slow)

### NeoPixel

| Color | Meaning |
|------|--------|
| Green | Correct move |
| Red | Incorrect move |
| Yellow | Too slow |
| Off | Idle |

---

## Code Structure

bopit.py
├── Hardware initialization
├── OLED display helper
├── Rotary encoder difficulty selection
├── Motion detection (EMA + persistence)
├── Game logic loop
│ ├── Level progression
│ ├── Time-based input window
│ ├── Life tracking
│ └── Replay handling


All functionality is contained in **a single file** bopit.py for easy deployment.

---

## Required Libraries

The following libraries are used and present for reference in the `/lib` folder:

- `adafruit_adxl34x.mpy`
- `adafruit_displayio_ssd1306.mpy`
- `adafruit_display_text`
- `adafruit_bus_device`
- `neopixel.mpy`
- `rotary_encoder.py`

---

## Educational Objectives

This project demonstrates:

- Embedded systems integration
- Sensor data filtering and analysis
- Real-time input processing
- State-based game logic
- Physical computing design principles
- Interactive system design

---

## Author

**Stanislav Slovetskiy**  
University of Washington – Global Innovation Exchange  
TECHIN 512 - Sensors and Circuits
=======
# README for TECHIN 512 - Bop-it Game Project implementation
>>>>>>> 17ac763af72f9cb75f8f8f7859ce705eabc04dd2
