"""Волна 3 «Готово к заливу» 30.09 (креативщик w3): 10 пакетов × 4 статики 1:1, Pillow (ключ OpenAI истёк). Запуск:
    python3 w3_packs.py            — все пакеты
    python3 w3_packs.py 3 5        — пакеты 3 и 5
    python3 w3_packs.py 3:a,c      — пакет 3, буквы a и c
    python3 w3_packs.py icons      — лист иконок (scratch, для проверки)
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json.
Шаблоны: p60_templates (grid / quiz / compare) + w2b_layouts (scene_d, price_tag) + свои иконки, «герои», сцены и
раскладка ee_grid (перенос доказанного LT-крео тепловых насосов 0819-GE02 на эстонский) — всё в этом файле.
Цифры на картинках — только из гипотез: US охрана дома $20–$60/мес (sourceNote), VA ~$3,900+ при 100 % (article +
sourceNote, va.gov), возраст 50–85 (угол final expense), 2–3 года graded benefit (article), до ~$40,000 покрытия
(article). Остальные цены — «?». Без «near you», до/после, обещаний эффекта и вопросов о положении зрителя."""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p60_lib import C, W, OUT, mix, rotpts
import p60_icons as I
import p60_scenes as S
import p60_templates as T
import p60w2_art as A  # noqa: F401  (иконки волны 2 + люди без лиц)
import w2b_icons  # noqa: F401
import w2b_scenes as WS
import w2b_layouts as L

WH = (255, 255, 255)
CONCEPT = {"a": "сетка выбора (fake interactivity)", "b": "карточка-опросник", "c": "сколько стоит / сравнение", "d": "сцена-иллюстрация"}
PACKS = {}
SKIN = A.SKIN


# =====================================================================  иконки (квадрат s, центр cx, cy)
def w3_paw(c, cx, cy, s, col, bg=WH):
    c.ellipse((cx - s * 0.22, cy - s * 0.02, cx + s * 0.22, cy + s * 0.34), fill=col)
    for dx, dy, r in ((-0.3, -0.14, 0.1), (-0.12, -0.32, 0.1), (0.12, -0.32, 0.1), (0.3, -0.14, 0.1)):
        c.ellipse((cx + (dx - r) * s, cy + (dy - r * 1.2) * s, cx + (dx + r) * s, cy + (dy + r * 1.2) * s), fill=col)


def w3_dog(c, cx, cy, s, col, bg=WH, muzzle=None, ear=None):
    ear = ear or mix(col, (0, 0, 0), 0.25)
    c.ellipse((cx - s * 0.46, cy - s * 0.3, cx - s * 0.2, cy + s * 0.18), fill=ear)
    c.ellipse((cx + s * 0.2, cy - s * 0.3, cx + s * 0.46, cy + s * 0.18), fill=ear)
    c.ellipse((cx - s * 0.3, cy - s * 0.36, cx + s * 0.3, cy + s * 0.3), fill=col)
    mz = muzzle or mix(col, WH, 0.55)
    c.ellipse((cx - s * 0.17, cy + s * 0.02, cx + s * 0.17, cy + s * 0.34), fill=mz)
    c.ellipse((cx - s * 0.07, cy + s * 0.06, cx + s * 0.07, cy + s * 0.15), fill=(40, 34, 34))
    c.circle(cx - s * 0.12, cy - s * 0.08, s * 0.035, fill=(40, 34, 34))
    c.circle(cx + s * 0.12, cy - s * 0.08, s * 0.035, fill=(40, 34, 34))


def w3_cat(c, cx, cy, s, col, bg=WH):
    c.poly([(cx - s * 0.34, cy - s * 0.04), (cx - s * 0.3, cy - s * 0.42), (cx - s * 0.06, cy - s * 0.22)], col)
    c.poly([(cx + s * 0.34, cy - s * 0.04), (cx + s * 0.3, cy - s * 0.42), (cx + s * 0.06, cy - s * 0.22)], col)
    c.ellipse((cx - s * 0.36, cy - s * 0.3, cx + s * 0.36, cy + s * 0.3), fill=col)
    for k in (-1, 1):
        c.ellipse((cx + k * s * 0.13 - s * 0.05, cy - s * 0.1, cx + k * s * 0.13 + s * 0.05, cy + s * 0.02), fill=(250, 214, 90))
        c.line([(cx + k * s * 0.12, cy + s * 0.12), (cx + k * s * 0.42, cy + s * 0.06)], mix(col, WH, 0.6), s * 0.018)
        c.line([(cx + k * s * 0.12, cy + s * 0.16), (cx + k * s * 0.42, cy + s * 0.18)], mix(col, WH, 0.6), s * 0.018)
    c.poly([(cx - s * 0.04, cy + s * 0.08), (cx + s * 0.04, cy + s * 0.08), (cx, cy + s * 0.13)], (236, 140, 150))


def w3_bandage(c, cx, cy, s, col, bg=WH):
    pts = rotpts([(cx - s * 0.46, cy - s * 0.15), (cx + s * 0.46, cy - s * 0.15), (cx + s * 0.46, cy + s * 0.15), (cx - s * 0.46, cy + s * 0.15)], cx, cy, -40)
    c.poly(pts, col)
    for k in (-1, 1):
        c.circle(cx + k * s * 0.31 * math.cos(math.radians(40)), cy - k * s * 0.31 * math.sin(math.radians(40)), s * 0.15, fill=col)
    pad = rotpts([(cx - s * 0.15, cy - s * 0.12), (cx + s * 0.15, cy - s * 0.12), (cx + s * 0.15, cy + s * 0.12), (cx - s * 0.15, cy + s * 0.12)], cx, cy, -40)
    c.poly(pad, mix(col, WH, 0.6))
    for dx, dy in ((-0.05, -0.02), (0.04, -0.06), (0.0, 0.05), (0.07, 0.03), (-0.07, 0.07)):
        c.circle(cx + dx * s, cy + dy * s, s * 0.018, fill=col)


def w3_pet_steth(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    """Стетоскоп + лапка (лечение болезней питомца)."""
    c.arc((cx - s * 0.34, cy - s * 0.5, cx + s * 0.06, cy - s * 0.02), 0, 180, col, s * 0.055)
    for x in (cx - s * 0.34, cx + s * 0.06):
        c.circle(x, cy - s * 0.26, s * 0.045, fill=col)
    c.line([(cx - s * 0.14, cy - s * 0.02), (cx - s * 0.14, cy + s * 0.14)], col, s * 0.055)
    c.arc((cx - s * 0.14, cy - s * 0.08, cx + s * 0.3, cy + s * 0.36), 90, 180, col, s * 0.055)
    c.arc((cx - s * 0.14 + s * 0.22 - s * 0.14, cy - s * 0.08, cx + s * 0.3 + s * 0.02, cy + s * 0.36), 0, 90, col, s * 0.055)
    c.line([(cx + s * 0.32, cy + s * 0.14), (cx + s * 0.32, cy - s * 0.02)], col, s * 0.055)
    c.circle(cx + s * 0.32, cy - s * 0.1, s * 0.12, fill=col)
    c.circle(cx + s * 0.32, cy - s * 0.1, s * 0.055, fill=bg)
    w3_paw(c, cx - s * 0.26, cy + s * 0.3, s * 0.34, acc)


def w3_old_dog(c, cx, cy, s, col, bg=WH):
    w3_dog(c, cx - s * 0.06, cy + s * 0.02, s * 0.86, col, muzzle=(226, 226, 230), ear=mix(col, (0, 0, 0), 0.3))
    c.circle(cx + s * 0.3, cy + s * 0.28, s * 0.17, fill=bg)
    I.clock(c, cx + s * 0.3, cy + s * 0.28, s * 0.3, (232, 120, 40), bg=bg)


def w3_wave(c, cx, cy, s, col, bg=WH, acc=(232, 88, 70)):
    c.line([(cx - s * 0.42, cy + s * 0.4), (cx + s * 0.44, cy + s * 0.4)], col, s * 0.04)
    c.line([(cx - s * 0.42, cy - s * 0.42), (cx - s * 0.42, cy + s * 0.4)], col, s * 0.04)
    pts = [(-0.34, 0.2), (-0.2, -0.06), (-0.08, 0.14), (0.06, -0.24), (0.18, 0.06), (0.36, -0.3)]
    c.line([(cx + x * s, cy + y * s) for x, y in pts], acc, s * 0.06)
    for x, y in pts:
        c.circle(cx + x * s, cy + y * s, s * 0.04, fill=acc)


def w3_index(c, cx, cy, s, col, bg=WH, acc=(40, 150, 90)):
    c.line([(cx - s * 0.42, cy + s * 0.4), (cx + s * 0.44, cy + s * 0.4)], col, s * 0.04)
    c.line([(cx - s * 0.42, cy - s * 0.42), (cx - s * 0.42, cy + s * 0.4)], col, s * 0.04)
    for x in range(0, 8):
        x0 = cx - s * 0.34 + x * s * 0.1
        c.line([(x0, cy - s * 0.26), (x0 + s * 0.05, cy - s * 0.26)], mix(col, bg, 0.3), s * 0.03)
        c.line([(x0, cy + s * 0.26), (x0 + s * 0.05, cy + s * 0.26)], mix(col, bg, 0.3), s * 0.03)
    pts = [(-0.34, 0.2), (-0.18, 0.02), (-0.04, 0.1), (0.1, -0.12), (0.22, -0.2), (0.36, -0.26)]
    c.line([(cx + x * s, cy + y * s) for x, y in pts], acc, s * 0.06)


def w3_door_sensor(c, cx, cy, s, col, bg=WH, acc=(236, 160, 40)):
    c.rect((cx - s * 0.28, cy - s * 0.44, cx + s * 0.2, cy + s * 0.44), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.2, cy - s * 0.36, cx + s * 0.12, cy + s * 0.44), fill=mix(col, bg, 0.75), r=s * 0.02)
    c.circle(cx + s * 0.05, cy + s * 0.04, s * 0.035, fill=col)
    c.rect((cx + s * 0.2, cy - s * 0.2, cx + s * 0.3, cy + s * 0.04), fill=WH, outline=col, width=s * 0.02, r=s * 0.02)
    c.rect((cx + s * 0.12, cy - s * 0.18, cx + s * 0.19, cy + s * 0.02), fill=WH, outline=col, width=s * 0.02, r=s * 0.02)
    for k, r in enumerate((0.12, 0.2, 0.28)):
        c.arc((cx + s * 0.25 - s * r, cy - s * 0.08 - s * r, cx + s * 0.25 + s * r, cy - s * 0.08 + s * r), 300, 360, acc, s * 0.035)


def w3_headset(c, cx, cy, s, col, bg=WH):
    c.arc((cx - s * 0.34, cy - s * 0.42, cx + s * 0.34, cy + s * 0.26), 180, 360, col, s * 0.07)
    for k in (-1, 1):
        c.rect((cx + k * s * 0.34 - s * 0.1, cy - s * 0.1, cx + k * s * 0.34 + s * 0.1, cy + s * 0.2), fill=col, r=s * 0.06)
    c.arc((cx - s * 0.36, cy - s * 0.1, cx + s * 0.24, cy + s * 0.4), 20, 90, col, s * 0.04)
    c.circle(cx - s * 0.02, cy + s * 0.39, s * 0.06, fill=col)


def w3_palm(c, cx, cy, s, col, bg=WH, sand=(236, 200, 120), leaf=None):
    leaf = leaf or col
    c.ellipse((cx - s * 0.46, cy + s * 0.26, cx + s * 0.46, cy + s * 0.46), fill=sand)
    pts = [(cx + s * 0.02 - t * s * 0.12 + math.sin(t * 2) * s * 0.04, cy + s * 0.34 - t * s * 0.6) for t in [i / 8 for i in range(9)]]
    c.line(pts, (150, 104, 60), s * 0.07)
    top = pts[-1]
    for ang in (-160, -120, -60, -20, -90):
        a = math.radians(ang)
        tip = (top[0] + math.cos(a) * s * 0.36, top[1] + math.sin(a) * s * 0.2 + s * 0.12)
        mid = ((top[0] + tip[0]) / 2, (top[1] + tip[1]) / 2 - s * 0.08)
        c.line([top, mid, tip], leaf, s * 0.08)


def w3_umbrella(c, cx, cy, s, col, bg=WH, sand=(236, 200, 120), acc=(232, 88, 70)):
    c.ellipse((cx - s * 0.46, cy + s * 0.28, cx + s * 0.46, cy + s * 0.46), fill=sand)
    c.line([(cx - s * 0.02, cy - s * 0.22), (cx + s * 0.06, cy + s * 0.38)], (120, 90, 60), s * 0.04)
    c.pie((cx - s * 0.44, cy - s * 0.44, cx + s * 0.4, cy + s * 0.12), 180, 360, col)
    for k in range(4):
        a0 = 180 + k * 45
        if k % 2 == 0:
            c.pie((cx - s * 0.44, cy - s * 0.44, cx + s * 0.4, cy + s * 0.12), a0, a0 + 45, acc)


def w3_sun(c, cx, cy, s, col, bg=WH):
    for k in range(12):
        a = math.radians(k * 30)
        c.line([(cx + math.cos(a) * s * 0.3, cy + math.sin(a) * s * 0.3), (cx + math.cos(a) * s * 0.45, cy + math.sin(a) * s * 0.45)], col, s * 0.06)
    c.circle(cx, cy, s * 0.24, fill=col)


def w3_moon(c, cx, cy, s, col, bg=WH):
    c.circle(cx - s * 0.04, cy, s * 0.36, fill=col)
    c.circle(cx + s * 0.12, cy - s * 0.1, s * 0.3, fill=bg)
    for dx, dy, r in ((0.26, 0.14, 0.05), (0.36, -0.3, 0.035), (0.14, 0.34, 0.03)):
        c.circle(cx + dx * s, cy + dy * s, r * s, fill=col)


