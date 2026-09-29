"""Волна 4 «Готово к заливу» 30.09 (креативщик w4): 5 пакетов GB/DE × 4 статики 1:1, Pillow.
    python3 w4_ukde.py            — все пакеты
    python3 w4_ukde.py 3 5        — пакеты 3 и 5
    python3 w4_ukde.py 3:a,c      — пакет 3, буквы a и c
Пишет <OUT>/<docId>/<a|b|c|d>.png и <OUT>/<docId>/creatives.json.
Движок — w3_packs (импорт, файл не меняется): шаблоны p60_templates (quiz / compare / grid 2x2), w2b_layouts.scene_d,
иконки p60/w2b/w3. Здесь — свои иконки w4_*, «герои», сцены и раскладки grid6 / pills6 / devices3 / list5 / table3 /
ladder / callouts. Весь текст на картинках — только из статей article_drafts/<docId> (разделы указаны в note).
Без сумм, процентов субсидии, цен, логотипов, гербов, «near you / in Ihrer Nähe», «click here», до/после,
вопросов о возрасте, здоровье, финансах или профессии зрителя."""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w3_packs as W3  # noqa: F401  (регистрирует иконки и сцены w3, тянет весь движок)
from p60_lib import C, W, OUT, mix
import p60_icons as I
import p60_scenes as S
import p60_templates as T
import p60w2_art as A
import w2b_scenes as WS
import w2b_layouts as L

WH = (255, 255, 255)
SKIN = A.SKIN
CONCEPT = W3.CONCEPT
PACKS = {}
INS = (250, 196, 50)       # цвет утеплителя
INS_D = (214, 150, 20)


def icon(c, name, cx, cy, s, col, bg=WH):
    I.ICONS[name](c, cx, cy, s, col, bg=bg)


# =====================================================================  иконки w4 (квадрат s, центр cx, cy)
def w4_sheet(c, cx, cy, s, col, bg=WH, acc=(40, 150, 90)):
    """Ввод данных: экран с таблицей + клавиатура."""
    c.rect((cx - s * 0.44, cy - s * 0.44, cx + s * 0.44, cy + s * 0.14), fill=col, r=s * 0.05)
    x0, y0, x1, y1 = cx - s * 0.39, cy - s * 0.38, cx + s * 0.39, cy + s * 0.08
    c.rect((x0, y0, x1, y1), fill=WH, r=s * 0.02)
    c.rect((x0, y0, x1, y0 + s * 0.09), fill=acc, r=s * 0.02)
    for k in range(1, 4):
        x = x0 + k * (x1 - x0) / 4
        c.line([(x, y0 + s * 0.09), (x, y1)], mix(col, WH, 0.7), s * 0.015)
    for k in range(1, 3):
        y = y0 + s * 0.09 + k * (y1 - y0 - s * 0.09) / 3
        c.line([(x0, y), (x1, y)], mix(col, WH, 0.7), s * 0.015)
    c.rect((x0 + (x1 - x0) / 4 + s * 0.02, y0 + s * 0.13, x0 + (x1 - x0) / 2 - s * 0.02, y0 + s * 0.2), fill=mix(acc, WH, 0.5), r=s * 0.01)
    c.rect((cx - s * 0.46, cy + s * 0.2, cx + s * 0.46, cy + s * 0.44), fill=col, r=s * 0.04)
    for j in range(2):
        for i in range(7):
            x = cx - s * 0.4 + i * s * 0.115
            y = cy + s * 0.25 + j * s * 0.085
            c.rect((x, y, x + s * 0.085, y + s * 0.055), fill=mix(col, WH, 0.75), r=s * 0.01)


def w4_transcribe(c, cx, cy, s, col, bg=WH, acc=(40, 150, 90)):
    """Расшифровка: лист с текстом + наушники."""
    c.rect((cx - s * 0.04, cy - s * 0.4, cx + s * 0.44, cy + s * 0.42), fill=WH, outline=col, width=s * 0.035, r=s * 0.04)
    for k in range(6):
        y = cy - s * 0.26 + k * s * 0.11
        c.rect((cx + s * 0.05, y, cx + s * (0.34 if k % 3 != 2 else 0.2), y + s * 0.04), fill=mix(col, WH, 0.45), r=s * 0.02)
    c.arc((cx - s * 0.46, cy - s * 0.36, cx + s * 0.1, cy + s * 0.2), 180, 360, col, s * 0.07)
    for x in (cx - s * 0.46, cx + s * 0.1):
        c.rect((x - s * 0.07, cy - s * 0.1, x + s * 0.07, cy + s * 0.18), fill=col, r=s * 0.05)
    c.rect((cx - s * 0.52, cy + s * 0.26, cx - s * 0.26, cy + s * 0.3), fill=acc, r=s * 0.02)
    c.rect((cx - s * 0.52, cy + s * 0.34, cx - s * 0.32, cy + s * 0.38), fill=acc, r=s * 0.02)


def w4_moderate(c, cx, cy, s, col, bg=WH, ok=(40, 160, 90), bad=(222, 72, 60)):
    """Модерация: два комментария — одобрен / скрыт."""
    for k, (y, mark) in enumerate(((cy - s * 0.2, "ok"), (cy + s * 0.2, "bad"))):
        x0 = cx - s * 0.46 + k * s * 0.08
        c.rect((x0, y - s * 0.15, x0 + s * 0.66, y + s * 0.15), fill=col if k == 0 else mix(col, bg, 0.35), r=s * 0.06)
        c.poly([(x0 + s * 0.1, y + s * 0.13), (x0 + s * 0.22, y + s * 0.13), (x0 + s * 0.08, y + s * 0.26)], col if k == 0 else mix(col, bg, 0.35))
        c.rect((x0 + s * 0.08, y - s * 0.07, x0 + s * 0.52, y - s * 0.03), fill=WH, r=s * 0.02)
        c.rect((x0 + s * 0.08, y + s * 0.02, x0 + s * 0.4, y + s * 0.06), fill=WH, r=s * 0.02)
        mx, my = cx + s * 0.34, y
        c.circle(mx, my, s * 0.13, fill=ok if mark == "ok" else bad, outline=bg, width=s * 0.03)
        if mark == "ok":
            c.check(mx - s * 0.07, my - s * 0.06, s * 0.14, WH, s * 0.035)
        else:
            c.line([(mx - s * 0.05, my - s * 0.05), (mx + s * 0.05, my + s * 0.05)], WH, s * 0.035)
            c.line([(mx - s * 0.05, my + s * 0.05), (mx + s * 0.05, my - s * 0.05)], WH, s * 0.035)


def w4_proof(c, cx, cy, s, col, bg=WH, red=(222, 60, 50)):
    """Корректура: лист с красной правкой + ручка."""
    c.rect((cx - s * 0.36, cy - s * 0.44, cx + s * 0.26, cy + s * 0.42), fill=WH, outline=col, width=s * 0.035, r=s * 0.03)
    for k in range(6):
        y = cy - s * 0.3 + k * s * 0.12
        c.rect((cx - s * 0.26, y, cx + s * (0.16 if k % 2 else 0.08), y + s * 0.04), fill=mix(col, WH, 0.45), r=s * 0.02)
    c.ellipse((cx - s * 0.3, cy - s * 0.1, cx - s * 0.02, cy + s * 0.04), outline=red, width=s * 0.03)
    c.line([(cx - s * 0.26, cy + s * 0.2), (cx + s * 0.12, cy + s * 0.2)], red, s * 0.03)
    c.line([(cx + s * 0.44, cy - s * 0.36), (cx + s * 0.12, cy + s * 0.1)], red, s * 0.07)
    c.poly([(cx + s * 0.1, cy + s * 0.06), (cx + s * 0.16, cy + s * 0.12), (cx + s * 0.07, cy + s * 0.17)], (240, 214, 170))


def w4_diary(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40)):
    """Админ-поддержка: ежедневник + конверт."""
    c.rect((cx - s * 0.42, cy - s * 0.4, cx + s * 0.18, cy + s * 0.4), fill=col, r=s * 0.04)
    c.rect((cx - s * 0.34, cy - s * 0.34, cx + s * 0.14, cy + s * 0.34), fill=WH, r=s * 0.02)
    for k in range(5):
        y = cy - s * 0.24 + k * s * 0.12
        c.rect((cx - s * 0.28, y, cx - s * 0.2, y + s * 0.05), fill=acc if k in (1, 3) else mix(col, WH, 0.6), r=s * 0.01)
        c.rect((cx - s * 0.16, y + s * 0.01, cx + s * 0.08, y + s * 0.04), fill=mix(col, WH, 0.6), r=s * 0.01)
    for k in range(4):
        c.circle(cx - s * 0.42, cy - s * 0.28 + k * s * 0.18, s * 0.035, fill=bg, outline=col, width=s * 0.02)
    ex0, ey0 = cx + s * 0.02, cy + s * 0.02
    c.rect((ex0, ey0, ex0 + s * 0.44, ey0 + s * 0.3), fill=acc, r=s * 0.03)
    c.line([(ex0 + s * 0.02, ey0 + s * 0.03), (ex0 + s * 0.22, ey0 + s * 0.17), (ex0 + s * 0.42, ey0 + s * 0.03)], WH, s * 0.03)


def w4_age60(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.44, fill=col)
    c.circle(cx, cy, s * 0.36, outline=WH, width=s * 0.03)
    c.text((cx, cy + s * 0.01), "60+", "db", s * 0.28, WH, anchor="mm")


def w4_ship(c, cx, cy, s, col, bg=WH, acc=(0, 132, 170)):
    """Круизный лайнер сбоку (без логотипа)."""
    liner(c, cx - s * 0.5, cy + s * 0.2, s * 1.0, hull=WH, band=col, deck=WH, win=mix(col, WH, 0.35), funnel=col, stripe=acc,
          outline=col, simple=True, hk=0.2)
    pts = [(cx - s * 0.5 + k * s * 0.05, cy + s * 0.33 + math.sin(k / 1.3) * s * 0.02) for k in range(21)]
    c.line(pts, acc, s * 0.035)


def w4_sim(c, cx, cy, s, col, bg=WH, chip=(236, 184, 60)):
    pts = [(cx - s * 0.3, cy - s * 0.42), (cx + s * 0.12, cy - s * 0.42), (cx + s * 0.3, cy - s * 0.24), (cx + s * 0.3, cy + s * 0.42), (cx - s * 0.3, cy + s * 0.42)]
    c.poly(pts, col)
    b = (cx - s * 0.17, cy - s * 0.08, cx + s * 0.17, cy + s * 0.26)
    c.rect(b, fill=chip, r=s * 0.04)
    c.line([(b[0], cy + s * 0.09), (b[2], cy + s * 0.09)], mix(chip, (0, 0, 0), 0.3), s * 0.02)
    c.line([(cx, b[1]), (cx, b[3])], mix(chip, (0, 0, 0), 0.3), s * 0.02)
    c.rect((cx - s * 0.06, cy + s * 0.03, cx + s * 0.06, cy + s * 0.15), fill=chip, r=s * 0.01)


