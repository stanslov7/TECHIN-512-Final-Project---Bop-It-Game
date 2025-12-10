# ============================================================
# 80s BOP-IT STYLE GAME — FULL INTEGRATION
# Rotary Encoder + OLED + ADXL345 + NeoPixel + Button
# ============================================================

import time
import random
import math
import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306
import adafruit_adxl34x
import neopixel
from digitalio import DigitalInOut, Direction, Pull
from rotary_encoder import RotaryEncoder

# ============================================================
# -------------------- HARDWARE SETUP -------------------------
# ============================================================

# ---- I2C ----
i2c = busio.I2C(board.SCL, board.SDA)

# ---- OLED ----
displayio.release_displays()
display_bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# ---- Accelerometer ----
accelerometer = adafruit_adxl34x.ADXL345(i2c)

# ---- Rotary Encoder ----
encoder = RotaryEncoder(board.D3, board.D2, debounce_ms=3, pulses_per_detent=3)

# ---- NeoPixel ----
pixels = neopixel.NeoPixel(board.D10, 1, brightness=0.4, auto_write=True)

# ---- Button ----
btn = DigitalInOut(board.D9)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

# ============================================================
# ------------------- CONSTANTS ------------------------------
# ============================================================

directions = ['up', 'down', 'left', 'right', 'forward', 'back']

COLOR_GREEN = (0, 255, 0)
COLOR_RED   = (255, 0, 0)
COLOR_YELLOW = (255, 255, 0)
COLOR_OFF   = (0, 0, 0)

EMA_ALPHA = 0.2
THRESHOLD = 1.5
PERSISTENCE = 4

# ============================================================
# ------------------- OLED HELPER -----------------------------
# ============================================================

def displayText(line1="", line2="", line3="", line4=""):
    splash = displayio.Group()
    lines = [line1, line2, line3, line4]
    y = 5
    for text in lines:
        if text:
            lbl = label.Label(
                terminalio.FONT,
                text=text,
                anchor_point=(0.5, 0),
                anchored_position=(64, y)
            )
            splash.append(lbl)
            y += 14
    display.root_group = splash

# ============================================================
# ------------- ROTARY DIFFICULTY SELECT ---------------------
# ============================================================

def get_difficulty():
    displayText("Select Difficulty", "Rotate + Press")

    last_pos = encoder.position

    while True:
        encoder.update()  # always call update

        pos = encoder.position % 3

        if pos != last_pos:
            last_pos = pos

            if pos == 0:
                displayText("Difficulty:", "EASY")
            elif pos == 1:
                displayText("Difficulty:", "NORMAL")
            else:
                displayText("Difficulty:", "HARD")

        # Button press confirms selection
        if not btn.value:
            time.sleep(0.3)  # debounce
            return pos + 1

        time.sleep(0.01)


# ============================================================
# ----------- IMPROVED DIRECTION DETECTION -------------------
# ============================================================

xFilt, yFilt, zFilt = accelerometer.acceleration
counters = {
    "xp":0, "xn":0,
    "yp":0, "yn":0,
    "zp":0, "zn":0
}

def detect_movement(level):
    global xFilt, yFilt, zFilt, counters

    x, y, z = accelerometer.acceleration

    # EMA filter
    xFilt = EMA_ALPHA * x + (1-EMA_ALPHA)*xFilt
    yFilt = EMA_ALPHA * y + (1-EMA_ALPHA)*yFilt
    zFilt = EMA_ALPHA * z + (1-EMA_ALPHA)*zFilt

    z_adj = zFilt - 9.81

    abs_vals = {
        "x": abs(xFilt),
        "y": abs(yFilt),
        "z": abs(z_adj)
    }

    dominant = max(abs_vals, key=abs_vals.get)

    thresh = THRESHOLD + 0.3 * (level - 1)
    if abs_vals[dominant] < thresh:
        for k in counters:
            counters[k] = 0
        return None

    direction = None

    if dominant == "x":
        if xFilt > thresh:
            counters["xp"] += 1
            counters["xn"] = 0
            if counters["xp"] >= PERSISTENCE:
                direction = "right"
        elif xFilt < -thresh:
            counters["xn"] += 1
            counters["xp"] = 0
            if counters["xn"] >= PERSISTENCE:
                direction = "left"

    elif dominant == "y":
        if yFilt > thresh:
            counters["yp"] += 1
            counters["yn"] = 0
            if counters["yp"] >= PERSISTENCE:
                direction = "forward"
        elif yFilt < -thresh:
            counters["yn"] += 1
            counters["yp"] = 0
            if counters["yn"] >= PERSISTENCE:
                direction = "back"

    elif dominant == "z":
        if z_adj > thresh:
            counters["zp"] += 1
            counters["zn"] = 0
            if counters["zp"] >= PERSISTENCE:
                direction = "up"
        elif z_adj < -thresh:
            counters["zn"] += 1
            counters["zp"] = 0
            if counters["zn"] >= PERSISTENCE:
                direction = "down"

    return direction

# ============================================================
# --------------------- GAME LOOP ----------------------------
# ============================================================

while True:

    difficulty = get_difficulty()
    lives = {1:5, 2:3, 3:1}[difficulty]

    displayText("Get Ready!")
    for i in [3,2,1]:
        displayText(str(i))
        pixels[0] = COLOR_RED if i==3 else COLOR_YELLOW if i==2 else COLOR_GREEN
        time.sleep(1)

    pixels[0] = COLOR_OFF
    level = 1
    game_over = False

    while level <= 10 and not game_over:
        time_per_move = 6 - (4/9)*(level-1)

        for _ in range(10):
            if lives <= 0:
                game_over = True
                break

            target = random.choice(directions)
            displayText(f"D{difficulty} L{level}", f"Lives:{lives}", target.upper())
            start = time.time()
            responded = False

            while time.time() - start < time_per_move:
                detected = detect_movement(level)
                if detected:
                    responded = True
                    if detected == target:
                        displayText("Correct!")
                        pixels[0] = COLOR_GREEN
                    else:
                        displayText("Wrong!")
                        pixels[0] = COLOR_RED
                        lives -= 1
                    time.sleep(0.5)
                    pixels[0] = COLOR_OFF
                    break
                time.sleep(0.02)

            if not responded:
                displayText("Too Slow!")
                pixels[0] = COLOR_YELLOW
                lives -= 1
                time.sleep(0.5)
                pixels[0] = COLOR_OFF

        if not game_over:
            level += 1
            displayText("Next Level!")
            time.sleep(1)

    displayText("GAME OVER", "Press Button")
    while btn.value:
        time.sleep(0.1)