def w3_boat(c, cx, cy, s, col, bg=WH, sea=(60, 160, 200)):
    c.poly([(cx - s * 0.02, cy - s * 0.44), (cx - s * 0.02, cy + s * 0.14), (cx - s * 0.36, cy + s * 0.14)], col)
    c.poly([(cx + s * 0.04, cy - s * 0.34), (cx + s * 0.04, cy + s * 0.14), (cx + s * 0.3, cy + s * 0.14)], mix(col, bg, 0.4))
    c.poly([(cx - s * 0.42, cy + s * 0.2), (cx + s * 0.42, cy + s * 0.2), (cx + s * 0.3, cy + s * 0.34), (cx - s * 0.3, cy + s * 0.34)], mix(col, (0, 0, 0), 0.2))
    pts = [(cx - s * 0.46 + k * s * 0.023, cy + s * 0.42 + math.sin(k / 2.2) * s * 0.03) for k in range(41)]
    c.line(pts, sea, s * 0.04)


def w3_cocktail(c, cx, cy, s, col, bg=WH, drink=(250, 150, 80), acc=(232, 88, 70)):
    c.poly([(cx - s * 0.3, cy - s * 0.26), (cx + s * 0.3, cy - s * 0.26), (cx, cy + s * 0.1)], drink)
    c.line([(cx - s * 0.3, cy - s * 0.26), (cx + s * 0.3, cy - s * 0.26), (cx, cy + s * 0.1), (cx - s * 0.3, cy - s * 0.26)], col, s * 0.035)
    c.line([(cx, cy + s * 0.1), (cx, cy + s * 0.38)], col, s * 0.04)
    c.rect((cx - s * 0.16, cy + s * 0.36, cx + s * 0.16, cy + s * 0.42), fill=col, r=s * 0.03)
    c.line([(cx + s * 0.06, cy - s * 0.2), (cx + s * 0.24, cy - s * 0.44)], (120, 90, 60), s * 0.025)
    c.pie((cx + s * 0.08, cy - s * 0.56, cx + s * 0.4, cy - s * 0.3), 190, 350, acc)
    c.circle(cx - s * 0.2, cy - s * 0.3, s * 0.08, fill=(250, 220, 80))


def w3_plane(c, cx, cy, s, col, bg=WH):
    body = rotpts([(cx - s * 0.46, cy - s * 0.06), (cx + s * 0.36, cy - s * 0.06), (cx + s * 0.46, cy), (cx + s * 0.36, cy + s * 0.06), (cx - s * 0.46, cy + s * 0.06)], cx, cy, -30)
    c.poly(body, col)
    wing = rotpts([(cx - s * 0.02, cy - s * 0.04), (cx - s * 0.2, cy - s * 0.4), (cx - s * 0.08, cy - s * 0.4), (cx + s * 0.16, cy - s * 0.04)], cx, cy, -30)
    c.poly(wing, col)
    wing2 = rotpts([(cx - s * 0.02, cy + s * 0.04), (cx - s * 0.2, cy + s * 0.4), (cx - s * 0.08, cy + s * 0.4), (cx + s * 0.16, cy + s * 0.04)], cx, cy, -30)
    c.poly(wing2, col)
    tail = rotpts([(cx - s * 0.44, cy - s * 0.04), (cx - s * 0.46, cy - s * 0.2), (cx - s * 0.36, cy - s * 0.2), (cx - s * 0.3, cy - s * 0.04)], cx, cy, -30)
    c.poly(tail, col)


def w3_hotel(c, cx, cy, s, col, bg=WH, acc=(236, 180, 50)):
    c.rect((cx - s * 0.3, cy - s * 0.38, cx + s * 0.3, cy + s * 0.42), fill=col, r=s * 0.03)
    for i in range(3):
        for j in range(4):
            x = cx - s * 0.2 + i * s * 0.2
            y = cy - s * 0.24 + j * s * 0.14
            c.rect((x - s * 0.05, y - s * 0.04, x + s * 0.05, y + s * 0.04), fill=acc if (i + j) % 3 == 0 else mix(col, bg, 0.75), r=s * 0.01)
    c.rect((cx - s * 0.08, cy + s * 0.26, cx + s * 0.08, cy + s * 0.42), fill=bg, r=s * 0.02)


def w3_scissors(c, cx, cy, s, col, bg=WH):
    for k in (-1, 1):
        c.line([(cx - s * 0.2, cy + k * s * 0.14), (cx + s * 0.44, cy - k * s * 0.2)], col, s * 0.07)
        c.circle(cx - s * 0.28, cy + k * s * 0.2, s * 0.14, fill=col)
        c.circle(cx - s * 0.28, cy + k * s * 0.2, s * 0.075, fill=bg)
    c.circle(cx + s * 0.06, cy, s * 0.04, fill=bg)


def w3_split_unit(c, cx, cy, s, col, bg=WH, air=(90, 170, 230)):
    c.rect((cx - s * 0.44, cy - s * 0.3, cx + s * 0.44, cy + s * 0.02), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.38, cy - s * 0.04, cx + s * 0.38, cy - s * 0.0), fill=mix(col, (0, 0, 0), 0.25), r=s * 0.01)
    c.circle(cx + s * 0.32, cy - s * 0.2, s * 0.03, fill=(80, 200, 120))
    for k in range(3):
        x = cx - s * 0.24 + k * s * 0.24
        pts = [(x + math.sin(t / 3) * s * 0.04, cy + s * 0.08 + t * s * 0.03) for t in range(11)]
        c.line(pts, air, s * 0.04)


def w3_outdoor_unit(c, cx, cy, s, col, bg=WH, grille=None, drop=(60, 150, 220)):
    grille = grille or mix(col, (0, 0, 0), 0.35)
    c.rect((cx - s * 0.44, cy - s * 0.3, cx + s * 0.44, cy + s * 0.3), fill=col, r=s * 0.05)
    c.circle(cx - s * 0.1, cy, s * 0.22, fill=mix(col, (0, 0, 0), 0.1), outline=grille, width=s * 0.03)
    for k in range(4):
        a = math.radians(k * 90 + 20)
        c.line([(cx - s * 0.1, cy), (cx - s * 0.1 + math.cos(a) * s * 0.18, cy + math.sin(a) * s * 0.18)], grille, s * 0.04)
    c.rect((cx - s * 0.36, cy + s * 0.3, cx - s * 0.28, cy + s * 0.4), fill=grille)
    c.rect((cx + s * 0.28, cy + s * 0.3, cx + s * 0.36, cy + s * 0.4), fill=grille)
    x, y = cx + s * 0.27, cy - s * 0.02
    c.circle(x, y + s * 0.05, s * 0.09, fill=drop)
    c.poly([(x - s * 0.08, y + s * 0.03), (x + s * 0.08, y + s * 0.03), (x, y - s * 0.14)], drop)


def w3_radiator(c, cx, cy, s, col, bg=WH):
    for k in range(5):
        x = cx - s * 0.32 + k * s * 0.16
        c.rect((x - s * 0.06, cy - s * 0.3, x + s * 0.06, cy + s * 0.3), fill=col, r=s * 0.05)
    c.rect((cx - s * 0.4, cy - s * 0.2, cx + s * 0.4, cy - s * 0.14), fill=col)
    c.rect((cx - s * 0.4, cy + s * 0.14, cx + s * 0.4, cy + s * 0.2), fill=col)
    for k in (-1, 1):
        pts = [(cx + k * s * 0.12 + math.sin(t / 2) * s * 0.03, cy - s * 0.36 - t * s * 0.012) for t in range(9)]
        c.line(pts, (232, 110, 60), s * 0.03)


def w3_folder(c, cx, cy, s, col, bg=WH, paper=WH, acc=(40, 170, 90)):
    c.rect((cx - s * 0.42, cy - s * 0.3, cx - s * 0.08, cy - s * 0.18), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.03)
    c.rect((cx - s * 0.42, cy - s * 0.22, cx + s * 0.42, cy + s * 0.34), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.04)
    c.rect((cx - s * 0.32, cy - s * 0.36, cx + s * 0.3, cy + s * 0.2), fill=paper, r=s * 0.02)
    for k in range(3):
        y = cy - s * 0.24 + k * s * 0.13
        c.rect((cx - s * 0.24, y - s * 0.035, cx - s * 0.16, y + s * 0.035), fill=acc, r=s * 0.01)
        c.rect((cx - s * 0.1, y - s * 0.02, cx + s * 0.22, y + s * 0.02), fill=mix(col, paper, 0.6), r=s * 0.01)
    c.rect((cx - s * 0.42, cy - s * 0.06, cx + s * 0.42, cy + s * 0.34), fill=col, r=s * 0.04)


def w3_wrench(c, cx, cy, s, col, bg=WH):
    p0, p1 = (cx - s * 0.28, cy + s * 0.28), (cx + s * 0.16, cy - s * 0.16)
    c.line([p0, p1], col, s * 0.1)
    c.circle(cx + s * 0.24, cy - s * 0.24, s * 0.17, fill=col)
    c.poly(rotpts([(cx + s * 0.2, cy - s * 0.48), (cx + s * 0.28, cy - s * 0.48), (cx + s * 0.28, cy - s * 0.26), (cx + s * 0.2, cy - s * 0.26)], cx + s * 0.24, cy - s * 0.24, 45), bg)
    c.circle(cx - s * 0.28, cy + s * 0.28, s * 0.07, fill=col)


def w3_bolt_book(c, cx, cy, s, col, bg=WH, acc=(255, 196, 40)):
    c.rect((cx - s * 0.36, cy - s * 0.4, cx + s * 0.32, cy + s * 0.4), fill=col, r=s * 0.04)
    c.rect((cx - s * 0.36, cy - s * 0.4, cx - s * 0.24, cy + s * 0.4), fill=mix(col, (0, 0, 0), 0.25), r=s * 0.03)
    c.poly([(cx + s * 0.06, cy - s * 0.3), (cx - s * 0.12, cy + s * 0.04), (cx + s * 0.02, cy + s * 0.04), (cx - s * 0.04, cy + s * 0.3),
            (cx + s * 0.18, cy - s * 0.06), (cx + s * 0.04, cy - s * 0.06)], acc)


W3_ICONS = {k: v for k, v in dict(globals()).items() if k.startswith("w3_") and callable(v)}
I.ICONS.update(W3_ICONS)