def w4_battery(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    """Домашний накопитель: шкаф-батарея с уровнем заряда."""
    c.rect((cx - s * 0.28, cy - s * 0.44, cx + s * 0.28, cy + s * 0.44), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.2, cy - s * 0.34, cx + s * 0.2, cy + s * 0.3), fill=mix(col, WH, 0.85), r=s * 0.03)
    for k in range(4):
        y = cy + s * 0.2 - k * s * 0.14
        c.rect((cx - s * 0.14, y - s * 0.05, cx + s * 0.14, y + s * 0.05), fill=acc, r=s * 0.02)
    c.poly([(cx + s * 0.04, cy - s * 0.3), (cx - s * 0.06, cy - s * 0.2), (cx + s * 0.0, cy - s * 0.2), (cx - s * 0.04, cy - s * 0.12),
            (cx + s * 0.07, cy - s * 0.23), (cx + s * 0.01, cy - s * 0.23)], (250, 200, 40))


def w4_panel(c, cx, cy, s, col, bg=WH, sun=(250, 190, 30)):
    """Солнечный модуль на стойке + солнце."""
    for k in range(8):
        a = math.radians(k * 45)
        c.line([(cx + s * 0.28 + math.cos(a) * s * 0.13, cy - s * 0.28 + math.sin(a) * s * 0.13),
                (cx + s * 0.28 + math.cos(a) * s * 0.2, cy - s * 0.28 + math.sin(a) * s * 0.2)], sun, s * 0.035)
    c.circle(cx + s * 0.28, cy - s * 0.28, s * 0.09, fill=sun)
    pts = [(cx - s * 0.44, cy + s * 0.2), (cx + s * 0.3, cy + s * 0.2), (cx + s * 0.14, cy - s * 0.1), (cx - s * 0.3, cy - s * 0.1)]
    c.poly(pts, col)
    for k in range(1, 4):
        t = k / 4
        c.line([(pts[0][0] + (pts[1][0] - pts[0][0]) * t, pts[0][1]), (pts[3][0] + (pts[2][0] - pts[3][0]) * t, pts[3][1])], mix(col, WH, 0.45), s * 0.02)
    c.line([((pts[0][0] + pts[3][0]) / 2, (pts[0][1] + pts[3][1]) / 2), ((pts[1][0] + pts[2][0]) / 2, (pts[1][1] + pts[2][1]) / 2)], mix(col, WH, 0.45), s * 0.02)
    c.line([(cx - s * 0.07, cy + s * 0.2), (cx - s * 0.07, cy + s * 0.42)], col, s * 0.05)
    c.rect((cx - s * 0.22, cy + s * 0.4, cx + s * 0.08, cy + s * 0.45), fill=col, r=s * 0.02)


def w4_roof(c, cx, cy, s, col, bg=WH, tile=(196, 84, 60)):
    """Состояние крыши: дом с черепицей и лупой."""
    c.poly([(cx - s * 0.46, cy - s * 0.02), (cx - s * 0.06, cy - s * 0.4), (cx + s * 0.34, cy - s * 0.02)], tile)
    for k in range(1, 4):
        y = cy - s * 0.02 - k * s * 0.09
        dx = (y - (cy - s * 0.02)) / (-0.38 * s) * 0.4 * s
        c.line([(cx - s * 0.46 + dx, y), (cx + s * 0.34 - dx, y)], mix(tile, (0, 0, 0), 0.25), s * 0.02)
    c.rect((cx - s * 0.36, cy - s * 0.02, cx + s * 0.24, cy + s * 0.36), fill=col, r=s * 0.02)
    c.rect((cx - s * 0.12, cy + s * 0.14, cx + s * 0.0, cy + s * 0.36), fill=bg)
    c.circle(cx + s * 0.26, cy + s * 0.18, s * 0.14, fill=bg, outline=(40, 150, 90), width=s * 0.04)
    c.line([(cx + s * 0.36, cy + s * 0.28), (cx + s * 0.46, cy + s * 0.38)], (40, 150, 90), s * 0.06)


# ---------- утепление: мини-дом с выделенной зоной
def zone_house(c, cx, cy, s, col, bg, zone, ins=INS):
    wall = mix(col, bg, 0.82)
    gy = cy + s * 0.2             # уровень земли
    x0, x1 = cx - s * 0.32, cx + s * 0.32
    ey = cy - s * 0.08            # верх стен / перекрытие чердака
    ay = cy - s * 0.44            # конёк
    # подвал
    c.rect((x0 + s * 0.02, gy, x1 - s * 0.02, cy + s * 0.42), fill=mix(col, bg, 0.9), outline=col, width=s * 0.025)
    c.rect((cx - s * 0.48, gy - s * 0.01, cx + s * 0.48, gy + s * 0.015), fill=mix((120, 90, 60), bg, 0.3))
    # стены
    c.rect((x0, ey, x1, gy), fill=wall, outline=col, width=s * 0.03)
    c.rect((cx - s * 0.22, ey + s * 0.07, cx - s * 0.06, ey + s * 0.19), fill=mix((120, 180, 220), bg, 0.3), outline=col, width=s * 0.02)
    c.rect((cx + s * 0.06, ey + s * 0.07, cx + s * 0.22, ey + s * 0.19), fill=mix((120, 180, 220), bg, 0.3), outline=col, width=s * 0.02)
    # крыша
    roof = [(cx - s * 0.42, ey + s * 0.01), (cx, ay), (cx + s * 0.42, ey + s * 0.01)]
    c.poly(roof, mix(col, bg, 0.55))
    c.poly([(cx - s * 0.3, ey), (cx, ay + s * 0.08), (cx + s * 0.3, ey)], mix(col, bg, 0.9))
    hi = mix(ins, (0, 0, 0), 0.0)
    if zone == "attic":
        c.rect((x0 + s * 0.02, ey - s * 0.035, x1 - s * 0.02, ey + s * 0.035), fill=hi, r=s * 0.01)
    elif zone == "roof":
        for sgn in (-1, 1):
            p0 = (cx + sgn * s * 0.3, ey)
            p1 = (cx, ay + s * 0.08)
            c.line([p0, p1], hi, s * 0.075)
        c.circle(cx, ay + s * 0.08, s * 0.035, fill=hi)
    elif zone == "facade":
        c.rect((x0 - s * 0.06, ey, x0, gy), fill=hi, r=s * 0.01)
        c.rect((x1, ey, x1 + s * 0.06, gy), fill=hi, r=s * 0.01)
    elif zone == "cellar":
        c.rect((x0 + s * 0.04, gy + s * 0.015, x1 - s * 0.04, gy + s * 0.075), fill=hi, r=s * 0.01)
    c.line(roof, col, s * 0.03)


def w4_z_attic(c, cx, cy, s, col, bg=WH):
    zone_house(c, cx, cy, s, col, bg, "attic")


def w4_z_roof(c, cx, cy, s, col, bg=WH):
    zone_house(c, cx, cy, s, col, bg, "roof")


def w4_z_facade(c, cx, cy, s, col, bg=WH):
    zone_house(c, cx, cy, s, col, bg, "facade")


def w4_z_cellar(c, cx, cy, s, col, bg=WH):
    zone_house(c, cx, cy, s, col, bg, "cellar")


W4_ICONS = {k: v for k, v in dict(globals()).items() if k.startswith("w4_") and callable(v)}
I.ICONS.update(W4_ICONS)


# =====================================================================  предметы
def liner(c, x0, base, L, hull=WH, band=(20, 40, 80), deck=WH, win=(90, 120, 160), funnel=(20, 40, 80), stripe=(0, 132, 170),
          outline=None, simple=False, boats=(240, 140, 40), hk=0.13):
    """Круизный лайнер, нос справа. x0 — корма, base — ватерлиния, L — длина. Без логотипа и названия."""
    h = L * hk
    top = base - h
    hullp = [(x0, top), (x0 + L, top - h * 0.18), (x0 + L * 0.9, base), (x0 + L * 0.05, base)]
    c.poly(hullp, hull)
    c.poly([(x0 + L * 0.035, base - h * 0.28), (x0 + L * 0.925, base - h * 0.28), (x0 + L * 0.9, base), (x0 + L * 0.05, base)], band)
    decks = [(0.05, 0.86, 0.42), (0.09, 0.8, 0.4), (0.14, 0.74, 0.38)] if not simple else [(0.07, 0.84, 0.5), (0.14, 0.72, 0.46)]
    y = top
    for a, b, hh in decks:
        dh = h * hh
        c.rect((x0 + L * a, y - dh, x0 + L * b, y + 1), fill=deck, r=2)
        if outline:
            c.line([(x0 + L * a, y - dh), (x0 + L * b, y - dh)], outline, max(1.5, L * 0.004))
        n = int((b - a) * L / (L * 0.03))
        for k in range(n):
            wx = x0 + L * a + L * 0.012 + k * L * 0.03
            c.rect((wx, y - dh * 0.72, wx + L * 0.018, y - dh * 0.3), fill=win, r=1)
        y -= dh
    # мостик
    c.rect((x0 + L * 0.66, y - h * 0.34, x0 + L * 0.76, y + 1), fill=deck, r=2)
    c.rect((x0 + L * 0.67, y - h * 0.24, x0 + L * 0.75, y - h * 0.12), fill=mix(band, WH, 0.1), r=1)
    # труба
    fx = x0 + L * 0.3
    c.poly([(fx, y), (fx + L * 0.1, y), (fx + L * 0.09, y - h * 0.62), (fx + L * 0.015, y - h * 0.62)], funnel)
    c.rect((fx + L * 0.01, y - h * 0.44, fx + L * 0.092, y - h * 0.32), fill=stripe)
    # иллюминаторы корпуса
    for k in range(int(L / (L * 0.035))):
        px = x0 + L * 0.08 + k * L * 0.035
        if px > x0 + L * 0.88:
            break
        c.circle(px, top + h * 0.3, max(1.5, L * 0.006), fill=win)
    if not simple:
        for k in range(8):
            bx = x0 + L * 0.12 + k * L * 0.08
            c.rect((bx, top - h * 0.12, bx + L * 0.05, top + h * 0.06), fill=boats, r=L * 0.01)


def volcano_island(c, x0, x1, hz, peak_x, peak_h, col=(120, 140, 110), far=(150, 168, 150), snow=True):
    rnd = random.Random(4)
    pts = [(x0, hz)]
    for k in range(1, 21):
        t = k / 21
        x = x0 + (x1 - x0) * t
        d = abs(x - peak_x) / ((x1 - x0) / 2)
        y = hz - peak_h * max(0.0, 1 - d) ** 1.6 - rnd.uniform(0, peak_h * 0.05)
        pts.append((x, y))
    pts.append((x1, hz))
    c.poly(pts, far)
    c.poly([(p[0], p[1] + peak_h * 0.12) if 0 < k < len(pts) - 1 else p for k, p in enumerate(pts)], col)
    if snow:
        c.poly([(peak_x - peak_h * 0.2, hz - peak_h * 0.82), (peak_x, hz - peak_h * 1.0), (peak_x + peak_h * 0.2, hz - peak_h * 0.82),
                (peak_x + peak_h * 0.08, hz - peak_h * 0.86), (peak_x - peak_h * 0.05, hz - peak_h * 0.8)], (248, 250, 252))


def lifebuoy(c, cx, cy, r, red=(222, 64, 50)):
    c.circle(cx, cy, r, fill=WH)
    for k in range(4):
        c.pie((cx - r, cy - r, cx + r, cy + r), k * 90 + 20, k * 90 + 70, red)
    c.circle(cx, cy, r * 0.55, fill=mix((230, 236, 240), WH, 0.2))
    c.arc((cx - r * 1.05, cy - r * 1.05, cx + r * 1.05, cy + r * 1.05), 0, 360, (200, 200, 200), 2)