def icon_sheet():
    names = list(W3_ICONS)
    c = C((244, 244, 246))
    n = 5
    for k, nm in enumerate(names):
        x = 110 + (k % n) * 215
        y = 110 + (k // n) * 215
        c.circle(x, y, 90, fill=WH)
        I.ICONS[nm](c, x, y, 120, (40, 60, 100), bg=WH)
        c.text((x, y + 100), nm[3:], "s", 18, (60, 60, 60), anchor="mm")
    img = c.im.convert("RGB").resize((W, W))
    p = "/tmp/claude-0/-home-user-alextest/f5dce882-fce7-5270-9036-ca9a0fe43d5e/scratchpad/w3_icons.png"
    img.save(p)
    print(p)


# =====================================================================  мелкие предметы для сцен
def palm_tree(c, x, by, h, lean=0.12, leaf=(46, 130, 80), trunk=(150, 108, 66), seed=1):
    rnd = random.Random(seed)
    pts = [(x + math.sin(t * 1.4) * h * lean * t + t * h * lean * 0.6, by - t * h) for t in [i / 12 for i in range(13)]]
    for k in range(len(pts) - 1):
        w = h * (0.07 - 0.025 * k / 12)
        c.line([pts[k], pts[k + 1]], trunk, w)
        c.line([(pts[k][0] - w * 0.45, pts[k][1]), (pts[k][0] + w * 0.45, pts[k][1])], mix(trunk, (0, 0, 0), 0.2), 3)
    tx, ty = pts[-1]
    for ang in (-170, -140, -110, -70, -40, -10, 200, 160):
        a = math.radians(ang)
        L = h * rnd.uniform(0.42, 0.55)
        tip = (tx + math.cos(a) * L, ty + math.sin(a) * L * 0.5 + L * 0.35)
        mid = (tx + math.cos(a) * L * 0.5, ty + math.sin(a) * L * 0.5 - L * 0.05)
        nx, ny = -math.sin(a) * L * 0.1, math.cos(a) * L * 0.1
        c.poly([(tx, ty), (mid[0] + nx, mid[1] + ny), tip, (mid[0] - nx * 0.4, mid[1] - ny * 0.4)], mix(leaf, (0, 0, 0), 0.12 * (int(ang) % 2)))
    for k in range(3):
        c.circle(tx - 10 + k * 12, ty + 10, h * 0.025, fill=(120, 84, 40))


def lounger(c, x, y, w, col=WH, frame=(120, 90, 60)):
    """Шезлонг сбоку: x — левый край, y — уровень сиденья."""
    c.poly([(x, y), (x + w * 0.7, y), (x + w * 0.7, y + 14), (x, y + 14)], frame)
    c.poly([(x + w * 0.66, y + 4), (x + w, y - w * 0.34), (x + w + 14, y - w * 0.3), (x + w * 0.72, y + 14)], frame)
    c.rect((x + 4, y - 16, x + w * 0.7, y + 2), fill=col, r=8)
    c.poly([(x + w * 0.68, y - 12), (x + w - 4, y - w * 0.36), (x + w + 10, y - w * 0.32), (x + w * 0.74, y + 2)], col)
    for xx in (x + 12, x + w * 0.62):
        c.rect((xx - 4, y + 12, xx + 4, y + 44), fill=frame)


def lying(c, x, y, w, skin, top, bottom, hair=(70, 50, 40), hat=None):
    """Человек лежит на шезлонге (голова справа, на спинке). Лица нет."""
    c.rect((x + 10, y - 40, x + w * 0.42, y - 12), fill=bottom, r=14)
    c.rect((x + w * 0.38, y - 48, x + w * 0.72, y - 12), fill=top, r=18)
    c.poly([(x + w * 0.66, y - 44), (x + w * 0.86, y - w * 0.26 - 10), (x + w * 0.92, y - w * 0.22), (x + w * 0.74, y - 14)], top)
    hx, hy = x + w * 0.95, y - w * 0.33
    c.circle(hx, hy, w * 0.085, fill=skin)
    c.pie((hx - w * 0.09, hy - w * 0.1, hx + w * 0.09, hy + w * 0.06), 180, 360, hair)
    if hat:
        c.ellipse((hx - w * 0.15, hy - w * 0.08, hx + w * 0.15, hy - w * 0.02), fill=hat)
        c.pie((hx - w * 0.08, hy - w * 0.16, hx + w * 0.08, hy), 180, 360, hat)
    c.rect((x + w * 0.3, y - 36, x + w * 0.5, y - 24), fill=skin, r=6)


def beach_umbrella(c, x, by, h, cols=((232, 88, 70), WH), r=None):
    r = r or h * 0.55
    c.line([(x, by), (x, by - h)], (120, 90, 60), 8)
    top = by - h
    for k in range(8):
        a0 = 180 + k * 22.5
        c.pie((x - r, top - r * 0.45, x + r, top + r * 0.45), a0, a0 + 22.5, cols[k % 2])
    c.circle(x, top - r * 0.45, 7, fill=(120, 90, 60))


def straw_umbrella(c, x, by, h, r=None, col=(206, 170, 100)):
    r = r or h * 0.6
    c.line([(x, by), (x, by - h)], (130, 96, 60), 9)
    top = by - h
    c.poly([(x - r, top + r * 0.25), (x, top - r * 0.3), (x + r, top + r * 0.25)], col)
    for k in range(-5, 6):
        c.line([(x, top - r * 0.28), (x + k * r * 0.19, top + r * 0.25)], mix(col, (0, 0, 0), 0.18), 3)
    for k in range(-6, 7):
        c.line([(x + k * r * 0.16, top + r * 0.2), (x + k * r * 0.16 + 3, top + r * 0.36)], mix(col, (0, 0, 0), 0.12), 4)


def pine(c, x, by, h, col=(40, 96, 70), snow=False):
    c.rect((x - h * 0.04, by - h * 0.12, x + h * 0.04, by), fill=(100, 72, 50))
    for k in range(4):
        y0 = by - h * 0.1 - k * h * 0.22
        wdt = h * (0.36 - k * 0.07)
        c.poly([(x - wdt, y0), (x, y0 - h * 0.34), (x + wdt, y0)], mix(col, (0, 0, 0), 0.06 * (k % 2)))
        if snow:
            c.poly([(x - wdt * 0.5, y0 - h * 0.17), (x, y0 - h * 0.34), (x + wdt * 0.5, y0 - h * 0.17), (x, y0 - h * 0.2)], (248, 250, 255))


def bush(c, x, by, w, col=(70, 130, 80)):
    for dx, dy, r in ((-0.3, -0.2, 0.28), (0.0, -0.32, 0.34), (0.3, -0.2, 0.28), (-0.12, -0.12, 0.26), (0.16, -0.1, 0.26)):
        c.circle(x + dx * w, by + dy * w, r * w, fill=mix(col, (0, 0, 0), 0.08 if dx > 0 else 0))


def mannequin(c, cx, by, s, hair=(120, 76, 44), skin=(236, 206, 180), stand=(60, 60, 70), long_=True):
    """Учебная голова-манекен на штативе (лица нет)."""
    c.rect((cx - 6 * s, by - 120 * s, cx + 6 * s, by), fill=stand)
    c.ellipse((cx - 50 * s, by - 10 * s, cx + 50 * s, by + 8 * s), fill=stand)
    c.rect((cx - 24 * s, by - 160 * s, cx + 24 * s, by - 116 * s), fill=skin, r=10 * s)
    if long_:
        c.rect((cx - 62 * s, by - 250 * s, cx + 62 * s, by - 110 * s), fill=hair, r=40 * s)
    c.ellipse((cx - 52 * s, by - 290 * s, cx + 52 * s, by - 150 * s), fill=skin)
    c.pie((cx - 60 * s, by - 300 * s, cx + 60 * s, by - 190 * s), 180, 360, hair)
    c.pie((cx - 60 * s, by - 280 * s, cx - 20 * s, by - 180 * s), 90, 270, hair)
    c.pie((cx + 20 * s, by - 280 * s, cx + 60 * s, by - 180 * s), 270, 450, hair)


def calc_obj(c, x, y, w, h, body=(52, 58, 70), screen=(200, 230, 210), shown="$?"):
    c.rect((x, y, x + w, y + h), fill=body, r=14)
    c.rect((x + 14, y + 14, x + w - 14, y + h * 0.3), fill=screen, r=6)
    c.text((x + w - 24, y + h * 0.17), shown, "db", h * 0.14, (40, 60, 50), anchor="rm")
    bw = (w - 28 - 3 * 10) / 4
    for i in range(4):
        for j in range(4):
            bx = x + 14 + i * (bw + 10)
            by_ = y + h * 0.38 + j * (h * 0.14)
            c.rect((bx, by_, bx + bw, by_ + h * 0.1), fill=(236, 150, 60) if i == 3 else (220, 224, 230), r=5)


# =====================================================================  «герои» для сеток
def _panel(c, box, c0, c1, r=28):
    A._panel(c, box, c0, c1, r)


def hero_funeral(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        _panel(t, box, (250, 240, 228), (240, 222, 204))
        t.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 38, 3, (170, 110, 90), alpha=30)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        # рамка с фото пары
        fb = (cx - 150, y0 + 36, cx + 150, y1 - 40)
        t.shadow(fb, r=8, alpha=80, blur=10, off=(0, 8))
        t.rect(fb, fill=(150, 104, 70), r=8)
        ib = (fb[0] + 22, fb[1] + 22, fb[2] - 22, fb[3] - 22)
        t.vgrad(ib, (206, 228, 240), (236, 244, 236))
        t.rect((ib[0], ib[3] - 60, ib[2], ib[3]), fill=(150, 196, 130))
        bh = ib[3] - ib[1]
        for dx, top, hair, kind in ((-52, (96, 128, 170), (226, 226, 230), "bald"), (52, (214, 110, 96), (236, 236, 240), "bun")):
            px = cx + dx
            t.rect((px - 58, ib[3] - bh * 0.42, px + 58, ib[3] + 20), fill=top, r=46)
            t.circle(px, ib[3] - bh * 0.56, 36, fill=SKIN[0] if dx > 0 else SKIN[3])
            A._head(t, px, ib[3] - bh * 0.56, 36, SKIN[0] if dx > 0 else SKIN[3], hair, kind)
        # чай слева, полис справа
        t.circle(cx - 320, cy + 10, 92, fill=WH)
        I.ICONS["coins"](t, cx - 320, cy + 14, 120, (30, 46, 84), bg=WH)
        t.circle(cx + 320, cy + 10, 92, fill=WH)
        I.ICONS["doc_heart"](t, cx + 320, cy + 10, 120, (30, 46, 84), bg=WH)
    S.clip_draw(c, box, 28, fn)


def hero_annuity(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        _panel(t, box, (230, 244, 234), (206, 232, 216))
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        t.circle(cx - 300, cy, 100, fill=WH)
        I.ICONS["piggy"](t, cx - 300, cy + 4, 150, (46, 128, 90), bg=WH)
        # стрелка
        t.line([(cx - 180, cy), (cx - 60, cy)], (226, 164, 48), 14)
        t.poly([(cx - 64, cy - 26), (cx - 24, cy), (cx - 64, cy + 26)], (226, 164, 48))
        # календарь 12 месяцев с монетами
        cb = (cx - 4, y0 + 30, cx + 420, y1 - 30)
        t.shadow(cb, r=18, alpha=70, blur=10, off=(0, 6))
        t.rect(cb, fill=WH, r=18)
        t.rect((cb[0], cb[1], cb[2], cb[1] + 44), fill=(24, 44, 86), r=18)
        t.rect((cb[0], cb[1] + 24, cb[2], cb[1] + 44), fill=(24, 44, 86))
        t.text(((cb[0] + cb[2]) / 2, cb[1] + 23), "EVERY MONTH: $?", "db", 22, WH, anchor="mm")
        gw = (cb[2] - cb[0] - 40) / 6
        gh = (cb[3] - cb[1] - 64) / 2
        for k in range(12):
            gx = cb[0] + 20 + (k % 6) * gw + gw / 2
            gy = cb[1] + 54 + (k // 6) * gh + gh / 2
            t.rect((gx - gw * 0.42, gy - gh * 0.42, gx + gw * 0.42, gy + gh * 0.42), fill=(244, 246, 248), r=8)
            t.circle(gx, gy, min(gw, gh) * 0.26, fill=(236, 180, 50), outline=(196, 140, 30), width=3)
    S.clip_draw(c, box, 28, fn)


def hero_va(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        _panel(t, box, (238, 234, 222), (222, 214, 196))
        t.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 40, 3, (26, 40, 72), alpha=26)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        w3_folder(t, cx, cy + 6, 250, (26, 40, 72), bg=(238, 234, 222), acc=(104, 128, 64))
        for x, y, ic, col in ((cx - 330, cy - 20, "calendar", (104, 128, 64)), (cx - 190, cy + 60, "doc_coin", (26, 40, 72)),
                              (cx + 200, cy + 60, "care_hands", (190, 96, 50)), (cx + 330, cy - 20, "house", (26, 40, 72))):
            t.circle(x, y, 64, fill=WH)
            I.ICONS[ic](t, x, y, 84, col, bg=WH)
    S.clip_draw(c, box, 28, fn)


def mini_beach(t, box, sign=None):
    x0, y0, x1, y1 = box
    hz = y0 + (y1 - y0) * 0.5
    t.vgrad((x0, y0, x1, hz), (120, 196, 236), (206, 236, 248))
    t.circle(x1 - 120, y0 + 70, 40, fill=(255, 226, 120))
    t.vgrad((x0, hz, x1, hz + (y1 - y0) * 0.2), (0, 150, 180), (40, 190, 200))
    t.rect((x0, hz + (y1 - y0) * 0.2, x1, y1), fill=(240, 222, 180))
    for k in range(6):
        yy = hz + 12 + k * 9
        t.line([(x0 + 60 + k * 70, yy), (x0 + 130 + k * 70, yy)], WH, 3, alpha=120)
    return hz


def hero_beach(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        hz = mini_beach(t, box)
        base = y1 - 30
        palm_tree(t, x0 + 110, base + 10, 250, lean=0.1, seed=3)
        palm_tree(t, x1 - 90, base + 10, 230, lean=-0.14, seed=5)
        beach_umbrella(t, x0 + 520, base - 20, 170, cols=((240, 96, 72), WH), r=110)
        lounger(t, x0 + 330, base - 40, 170)
        lounger(t, x0 + 560, base - 40, 170)
        lying(t, x0 + 560, base - 40, 170, SKIN[1], (240, 96, 72), (40, 60, 90), hair=(40, 30, 28))
        # табличка «solo adultos»
        sx = x0 + 250
        t.rect((sx - 4, base - 120, sx + 6, base), fill=(130, 96, 60))
        t.rect((sx - 90, base - 170, sx + 96, base - 110), fill=(250, 244, 230), r=8, outline=(130, 96, 60), width=5)
        t.text((sx + 3, base - 140), "SOLO ADULTOS", "db", 20, (0, 110, 130), anchor="mm")
    S.clip_draw(c, box, 28, fn)


def red_sea(t, box, mountains=True):
    x0, y0, x1, y1 = box
    H = y1 - y0
    hz = y0 + H * 0.46
    t.vgrad((x0, y0, x1, hz), (150, 206, 240), (236, 244, 246))
    if mountains:
        rnd = random.Random(7)
        pts = [(x0, hz)]
        x = x0
        while x < x1:
            x += rnd.uniform(60, 140)
            pts.append((x, hz - rnd.uniform(H * 0.05, H * 0.16)))
        pts.append((x1, hz))
        t.poly(pts, (214, 170, 120))
        t.poly([(p[0], p[1] + H * 0.04) if 0 < k < len(pts) - 1 else p for k, p in enumerate(pts)], (196, 150, 104))
    t.vgrad((x0, hz, x1, hz + H * 0.2), (10, 70, 140), (20, 140, 180))
    t.rect((x0, hz + H * 0.2, x1, y1), fill=(242, 222, 176))
    for k in range(7):
        yy = hz + H * 0.03 + k * H * 0.024
        t.line([(x0 + 40 + k * 110, yy), (x0 + 120 + k * 110, yy)], WH, 3, alpha=110)
    return hz


def hero_egypt(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        hz = red_sea(t, box)
        t.circle(x1 - 130, y0 + 60, 36, fill=(255, 214, 110))
        base = y1 - 26
        # отель с куполами слева
        hb = (x0 + 30, hz - 50, x0 + 300, base - 60)
        t.rect(hb, fill=(250, 246, 236))
        for k in range(4):
            for j in range(2):
                t.rect((hb[0] + 24 + k * 64, hb[1] + 30 + j * 56, hb[0] + 56 + k * 64, hb[1] + 66 + j * 56), fill=(120, 170, 200), r=12)
        for dx in (80, 200):
            t.pie((hb[0] + dx - 38, hb[1] - 38, hb[0] + dx + 38, hb[1] + 38), 180, 360, (250, 246, 236))
        palm_tree(t, x0 + 360, base, 230, lean=0.1, seed=11)
        palm_tree(t, x1 - 80, base, 250, lean=-0.12, seed=13)
        straw_umbrella(t, x0 + 560, base - 10, 140, r=100)
        straw_umbrella(t, x0 + 780, base - 10, 140, r=100)
        lounger(t, x0 + 470, base - 30, 150)
        lounger(t, x0 + 690, base - 30, 150)
    S.clip_draw(c, box, 28, fn)


def hero_salon(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        _panel(t, box, (252, 232, 238), (242, 208, 222))
        t.dots((x0 + 20, y0 + 20, x1 - 20, y1 - 20), 36, 3, (150, 60, 110), alpha=28)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        t.ellipse((cx - 200, y1 - 50, cx + 200, y1 - 20), fill=(150, 60, 110), alpha=35)
        mannequin(t, cx, y1 - 30, 0.78, hair=(122, 70, 40))
        for x, y, ic in ((cx - 320, cy - 10, "w3_scissors"), (cx + 320, cy - 10, "clock")):
            t.circle(x, y, 80, fill=WH)
            I.ICONS[ic](t, x, y, 104, (110, 44, 100), bg=WH)
        # расчёска
        t.rect((cx + 150, cy - 110, cx + 176, cy + 10), fill=(110, 44, 100), r=8)
        for k in range(8):
            t.rect((cx + 176, cy - 104 + k * 14, cx + 206, cy - 98 + k * 14), fill=(110, 44, 100), r=3)
    S.clip_draw(c, box, 28, fn)


# =====================================================================  сцены (концепция d), холст 1080
def sc_funeral_kitchen(c):
    """Кухня: пожилая женщина за столом читает бумаги полиса, чай, очки; на стене рамка с фото пары. Лиц нет.
    Верх (до y≈470) закрывает карточка."""
    c.vgrad((0, 0, W, 860), (250, 240, 228), (240, 224, 206))
    c.dots((0, 0, W, 860), 44, 3, (200, 150, 120), alpha=26)
    # окно слева
    WS.window(c, (70, 520, 300, 790), sky0=(170, 212, 236), sky1=(230, 242, 248), frame=(252, 248, 240))
    for (x, y, r) in ((110, 770, 44), (190, 780, 50), (270, 766, 40)):
        c.circle(x, y, r, fill=(128, 178, 112))
    c.rect((50, 792, 320, 808), fill=(236, 226, 212), r=4)
    S.plant(c, 250, 792, 0.45, pot=(200, 104, 80))
    # рамка с фото пары
    fb = (760, 520, 980, 720)
    c.shadow(fb, r=6, alpha=70, blur=8, off=(0, 6))
    c.rect(fb, fill=(150, 104, 70), r=6)
    ib = (fb[0] + 16, fb[1] + 16, fb[2] - 16, fb[3] - 16)
    c.vgrad(ib, (206, 228, 240), (236, 244, 236))
    for dx, top, hair, kind, sk in ((-42, (96, 128, 170), (226, 226, 230), "bald", SKIN[3]), (42, (214, 110, 96), (236, 236, 240), "bun", SKIN[0])):
        px = (ib[0] + ib[2]) / 2 + dx
        c.rect((px - 40, ib[3] - 62, px + 40, ib[3] + 10), fill=top, r=30)
        A._head(c, px, ib[3] - 88, 26, sk, hair, kind)
    c.rect((ib[0], ib[3], ib[2], fb[3] - 4), fill=(150, 104, 70))
    # женщина за столом
    A.seated(c, 480, 960, 1100, 640, SKIN[0], (232, 232, 236), "bun", (136, 160, 132), (70, 80, 110),
             arm_l=(390, 872), arm_r=(580, 868))
    # стол
    c.rect((0, 850, W, W), fill=(196, 150, 108))
    S.wood(c, (0, 862, W, W), (206, 160, 116), (186, 140, 98), lines=7, seed=31)
    c.rect((0, 850, W, 866), fill=(176, 128, 88))
    # бумаги и предметы
    S.paper(c, (360, 872, 620, 1100), -5, head="POLICY OPTIONS", head_size=22, lines=6)
    S.paper(c, (120, 900, 330, 1110), 8, lines=6)
    S.teacup(c, 760, 920, 0.95, rim=(88, 138, 118))
    S.glasses(c, 900, 1000, 0.8)
    S.pen(c, 640, 1040, 700, 960)


def sc_pet_sofa(c):
    """Гостиная: пожилая женщина на диване гладит собаку, кот на ковре, на столике счёт от ветеринара «$?».
    Верх (до y≈330) — заголовок."""
    c.vgrad((0, 0, W, 900), (236, 246, 244), (214, 234, 232))
    c.rect((0, 900, W, W), fill=(200, 160, 120))
    S.wood(c, (0, 906, W, W), (206, 166, 124), (190, 148, 106), lines=5, seed=41)
    c.rect((0, 894, W, 908), fill=(248, 250, 248))
    c.ellipse((140, 950, 1010, 1070), fill=(236, 150, 90))
    c.ellipse((190, 966, 960, 1054), outline=(250, 200, 140), width=6)
    # диван
    SOF = (18, 120, 124)
    c.rect((150, 560, 930, 780), fill=SOF, r=40)
    c.rect((110, 700, 970, 860), fill=mix(SOF, (0, 0, 0), 0.08), r=36)
    c.rect((90, 660, 190, 860), fill=mix(SOF, (0, 0, 0), 0.16), r=40)
    c.rect((890, 660, 990, 860), fill=mix(SOF, (0, 0, 0), 0.16), r=40)
    for x in (140, 940):
        c.rect((x - 8, 860, x + 8, 900), fill=(90, 64, 44))
    c.rect((600, 590, 760, 700), fill=(250, 200, 90), r=24)  # подушка
    # рамки на стене: лапка и собака
    for fb, kind in (((200, 380, 340, 510), "paw"), ((740, 370, 900, 520), "dog")):
        c.shadow(fb, r=6, alpha=60, blur=6, off=(0, 5))
        c.rect(fb, fill=(150, 104, 70), r=6)
        ib = (fb[0] + 12, fb[1] + 12, fb[2] - 12, fb[3] - 12)
        c.rect(ib, fill=(252, 244, 228))
        icx, icy = (ib[0] + ib[2]) / 2, (ib[1] + ib[3]) / 2
        if kind == "paw":
            w3_paw(c, icx, icy, 80, ORG2)
        else:
            w3_dog(c, icx, icy, 100, (196, 150, 96), muzzle=(236, 214, 180), ear=(150, 104, 60))
    # женщина
    A.seated(c, 370, 740, 930, 540, SKIN[3], (230, 230, 234), "short", (226, 120, 90), (60, 70, 100),
             arm_l=(320, 740), arm_r=(575, 630))
    # собака рядом на диване (сидит)
    dx, dy = 660, 690
    c.ellipse((dx - 90, dy - 20, dx + 90, dy + 120), fill=(196, 150, 96))
    c.ellipse((dx - 60, dy + 60, dx + 10, dy + 130), fill=(210, 168, 116))
    w3_dog(c, dx + 10, dy - 70, 190, (196, 150, 96), muzzle=(236, 214, 180), ear=(150, 104, 60))
    # кот на ковре
    kx, ky = 820, 990
    c.ellipse((kx - 110, ky - 40, kx + 80, ky + 34), fill=(110, 110, 120))
    c.line([(kx - 100, ky + 10), (kx - 160, ky + 20), (kx - 170, ky - 10)], (110, 110, 120), 18)
    w3_cat(c, kx + 70, ky - 40, 110, (110, 110, 120))
    # счёт от ветеринара на ковре
    WS.note(c, 150, 990, 190, 130, -8, (255, 250, 236), ["VET BILL", "$?"], size=32, font="db")


def sc_annuity_porch(c):
    """Веранда: пожилой мужчина в кресле-качалке с кружкой, столик с калькулятором и календарём, стикер «$? / month».
    Верх (до y≈420) — плашки заголовка и кнопка."""
    c.vgrad((0, 0, W, 900), (226, 234, 240), (208, 220, 230))
    for y in range(0, 900, 34):
        c.line([(0, y), (W, y)], (190, 204, 216), 3)
    # окно со ставнями
    wb = (700, 470, 940, 780)
    c.rect((wb[0] - 60, wb[1] - 10, wb[0] - 12, wb[3] + 10), fill=(46, 96, 80), r=4)
    c.rect((wb[2] + 12, wb[1] - 10, wb[2] + 60, wb[3] + 10), fill=(46, 96, 80), r=4)
    WS.window(c, wb, sky0=(190, 220, 236), sky1=(236, 244, 248), frame=WH)
    # пол веранды
    c.rect((0, 880, W, W), fill=(176, 130, 90))
    for x in range(-40, W + 40, 90):
        c.line([(x, 880), (x - 60, W)], (150, 106, 70), 4)
    c.rect((0, 872, W, 888), fill=(236, 230, 220))
    # кресло-качалка + мужчина
    CH = (120, 80, 50)
    c.rect((230, 560, 470, 780), fill=CH, r=30)
    for k in range(4):
        c.rect((250 + k * 56, 580, 280 + k * 56, 770), fill=mix(CH, WH, 0.12), r=10)
    A.seated(c, 350, 800, 960, 470, SKIN[2], (206, 206, 210), "short", (70, 110, 160), (80, 76, 70),
             arm_l=(290, 790), arm_r=(440, 720))
    c.rect((210, 780, 490, 812), fill=CH, r=12)
    c.arc((170, 900, 530, 1000), 200, 340, CH, 14)
    for x in (240, 460):
        c.line([(x, 812), (x + (20 if x > 300 else -20), 940)], CH, 12)
    # кружка
    c.rect((432, 690, 480, 740), fill=(236, 164, 48), r=8)
    c.arc((466, 700, 496, 730), 270, 90, (236, 164, 48), 7)
    # столик: калькулятор, календарь, стикер
    c.rect((560, 800, 900, 820), fill=(150, 104, 70), r=6)
    for x in (590, 870):
        c.rect((x - 8, 820, x + 8, 960), fill=(130, 90, 60))
    calc_obj(c, 600, 700, 130, 100, shown="$?")
    I.ICONS["calendar"](c, 820, 740, 120, (46, 128, 90), bg=WH, acc=(236, 180, 50))
    WS.note(c, 940, 600, 190, 130, 5, (255, 226, 110), ["$? /", "month"], size=38, font="db")


def sc_va_table(c):
    """Столовая: пожилой мужчина и консультант с ноутбуком разбирают бумаги по льготам. Без формы, флагов и эмблем.
    Верх (до y≈470) закрывает карточка."""
    c.vgrad((0, 0, W, 860), (238, 236, 228), (224, 220, 208))
    c.dots((0, 0, W, 860), 46, 3, (120, 120, 100), alpha=24)
    WS.window(c, (60, 500, 250, 780), sky0=(176, 210, 232), sky1=(232, 242, 248), frame=(250, 250, 246))
    for (x, y, r) in ((100, 760, 40), (170, 770, 46), (230, 758, 36)):
        c.circle(x, y, r, fill=(120, 170, 110))
    A.wall_clock(c, 980, 560, 44)
    # мужчина слева, консультант справа
    A.seated(c, 380, 960, 1100, 620, SKIN[3], (214, 214, 218), "short", (176, 92, 70), (60, 64, 80),
             arm_l=(310, 872), arm_r=(480, 868))
    A.seated(c, 770, 960, 1100, 600, SKIN[1], (50, 36, 30), "long", (46, 70, 120), (50, 54, 70),
             arm_l=(690, 868), arm_r=(850, 872))
    # стол
    c.rect((0, 850, W, W), fill=(166, 120, 84))
    S.wood(c, (0, 862, W, W), (176, 130, 92), (156, 112, 76), lines=7, seed=51)
    c.rect((0, 850, W, 866), fill=(146, 104, 70))
    # ноутбук (крышкой к зрителю)
    c.rect((660, 760, 880, 880), fill=(60, 66, 80), r=10)
    c.circle(770, 820, 12, fill=(120, 126, 140))
    c.rect((640, 876, 900, 890), fill=(80, 86, 100), r=4)
    # бумаги
    S.paper(c, (270, 880, 540, 1110), -4, head="BENEFITS CHECKLIST", head_size=20, lines=6)
    I.ICONS["w3_folder"](c, 140, 960, 190, (104, 128, 64), bg=(176, 130, 92), acc=(26, 40, 72))
    S.pen(c, 560, 1040, 620, 960)
    WS.mug(c, 980, 930, 0.45, (190, 96, 50))


def sc_security_dusk(c):
    """Дом в сумерках: свет в окнах, фонарь у двери, клавиатура сигнализации, датчики на окнах, прожектор с датчиком движения.
    Верх (до y≈330) — белый заголовок на тёмном небе."""
    c.vgrad((0, 0, W, 560), (22, 30, 62), (70, 72, 120))
    c.vgrad((0, 560, W, 882), (70, 72, 120), (200, 130, 110))
    rnd = random.Random(3)
    for _ in range(30):
        x, y = rnd.uniform(0, W), rnd.uniform(310, 540)
        c.circle(x, y, rnd.uniform(1.5, 3), fill=WH, alpha=int(rnd.uniform(90, 200)))
    c.circle(930, 420, 40, fill=(250, 240, 200))
    c.circle(948, 408, 36, fill=(62, 66, 112))
    # газон
    c.rect((0, 880, W, W), fill=(46, 84, 62))
    c.vgrad((0, 880, W, W), (52, 92, 66), (34, 64, 48))
    c.poly([(470, W), (610, W), (590, 880), (500, 880)], (150, 140, 128))
    # дом
    HB = (190, 560, 890, 890)
    c.poly([(150, 572), (540, 380), (930, 572)], (60, 50, 60))
    c.rect(HB, fill=(214, 200, 180))
    c.rect((HB[0], HB[1], HB[2], HB[1] + 16), fill=(180, 164, 144))
    # окна
    for wx in (250, 690):
        wb = (wx, 620, wx + 150, 760)
        c.rect((wb[0] - 10, wb[1] - 10, wb[2] + 10, wb[3] + 10), fill=(250, 246, 236), r=4)
        c.glow((wb[0] - 20, wb[1] - 20, wb[2] + 20, wb[3] + 20), (255, 210, 120), alpha=120, blur=24, ellipse=False, r=10)
        c.vgrad(wb, (255, 226, 150), (250, 196, 100))
        c.line([((wb[0] + wb[2]) / 2, wb[1]), ((wb[0] + wb[2]) / 2, wb[3])], (250, 246, 236), 8)
        c.line([(wb[0], (wb[1] + wb[3]) / 2), (wb[2], (wb[1] + wb[3]) / 2)], (250, 246, 236), 8)
        c.rect((wb[2] - 30, wb[1] + 6, wb[2] - 16, wb[1] + 34), fill=WH, outline=(90, 90, 100), width=2, r=3)  # датчик
    # дверь, фонарь, клавиатура
    db = (480, 640, 600, 890)
    c.rect((db[0] - 12, db[1] - 12, db[2] + 12, db[3]), fill=(250, 246, 236), r=4)
    c.rect(db, fill=(120, 44, 40), r=4)
    c.circle(580, 770, 7, fill=(236, 190, 90))
    c.glow((430, 560, 650, 760), (255, 200, 110), alpha=110, blur=30)
    c.rect((446, 640, 466, 676), fill=(255, 226, 150), r=6)
    c.rect((620, 720, 660, 780), fill=(40, 44, 54), r=6)
    for i in range(3):
        for j in range(3):
            c.circle(630 + i * 10, 734 + j * 12, 3, fill=(120, 200, 140) if (i, j) == (1, 2) else (200, 204, 210))
    # прожектор с датчиком движения на углу + конус света
    c.poly([(870, 600), (1080, 900), (720, 900)], (255, 230, 170), alpha=40)
    c.rect((856, 588, 890, 610), fill=(50, 54, 64), r=6)
    c.circle(862, 610, 10, fill=(255, 240, 200))
    # кусты
    bush(c, 230, 900, 170, (40, 96, 64))
    bush(c, 850, 900, 180, (40, 96, 64))
    bush(c, 60, 910, 150, (36, 84, 58))
    bush(c, 1020, 910, 150, (36, 84, 58))


def sc_resort_pool(c):
    """Курорт только для взрослых: море, бассейн-инфинити, шезлонги с двумя взрослыми, пальмы, зонтик, коктейль.
    Верх (до y≈470) — плашки заголовка и кнопка."""
    c.vgrad((0, 0, W, 600), (110, 190, 236), (206, 236, 250))
    c.circle(900, 150, 60, fill=(255, 236, 150), alpha=200)
    c.vgrad((0, 600, W, 700), (0, 130, 170), (30, 170, 196))
    for k in range(8):
        y = 616 + k * 11
        c.line([(60 + k * 120, y), (150 + k * 120, y)], WH, 3, alpha=120)
    # бассейн
    c.vgrad((0, 700, W, 820), (60, 206, 220), (120, 226, 232))
    for k in range(6):
        y = 716 + k * 17
        c.line([(40 + (k % 2) * 80 + j * 190, y) for j in range(6)], WH, 3, alpha=90)
    c.rect((0, 812, W, 830), fill=(250, 246, 236))
    # терраса
    c.rect((0, 830, W, W), fill=(238, 220, 186))
    for x in range(0, W + 1, 120):
        c.line([(x, 830), (x, W)], (224, 204, 168), 3)
    palm_tree(c, 80, 1000, 560, lean=0.1, seed=21)
    palm_tree(c, 1010, 1000, 520, lean=-0.14, seed=23)
    beach_umbrella(c, 540, 930, 260, cols=((240, 96, 72), WH), r=160)
    lounger(c, 250, 950, 250)
    lying(c, 250, 950, 250, SKIN[0], (30, 60, 110), (240, 96, 72), hair=(110, 70, 40), hat=(236, 206, 140))
    lounger(c, 590, 950, 250)
    lying(c, 590, 950, 250, SKIN[2], (240, 96, 72), (30, 60, 110), hair=(40, 30, 28))
    # столик с коктейлями
    c.rect((500, 960, 580, 972), fill=(150, 104, 70), r=4)
    c.rect((534, 972, 546, 1030), fill=(130, 90, 60))
    w3_cocktail(c, 524, 924, 60, (80, 90, 110), bg=WH)
    w3_cocktail(c, 562, 924, 60, (80, 90, 110), bg=WH, drink=(236, 90, 120))


def sc_red_sea(c):
    """Красное море: горы пустыни, пляж с соломенными зонтиками, шезлонги, пальмы, отель с куполами; стикер «1 Woche · ? €».
    Верх (до y≈330) — заголовок тёмным по светлому небу."""
    hz = red_sea(c, (0, 0, W, W))
    c.circle(930, 380, 44, fill=(255, 214, 110))
    base = 1000
    hb = (30, hz - 70, 330, 820)
    c.rect(hb, fill=(250, 246, 236))
    for k in range(4):
        for j in range(3):
            c.rect((hb[0] + 26 + k * 70, hb[1] + 40 + j * 70, hb[0] + 62 + k * 70, hb[1] + 84 + j * 70), fill=(110, 166, 200), r=14)
    for dx in (90, 220):
        c.pie((hb[0] + dx - 46, hb[1] - 46, hb[0] + dx + 46, hb[1] + 46), 180, 360, (250, 246, 236))
    palm_tree(c, 380, 960, 440, lean=0.1, seed=31)
    palm_tree(c, 1020, 980, 480, lean=-0.14, seed=33)
    straw_umbrella(c, 560, 930, 220, r=150)
    straw_umbrella(c, 820, 930, 220, r=150)
    lounger(c, 450, 960, 200)
    lounger(c, 700, 960, 200)
    lying(c, 700, 960, 200, SKIN[3], (20, 110, 150), (236, 110, 30), hair=(200, 170, 120), hat=(236, 206, 140))
    WS.note(c, 170, 930, 230, 150, -6, (255, 226, 110), ["1 Woche", "? €"], size=40, font="db")


def sc_electric_workshop(c):
    """Учебная мастерская: стенд с щитком, розетками, выключателями и кабель-каналами; верстак с инструментом; ученик у стенда.
    Верх (до y≈470) закрывает карточка."""
    c.vgrad((0, 0, W, 880), (226, 230, 236), (206, 212, 222))
    # фанерный стенд
    bb = (60, 490, 760, 860)
    c.rect(bb, fill=(222, 190, 140), r=6)
    S.wood(c, (bb[0] + 6, bb[1] + 6, bb[2] - 6, bb[3] - 6), (230, 200, 150), (214, 180, 128), lines=8, seed=61)
    # щиток
    cu = (100, 540, 340, 700)
    c.rect(cu, fill=(244, 244, 246), r=10, outline=(150, 156, 166), width=3)
    c.rect((cu[0] + 16, cu[1] + 50, cu[2] - 16, cu[1] + 120), fill=(60, 66, 80), r=4)
    for k in range(8):
        x = cu[0] + 30 + k * 25
        c.rect((x, cu[1] + 60, x + 16, cu[1] + 110), fill=WH, r=3)
        c.rect((x + 3, cu[1] + 70 + (k % 3) * 4, x + 13, cu[1] + 84 + (k % 3) * 4), fill=(236, 160, 40) if k == 0 else (60, 66, 80), r=2)
    # кабель-каналы
    G = (246, 246, 248)
    c.rect((210, 700, 230, 800), fill=G, outline=(170, 176, 186), width=2)
    c.rect((210, 790, 720, 810), fill=G, outline=(170, 176, 186), width=2)
    c.rect((340, 610, 520, 630), fill=G, outline=(170, 176, 186), width=2)
    c.rect((500, 610, 520, 800), fill=G, outline=(170, 176, 186), width=2)
    # розетки и выключатели
    for x, y, kind in ((400, 660, "sw"), (580, 560, "sock"), (580, 690, "sock"), (680, 560, "sw")):
        c.rect((x - 40, y - 40, x + 40, y + 40), fill=WH, r=8, outline=(170, 176, 186), width=3)
        if kind == "sock":  # британская розетка: заземление сверху, два плоских гнезда снизу, клавиша
            c.rect((x - 26, y - 22, x - 18, y - 2), fill=(60, 60, 70))
            c.rect((x - 36, y + 10, x - 18, y + 17), fill=(60, 60, 70))
            c.rect((x - 6, y + 10, x + 12, y + 17), fill=(60, 60, 70))
            c.rect((x + 18, y - 26, x + 32, y - 4), fill=(236, 238, 240), r=3, outline=(190, 194, 200), width=2)
        else:
            c.rect((x - 16, y - 24, x + 16, y + 24), fill=(236, 238, 240), r=4, outline=(190, 194, 200), width=2)
    c.line([(580, 600), (580, 650)], (160, 160, 170), 8)
    c.line([(420, 700), (440, 790)], (236, 110, 40), 6)
    # верстак
    c.rect((0, 860, W, 890), fill=(120, 86, 58))
    c.rect((0, 890, W, W), fill=(90, 96, 110))
    for x in range(0, W, 180):
        c.rect((x + 10, 900, x + 170, 1060), fill=(100, 106, 120), r=6)
        c.rect((x + 70, 930, x + 110, 940), fill=(160, 166, 176), r=4)
    # инструмент на верстаке
    c.rect((80, 828, 240, 846), fill=(236, 190, 40), r=8)  # отвёртка
    c.rect((240, 832, 330, 842), fill=(160, 166, 176))
    c.rect((360, 790, 450, 860), fill=(236, 190, 40), r=12)  # мультиметр
    c.rect((372, 800, 438, 822), fill=(200, 230, 210), r=4)
    c.circle(405, 840, 11, fill=(60, 60, 70))
    c.circle(560, 824, 38, fill=(220, 70, 50))  # катушка кабеля
    c.circle(560, 824, 14, fill=(90, 96, 110))
    # ученик (спецодежда, каска) с отвёрткой у стенда
    A.standing(c, 900, 1030, 500, SKIN[1], (40, 30, 28), "short", (40, 60, 110), (40, 60, 110), shoe=(40, 40, 44),
               arm_l=(770, 700), arm_r=(960, 830))
    hx, hy = 900, 1030 - 500 * 0.79 - 500 * 0.085 * 1.25
    c.pie((hx - 56, hy - 64, hx + 56, hy + 30), 180, 360, (250, 200, 40))
    c.rect((hx - 64, hy - 20, hx + 64, hy - 8), fill=(250, 200, 40), r=5)
    c.rect((736, 690, 778, 702), fill=(236, 190, 40), r=4)


def sc_salon_training(c):
    """Учебный салон: зеркало, полка с головами-манекенами, ученица с ножницами у манекена, тележка с инструментом.
    Верх (до y≈430) — плашки заголовка и кнопка."""
    c.vgrad((0, 0, W, 900), (252, 236, 240), (242, 214, 224))
    c.dots((0, 0, W, 900), 42, 3, (180, 90, 130), alpha=22)
    # зеркало
    mb = (560, 440, 1000, 860)
    c.rect((mb[0] - 16, mb[1] - 16, mb[2] + 16, mb[3] + 16), fill=(214, 170, 90), r=30)
    c.vgrad(mb, (226, 238, 244), (200, 220, 232))
    c.line([(mb[0] + 60, mb[1] + 40), (mb[0] + 180, mb[1] + 200)], WH, 12, alpha=120)
    for k in range(5):
        c.circle(mb[0] + 40 + k * 90, mb[1] - 40, 14, fill=(255, 240, 200))
    # полка с манекенами у зеркала
    c.rect((540, 860, 1060, 890), fill=(150, 90, 110), r=6)
    mannequin(c, 640, 860, 0.62, hair=(236, 200, 120))
    mannequin(c, 940, 860, 0.62, hair=(60, 40, 30))
    # пол
    c.rect((0, 900, W, W), fill=(236, 226, 230))
    for x in range(-60, W + 60, 120):
        c.line([(x, 900), (x - 40, W)], (220, 206, 212), 3)
    # рабочий манекен на штативе и ученица
    mannequin(c, 420, 870, 1.0, hair=(120, 70, 40))
    A.standing(c, 200, 1030, 560, SKIN[0], (70, 40, 30), "bun", (30, 30, 36), (60, 60, 70), shoe=(30, 30, 34),
               arm_l=(140, 800), arm_r=(330, 690))
    w3_scissors(c, 352, 676, 70, (150, 156, 166), bg=(252, 236, 240))
    # тележка
    tb = (820, 900, 1040, 1060)
    c.rect(tb, fill=(60, 60, 70), r=10)
    c.rect((tb[0] + 10, tb[1] + 10, tb[2] - 10, tb[1] + 60), fill=(90, 90, 100), r=6)
    c.rect((tb[0] + 30, tb[1] - 40, tb[0] + 60, tb[1]), fill=(150, 60, 110), r=6)  # спрей
    c.rect((tb[0] + 100, tb[1] - 24, tb[0] + 200, tb[1]), fill=(110, 44, 100), r=10)  # фен
    c.circle(tb[0] + 200, tb[1] - 12, 16, fill=(110, 44, 100))


def sc_winter_house(c):
    """Зима: деревянный дом, снег, ели, наружный блок теплового насоса «воздух-вода» на подставке, пар. Без логотипа.
    Верх (до y≈470) закрывает карточка."""
    c.vgrad((0, 0, W, 800), (170, 196, 222), (226, 236, 244))
    rnd = random.Random(9)
    pine(c, 90, 830, 420, snow=True)
    pine(c, 1000, 820, 380, snow=True)
    # дом
    HB = (190, 560, 780, 880)
    c.poly([(150, 572), (485, 380), (820, 572)], (70, 60, 60))
    c.poly([(150, 572), (485, 380), (820, 572), (800, 556), (485, 396), (170, 556)], (250, 252, 255))
    c.poly([(170, 556), (485, 396), (800, 556), (780, 540), (485, 410), (190, 540)], (250, 252, 255))
    c.rect(HB, fill=(150, 56, 46))
    for x in range(HB[0], HB[2], 26):
        c.line([(x, HB[1]), (x, HB[3])], (130, 46, 38), 3)
    for wx in (240, 590):
        wb = (wx, 640, wx + 130, 780)
        c.rect((wb[0] - 12, wb[1] - 12, wb[2] + 12, wb[3] + 12), fill=(250, 250, 246))
        c.vgrad(wb, (255, 224, 150), (250, 196, 100))
        c.line([((wb[0] + wb[2]) / 2, wb[1]), ((wb[0] + wb[2]) / 2, wb[3])], (250, 250, 246), 8)
    db = (420, 680, 520, 880)
    c.rect((db[0] - 10, db[1] - 10, db[2] + 10, db[3]), fill=(250, 250, 246))
    c.rect(db, fill=(60, 70, 90))
    # снег
    c.rect((0, 870, W, W), fill=(244, 248, 252))
    c.poly([(0, 880), (200, 862), (460, 876), (760, 860), (W, 874), (W, 900), (0, 900)], (250, 252, 255))
    for x in (100, 330, 640, 960):
        c.ellipse((x - 80, 950 + (x % 3) * 20, x + 80, 980 + (x % 3) * 20), fill=(226, 234, 244))
    # тепловой насос на подставке
    ub = (820, 700, 1040, 850)
    c.rect((ub[0] + 20, ub[3], ub[0] + 36, ub[3] + 50), fill=(90, 96, 110))
    c.rect((ub[2] - 36, ub[3], ub[2] - 20, ub[3] + 50), fill=(90, 96, 110))
    c.shadow(ub, r=10, alpha=60, blur=8, off=(0, 6))
    c.rect(ub, fill=(246, 246, 244), r=10)
    c.circle(ub[0] + 84, (ub[1] + ub[3]) / 2, 58, fill=(210, 214, 220))
    for k in range(9):
        c.circle(ub[0] + 84, (ub[1] + ub[3]) / 2, 58 - k * 6, outline=(150, 156, 166), width=2)
    c.rect((ub[0], ub[1] - 12, ub[2], ub[1] + 6), fill=(250, 252, 255), r=6)
    c.line([(ub[0] + 4, ub[1] + 40), (HB[2], ub[1] + 40)], (200, 200, 204), 8)
    c.line([(ub[0] + 4, ub[1] + 56), (HB[2], ub[1] + 56)], (180, 180, 186), 8)
    for k in range(3):
        pts = [(ub[0] + 70 + k * 30 + math.sin(t / 3) * 8, ub[1] - 20 - t * 8) for t in range(12)]
        c.line(pts, WH, 7, alpha=150)
    for _ in range(70):
        x, y = rnd.uniform(0, W), rnd.uniform(460, 860)
        c.circle(x, y, rnd.uniform(2, 5), fill=WH, alpha=200)


def ee_unit_photo(c, box):
    """Иллюстрация «как на фото» доказанного LT-крео: наружный блок на кронштейнах у стены (сайдинг + кирпич), без логотипа."""
    def fn(t):
        x0, y0, x1, y1 = box
        H = y1 - y0
        split = y0 + H * 0.52
        t.rect((x0, y0, x1, split), fill=(206, 200, 188))
        for y in range(int(y0) + 8, int(split), 30):
            t.rect((x0, y, x1, y + 24), fill=(214, 208, 196))
            t.line([(x0, y + 24), (x1, y + 24)], (176, 168, 156), 3)
        t.rect((x0, split, x1, y1), fill=(160, 70, 56))
        rh = 34
        for j, y in enumerate(range(int(split), int(y1), rh)):
            off = 0 if j % 2 else 60
            t.line([(x0, y), (x1, y)], (206, 196, 184), 4)
            for x in range(int(x0) - off, int(x1), 120):
                t.line([(x, y), (x, y + rh)], (206, 196, 184), 4)
        # трубы
        t.line([(x0 + 610, y0), (x0 + 610, y0 + H * 0.2), (x0 + 600, y0 + H * 0.62)], (80, 86, 96), 16)
        t.line([(x0 + 636, y0), (x0 + 636, y0 + H * 0.2), (x0 + 630, y0 + H * 0.62)], (110, 116, 126), 12)
        t.rect((x0 + 590, y0 + 6, x0 + 650, y0 + 40), fill=(150, 156, 166), r=4)
        # кронштейны
        for bx in (x0 + 150, x0 + 470):
            t.rect((bx, y0 + H * 0.74, bx + 22, y1 - 10), fill=(170, 176, 186))
            t.rect((bx - 30, y0 + H * 0.74, bx + 90, y0 + H * 0.74 + 20), fill=(186, 190, 198))
        # блок
        ub = (x0 + 70, y0 + H * 0.12, x0 + 590, y0 + H * 0.76)
        t.shadow(ub, r=12, alpha=90, blur=12, off=(8, 12))
        t.rect(ub, fill=(244, 244, 242), r=12)
        t.rect((ub[2] - 60, ub[1] + 30, ub[2] - 20, ub[3] - 60), fill=(230, 230, 228), r=6)
        gx, gy, gr = ub[0] + 200, (ub[1] + ub[3]) / 2, (ub[3] - ub[1]) * 0.42
        t.rect((gx - gr - 20, gy - gr - 20, gx + gr + 20, gy + gr + 20), fill=(236, 236, 234), r=8)
        t.circle(gx, gy, gr, fill=(70, 74, 80))
        for k in range(4):
            a = math.radians(k * 90 + 30)
            t.poly([(gx, gy), (gx + math.cos(a) * gr * 0.9, gy + math.sin(a) * gr * 0.9), (gx + math.cos(a + 0.6) * gr * 0.8, gy + math.sin(a + 0.6) * gr * 0.8)], (46, 50, 56))
        for k in range(-9, 10):
            t.line([(gx + k * gr / 10, gy - gr - 20), (gx + k * gr / 10, gy + gr + 20)], (190, 192, 196), 2)
        for k in range(-9, 10):
            t.line([(gx - gr - 20, gy + k * gr / 10), (gx + gr + 20, gy + k * gr / 10)], (190, 192, 196), 2)
        t.circle(gx, gy, 16, fill=(200, 200, 204))
    S.clip_draw(c, box, 22, fn)


SCENES = dict(w3_funeral_kitchen=sc_funeral_kitchen, w3_pet_sofa=sc_pet_sofa, w3_annuity_porch=sc_annuity_porch,
              w3_va_table=sc_va_table, w3_security_dusk=sc_security_dusk, w3_resort_pool=sc_resort_pool,
              w3_red_sea=sc_red_sea, w3_electric_workshop=sc_electric_workshop, w3_salon_training=sc_salon_training,
              w3_winter_house=sc_winter_house)
for _k, _v in SCENES.items():
    setattr(WS, _k, _v)


# =====================================================================  свои раскладки
def ee_grid(P, t):
    """Перенос доказанного LT-крео 0819-GE02 (заголовок + фото блока + 4 плитки площади + красные кнопки) на эстонский.
    Фото заменено Pillow-иллюстрацией без логотипа."""
    p = P["pal"]
    c = C(WH)
    c.hgrad((0, 0, W, W), (70, 140, 200), (240, 140, 60))
    card = (18, 18, 1062, 1062)
    c.rect(card, fill=WH, r=34)
    c.block(t["title"], "db", t.get("size", 58), 44, 980, (20, 22, 26), max_lines=1)
    ee_unit_photo(c, (40, 140, 1040, 600))
    tiles = t["tiles"]
    g = 26
    tw = (1000 - 3 * g) / 4
    for k, lab in enumerate(tiles):
        x0 = 40 + k * (tw + g)
        tb = (x0, 636, x0 + tw, 722)
        c.shadow(tb, r=16, alpha=70, blur=6, off=(0, 4))
        c.rect(tb, fill=(226, 228, 230), r=16, outline=(150, 152, 156), width=3)
        c.rect((tb[0] + 6, tb[1] + 6, tb[2] - 6, (tb[1] + tb[3]) / 2), fill=WH, r=12, alpha=150)
        c.text(((tb[0] + tb[2]) / 2, (tb[1] + tb[3]) / 2 + 2), lab, "sb", 48, (20, 22, 26), anchor="mm")
        bb = (x0, 752, x0 + tw, 884)
        c.shadow(bb, r=18, alpha=110, blur=8, off=(0, 6))
        c.rect(bb, fill=p["btn"], r=18)
        c.rect((bb[0] + 8, bb[1] + 6, bb[2] - 8, bb[1] + 50), fill=WH, r=14, alpha=40)
        l1, l2 = t["btn_lines"]
        sz = min(c.fit(l1, "db", tw - 30, 1, 38), c.fit(l2, "db", tw - 30, 1, 38))
        c.text(((bb[0] + bb[2]) / 2, bb[1] + 44), l1, "db", sz, WH, anchor="mm")
        c.text(((bb[0] + bb[2]) / 2, bb[1] + 92), l2, "db", sz, WH, anchor="mm")
    if t.get("foot"):
        c.block(t["foot"], "sb", 36, 930, 980, (60, 64, 72), max_lines=1)
    return c


def gbp_tags(P, t):
    """Ценники «£?» (как w2b price_tags, но валюта — фунты)."""
    p = P["pal"]
    c = C(p["bg"])
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58))
    tags = t["tags"]
    n = len(tags)
    top = y + 34
    bot = 876
    h = min(190, (bot - top - 26 * (n - 1)) / n)
    top += (bot - top - (h * n + 26 * (n - 1))) / 2
    for k, (ic, lab, col) in enumerate(tags):
        cy = top + k * (h + 26) + h / 2
        ang = (-2.5, 2, -1.5)[k % 3]
        cx = 540 + (-20, 20, -6)[k % 3]
        hx = cx - 380 + h * 0.3
        c.arc((hx - 70, cy - 60, hx + 10, cy + 10), 150, 350, (120, 110, 100), 4)
        L.price_tag(c, cx, cy, 760, h, col, ang, lab, ic, price=t.get("price", "£?"))
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 900, 980, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 998, size=40, fill=p["btn"])
    return c


FN = {"grid": T.grid, "quiz": T.quiz, "compare": T.compare, "scene_d": L.scene_d, "ee_grid": ee_grid, "gbp_tags": gbp_tags}


# =====================================================================  ПАКЕТЫ
# ---------------------------------------------------------------- 1. US · страхование похоронных расходов (final expense)
NAVY1, SAGE1, ROSE1 = (30, 46, 84), (70, 128, 108), (206, 96, 80)
PACKS[1] = dict(
    doc="P60-funeral-insurance-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(252, 246, 238), ink=NAVY1, sub=(96, 100, 110), acc=SAGE1, btn=ROSE1, tile=WH, tile_ink=NAVY1, icon=NAVY1,
             iconbg=(236, 244, 238)),
    a=dict(fn="grid", layout="row4", title="Final expense insurance 2026: monthly cost by cover amount",
           sub="Pick a coverage amount:", size=56, hero=hero_funeral, hero_h=340,
           tiles=[(None, "$5,000"), (None, "$10,000"), (None, "$15,000"), (None, "$25,000")], tile_sub="a month: $?", big_size=46,
           note="сверху панель: рамка с фото пожилой пары, монеты, полис с сердцем; 4 плитки суммы покрытия (в пределах «от нескольких тысяч до ~$25–40 тыс.» из article), взнос «$?»; возраста и «no exam needed» на картинке нет"),
    b=dict(fn="quiz", layout="card", title="Final expense quiz:", title2="the first 2–3 years", size=58,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="Policies with no health questions: what often applies in the first 2–3 years?",
           opts=["Full payout from day one", "A graded death benefit", "A yearly medical exam", "Not sure"],
           pal=dict(bg=(234, 244, 238), bg2=(206, 228, 216), acc=SAGE1, t2=ROSE1, deco=True),
           note="мятный фон, вопрос о механике полиса (graded death benefit 2–3 года — article гипотезы), не о зрителе"),
    c=dict(fn="compare", layout="twocol", title="Final expense or traditional life insurance?",
           sub="What changes – and what each costs a month in 2026", size=54,
           cols=[("FINAL EXPENSE", "doc_heart", SAGE1), ("TRADITIONAL", "doc_sign", NAVY1)],
           rows=[("COVERAGE", "a few thousand to ~$40,000", "larger amounts"),
                 ("HEALTH CHECK", "short questions or none", "often a medical exam"),
                 ("A MONTH", "$?", "$?")],
           foot="Price depends on age, health and insurer",
           note="две колонки; покрытие до ~$40,000 и «короткие вопросы вместо медосмотра» — из article гипотезы, взнос «$?»"),
    d=dict(fn="scene_d", scene="w3_funeral_kitchen", style="card", card_box=(80, 40, 1000, 470), frame=True, font="lserb",
           kicker="FINAL EXPENSE INSURANCE 2026", title="Burial coverage without a medical exam: how it really works",
           sub="The first 2–3 years, and what a month costs", size=56, lines=3, btn_size=40, btn_off=70,
           pal=dict(frame=SAGE1, ink=NAVY1, sub=(96, 100, 110), acc=ROSE1, btn=ROSE1),
           scene_text="POLICY OPTIONS",
           note="кухня: пожилая женщина за столом с бумагами «POLICY OPTIONS», чай, очки, рамка с фото пары; без похоронной символики; карточка в рамке"),
)

# ---------------------------------------------------------------- 2. US · страховка питомцев (владельцы 60+)
ORG2, TEAL2, INK2 = (236, 130, 40), (16, 122, 124), (36, 44, 60)
PACKS[2] = dict(
    doc="P60-pet-insurance-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(253, 247, 238), ink=INK2, sub=(96, 100, 110), acc=ORG2, btn=TEAL2, tile=WH, tile_ink=INK2, icon=INK2,
             iconbg=(252, 232, 210)),
    a=dict(fn="grid", layout="2x2", title="Pet insurance 2026: which plan covers what?", sub="Pick a plan type:", size=58,
           tiles=[("w3_bandage", "Accident-only"), ("w3_pet_steth", "Accident & illness"), ("syringe", "Wellness add-on"),
                  ("w3_old_dog", "Older pets: age limits")],
           note="2×2 типов планов из article гипотезы (accident-only / accident & illness / wellness / возрастные лимиты)"),
    b=dict(fn="quiz", layout="phone", title="Pet insurance quiz:", title2="the rule many owners miss",
           sub="4 things to check before buying a policy", size=56, tag="PET INSURANCE QUIZ", step="Question 1 of 4", prog=0.25,
           q="Are pre-existing conditions usually covered?", opts=["Yes, always", "Usually excluded", "Only for cats", "Not sure"],
           pal=dict(bg=(16, 96, 100), bg2=(8, 52, 60), ink=WH, sub=(200, 230, 230), acc=ORG2, btn=ORG2),
           note="тёмно-бирюзовый фон, телефон с тестом; вопрос о правилах страховки (исключение pre-existing — article), не о зрителе"),
    c=dict(fn="compare", layout="split", title="Pet insurance or a vet savings fund?",
           sub="How each handles an unexpected vet bill", size=56,
           cols=[("PET INSURANCE", "w3_paw", TEAL2, ["Premium: $? a month", "Pays back part of the bill", "Pre-existing: usually excluded"]),
                 ("SAVINGS FUND", "piggy", ORG2, ["Set aside: $? a month", "Covers only what's saved", "Big bill in year one?"])],
           pal=dict(bg=(253, 247, 238), ink=INK2, sub=(96, 100, 110), btn=INK2, vs_bg=INK2, vs_ink=WH),
           note="сплит «страховка vs копилка на ветеринара» (сравнение из article), суммы «$?»"),
    d=dict(fn="scene_d", scene="w3_pet_sofa", style="top", size=56, lines=3, y=44,
           title="Pet insurance for older dogs and cats: what it really costs in 2026",
           sub="Why premiums rise as pets age – and what's excluded", btn_y=1000, btn_size=44,
           pal=dict(ink=INK2, sub=(70, 80, 90), btn=TEAL2),
           scene_text="VET BILL $?",
           note="гостиная: пожилая женщина на диване гладит собаку, кот на ковре, записка «VET BILL $?»; лиц нет"),
)

# ---------------------------------------------------------------- 3. US · аннуитеты
NAVY3, GREEN3, GOLD3, ORG3 = (24, 44, 86), (46, 128, 90), (226, 164, 48), (222, 120, 36)
PACKS[3] = dict(
    doc="P60-annuities-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(244, 249, 245), ink=NAVY3, sub=(90, 100, 110), acc=GREEN3, btn=ORG3, tile=WH, tile_ink=NAVY3, icon=NAVY3,
             iconbg=(226, 242, 232)),
    a=dict(fn="grid", layout="list4", title="Annuities 2026: how each type pays", sub="Pick a type to see how it works", size=58,
           hero=hero_annuity, hero_h=280,
           tiles=[("calendar", "Immediate annuity"), ("padlock", "Fixed annuity"), ("w3_wave", "Variable annuity"),
                  ("w3_index", "Indexed annuity")],
           scene_text="EVERY MONTH: $?",
           note="панель «копилка → календарь с монетой каждый месяц, $?» + 4 строки-кнопки по типам аннуитетов из article"),
    b=dict(fn="quiz", layout="card2x2", title="Annuity quiz:", title2="what sets the monthly payout?", size=60,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="What does annuity income mostly depend on?",
           opts=["Amount invested", "Age when payments start", "Payout option chosen", "All three"],
           pal=dict(bg=(24, 44, 86), bg2=(12, 24, 52), ink=WH, sub=(206, 214, 230), acc=GREEN3, t2=GOLD3, deco=True),
           note="тёмно-синий фон, вопрос о механике аннуитета (факторы выплаты — article), обещаний дохода нет"),
    c=dict(fn="compare", layout="table", title="Immediate or deferred annuity?", sub="When income starts – and what to check first",
           size=56, cols=[("IMMEDIATE", "calendar", GREEN3), ("DEFERRED", "hourglass", GOLD3)],
           rows=[("Payments start", "soon after purchase", "at a future date"), ("Paid for", "set years or life", "set years or life"),
                 ("Surrender period", "check the contract", "often several years"), ("A month", "?", "?")],
           foot="Fees and payout options vary by insurer",
           note="таблица немедленный / отложенный (из article), выплата в месяц — «?»"),
    d=dict(fn="scene_d", scene="w3_annuity_porch", style="bars", y=40,
           bars=[("IMMEDIATE ANNUITY EXPLAINED:", WH, GREEN3), ("HOW THE MONTHLY PAYOUT", NAVY3, None), ("IS WORKED OUT", NAVY3, None)],
           bar_size=74, cond=0.8, btn_y=400, btn_size=44, max_w=960, pal=dict(btn=ORG3),
           scene_text="$? / month",
           note="плашки (формула рабочих крео владельца) + веранда: пожилой мужчина в кресле-качалке с кружкой, столик с калькулятором и календарём, стикер «$? / month»"),
)

# ---------------------------------------------------------------- 4. US · льготы VA (без утверждения, что зритель ветеран)
NAVY4, OLIVE4, AMB4 = (26, 40, 72), (96, 120, 56), (206, 120, 36)
PACKS[4] = dict(
    doc="P60-va-benefits-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(246, 244, 236), ink=NAVY4, sub=(90, 94, 100), acc=OLIVE4, btn=AMB4, tile=WH, tile_ink=NAVY4, icon=NAVY4,
             iconbg=(234, 236, 220)),
    a=dict(fn="grid", layout="list4", title="VA benefits 2026: the 4 main types", sub="Pick one to see how it works", size=58,
           hero=hero_va, hero_h=280,
           tiles=[("doc_coin", "Disability compensation"), ("coins", "Veterans Pension"), ("care_hands", "Aid & Attendance"),
                  ("med_bag", "VA health care")],
           note="панель: папка с чек-листом, календарь, документ, дом, забота — без звёзд, флагов и эмблем; 4 вида льгот из article"),
    b=dict(fn="quiz", layout="card", title="VA benefits quiz:", title2="the Aid & Attendance question", size=58,
           tag="QUIZ", step="Question 1 of 4", prog=0.25,
           q="Can a surviving spouse receive Aid & Attendance?",
           opts=["Yes, in some cases", "No, never", "Only before age 65", "Not sure"],
           pal=dict(bg=(238, 240, 228), bg2=(214, 222, 200), acc=OLIVE4, t2=AMB4, deco=True),
           note="вопрос о правилах VA (Aid & Attendance для вдов/вдовцов — article), не о зрителе"),
    c=dict(fn="compare", layout="twocol", title="Disability compensation or VA Pension?", sub="Two different VA payments – the 2026 basics",
           size=54, cols=[("COMPENSATION", "doc_coin", NAVY4), ("VA PENSION", "coins", OLIVE4)],
           rows=[("BASED ON", "a service-connected condition", "income, assets, wartime service"),
                 ("WHO", "rated 10% to 100%", "65+ or permanently disabled"),
                 ("A MONTH", "? – set by rating", "? – set by income limit")],
           foot="2026 amounts – updated every year",
           note="две колонки; рейтинг 10–100 %, 65+; суммы — «?» (в статье суммы нет, главный 29.09)"),
    d=dict(fn="scene_d", scene="w3_va_table", style="card", card_box=(80, 40, 1000, 470), frame=True, font="lserb",
           kicker="VA BENEFITS 2026", title="The VA benefits many older veterans don't know about",
           sub="Pension, Aid & Attendance, disability pay – a plain guide", size=56, lines=3, btn_size=40, btn_off=70,
           pal=dict(frame=NAVY4, ink=NAVY4, sub=(90, 94, 100), acc=OLIVE4, btn=AMB4),
           scene_text="BENEFITS CHECKLIST",
           note="столовая: пожилой мужчина и консультант с ноутбуком, «BENEFITS CHECKLIST», папка; без формы, флагов, эмблем; о ветеранах в 3-м лице"),
)