def big_button_phone(c, cx, cy, h, body=(44, 48, 60), sos=False, photos=False, screen_txt="10:30"):
    w = h * 0.46
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    c.shadow((x0, y0, x1, y1), r=w * 0.2, alpha=90, blur=12, off=(0, 10))
    c.rect((x0, y0, x1, y1), fill=body, r=w * 0.2)
    # динамик
    for k in range(5):
        c.rect((cx - w * 0.2 + k * w * 0.09, y0 + h * 0.03, cx - w * 0.15 + k * w * 0.09, y0 + h * 0.045), fill=mix(body, WH, 0.35), r=2)
    sc = (x0 + w * 0.1, y0 + h * 0.065, x1 - w * 0.1, y0 + h * 0.25)
    c.rect(sc, fill=(18, 22, 30), r=w * 0.04)
    c.text(((sc[0] + sc[2]) / 2, (sc[1] + sc[3]) / 2 - h * 0.01), screen_txt, "db", h * 0.075, WH, anchor="mm")
    c.rect((sc[0] + w * 0.06, sc[3] - h * 0.03, sc[0] + w * 0.24, sc[3] - h * 0.018), fill=(90, 210, 120), r=2)
    y = y0 + h * 0.275
    if photos:
        pw = (w * 0.8 - 2 * w * 0.05) / 3
        for k, (bgc, hair) in enumerate((((236, 150, 90), (226, 226, 230)), ((90, 150, 210), (60, 44, 36)), ((150, 110, 190), (236, 236, 240)))):
            px = x0 + w * 0.1 + k * (pw + w * 0.05)
            c.rect((px, y, px + pw, y + h * 0.075), fill=bgc, r=w * 0.03)
            c.circle(px + pw / 2, y + h * 0.03, h * 0.016, fill=(238, 200, 170))
            c.pie((px + pw / 2 - h * 0.017, y + h * 0.012, px + pw / 2 + h * 0.017, y + h * 0.04), 180, 360, hair)
            c.rect((px + pw / 2 - h * 0.025, y + h * 0.05, px + pw / 2 + h * 0.025, y + h * 0.075), fill=mix(bgc, (0, 0, 0), 0.2), r=w * 0.02)
        y += h * 0.095
    # зелёная / красная
    kh = h * 0.06
    c.rect((x0 + w * 0.1, y, cx - w * 0.14, y + kh), fill=(52, 170, 90), r=kh / 2)
    c.rect((cx + w * 0.14, y, x1 - w * 0.1, y + kh), fill=(214, 64, 56), r=kh / 2)
    c.circle(cx, y + kh / 2, kh * 0.62, fill=mix(body, WH, 0.25))
    y += kh + h * 0.022
    keys = "123456789*0#"
    kw = (w * 0.8 - 2 * w * 0.05) / 3
    kh2 = (y1 - h * 0.035 - y - 3 * h * 0.014) / 4
    for i, ch in enumerate(keys):
        kx = x0 + w * 0.1 + (i % 3) * (kw + w * 0.05)
        ky = y + (i // 3) * (kh2 + h * 0.014)
        c.rect((kx, ky, kx + kw, ky + kh2), fill=(246, 246, 242), r=kh2 * 0.3)
        c.text((kx + kw / 2, ky + kh2 / 2 + 1), ch, "db", kh2 * 0.62, (30, 34, 44), anchor="mm")
    if sos:
        c.rect((x1 - 4, y0 + h * 0.12, x1 + w * 0.07, y0 + h * 0.2), fill=(214, 44, 44), r=w * 0.03)
    return (x0, y0, x1, y1)


def simple_smartphone(c, cx, cy, h, body=(36, 40, 50), tiles=None):
    w = h * 0.5
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    c.shadow((x0, y0, x1, y1), r=w * 0.14, alpha=90, blur=12, off=(0, 10))
    c.rect((x0, y0, x1, y1), fill=body, r=w * 0.14)
    sc = (x0 + w * 0.06, y0 + h * 0.05, x1 - w * 0.06, y1 - h * 0.05)
    c.rect(sc, fill=(246, 248, 250), r=w * 0.08)
    c.rect((cx - w * 0.14, y0 + h * 0.018, cx + w * 0.14, y0 + h * 0.032), fill=mix(body, WH, 0.2), r=3)
    tiles = tiles or [("Call", (52, 170, 90)), ("Messages", (40, 120, 210)), ("Photos", (236, 150, 40)), ("Video call", (150, 90, 190))]
    g = w * 0.05
    tw = sc[2] - sc[0] - 2 * g
    n = len(tiles)
    th = (sc[3] - sc[1] - h * 0.08 - (n + 1) * g) / n
    fs = min(c.fit(lab, "sb", tw - th * 1.1, 1, th * 0.34, min_size=10) for lab, _ in tiles)
    for k, (lab, col) in enumerate(tiles):
        tx = sc[0] + g
        ty = sc[1] + h * 0.07 + g + k * (th + g)
        c.rect((tx, ty, tx + tw, ty + th), fill=col, r=w * 0.05)
        ic = {"Call": "w4_handset", "Messages": "envelope", "Photos": "w4_photo", "Video call": "videocam", "Video calls": "videocam",
              "News": "w4_news", "Radio": "w4_radio"}.get(lab)
        if ic:
            _mini(c, ic, tx + th * 0.5, ty + th / 2, th * 0.6, WH, col)
        c.text((tx + th * 0.98, ty + th / 2), lab, "sb", fs, WH, anchor="lm")
    c.text((sc[0] + w * 0.08, sc[1] + h * 0.04), "10:30", "sb", h * 0.035, (40, 44, 54), anchor="lm")
    return (x0, y0, x1, y1)


def tablet(c, cx, cy, w, body=(36, 40, 50), tiles=None, stand=True):
    h = w * 0.68
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    if stand:
        c.poly([(cx - w * 0.12, y1 - h * 0.1), (cx + w * 0.12, y1 - h * 0.1), (cx + w * 0.2, y1 + h * 0.2), (cx - w * 0.2, y1 + h * 0.2)], mix(body, WH, 0.3))
    c.shadow((x0, y0, x1, y1), r=w * 0.05, alpha=90, blur=12, off=(0, 10))
    c.rect((x0, y0, x1, y1), fill=body, r=w * 0.05)
    sc = (x0 + w * 0.05, y0 + w * 0.05, x1 - w * 0.05, y1 - w * 0.05)
    c.rect(sc, fill=(246, 248, 250), r=w * 0.02)
    tiles = tiles or [("Video calls", (150, 90, 190)), ("Photos", (236, 150, 40)), ("News", (40, 120, 210)), ("Radio", (52, 170, 90))]
    g = w * 0.025
    tw = (sc[2] - sc[0] - 3 * g) / 2
    th = (sc[3] - sc[1] - 3 * g) / 2
    for k, (lab, col) in enumerate(tiles):
        tx = sc[0] + g + (k % 2) * (tw + g)
        ty = sc[1] + g + (k // 2) * (th + g)
        c.rect((tx, ty, tx + tw, ty + th), fill=col, r=w * 0.02)
        ic = {"Video calls": "videocam", "Photos": "w4_photo", "News": "w4_news", "Radio": "w4_radio"}.get(lab)
        _mini(c, ic, tx + tw / 2, ty + th * 0.38, th * 0.46, WH, col)
        fs = min(c.fit(l_, "sb", tw - 10, 1, th * 0.2, min_size=10) for l_, _ in tiles)
        c.text((tx + tw / 2, ty + th * 0.8), lab, "sb", fs, WH, anchor="mm")
    return (x0, y0, x1, y1)


def _mini(c, name, cx, cy, s, col, bg):
    if name == "w4_handset":
        c.arc((cx - s * 0.36, cy - s * 0.4, cx + s * 0.36, cy + s * 0.36), 110, 250, col, s * 0.18)
        c.circle(cx - s * 0.2, cy - s * 0.28, s * 0.12, fill=col)
        c.circle(cx - s * 0.2, cy + s * 0.26, s * 0.12, fill=col)
    elif name == "w4_photo":
        c.rect((cx - s * 0.42, cy - s * 0.32, cx + s * 0.42, cy + s * 0.32), fill=col, r=s * 0.06)
        c.poly([(cx - s * 0.34, cy + s * 0.24), (cx - s * 0.1, cy - s * 0.06), (cx + s * 0.06, cy + s * 0.1), (cx + s * 0.16, cy),
                (cx + s * 0.34, cy + s * 0.24)], bg)
        c.circle(cx + s * 0.18, cy - s * 0.14, s * 0.07, fill=bg)
    elif name == "w4_news":
        c.rect((cx - s * 0.4, cy - s * 0.3, cx + s * 0.4, cy + s * 0.3), fill=col, r=s * 0.04)
        c.rect((cx - s * 0.32, cy - s * 0.22, cx - s * 0.02, cy + s * 0.02), fill=bg)
        for k in range(4):
            c.rect((cx + s * 0.04, cy - s * 0.2 + k * s * 0.12, cx + s * 0.32, cy - s * 0.16 + k * s * 0.12), fill=bg)
        c.rect((cx - s * 0.32, cy + s * 0.1, cx + s * 0.32, cy + s * 0.14), fill=bg)
    elif name == "w4_radio":
        c.rect((cx - s * 0.42, cy - s * 0.18, cx + s * 0.42, cy + s * 0.32), fill=col, r=s * 0.06)
        c.line([(cx - s * 0.3, cy - s * 0.2), (cx + s * 0.2, cy - s * 0.42)], col, s * 0.05)
        c.circle(cx - s * 0.16, cy + s * 0.07, s * 0.15, fill=bg)
        for k in range(3):
            c.rect((cx + s * 0.06, cy - s * 0.06 + k * s * 0.1, cx + s * 0.32, cy - s * 0.03 + k * s * 0.1), fill=bg)
    else:
        I.ICONS[name](c, cx, cy, s, col, bg=bg)


def solar_roof(c, pts, rows=3, cols=6, panel=(26, 46, 96), line=(120, 150, 200), frame=(200, 206, 214)):
    """Модули на скате: pts — четырёхугольник (нижний левый, нижний правый, верхний правый, верхний левый)."""
    bl, br, tr, tl = pts
    c.poly(pts, frame)

    def lerp(p, q, t):
        return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    g = 0.012
    for i in range(cols):
        for j in range(rows):
            u0, u1 = i / cols + g, (i + 1) / cols - g
            v0, v1 = j / rows + g * 2, (j + 1) / rows - g * 2
            q = [lerp(lerp(bl, br, u0), lerp(tl, tr, u0), v0), lerp(lerp(bl, br, u1), lerp(tl, tr, u1), v0),
                 lerp(lerp(bl, br, u1), lerp(tl, tr, u1), v1), lerp(lerp(bl, br, u0), lerp(tl, tr, u0), v1)]
            c.poly(q, panel)
            c.line([lerp(q[0], q[1], 0.5), lerp(q[3], q[2], 0.5)], line, 1.5)
            c.line([lerp(q[0], q[3], 0.5), lerp(q[1], q[2], 0.5)], line, 1.5)
    c.line([lerp(tl, bl, 0.1), lerp(tr, br, 0.1)], WH, 3, alpha=60)


def roof_method(c, cx, cy, s, method, col=(60, 64, 72), tile=(190, 80, 58), rafter=(150, 104, 66)):
    """Разрез скатной крыши: где лежит утеплитель — 'ceiling' (на перекрытии), 'between' (между стропилами), 'above' (на стропилах)."""
    ax, ay = cx, cy - s * 0.42
    hw = s * 0.48
    by = cy + s * 0.2
    L, R = (cx - hw, by), (cx + hw, by)
    ln = math.hypot(hw, by - ay)
    vx, vy = hw / ln, (ay - by) / ln        # левый скат вверх

    def off(d):
        """Точки левого/правого ската, сдвинутые внутрь на d: (низ слева, конёк, низ справа)."""
        nx, ny = -vy, vx
        px, py = L[0] + nx * d, L[1] + ny * d
        tb = (by - py) / vy
        tA = (cx - px) / vx
        lb = (px + vx * tb, by)
        apex = (cx, py + vy * tA)
        return lb, apex, (2 * cx - lb[0], by)

    def band(d0, d1, fill):
        a0, b0, c0 = off(d0)
        a1, b1, c1 = off(d1)
        c.poly([a0, b0, c0, c1, b1, a1], fill)

    c.poly([L, (ax, ay), R], (236, 232, 224))
    layers = {"ceiling": [(0, 0.07, tile), (0.07, 0.13, rafter)],
              "between": [(0, 0.07, tile), (0.07, 0.17, INS)],
              "above": [(0, 0.07, tile), (0.07, 0.16, INS), (0.16, 0.22, rafter)]}[method]
    for d0, d1, fill in layers:
        band(s * d0, s * d1, fill)
    if method == "between":
        a0, b0, c0 = off(s * 0.07)
        a1, b1, c1 = off(s * 0.17)
        for t in (0.2, 0.45, 0.7):
            for (p0, p1, q0, q1) in ((a0, b0, a1, b1), (c0, b0, c1, b1)):
                pa = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
                pb = (q0[0] + (q1[0] - q0[0]) * t, q0[1] + (q1[1] - q0[1]) * t)
                c.line([pa, pb], rafter, s * 0.03)
    inner = off(s * (0.13 if method == "ceiling" else (0.17 if method == "between" else 0.22)))
    c.poly(list(inner), (250, 248, 242))
    if method == "ceiling":
        la, apex, ra = inner
        t = s * 0.1
        fx = lambda y: la[0] + (apex[0] - la[0]) * (by - y) / (by - apex[1])  # noqa: E731
        c.poly([(fx(by - t), by - t), (2 * cx - fx(by - t), by - t), (ra[0], by), (la[0], by)], INS)
    c.rect((cx - hw - s * 0.02, by, cx + hw + s * 0.02, by + s * 0.05), fill=(170, 170, 176))
    c.rect((cx - hw * 0.86, by + s * 0.05, cx - hw * 0.72, by + s * 0.3), fill=(214, 206, 196))
    c.rect((cx + hw * 0.72, by + s * 0.05, cx + hw * 0.86, by + s * 0.3), fill=(214, 206, 196))
    c.line([L, (ax, ay), R], mix(tile, (0, 0, 0), 0.3), s * 0.012)


# =====================================================================  «герои» (панели в сетках)
def hero_ship(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        H = y1 - y0
        hz = y0 + H * 0.62
        t.vgrad((x0, y0, x1, hz), (110, 186, 230), (214, 236, 248))
        t.circle(x1 - 120, y0 + 64, 34, fill=(255, 232, 150))
        for cx_, cy_, w_ in ((x0 + 180, y0 + 50, 150), (x0 + 520, y0 + 36, 110)):
            t.ellipse((cx_ - w_ / 2, cy_ - 18, cx_ + w_ / 2, cy_ + 18), fill=WH, alpha=200)
            t.ellipse((cx_ - w_ / 4, cy_ - 34, cx_ + w_ / 4, cy_ + 4), fill=WH, alpha=200)
        volcano_island(t, x0 - 40, x0 + 430, hz, x0 + 200, H * 0.34)
        t.vgrad((x0, hz, x1, y1), (20, 104, 156), (40, 150, 190))
        for k in range(9):
            yy = hz + 16 + k * 12
            t.line([(x0 + 30 + (k * 97) % 700, yy), (x0 + 110 + (k * 97) % 700, yy)], WH, 3, alpha=110)
        sx0, sb = x0 + 380, hz + H * 0.2
        liner(t, sx0, sb, 520, band=(20, 44, 90), win=(80, 110, 150), funnel=(20, 44, 90), stripe=(0, 150, 180))
        t.poly([(sx0 + 20, sb - 4), (sx0 - 220, sb - 20), (sx0 - 230, sb - 10), (sx0 + 20, sb + 2)], WH, alpha=120)
        t.poly([(sx0 + 20, sb - 2), (sx0 - 200, sb + 22), (sx0 - 206, sb + 30), (sx0 + 26, sb + 4)], WH, alpha=120)
    S.clip_draw(c, box, 28, fn)


def hero_solar(c, box):
    def fn(t):
        x0, y0, x1, y1 = box
        H = y1 - y0
        gy = y1 - H * 0.16
        t.vgrad((x0, y0, x1, gy), (120, 190, 236), (220, 238, 250))
        sx, sy = x1 - 110, y0 + 64
        for k in range(12):
            a = math.radians(k * 30)
            t.line([(sx + math.cos(a) * 48, sy + math.sin(a) * 48), (sx + math.cos(a) * 66, sy + math.sin(a) * 66)], (255, 200, 60), 6)
        t.circle(sx, sy, 38, fill=(255, 208, 70))
        t.rect((x0, gy, x1, y1), fill=(110, 170, 90))
        t.rect((x0, gy, x1, gy + 8), fill=(96, 150, 80))
        # дом
        hx0, hx1 = x0 + 250, x0 + 700
        wy = gy - H * 0.36
        t.rect((hx0, wy, hx1, gy), fill=(248, 244, 236))
        ay = y0 + H * 0.1
        t.poly([(hx0 - 40, wy + 4), ((hx0 + hx1) / 2 - 60, ay), ((hx0 + hx1) / 2 + 60, ay), (hx1 + 40, wy + 4)], (80, 80, 88))
        solar_roof(t, [(hx0 + 10, wy - 10), (hx1 - 10, wy - 10), ((hx0 + hx1) / 2 + 50, ay + 14), ((hx0 + hx1) / 2 - 50, ay + 14)], rows=2, cols=7)
        for wx in (hx0 + 40, hx0 + 150, hx1 - 130):
            t.rect((wx, wy + 24, wx + 90, wy + 90), fill=(170, 206, 232), outline=WH, width=6)
        t.rect((hx1 - 240, wy + 40, hx1 - 170, gy), fill=(150, 90, 60))
        W3.bush(t, x0 + 150, gy + 6, 120, col=(70, 140, 80))
        W3.bush(t, x1 - 200, gy + 6, 140, col=(60, 130, 76))
    S.clip_draw(c, box, 28, fn)


# =====================================================================  сцены (концепция d)
def sc_remote_desk(c):
    """Домашний рабочий угол: человек со спины в гарнитуре за монитором с таблицей, роутер, стикер «Never pay upfront».
    Верх (до y≈300) — заголовок."""
    c.vgrad((0, 0, W, 800), (236, 244, 242), (214, 228, 226))
    WS.window(c, (70, 360, 290, 610), sky0=(170, 210, 236), sky1=(226, 240, 248))
    c.rect((54, 622, 306, 638), fill=(250, 250, 248), r=4)
    S.plant(c, 120, 622, 0.36, pot=(200, 104, 80))
    # стол
    c.rect((0, 790, W, W), fill=(176, 130, 92))
    S.wood(c, (0, 804, W, W), (186, 140, 100), (166, 120, 84), lines=6, seed=12)
    c.rect((0, 790, W, 806), fill=(150, 106, 72))
    # монитор
    mb = (500, 440, 880, 700)
    c.rect(((mb[0] + mb[2]) / 2 - 16, mb[3], (mb[0] + mb[2]) / 2 + 16, 780), fill=(70, 74, 84))
    c.rect(((mb[0] + mb[2]) / 2 - 80, 772, (mb[0] + mb[2]) / 2 + 80, 792), fill=(70, 74, 84), r=6)
    c.shadow(mb, r=12, alpha=70, blur=10, off=(0, 8))
    c.rect(mb, fill=(40, 44, 54), r=12)
    sc = (mb[0] + 14, mb[1] + 14, mb[2] - 14, mb[3] - 14)
    c.rect(sc, fill=WH, r=4)
    c.rect((sc[0], sc[1], sc[2], sc[1] + 34), fill=(0, 128, 128), r=4)
    for k in range(3):
        c.circle(sc[0] + 20 + k * 22, sc[1] + 17, 6, fill=WH, alpha=180)
    cw = (sc[2] - sc[0]) / 5
    rh = (sc[3] - sc[1] - 34) / 6
    for i in range(1, 5):
        c.line([(sc[0] + i * cw, sc[1] + 34), (sc[0] + i * cw, sc[3])], (214, 220, 226), 2)
    for j in range(1, 6):
        c.line([(sc[0], sc[1] + 34 + j * rh), (sc[2], sc[1] + 34 + j * rh)], (214, 220, 226), 2)
    rnd = random.Random(5)
    for j in range(6):
        for i in range(5):
            if rnd.random() < 0.7:
                bx = sc[0] + i * cw + 10
                by_ = sc[1] + 34 + j * rh + rh * 0.35
                c.rect((bx, by_, bx + cw * rnd.uniform(0.35, 0.8), by_ + rh * 0.3), fill=(150, 160, 172) if i else (60, 80, 100), r=3)
    c.rect((sc[0] + cw + 4, sc[1] + 34 + 2 * rh + 3, sc[0] + 2 * cw - 4, sc[1] + 34 + 3 * rh - 3), outline=(0, 128, 128), width=4)
    WS.note(c, 972, 560, 160, 124, 5, (255, 226, 110), ["Never pay", "upfront"], size=27, font="db")
    # роутер
    c.line([(170, 760), (150, 690)], (60, 64, 74), 6)
    c.line([(250, 760), (272, 690)], (60, 64, 74), 6)
    c.rect((130, 752, 290, 792), fill=(236, 238, 242), r=10)
    for k in range(4):
        c.circle(160 + k * 22, 772, 5, fill=(60, 200, 110))
    for r_ in (24, 40, 56):
        c.arc((210 - r_, 700 - r_, 210 + r_, 700 + r_), 225, 315, (0, 128, 128), 5)
    # клавиатура
    c.rect((560, 800, 880, 836), fill=(226, 228, 232), r=8)
    WS.mug(c, 990, 830, 0.42, (236, 128, 32))
    # человек со спины + кресло + гарнитура
    px, pby, s = 400, 960, 1.4
    WS.senior_back(c, px, pby, s, (0, 110, 120), hair=(220, 220, 226))
    hy, hr = pby - 250 * s, 50 * s
    c.arc((px - hr * 1.15, hy - hr * 1.2, px + hr * 1.15, hy + hr * 1.1), 190, 350, (40, 44, 54), 12)
    for k in (-1, 1):
        c.rect((px + k * hr * 1.08 - 16, hy - 26, px + k * hr * 1.08 + 16, hy + 30), fill=(40, 44, 54), r=12)
    c.line([(px - hr * 1.08, hy + 20), (px - hr * 1.2, hy + 70), (px - hr * 0.9, hy + 96)], (40, 44, 54), 7)
    c.rect((px - 150, 850, px + 150, 1080), fill=(52, 58, 70), r=40)
    c.rect((px - 130, 870, px + 130, 1080), fill=(64, 70, 84), r=30)


def sc_cruise_deck(c):
    """Палуба лайнера: пара 60+ со спины у борта, море, остров с вулканом, спасательный круг. Без логотипов.
    Верх (до y≈420) — плашки и кнопка на небе."""
    c.vgrad((0, 0, W, 640), (70, 150, 210), (206, 232, 246))
    c.glow((780, 380, 980, 580), (255, 240, 190), alpha=160, blur=40)
    c.circle(880, 480, 46, fill=(255, 238, 180))
    for cx_, cy_, w_ in ((180, 520, 220), (640, 560, 180)):
        c.ellipse((cx_ - w_ / 2, cy_ - 20, cx_ + w_ / 2, cy_ + 20), fill=WH, alpha=180)
        c.ellipse((cx_ - w_ / 4, cy_ - 40, cx_ + w_ / 4, cy_ + 6), fill=WH, alpha=180)
    hz = 660
    volcano_island(c, -60, 620, hz, 260, 190)
    c.vgrad((0, hz, W, 900), (18, 96, 150), (36, 146, 190))
    for k in range(14):
        yy = hz + 14 + k * 14
        x = (k * 173) % 900
        c.line([(x, yy), (x + 90 + k * 4, yy)], WH, 3, alpha=110)
    # борт
    c.rect((0, 836, W, W), fill=(246, 248, 250))
    c.rect((0, 836, W, 850), fill=(214, 220, 228))
    c.rect((0, 812, W, 840), fill=(156, 110, 70), r=6)
    c.rect((0, 812, W, 818), fill=(186, 138, 94))
    for x in range(40, W, 160):
        c.rect((x, 850, x + 10, W), fill=(226, 230, 236))
    lifebuoy(c, 170, 950, 74)
    # пара со спины
    WS.senior_back(c, 560, 930, 1.3, (38, 70, 120), hair=(214, 214, 220))
    WS.senior_back(c, 780, 936, 1.22, (206, 96, 84), hair=(236, 236, 240), bun=True)
    c.rect((0, 812, W, 840), fill=(156, 110, 70), r=6)
    c.rect((0, 812, W, 818), fill=(186, 138, 94))
    for x, y in ((470, 820), (660, 824), (690, 824), (870, 828)):
        c.ellipse((x - 20, y - 12, x + 20, y + 12), fill=(236, 196, 164))
    for gx, gy in ((420, 430), (470, 410), (980, 600)):
        c.arc((gx - 18, gy - 8, gx, gy + 8), 200, 340, (60, 70, 90), 4)
        c.arc((gx, gy - 8, gx + 18, gy + 8), 200, 340, (60, 70, 90), 4)


def sc_house_section(c):
    """Разрез дома зимним вечером: утеплитель на перекрытии чердака, между стропилами, на фасаде и под потолком подвала;
    тёплый свет, человек в кресле (без лица), снег. Верх (до y≈330) — плашки и кнопка на тёмном небе."""
    c.vgrad((0, 0, W, 860), (24, 36, 72), (96, 104, 150))
    rnd = random.Random(21)
    for _ in range(40):
        c.circle(rnd.uniform(0, W), rnd.uniform(0, 700), rnd.uniform(1.5, 3), fill=WH, alpha=int(rnd.uniform(80, 200)))
    W3.pine(c, 70, 880, 330, col=(30, 70, 60), snow=True)
    W3.pine(c, 1010, 880, 300, col=(30, 70, 60), snow=True)
    gy = 860
    # грунт в разрезе
    c.rect((0, gy, W, W), fill=(120, 92, 66))
    c.rect((0, gy, W, gy + 18), fill=(244, 248, 252))
    # подвал
    cb = (220, gy, 860, 1050)
    c.rect(cb, fill=(206, 200, 190))
    c.rect((cb[0] + 18, gy + 20, cb[2] - 18, cb[3] - 10), fill=(236, 230, 218))
    c.rect((cb[0] + 18, gy + 20, cb[2] - 18, gy + 42), fill=INS)
    for x in range(int(cb[0]) + 26, int(cb[2]) - 20, 22):
        c.line([(x, gy + 22), (x + 10, gy + 40)], INS_D, 3)
    for k in range(3):
        c.rect((300, 950 + k * 30, 460, 956 + k * 30), fill=(150, 110, 76))
        for j in range(5):
            c.rect((310 + j * 30, 928 + k * 30, 330 + j * 30, 950 + k * 30), fill=((200, 80, 60), (236, 180, 60), (120, 160, 90))[(j + k) % 3], r=4)
    c.rect((640, 930, 800, 1040), fill=(170, 130, 90), r=6)
    c.rect((650, 940, 790, 1030), fill=(186, 146, 104), r=4)
    # стены + фасадная изоляция
    wall = (190, 580, 890, gy)
    c.rect((wall[0] - 26, wall[1], wall[0], gy), fill=INS)
    c.rect((wall[2], wall[1], wall[2] + 26, gy), fill=INS)
    for y in range(wall[1] + 6, gy, 24):
        c.line([(wall[0] - 22, y), (wall[0] - 4, y + 12)], INS_D, 3)
        c.line([(wall[2] + 4, y), (wall[2] + 22, y + 12)], INS_D, 3)
    c.rect(wall, fill=(214, 200, 184))
    room = (wall[0] + 22, wall[1] + 22, wall[2] - 22, gy)
    c.vgrad(room, (255, 230, 180), (250, 208, 150))
    c.rect((room[0], gy - 26, room[2], gy), fill=(176, 128, 88))
    c.glow((360, 600, 760, 860), (255, 236, 170), alpha=120, blur=50)
    # окно в разрезе на правой стене не видно — картина + лампа + кресло с человеком
    c.rect((600, 650, 740, 740), fill=(150, 110, 80), r=4)
    c.rect((612, 662, 728, 728), fill=(170, 206, 220))
    c.poly([(612, 728), (660, 690), (690, 710), (728, 680), (728, 728)], (110, 150, 100))
    c.line([(800, gy - 26), (800, 700)], (80, 70, 60), 6)
    c.poly([(770, 700), (830, 700), (815, 660), (785, 660)], (250, 220, 150))
    A.armchair(c, 430, 780, gy - 26, 230, (170, 70, 60))
    A.seated(c, 430, 772, gy - 26, 330, SKIN[3], (230, 230, 234), "bun", (70, 110, 150), (60, 64, 80),
             arm_l=(372, 790), arm_r=(488, 790))
    c.rect((370, 770, 490, 800), fill=(236, 200, 120), r=8)  # плед
    # перекрытие чердака с изоляцией
    c.rect((wall[0] - 26, 560, wall[2] + 26, 582), fill=(160, 150, 140))
    c.rect((wall[0] + 10, 540, wall[2] - 10, 562), fill=INS)
    for x in range(wall[0] + 14, wall[2] - 14, 22):
        c.line([(x, 542), (x + 10, 560)], INS_D, 3)
    # крыша: черепица + изоляция между стропилами
    apex = (540, 350)
    Lr, Rr = (130, 590), (950, 590)
    c.poly([Lr, apex, Rr], (190, 80, 58))
    inner = [(176, 584), (540, 376), (904, 584)]
    c.poly(inner, INS)
    inner2 = [(214, 562), (540, 400), (866, 562)]
    c.poly(inner2, (236, 226, 208))
    for t in (0.25, 0.5, 0.75):
        for (p0, p1, q0, q1) in (((176, 584), (540, 376), (214, 562), (540, 400)), ((904, 584), (540, 376), (866, 562), (540, 400))):
            pa = (p0[0] + (p1[0] - p0[0]) * t, p0[1] + (p1[1] - p0[1]) * t)
            pb = (q0[0] + (q1[0] - q0[0]) * t, q0[1] + (q1[1] - q0[1]) * t)
            c.line([pa, pb], (150, 104, 66), 8)
    c.rect((470, 500, 540, 540), fill=(186, 146, 104), r=4)
    c.rect((560, 510, 610, 540), fill=(170, 130, 90), r=4)
    c.line([Lr, apex, Rr], (140, 56, 40), 8)
    c.poly([(120, 594), (apex[0], 342), (960, 594), (950, 590), (apex[0], 350), (130, 590)], (248, 250, 255))
    # снег
    for _ in range(60):
        c.circle(rnd.uniform(0, W), rnd.uniform(340, 850), rnd.uniform(2, 4.5), fill=WH, alpha=200)


def sc_solar_offers(c):
    """Кухонный стол: три предложения «ANGEBOT 1/2/3», калькулятор, очки, чай; в окне — крыша пристройки с модулями.
    Верх (до y≈450) закрывает карточка."""
    c.vgrad((0, 0, W, 860), (244, 238, 228), (230, 222, 208))
    c.dots((0, 0, W, 860), 46, 3, (180, 150, 110), alpha=24)
    wb = (700, 470, 1000, 770)

    def view(t):
        x0, y0, x1, y1 = wb
        t.vgrad(wb, (130, 196, 236), (220, 238, 248))
        t.circle(x1 - 50, y0 + 50, 26, fill=(255, 214, 90))
        t.rect((x0, y1 - 70, x1, y1), fill=(110, 170, 90))
        t.poly([(x0 - 10, y1 - 70), (x0 + 60, y0 + 110), (x1 + 10, y0 + 110), (x1 + 10, y1 - 70)], (90, 90, 96))
        solar_roof(t, [(x0 + 30, y1 - 84), (x1 - 10, y1 - 84), (x1 - 10, y0 + 124), (x0 + 80, y0 + 124)], rows=2, cols=5)
    S.clip_draw(c, wb, 0, view)
    c.rect((wb[0] - 14, wb[1] - 14, wb[2] + 14, wb[1]), fill=(250, 250, 246))
    c.rect((wb[0] - 14, wb[3], wb[2] + 14, wb[3] + 14), fill=(250, 250, 246))
    c.rect((wb[0] - 14, wb[1], wb[0], wb[3]), fill=(250, 250, 246))
    c.rect((wb[2], wb[1], wb[2] + 14, wb[3]), fill=(250, 250, 246))
    c.rect(((wb[0] + wb[2]) / 2 - 6, wb[1], (wb[0] + wb[2]) / 2 + 6, wb[3]), fill=(250, 250, 246))
    A.wall_clock(c, 140, 560, 46)
    S.plant(c, 620, 840, 0.4, pot=(70, 120, 150))
    # человек за столом
    A.seated(c, 380, 960, 1100, 620, SKIN[3], (226, 226, 230), "short", (60, 100, 150), (60, 64, 80), arm_l=(300, 872), arm_r=(470, 868))
    c.rect((0, 850, W, W), fill=(196, 150, 108))
    S.wood(c, (0, 862, W, W), (206, 160, 116), (186, 140, 98), lines=7, seed=33)
    c.rect((0, 850, W, 866), fill=(176, 128, 88))
    S.paper(c, (60, 880, 300, 1110), -7, head="ANGEBOT 1", head_size=24, lines=6)
    S.paper(c, (320, 872, 560, 1100), 2, head="ANGEBOT 2", head_size=24, lines=6)
    S.paper(c, (590, 884, 830, 1110), 7, head="ANGEBOT 3", head_size=24, lines=6)
    W3.calc_obj(c, 860, 890, 150, 120, shown="kWp")
    S.glasses(c, 960, 1050, 0.7)
    S.pen(c, 520, 1060, 600, 990)


# =====================================================================  свои раскладки
def _bg(c, p):
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])


def grid6(P, t):
    """6 плиток 3×2: иконка, подпись, у каждой одинаковая кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    top = y + 28
    g = 20
    tw = (980 - 2 * g) / 3
    th = (1044 - top - g) / 2
    for i, (ic, lab) in enumerate(t["tiles"]):
        x0 = 50 + (i % 3) * (tw + g)
        y0 = top + (i // 3) * (th + g)
        c.card((x0, y0, x0 + tw, y0 + th), fill=p["tile"], r=26, sh_alpha=55, blur=12, off=(0, 6))
        cx = x0 + tw / 2
        isz = min(104, th * 0.3)
        c.circle(cx, y0 + th * 0.29, isz * 0.74, fill=p["iconbg"])
        icon(c, ic, cx, y0 + th * 0.29, isz, p["icon"], bg=p["iconbg"])
        fs = 32
        nl = len(c.wrap(lab, c.font("sb", fs), tw - 34))
        ly = y0 + th * 0.63 - nl * c.lh("sb", fs, 1.05) / 2 - 4
        c.block(lab, "sb", fs, ly, tw - 34, p["tile_ink"], cx=cx, max_lines=2, gap=1.05)
        c.pill(P["cta"], cx, y0 + th - 40, size=22, fill=p["btn"], padx=20, pady=10)
    return c


def pills6(P, t):
    """Панель-«герой» + 6 плиток-кнопок 2×3 (иконка, подпись, кнопка)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    hb = (50, y + 22, 1030, y + 22 + t.get("hero_h", 280))
    t["hero"](c, hb)
    top = hb[3] + 22
    g = 16
    tw = (980 - g) / 2
    th = (1044 - top - 2 * g) / 3
    for i, (ic, lab) in enumerate(t["tiles"]):
        x0 = 50 + (i % 2) * (tw + g)
        y0 = top + (i // 2) * (th + g)
        c.card((x0, y0, x0 + tw, y0 + th), fill=p["tile"], r=22, sh_alpha=50, blur=10, off=(0, 5))
        r = th * 0.36
        icx = x0 + 22 + r
        c.circle(icx, y0 + th / 2, r, fill=p["iconbg"])
        icon(c, ic, icx, y0 + th / 2, r * 1.4, p["icon"], bg=p["iconbg"])
        lx = icx + r + 22
        c.block(lab, "sb", 31, y0 + th * 0.2, x0 + tw - lx - 16, p["tile_ink"], align="left", x=lx, max_lines=1)
        pb = c.pill(P["cta"], 0, -500, size=20, fill=p["btn"], padx=16, pady=8)
        pw = pb[2] - pb[0]
        c.pill(P["cta"], lx + pw / 2, y0 + th * 0.72, size=20, fill=p["btn"], padx=16, pady=8)
    return c


def devices3(P, t):
    """3 высокие карточки с устройствами + подпись + строка + кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    top = y + 30
    g = 22
    tw = (980 - 2 * g) / 3
    bot = 1044
    for i, (kind, lab, desc) in enumerate(t["devices"]):
        x0 = 50 + i * (tw + g)
        box = (x0, top, x0 + tw, bot)
        c.card(box, fill=p["tile"], r=28, sh_alpha=60, blur=14, off=(0, 8))
        cx = x0 + tw / 2
        ih = (bot - top) * 0.56
        icy = top + 26 + ih / 2
        c.rect((x0 + 14, top + 14, x0 + tw - 14, top + 26 + ih + 14), fill=p["iconbg"], r=20)
        if kind == "bar":
            big_button_phone(c, cx, icy, ih * 0.9)
        elif kind == "smart":
            simple_smartphone(c, cx, icy, ih * 0.9)
        else:
            tablet(c, cx, icy - ih * 0.06, tw * 0.88)
        ly = top + 26 + ih + 34
        ly = c.block(lab, "db", 32, ly, tw - 30, p["tile_ink"], cx=cx, max_lines=2, gap=1.04)
        c.block(desc, "s", 25, ly + 8, tw - 34, p["sub"], cx=cx, max_lines=2, gap=1.08)
        c.pill(P["cta"], cx, bot - 44, size=22, fill=p["btn"], padx=20, pady=10)
    return c


def list5(P, t):
    """Панель-«герой» + N строк-кнопок (иконка, подпись, кнопка справа)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    hb = (60, y + 20, 1020, y + 20 + t.get("hero_h", 220))
    t["hero"](c, hb)
    tiles = t["tiles"]
    n = len(tiles)
    top = hb[3] + 20
    g = 12
    rh = (1044 - top - (n - 1) * g) / n
    pb = c.pill(P["cta"], 0, -500, size=22, fill=p["btn"], padx=22, pady=11)
    pw = pb[2] - pb[0]
    for i, (ic, lab) in enumerate(tiles):
        y0 = top + i * (rh + g)
        c.card((60, y0, 1020, y0 + rh), fill=p["tile"], r=rh / 2, sh_alpha=50, blur=10, off=(0, 5))
        icx = 60 + rh / 2 + 4
        c.circle(icx, y0 + rh / 2, rh * 0.4, fill=p["iconbg"])
        icon(c, ic, icx, y0 + rh / 2, rh * 0.56, p["icon"], bg=p["iconbg"])
        c.text((60 + rh + 16, y0 + rh / 2), f"{i + 1}.", "db", 32, p["acc"], anchor="lm")
        c.block(lab, "sb", 33, y0 + rh / 2 - 20, 1020 - 18 - pw - 30 - (60 + rh + 64), p["tile_ink"], align="left", x=60 + rh + 64, max_lines=1)
        c.pill(P["cta"], 1020 - 18 - pw / 2, y0 + rh / 2, size=22, fill=p["btn"], padx=22, pady=11)
    return c


def table3(P, t):
    """Таблица на 3 колонки (шапка с иконками, строки с подписью слева)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56))
    top = y + 26
    bot = 866 if t.get("foot") else 900
    box = (40, top, 1040, bot)
    c.card(box, r=28, sh_alpha=60, blur=14, off=(0, 8))
    lw = 176
    cw = (box[2] - box[0] - lw) / 3
    cols = t["cols"]
    for k, (head, ic, col) in enumerate(cols):
        x0 = box[0] + lw + k * cw
        if k % 2 == 1:
            c.rect((x0, box[1], x0 + cw, box[3]), fill=mix(col, WH, 0.9))
        if k == 2:
            c.rect((x0, box[1], x0 + cw, box[3]), fill=mix(col, WH, 0.9), r=28)
            c.rect((x0, box[1], x0 + 30, box[3]), fill=mix(col, WH, 0.9))
        cx = x0 + cw / 2
        icon(c, ic, cx, box[1] + 64, 84, col, bg=WH if k % 2 == 0 else mix(col, WH, 0.9))
        c.block(head, "db", c.fit(head, "db", cw - 20, 1, 28), box[1] + 118, cw - 20, col, cx=cx, max_lines=1)
    hh = 172
    rows = t["rows"]
    rh = (box[3] - box[1] - hh - 8) / len(rows)
    ry = box[1] + hh
    for lab, *vals in rows:
        c.line([(box[0] + 20, ry), (box[2] - 20, ry)], (224, 228, 234), 2)
        c.block(lab, "sb", 26, ry + rh / 2 - c.lh("sb", 26, 1.04) * len(c.wrap(lab, c.font("sb", 26), lw - 36)) / 2, lw - 36,
                (80, 86, 98), align="left", x=box[0] + 26, max_lines=2, gap=1.04)
        for k, v in enumerate(vals):
            x0 = box[0] + lw + k * cw
            sz = 27
            while sz > 20 and len(c.wrap(v, c.font("sb", sz), cw - 30)) > 3:
                sz -= 1
            nl = len(c.wrap(v, c.font("sb", sz), cw - 30))
            c.block(v, "sb", sz, ry + rh / 2 - nl * c.lh("sb", sz, 1.04) / 2 + 2, cw - 30, (36, 40, 50), cx=x0 + cw / 2, max_lines=3, gap=1.04)
        ry += rh
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 888, 1000, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 984, size=42, fill=p["btn"])
    return c


def ladder(P, t):
    """«Сколько стоит»: 3 способа по возрастанию цены — разрез крыши сверху, столбик с €…€€€, подписи."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56), t2_col=p.get("acc"))
    steps = t["steps"]
    n = len(steps)
    g = 30
    cw = (980 - (n - 1) * g) / n
    ic_y = y + 30
    ic_h = 190
    base = 740
    hs = t.get("heights", (120, 200, 280))
    cols = t.get("step_cols", ((60, 150, 100), (236, 160, 40), (214, 72, 40)))
    for k, (method, lab, desc, eur) in enumerate(steps):
        x0 = 50 + k * (cw + g)
        cx = x0 + cw / 2
        cb = (x0, ic_y, x0 + cw, ic_y + ic_h)
        c.card(cb, fill=WH, r=22, sh_alpha=45, blur=10, off=(0, 5))
        roof_method(c, cx, ic_y + ic_h * 0.52, ic_h * 0.78, method)
        bh = hs[k]
        bb = (x0 + 30, base - bh, x0 + cw - 30, base)
        c.shadow(bb, r=16, alpha=60, blur=8, off=(0, 6))
        c.rect(bb, fill=cols[k], r=16)
        c.rect((bb[0], bb[3] - 16, bb[2], bb[3]), fill=cols[k])
        c.text((cx, bb[1] + 46), eur, "db", 46, WH, anchor="mm")
        c.poly([(cx - 16, ic_y + ic_h + 4), (cx + 16, ic_y + ic_h + 4), (cx, ic_y + ic_h + 22)], (200, 204, 212))
    c.line([(40, base), (1040, base)], (170, 176, 186), 4)
    for k, (method, lab, desc, eur) in enumerate(steps):
        x0 = 50 + k * (cw + g)
        cx = x0 + cw / 2
        yy = c.block(lab, "db", 28, base + 16, cw - 10, p["ink"], cx=cx, max_lines=2, gap=1.04)
        c.block(desc, "s", 25, yy + 4, cw - 10, p["sub"], cx=cx, max_lines=2, gap=1.06)
    if t.get("foot"):
        c.block(t["foot"], "sb", 30, 900, 1000, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 990, size=40, fill=p["btn"])
    return c


def callouts(P, t):
    """Сцена со сносками: телефон в зарядной подставке на столе, 7 пронумерованных подписей по бокам."""
    p = P["pal"]
    c = C(p["bg"])
    c.vgrad((0, 0, W, 860), p["bg"], p["bg2"])
    y = c.block(t["title"], "db", t.get("size", 54), 40, 980, p["ink"], max_lines=2)
    if t.get("sub"):
        y = c.block(t["sub"], "s", 30, y + 8, 960, p["sub"], max_lines=1)
    # стол
    c.rect((0, 860, W, W), fill=(196, 150, 108))
    S.wood(c, (0, 872, W, W), (206, 160, 116), (186, 140, 98), lines=6, seed=44)
    c.rect((0, 860, W, 876), fill=(176, 128, 88))
    # подставка + телефон
    cx = 540
    ph_h = 520
    pcy = 820 - ph_h / 2 + 18
    c.shadow((cx - 150, 790, cx + 150, 880), r=30, alpha=80, blur=10, off=(0, 8))
    c.rect((cx - 150, 790, cx + 150, 880), fill=(236, 238, 242), r=30)
    c.rect((cx - 130, 800, cx + 130, 820), fill=(200, 204, 212), r=8)
    c.circle(cx + 110, 850, 8, fill=(60, 200, 110))
    pb = big_button_phone(c, cx, pcy, ph_h, sos=True, photos=True)
    c.rect((cx - 150, 820, cx + 150, 880), fill=(236, 238, 242), r=24)
    c.circle(cx + 110, 850, 8, fill=(60, 200, 110))
    c.text((pb[2] + 30, pb[1] + ph_h * 0.16), "SOS", "db", 22, (214, 44, 44), anchor="lm")
    S.teacup(c, 900, 900, 0.8, rim=(40, 120, 200))
    S.glasses(c, 190, 930, 0.7)
    # сноски
    x0p, y0p, x1p, y1p = pb
    w = x1p - x0p
    anchors = {
        "speaker": (cx + w * 0.1, y0p + ph_h * 0.04),
        "screen": (x0p + w * 0.14, y0p + ph_h * 0.16),
        "photos": (x0p + w * 0.14, y0p + ph_h * 0.31),
        "sos": (x1p + 8, y0p + ph_h * 0.16),
        "keys": (x0p + w * 0.12, y0p + ph_h * 0.72),
        "hac": (x1p - 4, y0p + ph_h * 0.55),
        "dock": (cx - 150, 850),
    }
    for k, (key, lab, side, ly) in enumerate(t["callouts"]):
        ax, ay = anchors[key]
        if side == "l":
            bx0, bx1 = 24, 326
        else:
            bx0, bx1 = 754, 1056
        fs = c.fit(lab, "sb", bx1 - bx0 - 80, 2, 26)
        lines = c.wrap(lab, c.font("sb", fs), bx1 - bx0 - 80)
        bh = 24 + len(lines) * c.lh("sb", fs, 1.04)
        bb = (bx0, ly - bh / 2, bx1, ly + bh / 2)
        ex = bx1 if side == "l" else bx0
        c.line([(ex, ly), (ax, ay)], p["acc"], 4)
        c.circle(ax, ay, 9, fill=p["acc"], outline=WH, width=3)
        c.card(bb, fill=WH, r=bh / 2 if len(lines) == 1 else 22, sh_alpha=50, blur=8, off=(0, 4))
        c.circle(bx0 + 34, ly, 21, fill=p["acc"])
        c.text((bx0 + 34, ly + 1), str(k + 1), "db", 24, WH, anchor="mm")
        c.block(lab, "sb", fs, ly - len(lines) * c.lh("sb", fs, 1.04) / 2 + 2, bx1 - bx0 - 80, p["ink"], align="left", x=bx0 + 64, max_lines=2, gap=1.04)
    c.button(P["cta"], W / 2, 1000, size=44, fill=p["btn"])
    return c


FN = {"grid": T.grid, "quiz": T.quiz, "compare": T.compare, "scene_d": L.scene_d, "grid6": grid6, "pills6": pills6,
      "devices3": devices3, "list5": list5, "table3": table3, "ladder": ladder, "callouts": callouts}

SCENES = dict(w4_remote_desk=sc_remote_desk, w4_cruise_deck=sc_cruise_deck, w4_house_section=sc_house_section,
              w4_solar_offers=sc_solar_offers)
for _k, _v in SCENES.items():
    setattr(WS, _k, _v)


# =====================================================================  ПАКЕТЫ
# ---------------------------------------------------------------- 1. GB · джобсы · удалёнка 60+ (Employment: без сумм и обещания работы)
TEAL1, NAVY1, ORG1 = (0, 128, 128), (22, 44, 66), (226, 106, 28)
PACKS[1] = dict(
    doc="P60-remote-work-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(240, 247, 246), ink=NAVY1, sub=(84, 96, 108), acc=TEAL1, btn=ORG1, tile=WH, tile_ink=NAVY1, icon=NAVY1,
             iconbg=(222, 240, 238)),
    a=dict(fn="grid6", title="6 types of remote work that often suit people over 60", sub="What each role involves – pick one:", size=54,
           tiles=[("w4_sheet", "Data entry"), ("w3_headset", "Call handling"), ("w4_moderate", "Content moderation"),
                  ("w4_transcribe", "Transcription"), ("w4_proof", "Proofreading"), ("w4_diary", "Admin support")],
           src="раздел «Six types of remote work that often suit people over 60»",
           note="6 плиток 3×2 = 6 видов удалёнки из статьи, у каждой «Learn more»; без сумм, ставок, «Hiring now / Apply now»"),
    b=dict(fn="quiz", layout="phone", title="Genuine employer or a scam?", title2="6 quick checks", size=54,
           sub="Before replying to any work-from-home advert", tag="SCAM CHECK", step="Question 1 of 6", prog=1 / 6,
           q="An advert asks for a fee for training or a starter kit. What does that usually mean?",
           opts=["It's normal", "A warning sign", "Only if it's small", "Not sure"],
           pal=dict(bg=(0, 96, 100), bg2=(0, 50, 58), ink=WH, sub=(200, 230, 230), acc=ORG1, btn=ORG1),
           src="раздел «How to check an employer is genuine» (never pay upfront: training, starter kits, software)",
           note="тёмно-бирюзовый фон, телефон с тестом; вопрос о признаке мошенничества, не о зрителе"),
    c=dict(fn="table3", title="Employee, freelance or platform work?", sub="How the three differ on pay, tax and holiday", size=56,
           cols=[("EMPLOYEE", "briefcase", NAVY1), ("FREELANCE", "laptop_doc", TEAL1), ("PLATFORM", "laptop", ORG1)],
           rows=[("Works for", "one company", "several clients", "short tasks on an online marketplace"),
                 ("Pay & tax", "payroll, tax already deducted", "invoice per job, self-assessment", "the platform usually takes a fee"),
                 ("Good to know", "paid holiday, equipment often provided", "more freedom, no holiday or sick pay",
                  "easy to join, strong competition")],
           foot="Genuine roles: an interview and written terms first",
           src="раздел «Employee, freelance or platform work» + «What a genuine role usually asks for» (foot)",
           note="таблица на 3 колонки; без сумм заработка"),
    d=dict(fn="scene_d", scene="w4_remote_desk", style="top", size=54, lines=2, y=40,
           title="Working from home after 60: what a genuine role asks for",
           sub="Computer, broadband, a quiet space – and a real interview", btn_y=1000, btn_size=44,
           pal=dict(ink=NAVY1, sub=(60, 76, 90), btn=ORG1), scene_text="Never pay upfront",
           src="раздел «What a genuine role usually asks for» + «How to check…» (стикер «Never pay upfront»)",
           note="домашний угол: человек со спины в гарнитуре, монитор с таблицей, роутер, окно; лиц нет"),
)

# ---------------------------------------------------------------- 2. GB · путешествия · круизы 60+
NAVY2, SEA2, CORAL2, GOLD2 = (14, 46, 92), (0, 132, 170), (228, 84, 62), (250, 200, 70)
PACKS[2] = dict(
    doc="P60-senior-cruise-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(244, 249, 252), ink=NAVY2, sub=(80, 96, 112), acc=SEA2, btn=CORAL2, tile=WH, tile_ink=NAVY2, icon=NAVY2,
             iconbg=(222, 238, 246)),
    a=dict(fn="pills6", title="Cruise ship discounts\nfor over 60s:", title2="6 ways to pay less", size=56, hero=hero_ship, hero_h=262,
           tiles=[("w4_age60", "Senior rates"), ("calendar", "Off-peak sailings"), ("hourglass", "Last-minute cabins"),
                  ("star", "Loyalty schemes"), ("person", "Solo offers"), ("people2", "Group bookings")],
           src="раздел «Six common cruise ship discounts» (пункты 1–6)",
           note="панель: лайнер без логотипа у острова с вулканом + 6 плиток-кнопок по способам; без процентов и цен"),
    b=dict(fn="quiz", layout="card", title="Cruise price quiz:", title2="what's often not included?", size=58,
           tag="QUIZ", step="Question 1 of 5", prog=0.2,
           q="Which of these can the headline cruise fare leave out?", opts=["Drinks", "Gratuities", "Shore excursions", "All three"],
           pal=dict(bg=(226, 242, 248), bg2=(196, 226, 240), acc=SEA2, t2=CORAL2, deco=True),
           src="раздел «What the price includes, and what it often leaves out» (+ «Questions to ask before booking» — 5 вопросов)",
           note="светло-морской фон, вопрос о составе цены круиза (правильный ответ по статье — все три)"),
    c=dict(fn="compare", layout="split", title="Canary Islands cruise or all inclusive in Tenerife?", size=50, band=282,
           sub="Variety or a slower pace – a simple side-by-side",
           cols=[("CRUISE", "w4_ship", NAVY2, ["Several islands", "Only one unpack", "New port most mornings"]),
                 ("TENERIFE RESORT", "w3_hotel", CORAL2, ["One hotel, one base", "No tender boats", "Pool, promenade, walks"])],
           pal=dict(bg=(244, 249, 252), ink=NAVY2, sub=(80, 96, 112), btn=GOLD2, btn_ink=NAVY2, vs_bg=GOLD2, vs_ink=NAVY2),
           src="раздел «Cruise or resort? A quick comparison»",
           note="сплит круиз по Канарам vs отель всё включено на Тенерифе; цен нет"),
    d=dict(fn="scene_d", scene="w4_cruise_deck", style="bars", y=40,
           bars=[("WHAT THE CRUISE FARE", WH, NAVY2), ("OFTEN LEAVES OUT:", WH, NAVY2), ("DRINKS, GRATUITIES, EXCURSIONS", NAVY2, GOLD2)],
           bar_size=74, cond=0.8, btn_size=44, max_w=960, pal=dict(btn=CORAL2),
           src="раздел «What the price includes, and what it often leaves out»",
           note="плашки + палуба: пара 60+ со спины у борта, море, остров с вулканом, спасательный круг; без логотипов и названий лайнеров"),
)