# ---------------------------------------------------------------- 5. US · охрана дома для пожилых
NIGHT5, AMB5, TEAL5 = (20, 32, 58), (234, 150, 30), (0, 118, 118)
PACKS[5] = dict(
    doc="P60-home-security-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(242, 245, 250), ink=NIGHT5, sub=(84, 92, 110), acc=AMB5, btn=AMB5, tile=WH, tile_ink=NIGHT5, icon=NIGHT5,
             iconbg=(255, 238, 206)),
    a=dict(fn="grid", layout="2x2", title="Home security for seniors 2026: what to choose?", sub="Pick a part of the system:", size=56,
           tiles=[("w3_door_sensor", "Door & window sensors"), ("pendant", "Panic button pendant"), ("w3_headset", "24/7 monitoring"),
                  ("phone", "Self-monitored app")],
           note="2×2 частей системы из article (датчики, тревожная кнопка, мониторинг 24/7, приложение)"),
    b=dict(fn="quiz", layout="phone", title="Home alarm quiz:", title2="the Wi-Fi question", sub="What to check before choosing a system",
           size=58, tag="HOME ALARM QUIZ", step="Question 1 of 4", prog=0.25,
           q="The home internet goes down. What keeps the alarm working?",
           opts=["Nothing", "Cellular backup", "A louder siren", "Not sure"],
           pal=dict(bg=(24, 38, 70), bg2=(10, 18, 36), ink=WH, sub=(200, 210, 230), acc=AMB5, btn=AMB5),
           note="ночной синий фон, телефон с тестом; вопрос о технике (сотовая связь как резерв — article)"),
    c=dict(fn="compare", layout="split", title="Monitored or self-monitored alarm?", sub="What each one costs a month in 2026", size=56,
           cols=[("MONITORED", "w3_headset", NIGHT5, ["About $20–$60 a month", "A center watches 24/7", "Equipment cost?"]),
                 ("SELF-MONITORED", "phone", TEAL5, ["Low or no monthly fee", "Alerts go to a phone", "Who answers at 3 a.m.?"])],
           pal=dict(bg=(242, 245, 250), ink=NIGHT5, sub=(84, 92, 110), btn=AMB5, vs_bg=AMB5, vs_ink=WH),
           note="сплит; $20–$60/мес — ориентир из sourceNote гипотезы, оборудование — «?»"),
    d=dict(fn="scene_d", scene="w3_security_dusk", style="top", size=58, y=44,
           title="Senior alarm systems 2026: what families compare first",
           sub="Sensors, panic button, battery backup – and the monthly fee", btn_y=1000, btn_size=44,
           pal=dict(ink=WH, sub=(214, 220, 240), btn=AMB5),
           note="дом в сумерках: свет в окнах, фонарь, клавиатура сигнализации, датчики на окнах, прожектор; людей нет, «до/после» нет"),
)

# ---------------------------------------------------------------- 6. ES · отели только для взрослых (путешествия)
TURQ6, CORAL6, NAVY6, YEL6 = (0, 136, 158), (236, 92, 66), (20, 50, 80), (255, 214, 90)
PACKS[6] = dict(
    doc="NT-adults-only-resorts-es-2026-09-30", cta="Más información",
    pal=dict(bg=(252, 247, 236), ink=NAVY6, sub=(90, 96, 104), acc=TURQ6, btn=CORAL6, tile=WH, tile_ink=NAVY6, icon=TURQ6,
             iconbg=(222, 242, 244)),
    a=dict(fn="grid", layout="list4", title="Hoteles solo adultos 2026: ¿dónde?", sub="Elige destino:", size=60,
           hero=hero_beach, hero_h=290,
           tiles=[("w3_palm", "Canarias"), ("w3_umbrella", "Baleares"), ("w3_sun", "Costa del Sol"), ("w3_boat", "Caribe")],
           scene_text="SOLO ADULTOS",
           note="панель пляжа (пальмы, зонт, шезлонги, табличка «SOLO ADULTOS») + 4 строки-направления; без «barato/oferta»"),
    b=dict(fn="quiz", layout="card2x2", title="Resort solo adultos:", title2="¿qué pesa más al elegir?", size=60,
           tag="TEST", step="Pregunta 1 de 3", prog=0.33,
           q="¿Qué es lo primero que miras en un resort solo adultos?",
           opts=["Todo incluido", "Frente a la playa", "Spa y tranquilidad", "Precio por noche"],
           pal=dict(bg=(0, 136, 158), bg2=(0, 84, 104), ink=WH, sub=(210, 240, 244), acc=CORAL6, t2=YEL6, deco=True),
           note="бирюзовый фон, опрос о предпочтениях (не о положении зрителя)"),
    c=dict(fn="compare", layout="twocol", title="¿Hotel solo adultos u hotel familiar?", sub="Qué cambia – y cuánto cuesta la noche en 2026",
           size=54, cols=[("SOLO ADULTOS", "w3_cocktail", TURQ6), ("FAMILIAR", "people2", CORAL6)],
           rows=[("AMBIENTE", "tranquilo, sin niños", "animado, con niños"), ("PISCINA", "zonas de relax", "con zona infantil"),
                 ("PRECIO / NOCHE", "? €", "? €")],
           foot="Todo incluido y frente al mar: qué entra",
           note="две колонки «только для взрослых vs семейный», цена ночи «? €» — цен в гипотезе нет"),
    d=dict(fn="scene_d", scene="w3_resort_pool", style="bars", y=40,
           bars=[("RESORTS EXCLUSIVOS", WH, TURQ6), ("EN LA PLAYA", WH, TURQ6), ("SOLO PARA ADULTOS", NAVY6, YEL6)],
           bar_size=84, cond=0.8, btn_y=420, btn_size=44, max_w=960, pal=dict(btn=CORAL6),
           note="плашки = ключ №1 гипотезы «Resorts exclusivos en la playa para adultos» + курорт: бассейн-инфинити у моря, двое взрослых на шезлонгах, пальмы"),
)