# ---------------------------------------------------------------- 3. GB · товарка · телефоны для пожилых (без брендов и цен)
SLATE3, BLUE3, AMB3, GRN3 = (24, 34, 58), (20, 104, 200), (232, 140, 20), (0, 140, 120)
PACKS[3] = dict(
    doc="P60-senior-phones-uk-2026-09-30", cta="Learn more",
    pal=dict(bg=(246, 247, 251), ink=SLATE3, sub=(90, 98, 112), acc=BLUE3, btn=BLUE3, tile=WH, tile_ink=SLATE3, icon=SLATE3,
             iconbg=(232, 238, 248)),
    a=dict(fn="devices3", title="Senior-friendly phones:", title2="3 types to choose from", size=60,
           devices=[("bar", "Big-button phone", "Large keys for calls and texts"),
                    ("smart", "Simplified smartphone", "Only the most-used functions"),
                    ("tablet", "Senior tablet", "A larger screen for video calls")],
           src="раздел «Three types of senior-friendly devices»",
           note="3 карточки с нарисованными устройствами без бренда и фирменного дизайна, у каждой «Learn more»"),
    b=dict(fn="quiz", layout="card2x2", title="Choosing a simple phone:", title2="5 questions first", size=60,
           tag="QUIZ", step="Question 1 of 5", prog=0.2,
           q="Mostly calls, or video calls and photos too?", opts=["Mostly calls", "Video calls too", "Photos and messages", "Not sure yet"],
           pal=dict(bg=(255, 247, 234), bg2=(250, 226, 196), acc=AMB3, t2=BLUE3, deco=True),
           src="раздел «Five questions before buying» (вопрос 1)",
           note="тёплый фон, вопрос о привычках использования, не о здоровье зрителя"),
    c=dict(fn="compare", layout="twocol", title="Pay as you go or SIM only?", sub="Which suits whom – before choosing a network", size=58,
           cols=[("PAY AS YOU GO", "w4_sim", GRN3), ("SIM ONLY", "calendar", BLUE3)],
           rows=[("CONTRACT", "none", "rolling 30 days or 12–24 months"),
                 ("HOW IT WORKS", "top up credit when needed", "monthly minutes, texts and data"),
                 ("SUITS", "light users", "regular users, video calls")],
           foot="Keep enough credit for the SOS button to work",
           src="раздел «Choosing a SIM: pay as you go sims or sim only deals»",
           note="две колонки; без операторов и цен в £"),
    d=dict(fn="callouts", title="Senior phones: 7 features that matter most", size=54,
           pal=dict(bg=(250, 244, 234), bg2=(238, 226, 208), ink=SLATE3, sub=(90, 98, 112), acc=BLUE3, btn=BLUE3),
           callouts=[("keys", "Large, well-spaced keys", "l", 690), ("screen", "High-contrast screen", "l", 380),
                     ("speaker", "Loud, clear speaker", "r", 330), ("hac", "Hearing aid compatible", "r", 620),
                     ("sos", "SOS button", "r", 450), ("photos", "Photo contacts", "l", 520), ("dock", "Charging dock", "l", 820)],
           scene_text="10:30 / SOS",
           src="раздел «Seven features that matter most» (пункты 1–7, нумерация как в статье)",
           note="стол: кнопочный телефон без бренда в зарядной подставке, фото-кнопки, кнопка SOS; 7 сносок; без «Call 999» и обещаний безопасности"),
)

# ---------------------------------------------------------------- 4. DE · субсидии 60+ · утепление (без % субсидии и эмблем)
GREEN4, ORG4, OCH4 = (22, 84, 66), (214, 76, 34), (200, 120, 20)
PACKS[4] = dict(
    doc="P60-home-insulation-de-2026-09-30", cta="Mehr erfahren",
    pal=dict(bg=(250, 246, 238), ink=GREEN4, sub=(86, 92, 96), acc=OCH4, btn=ORG4, tile=WH, tile_ink=GREEN4, icon=GREEN4,
             iconbg=(252, 238, 214)),
    a=dict(fn="grid", layout="2x2", title="Dämmung Förderung 2026:", title2="Welche Dämmung bringt am meisten?", sub="Bauteil wählen:",
           size=58, tiles=[("w4_z_attic", "Oberste Geschossdecke"), ("w4_z_roof", "Dach"), ("w4_z_facade", "Fassade"),
                           ("w4_z_cellar", "Kellerdecke")],
           src="раздел «Welche Dämmung bringt am meisten?» (4 Bauteile)",
           note="2×2: мини-дом с подсвеченной зоной утепления на каждой плитке, у каждой «Mehr erfahren»"),
    b=dict(fn="quiz", layout="calc", title="Dämmung Förderung 2026:", title2="die Reihenfolge zählt", size=58,
           steps=[("Beratung", "done"), ("Angebote", "done"), ("Antrag", "now")], tag="SCHRITT 3 VON 5", step="", prog=0.6,
           q="Wann wird der Förderantrag gestellt?", opts=["Vor dem Auftrag", "Nach Baubeginn", "Nach der Rechnung", "Weiß nicht"],
           pal=dict(bg=(240, 246, 242), bg2=(212, 230, 220), ink=GREEN4, sub=(70, 84, 80), acc=GREEN4, t2=ORG4, btn=ORG4),
           src="раздел «Dämmung Förderung 2026: so funktioniert der Zuschuss» («Wichtig: vor Beginn der Arbeiten») + «In fünf Schritten»",
           note="опросник-калькулятор: шаги 1–3 из 5 шагов статьи, вопрос о сроке заявки; без процентов"),
    c=dict(fn="ladder", title="Dachdämmung Kosten pro m²:", title2="Wovon der Preis abhängt", size=58,
           steps=[("ceiling", "Oberste\nGeschossdecke", "meist am günstigsten", "€"),
                  ("between", "Zwischensparren-\ndämmung", "mittlerer Aufwand", "€ €"),
                  ("above", "Aufsparren-\ndämmung", "am teuersten", "€ € €")],
           foot="Dazu: Dämmstoff, Gerüst, Zustand der Holzkonstruktion",
           src="раздел «Dachdämmung Kosten pro m2: wovon der Preis abhängt»",
           note="3 разреза крыши (где лежит утеплитель) + столбики €/€€/€€€ по возрастанию — порядок из статьи, без €/m²"),
    d=dict(fn="scene_d", scene="w4_house_section", style="bars", y=40,
           bars=[("DÄMMUNG IM EIGENEN HAUS:", WH, GREEN4), ("ZUSCHUSS ODER STEUERBONUS?", GREEN4, INS)],
           bar_size=78, cond=0.8, btn_size=44, max_w=960, pal=dict(btn=ORG4),
           src="раздел «Steuerbonus als Alternative» (+ разрез дома — 4 Bauteile из раздела 1)",
           note="плашки + разрез дома зимним вечером: утеплитель на перекрытии, в крыше, на фасаде, под потолком подвала; человек в кресле без лица; без до/после и тепловизора"),
)