# ---------------------------------------------------------------- 7. DE · Египет всё включено
BLUE7, ORG7, GOLD7 = (16, 64, 130), (232, 104, 30), (255, 214, 110)
PACKS[7] = dict(
    doc="NT-egypt-allinclusive-de-2026-09-30", cta="Mehr erfahren",
    pal=dict(bg=(250, 246, 236), ink=BLUE7, sub=(90, 96, 104), acc=ORG7, btn=ORG7, tile=WH, tile_ink=BLUE7, icon=BLUE7,
             iconbg=(252, 236, 210)),
    a=dict(fn="grid", layout="row4", title="All-Inclusive-Urlaub in Ägypten 2026", sub="Mit Flug und Hotel – wie viele Nächte?", size=58,
           hero=hero_egypt, hero_h=320, tiles=[(None, "7"), (None, "10"), (None, "14"), (None, "21")], tile_sub="Nächte · ? €",
           big_size=86,
           note="панель Красного моря (горы, отель с куполами, пальмы, соломенные зонты) + 4 плитки по числу ночей, цена «? €»; без «günstig»"),
    b=dict(fn="quiz", layout="card", title="Ägypten All-Inclusive:", title2="welcher Badeort passt?", size=58,
           tag="TEST", step="Frage 1 von 3", prog=0.33,
           q="Welcher Badeort am Roten Meer passt zu Ihnen?", opts=["Hurghada", "Marsa Alam", "Sharm El-Sheikh", "El Gouna"],
           pal=dict(bg=(16, 64, 130), bg2=(8, 36, 80), ink=WH, sub=(210, 222, 240), acc=ORG7, t2=GOLD7, deco=True),
           note="синий фон, опрос о выборе курорта (Hurghada — из ключа гипотезы)"),
    c=dict(fn="compare", layout="twocol", title="Pauschalreise oder Flug und Hotel einzeln?",
           sub="Was 1 Woche All-Inclusive in Ägypten 2026 kostet", size=54,
           cols=[("PAUSCHALREISE", "w3_plane", BLUE7), ("EINZELN", "w3_hotel", ORG7)],
           rows=[("FLUG", "inklusive", "separat buchen"), ("TRANSFER", "oft inklusive", "selbst organisieren"),
                 ("PREIS 7 NÄCHTE", "? €", "? €")],
           foot="Hurghada, Marsa Alam, El Gouna im Vergleich",
           note="две колонки «пакет с перелётом vs по отдельности» (ключ «mit Flug und Hotel»), цены «? €»"),
    d=dict(fn="scene_d", scene="w3_red_sea", style="top", size=58, y=44,
           title="Ägypten im November: was 1\u00a0Woche All-Inclusive kostet", sub="Mit Flug und Hotel – Hurghada, Marsa Alam, El Gouna",
           btn_y=1000, btn_size=44, pal=dict(ink=BLUE7, sub=(40, 60, 90), btn=ORG7),
           scene_text="1 Woche ? €",
           note="пляж Красного моря: горы пустыни, отель с куполами, пальмы, соломенные зонты, шезлонги; стикер «1 Woche ? €»; ноябрь — из ключа гипотезы"),
)