# ---------------------------------------------------------------- 5. DE · субсидии 60+ · солнечные панели (без «Kredit», без цифр экономии)
NAVY5, SUN5, GREEN5, ORG5 = (16, 48, 96), (250, 196, 40), (22, 136, 82), (214, 120, 0)
PACKS[5] = dict(
    doc="P60-solar-subsidy-de-2026-09-30", cta="Mehr erfahren",
    pal=dict(bg=(242, 248, 252), ink=NAVY5, sub=(80, 92, 108), acc=ORG5, btn=GREEN5, tile=WH, tile_ink=NAVY5, icon=NAVY5,
             iconbg=(226, 238, 250)),
    a=dict(fn="list5", title="Lohnt sich Photovoltaik im Ruhestand?", title2="5 Fragen entscheiden", size=54, hero=hero_solar, hero_h=200,
           tiles=[("w3_sun", "Verbrauch tagsüber"), ("w4_roof", "Zustand des Dachs"), ("home_heart", "Wohndauer und Erben"),
                  ("piggy", "Ersparnisse oder Miete"), ("meter", "Stromrechnung heute")],
           src="раздел «Lohnt sich Photovoltaik für Rentner? Fünf Fragen»",
           note="панель: дом с модулями на крыше, солнце + 5 строк-кнопок по 5 вопросам статьи; «Kredit» не выносил"),
    b=dict(fn="quiz", layout="card", title="Solar aufs Dach 2026:", title2="die Frage zum Zuschuss", size=58,
           tag="QUIZ", step="Frage 1 von 3", prog=0.33,
           q="Gibt es 2026 einen bundesweiten Zuschuss für eine Solaranlage auf dem Dach?",
           opts=["Ja, für alle", "Nein", "Nur mit Speicher", "Weiß nicht"],
           pal=dict(bg=(16, 48, 96), bg2=(8, 26, 58), ink=WH, sub=(206, 218, 236), acc=GREEN5, t2=SUN5, btn=GREEN5, deco=True),
           src="раздел «Photovoltaik Förderung 2026: was es gibt und was nicht» (ответ по статье — «Nein»)",
           note="тёмно-синий фон, вопрос о правилах поддержки; без «staatlicher Zuschuss» как обещания"),
    c=dict(fn="compare", layout="table", title="Photovoltaik mit oder ohne Speicher?", sub="Wovon die Kosten wirklich abhängen", size=56,
           cols=[("OHNE SPEICHER", "w4_panel", (20, 90, 170)), ("MIT SPEICHER", "w4_battery", GREEN5)],
           rows=[("Eigenverbrauch", "oft rund ein Drittel", "deutlich mehr"), ("Mittagsstrom", "Rest geht ins Netz", "am Abend nutzen"),
                 ("Anlagenpreis", "niedriger", "spürbar höher")],
           foot="Angebote: Preis pro kWp mit und ohne Speicher",
           src="раздел «Photovoltaik mit Speicher Kosten» + «Angebote Komplettanlagen vergleichen» (foot)",
           note="таблица без € и центов; «rund ein Drittel» — формулировка статьи (в списке сверки)"),
    d=dict(fn="scene_d", scene="w4_solar_offers", style="card", card_box=(60, 36, 1020, 446), frame=True, font="lserb",
           kicker="PHOTOVOLTAIK 2026", title="Komplettangebote vergleichen: 5 Punkte, die zählen",
           sub="Preis pro kWp, Garantien, Gerüst und Zählerschrank, Ertragsprognose, Wartung", size=54, lines=3, btn_size=40, btn_off=64,
           pal=dict(frame=NAVY5, ink=NAVY5, sub=(80, 92, 108), acc=ORG5, btn=GREEN5),
           scene_text="ANGEBOT 1 / ANGEBOT 2 / ANGEBOT 3 · kWp",
           src="раздел «Photovoltaik Angebote Komplettanlagen vergleichen» (5 пунктов)",
           note="карточка в рамке + кухонный стол: три предложения, калькулятор, очки; в окне — крыша пристройки с модулями; человек без лица"),
)


# =====================================================================  сборка
def _clean(s):
    return s.replace("-\n", "").replace("\n", " ").replace("­", "").replace(" ", " ")


def texts(t, cta):
    """Весь текст на картинке — для creatives.json."""
    out = []
    for k in ("kicker", "title", "title2", "sub"):
        if t.get(k):
            out.append(t[k])
    if t.get("bars"):
        out.append(" ".join(b[0] for b in t["bars"]))
    if t.get("steps") and t["fn"] == "quiz":
        out.append(" · ".join(s[0] for s in t["steps"]))
    for k in ("tag", "step", "q"):
        if t.get(k):
            out.append(t[k])
    if t.get("opts"):
        out.append(" / ".join(t["opts"]))
    if t.get("tiles"):
        out.append(" / ".join(x[1] for x in t["tiles"]) + f" (у каждой «{cta}»)")
    if t.get("devices"):
        out.append(" / ".join(f"{lab} – {d}" for _, lab, d in t["devices"]) + f" (у каждой «{cta}»)")
        out.append("на экранах: 10:30 / Call · Messages · Photos · Video call / Video calls · Photos · News · Radio")
    if t.get("cols"):
        out.append(" vs ".join(x[0] for x in t["cols"]))
        for x in t["cols"]:
            if len(x) >= 4 and isinstance(x[-1], list):
                out.append(x[0] + ": " + " · ".join(x[-1]))
    if t.get("rows"):
        out.append(" · ".join(f"{r[0]}: " + " / ".join(r[1:]) for r in t["rows"]))
    if t.get("steps") and t["fn"] == "ladder":
        out.append(" · ".join(f"{lab} – {d} ({e.replace(' ', '')})" for _, lab, d, e in t["steps"]))
    if t.get("callouts"):
        out.append(" · ".join(f"{k + 1}. {x[1]}" for k, x in enumerate(t["callouts"])))
    for k in ("foot", "scene_text"):
        if t.get(k):
            out.append(t[k])
    out.append(f"кнопка «{cta} →»")
    return _clean(" / ".join(out))


def build(n, letters="abcd"):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for Lt in "abcd":
        t = P[Lt]
        PPk = dict(P, pal={**P["pal"], **t.get("pal", {})})
        if Lt in letters:
            c = FN[t["fn"]](PPk, t)
            c.save(f"{doc}/{Lt}.png")
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png",
                          concept=CONCEPT[Lt] + " — " + t.get("note", "") + "; опора: " + t.get("src", ""),
                          text=texts(t, P["cta"]), cta=P["cta"]))
    os.makedirs(os.path.join(OUT, doc), exist_ok=True)
    with open(os.path.join(OUT, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