# ---------------------------------------------------------------- 8. GB · курс электрика 3 месяца (обучение)
SLATE8, YEL8, ORG8, BLUE8 = (30, 38, 52), (255, 196, 0), (226, 92, 22), (30, 90, 170)
PACKS[8] = dict(
    doc="NT-electrician-course-gb-2026-09-30", cta="Learn more",
    pal=dict(bg=(246, 247, 250), ink=SLATE8, sub=(84, 90, 100), acc=ORG8, btn=ORG8, tile=WH, tile_ink=SLATE8, icon=SLATE8,
             iconbg=(255, 240, 190)),
    a=dict(fn="grid", layout="2x2", title="3 month electrician course 2026", sub="Pick a study format:", size=60,
           tiles=[("w3_sun", "Daytime"), ("w3_moon", "Evenings"), ("calendar", "Weekends"), ("laptop", "Online theory")],
           note="2×2 форматов обучения (днём / вечером / выходные / онлайн) — плейбук «обучение»; без обещаний работы и зарплаты"),
    b=dict(fn="quiz", layout="card", title="Electrician course quiz:", title2="which level comes first?", size=58,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="Which course level do beginners usually start with?", opts=["Level 1", "Level 2", "Level 3", "Not sure"],
           pal=dict(bg=(34, 42, 58), bg2=(16, 20, 30), ink=WH, sub=(210, 214, 224), acc=ORG8, t2=YEL8, deco=True),
           note="графитовый фон, вопрос об уровнях курса, не о зрителе; без диплома/работы/зарплаты"),
    c=dict(fn="compare", layout="twocol", title="Fast-track or college electrician course?", sub="Length, format and cost in 2026", size=54,
           cols=[("FAST-TRACK", "hourglass", ORG8), ("COLLEGE", "cap", BLUE8)],
           rows=[("LENGTH", "about 3 months", "longer, often part time"), ("FORMAT", "intensive days", "weekly classes"),
                 ("COST", "£?", "£?")],
           foot="Levels, practical hours and what's included",
           note="две колонки «ускоренный vs колледж», стоимость «£?» (ключ «electrician course cost», цен в гипотезе нет)"),
    d=dict(fn="scene_d", scene="w3_electric_workshop", style="card", card_box=(80, 40, 1000, 470), frame=True,
           kicker="3 MONTH ELECTRICIAN COURSE", title="What's inside a fast-track course",
           sub="Levels, practical work and course cost in 2026", size=62, btn_size=40, btn_off=70,
           pal=dict(frame=ORG8, ink=SLATE8, sub=(84, 90, 100), acc=ORG8, btn=ORG8),
           note="учебная мастерская: стенд со щитком, розетками и кабель-каналами, верстак с инструментом, ученик в каске; карточка в рамке"),
)

# ---------------------------------------------------------------- 9. GB · короткий курс парикмахера (обучение)
PLUM9, PINK9, INK9 = (110, 44, 100), (214, 84, 132), (50, 30, 50)
PACKS[9] = dict(
    doc="NT-hairdresser-course-gb-2026-09-30", cta="Learn more",
    pal=dict(bg=(253, 244, 247), ink=INK9, sub=(100, 86, 100), acc=PLUM9, btn=PINK9, tile=WH, tile_ink=INK9, icon=PLUM9,
             iconbg=(250, 226, 236)),
    a=dict(fn="grid", layout="row4", title="Hairdressing courses for adults 2026", sub="Pick a format:", size=58,
           hero=hero_salon, hero_h=300,
           tiles=[("w3_scissors", "3-day course"), ("clock", "Part time"), ("w3_moon", "Evenings"), ("laptop", "Online")],
           note="панель: голова-манекен, ножницы, расчёска, часы + 4 плитки форматов (3 дня — из ключа гипотезы)"),
    b=dict(fn="quiz", layout="phone", title="3-day hairdressing course:", title2="what's covered?", sub="What to check before booking",
           size=54, tag="COURSE QUIZ", step="Question 1 of 3", prog=0.33,
           q="What can a 3-day hairdressing course cover?",
           opts=["Cutting basics", "Colour basics", "Blow-dry & styling", "Depends on the course"],
           pal=dict(bg=(110, 44, 100), bg2=(60, 20, 56), ink=WH, sub=(240, 214, 232), acc=PINK9, btn=PINK9),
           note="сливовый фон, телефон с вопросом о содержании курса; без обещаний работы и зарплаты"),
    c=dict(fn="gbp_tags", title="Hairdressing course cost 2026", sub="3 days, part time or online – what each costs", size=58,
           tags=[("w3_scissors", "3-day course", PLUM9), ("clock", "Part-time course", PINK9), ("laptop", "Online course", (40, 120, 140))],
           foot="Kit and practice heads: included or extra?", price="£?",
           note="3 ценника «£?» на штанге — цен в гипотезе нет"),
    d=dict(fn="scene_d", scene="w3_salon_training", style="bars", y=40,
           bars=[("3-DAY HAIRDRESSING", WH, PLUM9), ("COURSE FOR ADULTS:", WH, PLUM9), ("WHAT'S INSIDE", PLUM9, (255, 214, 226))],
           bar_size=80, cond=0.8, btn_y=400, btn_size=44, max_w=960, pal=dict(btn=PINK9),
           note="плашки + учебный салон: зеркало, головы-манекены, ученица с ножницами у манекена, тележка; лиц нет"),
)

# ---------------------------------------------------------------- 10. EE · тепловой насос воздух-вода (товарка, перенос LT 0819-GE02)
RED10, BLUE10, INK10 = (200, 30, 36), (20, 70, 140), (20, 24, 30)
PACKS[10] = dict(
    doc="NT-heatpump-ee-2026-09-30", cta="Uuri lähemalt",
    pal=dict(bg=(236, 242, 250), ink=BLUE10, sub=(80, 90, 104), acc=BLUE10, btn=RED10, tile=WH, tile_ink=INK10, icon=BLUE10,
             iconbg=(222, 234, 248)),
    a=dict(fn="ee_grid", title="Õhk-vesi soojuspumba hind 2026", tiles=["100 m²", "150 m²", "200 m²", "280 m²"],
           btn_lines=("VAATA", "LÄHEMALT"), foot="Hind koos paigaldusega · vali maja pindala", size=58, cta="Vaata lähemalt",
           note="перевод доказанного LT-крео 0819-GE02 (заголовок + блок у стены + 4 плитки m² + красные кнопки): фото заменено иллюстрацией без логотипа, 100 m² — из ключа гипотезы; кнопки «Vaata lähemalt» = LT «Žiūrėti daugiau»"),
    b=dict(fn="quiz", layout="calc", title="Soojuspumba hinnakalkulaator", sub="Hind koos paigaldusega 3 sammuga", size=58,
           steps=[("Pindala", "done"), ("Tüüp", "now"), ("Paigaldus", "todo")], tag="SAMM 2 / 3", step="", prog=0.66,
           q="Millist soojuspumpa vajab 100 m² maja?", opts=["Õhk-õhk", "Õhk-vesi", "Maasoojuspump", "Ei tea"],
           pal=dict(bg=(236, 242, 250), bg2=(206, 222, 242), ink=BLUE10, sub=(70, 84, 104), acc=BLUE10, btn=RED10),
           note="калькулятор-опросник в 3 шага (площадь → тип → монтаж), без цифр цены"),
    c=dict(fn="compare", layout="twocol", title="Õhk-õhk või õhk-vesi soojuspump?", sub="Mida kumbki kütab ja mis on hind koos paigaldusega",
           size=54, cols=[("ÕHK-ÕHK", "w3_split_unit", BLUE10), ("ÕHK-VESI", "w3_outdoor_unit", RED10)],
           rows=[("KÜTAB", "toaõhku", "radiaatoreid ja põrandakütet"), ("SOE TARBEVESI", "ei", "jah"),
                 ("HIND KOOS PAIGALDUSEGA", "? €", "? €")],
           foot="100 m² maja: kumb tuleb odavam?",
           note="две колонки «воздух-воздух vs воздух-вода» (оба типа — ключи гипотезы), цены «? €»"),
    d=dict(fn="scene_d", scene="w3_winter_house", style="card", card_box=(60, 36, 1020, 450), frame=True,
           kicker="SOOJUSPUMP 2026", title="Kui palju maksab õhk-vesi soojuspump 100 m² majale?",
           sub="Hinnad koos paigaldusega: mis mõjutab lõppsummat", size=54, lines=3, btn_size=40, btn_off=64,
           pal=dict(frame=BLUE10, ink=INK10, sub=(80, 90, 104), acc=BLUE10, btn=RED10),
           note="зима: деревянный дом в снегу, ели, наружный блок насоса на подставке с паром; без логотипа; карточка в рамке"),
)


# =====================================================================  сборка
def _clean(s):
    return s.replace("\n", " ").replace("­", "").replace(" ", " ")


def texts(t, cta):
    """Весь текст на картинке — для creatives.json."""
    out = []
    for k in ("kicker", "title", "title2", "sub"):
        if t.get(k):
            out.append(t[k])
    if t.get("bars"):
        out.append(" ".join(b[0] for b in t["bars"]))
    if t.get("steps"):
        out.append(" · ".join(s[0] for s in t["steps"]))
    for k in ("tag", "step", "q"):
        if t.get(k):
            out.append(t[k])
    if t.get("opts"):
        out.append(" / ".join(t["opts"]))
    if t.get("tiles"):
        labs = [x if isinstance(x, str) else x[1] for x in t["tiles"]]
        if t.get("tile_sub"):
            labs = [f"{x} ({t['tile_sub']})" for x in labs]
        tc = t.get("cta", cta)
        out.append(" / ".join(labs) + f" (у каждой «{tc}»)")
    if t.get("cols"):
        out.append(" vs ".join(x[0] for x in t["cols"]))
        for x in t["cols"]:
            if len(x) >= 4 and isinstance(x[-1], list):
                out.append(x[0] + ": " + " · ".join(x[-1]))
    if t.get("rows"):
        out.append(" · ".join(f"{r[0]}: {r[1]} / {r[2]}" for r in t["rows"]))
    if t.get("tags"):
        out.append(" · ".join(f"{x[1]}: {t.get('price', '? €')}" for x in t["tags"]))
    for k in ("foot", "scene_text"):
        if t.get(k):
            out.append(t[k])
    return _clean(" / ".join(out))


def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for Lt in "abcd":
        t = P[Lt]
        PPk = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if t.get("cta"):
            PPk["cta"] = t["cta"]
        if Lt in letters:
            c = FN[t["fn"]](PPk, t)
            c.save(f"{doc}/{Lt}.png")
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png", concept=CONCEPT[Lt] + " — " + t.get("note", ""),
                          text=texts(t, P["cta"]), cta=t.get("cta", P["cta"])))
    os.makedirs(os.path.join(OUT, doc), exist_ok=True)
    with open(os.path.join(OUT, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if a == "icons":
            icon_sheet()
        elif ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
