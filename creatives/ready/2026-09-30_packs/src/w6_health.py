"""Волна 6 · здоровье (29.09, креативщик w6): 5 карточек «Готово к заливу» × 4 статики 1:1, Pillow.
    python3 w6_health.py            — все пакеты
    python3 w6_health.py 3 5        — пакеты 3 и 5
    python3 w6_health.py 3:a,c      — пакет 3, буквы a и c
    python3 w6_health.py check      — проверка запретных слов во всех текстах картинок
Пишет /home/user/alextest/creatives/ready/2026-09-30_packs/<docId>/<a|b|c|d>.png и creatives.json рядом.
Движок — p60_lib (холст C), иконки p60/w2b/p60w2, хелперы сцен p60_scenes / w2b_scenes (импорт, файлы не меняются).
Здесь — свои раскладки (сетки, опросники, шкала 0–28, таблица «public / private», «vrai ou faux», сравнения),
сцены (тумбочка в 03:47, стол с чек-листом оценки, две часовые стрелки 21/4, кабинет центра, гостиная с массажным
столом) и иконки ic_*.
Весь текст на картинках — только из статей карточек article_drafts (раздел — в поле src).
Запреты: без вопросов и утверждений о зрителе (you / your, «Can't sleep?», «Non riesci a dormire?», «Vous avez…»),
без таблеток, упаковок, названий лекарств, мелатонина; без cure / fix / free / guaranteed; без логотипов и названий
ведомств на картинке (NHS, Medicare, WHO, SSN/ASL, CECOS) и без до/после; донорство — без денег, «rémunéré», «gagner», €;
массаж — без мед. обещаний, тел, «private / discreet / sensual» и цен в £ (только «£?»); шкалы теста —
«self-assessment, not a diagnosis»; без «click here» и обращения к локации зрителя."""
import json
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import p60_lib  # noqa: E402
from p60_lib import C, W, mix, rotpts  # noqa: E402
import p60_icons as I  # noqa: E402
import p60_scenes as S  # noqa: E402
import w2b_scenes as WS  # noqa: E402  (регистрирует иконки w2b и шрифт sbi)
import p60w2_art  # noqa: E402,F401  (иконки волны 2)

OUT6 = "/home/user/alextest/creatives/ready/2026-09-30_packs"
p60_lib.OUT = OUT6
p60_lib.F.update({
    "mx": os.path.join(SRC, "fonts", "Montserrat-ExtraBold.ttf"),
    "mb": os.path.join(SRC, "fonts", "Montserrat-Bold.ttf"),
    "msb": os.path.join(SRC, "fonts", "Montserrat-SemiBold.ttf"),
    "dmb": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    "sbi": "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
})
WH = (255, 255, 255)
PACKS = {}


# =====================================================================  общие хелперы
def bwidth(c, label, size=42, padx=56):
    return c.tw(label + "  →", c.font("sb", size))[0] + 2 * padx


def stars(c, box, n, seed, col=WH, rmin=1.4, rmax=3.2, alpha=190):
    rnd = random.Random(seed)
    lay = c.layer()
    dd = ImageDraw.Draw(lay)
    for _ in range(n):
        x, y = rnd.uniform(box[0], box[2]), rnd.uniform(box[1], box[3])
        r = rnd.uniform(rmin, rmax)
        dd.ellipse(c.sb((x - r, y - r, x + r, y + r)), fill=col + (int(alpha * rnd.uniform(0.45, 1)),))
    c.put(lay)


def crescent(c, cx, cy, r, col, bg, dx=0.42, dy=-0.3):
    c.circle(cx, cy, r, fill=col)
    c.circle(cx + r * dx, cy + r * dy, r * 0.84, fill=bg)


def heart(c, cx, cy, s, col):
    r = s * 0.27
    c.circle(cx - r * 0.95, cy - r * 0.3, r, fill=col)
    c.circle(cx + r * 0.95, cy - r * 0.3, r, fill=col)
    c.poly([(cx - r * 1.9, cy - r * 0.02), (cx + r * 1.9, cy - r * 0.02), (cx, cy + r * 2.0)], col)


def teardrop(cx, by, w, h, n=28):
    r = w / 2
    ccy = by - r
    pts = [(cx + r * math.cos(math.pi * k / n), ccy + r * math.sin(math.pi * k / n)) for k in range(n + 1)]
    # плавный бок к острию
    for k in range(1, 8):
        t = k / 8
        pts.append((cx - r * (1 - t) ** 1.3, ccy - (h - r) * t))
    pts.append((cx, by - h))
    for k in range(7, 0, -1):
        t = k / 8
        pts.append((cx + r * (1 - t) ** 1.3, ccy - (h - r) * t))
    return pts


def clock(c, cx, cy, r, h, m, face=WH, rim=(50, 56, 70), hand=(40, 44, 56), accent=(226, 80, 60)):
    c.circle(cx, cy, r, fill=rim)
    c.circle(cx, cy, r * 0.88, fill=face)
    for k in range(12):
        a = math.radians(k * 30 - 90)
        r0 = r * (0.66 if k % 3 == 0 else 0.74)
        c.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8)],
               hand, r * (0.055 if k % 3 == 0 else 0.03))
    ah = math.radians(((h % 12) + m / 60) * 30 - 90)
    am = math.radians(m * 6 - 90)
    c.line([(cx, cy), (cx + math.cos(ah) * r * 0.44, cy + math.sin(ah) * r * 0.44)], hand, r * 0.075)
    c.line([(cx, cy), (cx + math.cos(am) * r * 0.64, cy + math.sin(am) * r * 0.64)], hand, r * 0.045)
    c.circle(cx, cy, r * 0.07, fill=accent)


def chip(c, text, cx, cy, size=26, fill=WH, ink=(30, 34, 50), dot=None, padx=22, pady=12, name="sb", alpha=255, shadow=True):
    tw = c.tw(text, c.font(name, size))[0]
    extra = 26 if dot else 0
    w_ = tw + 2 * padx + extra
    h_ = c.lh(name, size, 1.0) + 2 * pady
    box = (cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2)
    if shadow:
        c.shadow(box, r=h_ / 2, alpha=70, blur=8, off=(0, 5))
    c.rect(box, fill=fill, r=h_ / 2, alpha=alpha)
    if dot:
        c.circle(box[0] + padx + 8, cy, 8, fill=dot)
    c.text((box[0] + padx + extra, cy), text, name, size, ink, anchor="lm")
    return box


def cbox(c, x, y, s, checked, col, line=(170, 176, 186)):
    if checked:
        c.rect((x, y, x + s, y + s), fill=col, r=s * 0.22)
        c.check(x + s * 0.2, y + s * 0.2, s * 0.6, WH, s * 0.12)
    else:
        c.rect((x, y, x + s, y + s), fill=WH, r=s * 0.22, outline=line, width=3)


def phone(c, ph, frame=(26, 28, 34)):
    c.shadow(ph, r=64, alpha=120, blur=26, off=(0, 16))
    c.rect(ph, fill=frame, r=64)
    sc = (ph[0] + 16, ph[1] + 16, ph[2] - 16, ph[3] - 16)
    c.rect(sc, fill=WH, r=50)
    mx = (ph[0] + ph[2]) / 2
    c.rect((mx - 70, ph[1] + 30, mx + 70, ph[1] + 62), fill=frame, r=16)
    c.text((sc[0] + 36, ph[1] + 46), "9:41", "sb", 22, (40, 40, 40), anchor="lm")
    return sc


def radio_rows(c, opts, x0, x1, y, h, gap, size=28, ink=(44, 48, 58)):
    for o in opts:
        c.rect((x0, y, x1, y + h), fill=(246, 248, 250), r=h / 2, outline=(206, 212, 222), width=3)
        c.circle(x0 + h / 2 + 4, y + h / 2, h * 0.21, fill=WH, outline=(150, 158, 170), width=3)
        c.text((x0 + h + 10, y + h / 2), o, "sb", size, ink, anchor="lm")
        y += h + gap
    return y


def ico(c, name, cx, cy, s, col, bg=WH):
    if name in LOCAL:
        LOCAL[name](c, cx, cy, s, col, bg)
    else:
        I.ICONS[name](c, cx, cy, s, col, bg=bg)


def tiles_grid(c, tiles, top, bottom, cols, cta, pal, label_size=34, sub_size=25, icon_r=64, gap=24, x0=60, x1=1020,
               pill_size=22, label_font="sb"):
    rows = (len(tiles) + cols - 1) // cols
    tw = (x1 - x0 - gap * (cols - 1)) / cols
    th = (bottom - top - gap * (rows - 1)) / rows
    ls = min(c.fit(t[1], label_font, tw - 40, 2, label_size) for t in tiles)
    subs = [t[2] for t in tiles if len(t) > 2 and t[2]]
    ss = min([c.fit(s_, "s", tw - 44, 2, sub_size) for s_ in subs] or [sub_size])
    for i, tl in enumerate(tiles):
        ic, lab = tl[0], tl[1]
        sub = tl[2] if len(tl) > 2 else None
        tx = x0 + (i % cols) * (tw + gap)
        ty = top + (i // cols) * (th + gap)
        c.card((tx, ty, tx + tw, ty + th), fill=pal["tile"], r=28, sh_alpha=55, blur=14, off=(0, 8))
        cx = tx + tw / 2
        icy = ty + 24 + icon_r
        c.circle(cx, icy, icon_r, fill=pal["iconbg"])
        ico(c, ic, cx, icy, icon_r * 1.42, pal["icon"], bg=pal["iconbg"])
        y = icy + icon_r + 16
        y = c.block(lab, label_font, ls, y, tw - 40, pal["ink"], cx=cx, gap=1.04)
        if sub:
            c.block(sub, "s", ss, y + 4, tw - 44, pal["sub"], cx=cx, gap=1.08)
        c.pill(cta, cx, ty + th - 40, size=pill_size, fill=pal["btn"], padx=22, pady=11)


# =====================================================================  иконки ic_*
def ic_doctor(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy - 0.2 * s, 0.17 * s, fill=col)
    c.pie((cx - 0.36 * s, cy + 0.02 * s, cx + 0.36 * s, cy + 0.74 * s), 180, 360, col)
    c.rect((cx - 0.36 * s, cy + 0.36 * s, cx + 0.36 * s, cy + 0.4 * s), fill=bg)
    c.arc((cx - 0.15 * s, cy - 0.02 * s, cx + 0.15 * s, cy + 0.26 * s), 0, 180, bg, 0.035 * s)
    c.line([(cx + 0.15 * s, cy + 0.12 * s), (cx + 0.2 * s, cy + 0.26 * s)], bg, 0.03 * s)
    c.circle(cx + 0.2 * s, cy + 0.28 * s, 0.045 * s, fill=bg)


def ic_clinic(c, cx, cy, s, col, bg=WH, moon=(244, 184, 56)):
    x0, x1 = cx - 0.38 * s, cx + 0.18 * s
    y0, y1 = cy - 0.14 * s, cy + 0.36 * s
    c.rect((x0, y0, x1, y1), fill=col, r=0.03 * s)
    c.rect((x0 - 0.04 * s, y0 - 0.06 * s, x1 + 0.04 * s, y0 + 0.02 * s), fill=col, r=0.02 * s)
    for i in range(3):
        for j in range(2):
            wx = x0 + 0.06 * s + i * 0.165 * s
            wy = y0 + 0.08 * s + j * 0.13 * s
            c.rect((wx, wy, wx + 0.1 * s, wy + 0.08 * s), fill=bg)
    c.rect((cx - 0.15 * s, y1 - 0.13 * s, cx - 0.05 * s, y1), fill=bg)
    crescent(c, cx + 0.26 * s, cy - 0.28 * s, 0.14 * s, moon, bg)


def ic_laptop_moon(c, cx, cy, s, col, bg=WH, moon=(244, 184, 56)):
    scr = (46, 54, 110)
    c.rect((cx - 0.34 * s, cy - 0.32 * s, cx + 0.34 * s, cy + 0.12 * s), fill=col, r=0.04 * s)
    c.rect((cx - 0.29 * s, cy - 0.27 * s, cx + 0.29 * s, cy + 0.07 * s), fill=scr)
    crescent(c, cx - 0.08 * s, cy - 0.1 * s, 0.1 * s, moon, scr)
    c.text((cx + 0.1 * s, cy - 0.13 * s), "z", "db", 0.12 * s, WH, anchor="mm")
    c.text((cx + 0.18 * s, cy - 0.2 * s), "z", "db", 0.09 * s, WH, anchor="mm")
    c.rect((cx - 0.44 * s, cy + 0.13 * s, cx + 0.44 * s, cy + 0.21 * s), fill=col, r=0.03 * s)


def ic_drop_moon(c, cx, cy, s, col, bg=WH):
    c.poly(teardrop(cx - 0.06 * s, cy + 0.36 * s, 0.46 * s, 0.68 * s), (60, 150, 220))
    c.ellipse((cx - 0.2 * s, cy + 0.05 * s, cx - 0.1 * s, cy + 0.18 * s), fill=WH, alpha=160)
    crescent(c, cx + 0.26 * s, cy - 0.24 * s, 0.13 * s, col, bg)


def ic_joint(c, cx, cy, s, col, bg=WH, acc=(222, 70, 56)):
    kx, ky = cx + 0.02 * s, cy - 0.04 * s
    c.line([(cx - 0.38 * s, cy - 0.2 * s), (kx, ky)], col, 0.17 * s)
    c.line([(kx, ky), (cx - 0.1 * s, cy + 0.36 * s)], col, 0.14 * s)
    c.line([(cx - 0.1 * s, cy + 0.36 * s), (cx + 0.1 * s, cy + 0.38 * s)], col, 0.1 * s)
    c.circle(kx, ky, 0.11 * s, fill=col)
    for k in range(5):
        a = math.radians(-70 + k * 35)
        c.line([(kx + math.cos(a) * 0.19 * s, ky + math.sin(a) * 0.19 * s), (kx + math.cos(a) * 0.33 * s, ky + math.sin(a) * 0.33 * s)],
               acc, 0.05 * s)


def ic_snore(c, cx, cy, s, col, bg=WH, acc=(222, 110, 56)):
    c.text((cx - 0.3 * s, cy + 0.12 * s), "Z", "db", 0.5 * s, col, anchor="mm")
    c.text((cx - 0.02 * s, cy - 0.08 * s), "z", "db", 0.34 * s, col, anchor="mm")
    c.rect((cx + 0.16 * s, cy - 0.06 * s, cx + 0.23 * s, cy + 0.3 * s), fill=acc, r=0.02 * s)
    c.rect((cx + 0.3 * s, cy - 0.06 * s, cx + 0.37 * s, cy + 0.3 * s), fill=acc, r=0.02 * s)


def ic_legs(c, cx, cy, s, col, bg=WH, acc=(222, 110, 56)):
    for dx in (-0.16, 0.06):
        x = cx + dx * s
        c.line([(x, cy - 0.38 * s), (x, cy + 0.26 * s), (x + 0.16 * s, cy + 0.3 * s)], col, 0.1 * s)
    for k in range(3):
        y = cy - 0.2 * s + k * 0.16 * s
        c.arc((cx + 0.2 * s, y - 0.08 * s, cx + 0.36 * s, y + 0.08 * s), 300, 60, acc, 0.035 * s)


def ic_flame(c, cx, cy, s, col, bg=WH):
    c.poly(teardrop(cx, cy + 0.38 * s, 0.56 * s, 0.8 * s), (236, 110, 40))
    c.poly(teardrop(cx, cy + 0.36 * s, 0.3 * s, 0.44 * s), (250, 196, 60))


def ic_anon(c, cx, cy, s, col, bg=WH, acc=(222, 72, 72)):
    I.ICONS["person"](c, cx - 0.06 * s, cy + 0.02 * s, s * 0.92, col, bg=bg)
    c.circle(cx + 0.26 * s, cy - 0.22 * s, 0.17 * s, fill=bg)
    c.circle(cx + 0.26 * s, cy - 0.22 * s, 0.14 * s, fill=acc)
    c.text((cx + 0.26 * s, cy - 0.22 * s), "?", "db", 0.2 * s, WH, anchor="mm")


def ic_leaf(c, cx, cy, s, col, bg=WH):
    A, B = (cx - 0.3 * s, cy + 0.3 * s), (cx + 0.32 * s, cy - 0.32 * s)
    ux, uy = B[0] - A[0], B[1] - A[1]
    L = math.hypot(ux, uy)
    nx, ny = -uy / L, ux / L
    up, dn = [], []
    for k in range(31):
        t = k / 30
        w = math.sin(math.pi * t) ** 0.9 * 0.2 * s
        px, py = A[0] + ux * t, A[1] + uy * t
        up.append((px + nx * w, py + ny * w))
        dn.append((px - nx * w, py - ny * w))
    c.poly(up + dn[::-1], col)
    c.line([A, (A[0] + ux * 0.85, A[1] + uy * 0.85)], bg, 0.03 * s)
    c.line([(A[0] - 0.08 * s, A[1] + 0.08 * s), A], col, 0.04 * s)


def ic_press(c, cx, cy, s, col, bg=WH, acc=(206, 96, 64)):
    for k in range(3):
        y = cy + 0.1 * s + k * 0.12 * s
        pts = [(cx - 0.38 * s + t * 0.76 * s / 24, y + math.sin(t / 24 * math.pi * 3) * 0.03 * s) for t in range(25)]
        c.line(pts, col, 0.045 * s)
    c.rect((cx - 0.06 * s, cy - 0.4 * s, cx + 0.06 * s, cy - 0.14 * s), fill=acc)
    c.poly([(cx - 0.16 * s, cy - 0.16 * s), (cx + 0.16 * s, cy - 0.16 * s), (cx, cy + 0.02 * s)], acc)


def ic_shoe(c, cx, cy, s, col, bg=WH, acc=(206, 96, 64)):
    c.poly([(cx - 0.42 * s, cy + 0.12 * s), (cx - 0.4 * s, cy - 0.2 * s), (cx - 0.18 * s, cy - 0.22 * s), (cx - 0.02 * s, cy - 0.02 * s),
            (cx + 0.3 * s, cy + 0.02 * s), (cx + 0.44 * s, cy + 0.12 * s)], col)
    c.rect((cx - 0.44 * s, cy + 0.1 * s, cx + 0.46 * s, cy + 0.22 * s), fill=acc, r=0.05 * s)
    for k in range(3):
        c.circle(cx - 0.2 * s + k * 0.07 * s, cy - 0.13 * s + k * 0.045 * s, 0.022 * s, fill=bg)


def ic_oil(c, cx, cy, s, col, bg=WH, acc=(206, 150, 50)):
    c.rect((cx - 0.24 * s, cy - 0.06 * s, cx + 0.12 * s, cy + 0.38 * s), fill=col, r=0.07 * s)
    c.rect((cx - 0.18 * s, cy + 0.06 * s, cx + 0.06 * s, cy + 0.24 * s), fill=bg, r=0.02 * s)
    c.rect((cx - 0.11 * s, cy - 0.18 * s, cx - 0.01 * s, cy - 0.06 * s), fill=col)
    c.ellipse((cx - 0.13 * s, cy - 0.4 * s, cx + 0.01 * s, cy - 0.16 * s), fill=acc)
    c.poly(teardrop(cx + 0.3 * s, cy + 0.18 * s, 0.16 * s, 0.24 * s), acc)


def ic_pillow(c, cx, cy, s, col, bg=WH, acc=(206, 96, 64)):
    c.rect((cx - 0.4 * s, cy + 0.06 * s, cx + 0.4 * s, cy + 0.34 * s), fill=col, r=0.12 * s)
    c.rect((cx - 0.32 * s, cy - 0.16 * s, cx + 0.32 * s, cy + 0.08 * s), fill=mix(col, WH, 0.35), r=0.1 * s)
    heart(c, cx, cy - 0.3 * s, 0.26 * s, acc)


def ic_city(c, cx, cy, s, col, bg=WH):
    for x0, top, x1 in ((-0.42, -0.04, -0.22), (-0.2, -0.34, 0.0), (0.02, -0.14, 0.18), (0.2, -0.42, 0.4)):
        c.rect((cx + x0 * s, cy + top * s, cx + x1 * s, cy + 0.34 * s), fill=col)
        yy = cy + (top + 0.07) * s
        while yy < cy + 0.26 * s:
            c.rect((cx + (x0 + 0.05) * s, yy, cx + (x1 - 0.05) * s, yy + 0.04 * s), fill=bg)
            yy += 0.1 * s
    c.rect((cx - 0.46 * s, cy + 0.34 * s, cx + 0.44 * s, cy + 0.39 * s), fill=col)


def ic_stones(c, cx, cy, s, col, bg=WH):
    c.ellipse((cx - 0.4 * s, cy + 0.12 * s, cx + 0.4 * s, cy + 0.38 * s), fill=col)
    c.ellipse((cx - 0.31 * s, cy - 0.08 * s, cx + 0.31 * s, cy + 0.17 * s), fill=mix(col, WH, 0.28))
    c.ellipse((cx - 0.22 * s, cy - 0.26 * s, cx + 0.22 * s, cy - 0.04 * s), fill=mix(col, WH, 0.5))
    for k in (-1, 1):
        pts = [(cx + k * 0.1 * s + math.sin(t / 3) * 0.03 * s, cy - 0.3 * s - t * 0.012 * s) for t in range(12)]
        c.line(pts, (220, 120, 80), 0.03 * s)


def ic_moon_cal(c, cx, cy, s, col, bg=WH, moon=(236, 170, 50)):
    I.ICONS["calendar"](c, cx - 0.08 * s, cy + 0.06 * s, s * 0.78, col, bg=bg)
    c.circle(cx + 0.27 * s, cy - 0.26 * s, 0.19 * s, fill=bg)
    crescent(c, cx + 0.27 * s, cy - 0.26 * s, 0.15 * s, moon, bg)


LOCAL = dict(doctor=ic_doctor, clinic=ic_clinic, laptop_moon=ic_laptop_moon, drop_moon=ic_drop_moon, joint=ic_joint,
             snore=ic_snore, legs=ic_legs, flame=ic_flame, anon=ic_anon, leaf=ic_leaf, press=ic_press, shoe=ic_shoe,
             oil=ic_oil, pillow=ic_pillow, city=ic_city, stones=ic_stones, moon_cal=ic_moon_cal)


def icon_sheet():
    c = C((250, 250, 250))
    for i, nm in enumerate(LOCAL):
        x, y = 90 + (i % 6) * 170, 110 + (i // 6) * 200
        c.circle(x, y, 64, fill=(230, 236, 246))
        ico(c, nm, x, y, 92, (30, 40, 80), bg=(230, 236, 246))
        c.text((x, y + 80), nm, "s", 20, (200, 0, 0), anchor="mm")
    c.im.convert("RGB").resize((W, W)).save(os.path.join(os.environ.get("W6_SCRATCH", "/tmp"), "w6_icons.png"))


# =====================================================================  1. NT · психотесты · сон: тест ISI → КПТ-И (EN)
NAVY1, CORAL1, IND1, AMB1 = (24, 30, 76), (232, 84, 60), (84, 76, 200), (250, 196, 96)


def s1a(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (248, 246, 252), (226, 228, 246))
    y = c.block("Insomnia treatment options", "db", 66, 42, 980, NAVY1, max_lines=1)
    sub = "From the family doctor to online CBT-I – pick one:"
    y = c.block(sub, "s", 32, y + 6, 980, (84, 90, 124), max_lines=1)
    tiles = [("doctor", "Family doctor (GP)", "Usually the first step"),
             ("clinic", "Sleep clinic", "May include an overnight sleep study"),
             ("talk", "Psychologist trained in CBT-I", "In person or by video"),
             ("laptop_moon", "Online CBT-I program", "Sleep diary and weekly steps")]
    pal = dict(tile=WH, iconbg=(230, 230, 250), icon=NAVY1, ink=NAVY1, sub=(98, 104, 130), btn=CORAL1)
    tiles_grid(c, tiles, y + 28, 1044, 2, P["cta"], pal, label_size=34, sub_size=26, icon_r=66)
    return c, ["Insomnia treatment options", sub] + [f"{t[1]} – {t[2]}" for t in tiles] + [f"×4 «{P['cta']}»"]


def s1b(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (58, 50, 146), (22, 20, 66))
    stars(c, (0, 0, W, 300), 38, 11)
    crescent(c, 990, 258, 30, (250, 214, 130), mix((58, 50, 146), (22, 20, 66), 0.25))
    t1 = "The 7-question insomnia test sleep specialists use"
    y = c.block(t1, "db", 56, 44, 860, WH, max_lines=2, gap=1.1)
    sub = "Each answer 0–4 · total 0–28"
    c.block(sub, "s", 32, y + 8, 900, (206, 204, 244), max_lines=1)
    box = (70, 290, 1010, 792)
    c.card(box, r=36, sh_alpha=130, blur=24)
    x0, x1 = box[0] + 50, box[2] - 50
    yy = box[1] + 44
    tag, step = "INSOMNIA SEVERITY INDEX (ISI)", "Question 1 of 7"
    c.text((x0, yy), tag, "sb", 24, IND1)
    c.text((x1, yy), step, "s", 26, (110, 116, 130), anchor="ra")
    yy += 48
    sw = (x1 - x0 - 6 * 10) / 7
    for k in range(7):
        c.rect((x0 + k * (sw + 10), yy, x0 + k * (sw + 10) + sw, yy + 12), fill=IND1 if k == 0 else (226, 228, 238), r=6)
    yy += 44
    lead = "Over the last 2 weeks:"
    c.text((x0, yy), lead, "s", 30, (110, 116, 130))
    yy += 46
    q = "Difficulty falling asleep"
    c.text((x0, yy), q, "db", 52, (30, 32, 44))
    cy = yy + 150
    for k in range(5):
        cx = x0 + 70 + k * (x1 - x0 - 140) / 4
        c.circle(cx, cy + 5, 60, fill=(0, 0, 0), alpha=30)
        c.circle(cx, cy, 60, fill=(246, 246, 252), outline=(196, 198, 222), width=4)
        c.text((cx, cy), str(k), "db", 50, NAVY1, anchor="mm")
    c.text((x0 + 70, cy + 92), "none", "s", 26, (110, 116, 130), anchor="mm")
    c.text((x1 - 70, cy + 92), "very severe", "s", 26, (110, 116, 130), anchor="mm")
    note = "A self-assessment, not a diagnosis"
    c.text((W / 2, 838), note, "sbi", 30, (214, 212, 250), anchor="mm")
    c.button(P["cta"], W / 2, 958, size=44, fill=CORAL1)
    return c, [t1, sub, f"{tag} · {step} · {lead} {q} · 0 1 2 3 4 (0 = none, 4 = very severe)", note, P["cta"]]


def s1c(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (255, 255, 255), (238, 240, 248))
    t1, t2 = "Insomnia test score 0–28:", "what each range means"
    y = c.block(t1, "db", 62, 40, 980, NAVY1, max_lines=1)
    y = c.block(t2, "db", 54, y, 980, IND1, max_lines=1)
    sub = "Insomnia Severity Index (ISI) · 7 questions"
    y = c.block(sub, "s", 30, y + 8, 980, (96, 102, 126), max_lines=1)
    rows = [("0–7", "No clinically significant insomnia", None, (64, 166, 108), 8),
            ("8–14", "Subthreshold insomnia", "a problem worth watching", (226, 176, 36), 7),
            ("15–21", "Clinical insomnia", "moderate severity", (236, 126, 44), 7),
            ("22–28", "Severe clinical insomnia", None, (210, 64, 56), 7)]
    gy = y + 30
    gx0, gx1 = 70, 1010
    x = gx0
    for i, (_, _, _, col, n) in enumerate(rows):
        w_ = (gx1 - gx0) * n / 29
        c.rect((x, gy, x + w_, gy + 46), fill=col, r=23 if i in (0, 3) else 0)
        if i in (0, 3):
            c.rect((x + (23 if i == 0 else 0), gy, x + w_ - (23 if i == 3 else 0), gy + 46), fill=col)
        x += w_
    for v in (0, 8, 15, 22, 28):
        tx = gx0 + (gx1 - gx0) * (v if v < 28 else 29) / 29
        c.text((min(max(tx, gx0 + 12), gx1 - 16), gy + 64), str(v), "sb", 24, (90, 96, 116), anchor="ma")
    top = gy + 118
    rh, g = 104, 14
    for k, (rng, lab, sub2, col, _) in enumerate(rows):
        ry = top + k * (rh + g)
        c.card((60, ry, 1020, ry + rh), r=22, sh_alpha=40, blur=10, off=(0, 5))
        c.rect((60, ry, 250, ry + rh), fill=col, r=22)
        c.rect((200, ry, 250, ry + rh), fill=col)
        c.text((155, ry + rh / 2), rng, "db", 42, WH, anchor="mm")
        if sub2:
            c.text((282, ry + rh / 2 - 18), lab, "sb", 34, (30, 32, 46), anchor="lm")
            c.text((282, ry + rh / 2 + 22), sub2, "s", 27, (100, 104, 120), anchor="lm")
        else:
            c.text((282, ry + rh / 2), lab, "sb", 34, (30, 32, 46), anchor="lm")
    note = "A self-assessment, not a diagnosis"
    c.text((W / 2, top + 4 * (rh + g) + 22), note, "sbi", 30, (96, 100, 124), anchor="mm")
    c.button(P["cta"], W / 2, 978, size=44, fill=IND1)
    return c, [t1 + " " + t2, sub, "шкала 0 · 8 · 15 · 22 · 28"] + [f"{r[0]} {r[1]}" + (f" ({r[2]})" if r[2] else "") for r in rows] + [note, P["cta"]]


def s1d(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (12, 18, 48), (34, 42, 92))
    stars(c, (0, 0, W, 360), 30, 5)
    t1 = "Less time in bed,\nnot more"
    y = c.block(t1, "db", 74, 40, 980, WH, max_lines=2, gap=1.06)
    sub = "How CBT-I for insomnia works, week by week"
    y = c.block(sub, "s", 34, y + 6, 980, AMB1, max_lines=1)
    chips = ["Not below 5–5.5 h in bed", "+15 min a week", "20 min awake → get up"]
    ws = [c.tw(t, c.font("sb", 27))[0] + 44 for t in chips]
    gap = 18
    x = (W - sum(ws) - gap * 2) / 2
    cy = y + 46
    for t, w_ in zip(chips, ws):
        chip(c, t, x + w_ / 2, cy, size=27, fill=(255, 255, 255), ink=NAVY1, padx=22, pady=12, alpha=235)
        x += w_ + gap
    # окно с луной
    wb = (70, 440, 300, 690)
    c.rect((wb[0] - 14, wb[1] - 14, wb[2] + 14, wb[3] + 14), fill=(58, 66, 118), r=8)
    c.vgrad(wb, (10, 14, 40), (30, 40, 90))
    stars(c, wb, 12, 9, rmax=2.6)
    crescent(c, 220, 520, 34, (250, 226, 150), (16, 22, 54))
    c.line([((wb[0] + wb[2]) / 2, wb[1]), ((wb[0] + wb[2]) / 2, wb[3])], (58, 66, 118), 10)
    c.line([(wb[0], (wb[1] + wb[3]) / 2), (wb[2], (wb[1] + wb[3]) / 2)], (58, 66, 118), 10)
    # пол
    c.rect((0, 900, W, W), fill=(26, 28, 58))
    # кровать справа
    c.rect((760, 560, 1100, 820), fill=(64, 58, 112), r=26)
    c.rect((740, 800, 1100, 868), fill=(214, 218, 238), r=14)
    c.rect((740, 860, 1100, 900), fill=(52, 46, 92))
    c.rect((790, 740, 960, 812), fill=(240, 242, 250), r=26)
    c.poly([(900, 790), (1100, 770), (1100, 880), (880, 880)], (86, 98, 186))
    c.poly([(880, 800), (940, 796), (930, 880), (880, 880)], (116, 128, 206))
    # тумбочка
    ns = (330, 780, 710, 1080)
    c.rect((ns[0] - 10, ns[1] - 18, ns[2] + 10, ns[1] + 6), fill=(112, 88, 88), r=6)
    c.rect(ns, fill=(92, 72, 76))
    for k in range(2):
        dy = ns[1] + 40 + k * 110
        c.rect((ns[0] + 30, dy, ns[2] - 30, dy + 90), fill=(104, 82, 86), r=8)
        c.rect(((ns[0] + ns[2]) / 2 - 30, dy + 38, (ns[0] + ns[2]) / 2 + 30, dy + 50), fill=(150, 120, 110), r=5)
    # блокнот «7 questions»
    nb = (350, 596, 500, 764)
    c.shadow(nb, r=10, alpha=90, blur=8, off=(4, 6))
    c.rect(nb, fill=(244, 184, 72), r=10)
    for k in range(6):
        x = nb[0] + 18 + k * 23
        c.circle(x, nb[1] + 6, 6, fill=(220, 222, 232))
    c.text(((nb[0] + nb[2]) / 2, nb[1] + 66), "7", "db", 68, NAVY1, anchor="mm")
    c.text(((nb[0] + nb[2]) / 2, nb[1] + 126), "questions", "sb", 25, NAVY1, anchor="mm")
    # цифровой будильник 03:47
    ck = (512, 672, 668, 764)
    c.glow((ck[0] - 40, ck[1] - 40, ck[2] + 40, ck[3] + 30), (255, 110, 80), alpha=70, blur=30)
    c.rect(ck, fill=(30, 30, 40), r=16)
    c.rect((ck[0] + 12, ck[1] + 12, ck[2] - 12, ck[3] - 22), fill=(10, 10, 16), r=8)
    c.text(((ck[0] + ck[2]) / 2, (ck[1] + ck[3] - 10) / 2), "03:47", "dmb", 42, (255, 116, 84), anchor="mm")
    # стакан воды
    gx0, gx1, gyt, gyb = 676, 716, 694, 766
    c.poly([(gx0, gyt), (gx1, gyt), (gx1 - 5, gyb), (gx0 + 5, gyb)], (200, 220, 250), alpha=110)
    c.poly([(gx0 + 2, gyt + 22), (gx1 - 2, gyt + 22), (gx1 - 6, gyb - 2), (gx0 + 6, gyb - 2)], (130, 180, 240), alpha=140)
    c.line([(gx0, gyt), (gx0 + 5, gyb), (gx1 - 5, gyb), (gx1, gyt)], (220, 230, 250), 3, alpha=200)
    c.button(P["cta"], W / 2, 986, size=44, fill=CORAL1)
    return c, [t1.replace("\n", " "), sub] + chips + ["на блокноте: 7 questions", "на будильнике: 03:47", P["cta"]]


PACKS[1] = dict(
    doc="NT-psy-sleep-en-2026-09-30", cta="Learn more",
    a=dict(fn=s1a, concept="сетка выбора 2×2 (fake interactivity): 4 пути лечения бессонницы, у каждой плитки «Learn more»",
           src="раздел 5 «Insomnia treatment options: family doctor, sleep clinic or online CBT-I» (GP — the usual first step; sleep clinic — overnight sleep study; psychologist trained in CBT-I — in person or by video; online CBT-I — sleep diary and weekly steps)",
           note="иконки без логотипов: врач со стетоскопом, здание с луной, два облачка-диалога, ноутбук с луной; ни слова про таблетки, без «free» и «near me»"),
    b=dict(fn=s1b, concept="карточка-опросник: вопрос 1 из 7 теста ISI со шкалой 0–4 кружками-кнопками",
           src="раздел 1 «The Insomnia Severity Index: 7 questions about the last two weeks» (пункт 1 Difficulty falling asleep, 0 = none … 4 = very severe) + раздел 2 (self-assessment)",
           note="фиолетовая ночь, белая карточка; вопрос теста без «you/your»; подпись «A self-assessment, not a diagnosis»"),
    c=dict(fn=s1c, concept="шкала-сравнение: 4 диапазона балла 0–28 полосой и строками",
           src="раздел 2 «How the 0–28 score is read – and why it is not a diagnosis» (0–7 / 8–14 / 15–21 / 22–28, self-assessment tool)",
           note="цвет от зелёного к красному, пороги 0 · 8 · 15 · 22 · 28; под шкалой — «A self-assessment, not a diagnosis»"),
    d=dict(fn=s1d, concept="сцена-иллюстрация: тумбочка ночью — будильник 03:47, блокнот «7 questions», стакан воды, пустая кровать, луна в окне",
           src="лид («Lying awake at 3 a.m.») + раздел 4 «Cognitive behavioral therapy for insomnia: how CBT-I works, week by week» (sleep restriction: not below 5–5.5 h, +15 min a week; stimulus control: after about 20 minutes awake, get up) + adPosts РК 2 «Less time in bed, not more»",
           note="без людей и измученных лиц; заголовок-крючок из РК 2; три факта КПТ-И плашками"),
)


# =====================================================================  2. NT · психотесты · СДВГ у взрослых: ASRS (EN)
NAVY2, TEAL2, CORAL2, AMB2 = (22, 36, 66), (0, 118, 128), (228, 76, 56), (250, 200, 90)


def sticker(c, cx, cy, w, h, ang, col, num, text, ink=(36, 38, 50), num_col=(200, 60, 56), size=30):
    K = c.K
    img = Image.new("RGBA", (int(w * K), int(h * K)), col + (255,))
    dd = ImageDraw.Draw(img)
    dd.rectangle((0, 0, img.width, int(20 * K)), fill=mix(col, (0, 0, 0), 0.07) + (255,))
    dd.text((int(22 * K), int(30 * K)), num, font=c.font("db", 58), fill=num_col + (255,))
    ft = c.font("sb", size)
    lines = c.wrap(text, ft, w - 44)
    asc, desc = ft.getmetrics()
    lh = (asc + desc) * 1.06
    y = img.height - int(24 * K) - lh * len(lines)
    for ln in lines:
        dd.text((int(22 * K), y), ln, font=ft, fill=ink + (255,))
        y += lh
    rot = img.rotate(-ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    sh.putalpha(rot.getchannel("A").point(lambda v: v * 80 // 255))
    sh = sh.filter(ImageFilter.GaussianBlur(5 * K))
    X, Y = c.s(cx), c.s(cy)
    c.im.alpha_composite(sh, (X - rot.width // 2 + 6 * K, Y - rot.height // 2 + 10 * K))
    c.im.alpha_composite(rot, (X - rot.width // 2, Y - rot.height // 2))
    px, py = rotpts([(cx, cy - h / 2 + 14)], cx, cy, ang)[0]
    c.circle(px + 3, py + 5, 13, fill=(0, 0, 0), alpha=70)
    c.circle(px, py, 13, fill=(212, 56, 56))
    c.circle(px - 4, py - 4, 4, fill=WH, alpha=190)


def s2a(P):
    c = C((198, 158, 110))
    rnd = random.Random(3)
    lay = c.layer()
    dd = ImageDraw.Draw(lay)
    for _ in range(2600):
        x, y = rnd.uniform(0, W), rnd.uniform(0, W)
        r = rnd.uniform(1.2, 3.6)
        col = (150, 108, 62) if rnd.random() < 0.6 else (228, 196, 150)
        dd.ellipse(c.sb((x - r, y - r, x + r, y + r)), fill=col + (int(rnd.uniform(60, 150)),))
    c.put(lay)
    for box in ((0, 0, W, 22), (0, W - 22, W, W), (0, 0, 22, W), (W - 22, 0, W, W)):
        c.rect(box, fill=(128, 86, 50))
    hb = (70, 50, 1010, 238)
    c.card(hb, r=10, sh_alpha=80, blur=10, off=(0, 6))
    for tx in (130, 950):
        c.rect((tx - 50, hb[1] - 14, tx + 50, hb[1] + 16), fill=(250, 244, 220), alpha=210)
    t1 = "The 6-question ADHD screener doctors use for adults"
    y = c.block(t1, "db", 46, hb[1] + 30, 860, NAVY2, max_lines=2, gap=1.08)
    sub = "ASRS · about 2 minutes"
    c.block(sub, "s", 28, y + 4, 860, (96, 100, 116), max_lines=1)
    items = ["Wrapping up the final details", "Getting things in order", "Remembering appointments",
             "Getting started", "Fidgeting when sitting for long", "As if “driven by a motor”"]
    cols = [(255, 228, 112), (255, 176, 186), (164, 212, 250), (176, 228, 164), (255, 198, 124), (214, 194, 250)]
    angs = [-3, 2, -2, 2.5, -1.5, 3]
    for k, it in enumerate(items):
        cx = 216 + (k % 3) * 324
        cy = 434 + (k // 3) * 262
        sticker(c, cx, cy, 282, 228, angs[k], cols[k], str(k + 1), it, size=30)
    note = "A screener, not a diagnosis"
    nb = (290, 842, 790, 902)
    c.card(nb, fill=(252, 250, 244), r=6, sh_alpha=70, blur=8, off=(0, 5))
    c.text((W / 2, 872), note, "sbi", 30, NAVY2, anchor="mm")
    c.button(P["cta"], W / 2, 976, size=42, fill=CORAL2)
    return c, [t1, sub] + [f"{k + 1} {it}" for k, it in enumerate(items)] + [note, P["cta"]]


def s2b(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (0, 112, 122), (0, 62, 76))
    c.ellipse((-180, 760, 300, 1240), fill=WH, alpha=14)
    lx = 60
    t1, t2 = "Adult ADHD screener:", "6 questions, about 2 minutes"
    y = c.block(t1, "db", 54, 250, 450, WH, align="left", x=lx, max_lines=3, gap=1.08)
    y = c.block(t2, "db", 44, y + 6, 450, AMB2, align="left", x=lx, max_lines=3, gap=1.08)
    sub = "Past 6 months · 5 possible answers"
    y = c.block(sub, "s", 30, y + 18, 440, (200, 232, 232), align="left", x=lx, max_lines=2)
    note = "A screener, not a diagnosis"
    y = c.block(note, "sbi", 28, y + 12, 440, (176, 222, 222), align="left", x=lx, max_lines=1)
    bw = bwidth(c, P["cta"], 40)
    c.button(P["cta"], lx + bw / 2, y + 88, size=40, fill=CORAL2)
    sc = phone(c, (560, 56, 1020, 1024))
    x0, x1 = sc[0] + 32, sc[2] - 32
    yy = sc[1] + 88
    tag, step = "ASRS SCREENER", "Question 4 of 6"
    tw = c.tw(tag, c.font("sb", 22))[0]
    c.rect((x0, yy, x0 + tw + 28, yy + 38), fill=mix(TEAL2, WH, 0.86), r=19)
    c.text((x0 + 14, yy + 19), tag, "sb", 22, TEAL2, anchor="lm")
    yy += 58
    c.text((x0, yy), step, "s", 24, (110, 116, 124))
    c.rect((x0, yy + 38, x1, yy + 48), fill=(226, 232, 236), r=5)
    c.rect((x0, yy + 38, x0 + (x1 - x0) * 4 / 6, yy + 48), fill=TEAL2, r=5)
    yy += 72
    q = "How often is getting started delayed when a task needs a lot of thought?"
    yy = c.block(q, "db", 31, yy, x1 - x0, (34, 36, 46), align="left", x=x0, max_lines=5, gap=1.12)
    opts = ["Never", "Rarely", "Sometimes", "Often", "Very often"]
    radio_rows(c, opts, x0, x1, yy + 14, 64, 11, size=27)
    for k in range(6):
        c.circle((sc[0] + sc[2]) / 2 - 50 + k * 20, sc[3] - 26, 5, fill=TEAL2 if k == 3 else (210, 214, 220))
    return c, [t1 + " " + t2, sub, note, P["cta"], f"на экране: {tag} · {step} · {q} · " + " / ".join(opts)]


def s2c(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (250, 248, 244), (236, 232, 224))
    t1, t2 = "Adult ADHD assessment in 2026:", "public or private?"
    y = c.block(t1, "db", 54, 40, 980, NAVY2, max_lines=1)
    y = c.block(t2, "db", 52, y, 980, CORAL2, max_lines=1)
    sub = "Waits and typical costs in 4 countries"
    y = c.block(sub, "s", 30, y + 6, 980, (96, 98, 110), max_lines=1)
    box = (50, y + 26, 1030, 882)
    c.card(box, r=26, sh_alpha=60, blur=14, off=(0, 8))
    cx0, cx1, cx2, cx3 = box[0], box[0] + 190, box[0] + 190 + 395, box[2]
    c.rect((cx2, box[1], cx3, box[3]), fill=(253, 238, 232), r=26)
    c.rect((cx2, box[1], cx2 + 30, box[3]), fill=(253, 238, 232))
    hh = 96
    heads = [("PUBLIC OR INSURED", "cheaper, slower", TEAL2, cx1, cx2), ("PRIVATE", "faster, more expensive", CORAL2, cx2, cx3)]
    for h, s_, col, a, b in heads:
        c.text(((a + b) / 2, box[1] + 36), h, "db", 28, col, anchor="mm")
        c.text(((a + b) / 2, box[1] + 72), s_, "s", 24, (100, 104, 116), anchor="mm")
    rows = [("US", "Insurance often covers part · waits: weeks to months", "Testing about $1,000–$3,000"),
            ("UK", "GP referral · waits of months or years", "About £500–£1,500, in weeks"),
            ("Canada", "Provincial plan with referral · often a long wait", "About CA$1,500–CA$3,000"),
            ("Australia", "Rebate with GP referral · waits can run for months", "Psychologist: usually paid privately")]
    rh = (box[3] - box[1] - hh) / len(rows)
    ry = box[1] + hh
    for lab, a, b in rows:
        c.line([(box[0] + 20, ry), (box[2] - 20, ry)], (224, 226, 232), 2)
        c.text((cx0 + 26, ry + rh / 2), lab, "db", c.fit(lab, "db", cx1 - cx0 - 36, 1, 30), NAVY2, anchor="lm")
        for txt, xa, xb in ((a, cx1, cx2), (b, cx2, cx3)):
            sz = c.fit(txt, "sb", xb - xa - 44, 3, 27)
            nl = len(c.wrap(txt, c.font("sb", sz), xb - xa - 44))
            lh = c.lh("sb", sz, 1.08)
            c.block(txt, "sb", sz, ry + rh / 2 - nl * lh / 2 + 2, xb - xa - 44, (40, 42, 52), align="left", x=xa + 22, gap=1.08)
        ry += rh
    note = "Numbers vary widely"
    c.text((W / 2, 912), note, "si", 26, (110, 112, 124), anchor="mm")
    c.button(P["cta"], W / 2, 988, size=42, fill=CORAL2)
    return c, [t1 + " " + t2, sub, "PUBLIC OR INSURED (cheaper, slower) / PRIVATE (faster, more expensive)"] + \
        [f"{r[0]}: {r[1]} | {r[2]}" for r in rows] + [note, P["cta"]]


def s2d(P):
    c = C(WH)
    c.vgrad((0, 0, W, 660), (236, 240, 246), (218, 226, 238))
    S.wood(c, (0, 660, W, W), (190, 146, 100), (170, 126, 84), lines=9, seed=4)
    c.rect((0, 650, W, 666), fill=(160, 116, 76))
    t1 = "A 2-minute screener is only the start"
    y = c.block(t1, "db", 56, 40, 980, NAVY2, max_lines=2, gap=1.08)
    sub = "What a full adult ADHD assessment adds"
    y = c.block(sub, "s", 32, y + 6, 980, (90, 96, 112), max_lines=1)
    # школьный табель справа
    S.paper(c, (668, 336, 988, 690), 7, col=(250, 244, 226), lines=8, head="SCHOOL REPORT", head_col=(130, 70, 44),
            line_col=(214, 204, 180), head_size=26)
    WS.mug(c, 900, 870, 0.78, (0, 118, 128))
    S.pen(c, 690, 905, 790, 790, col=(40, 60, 140), w=13)
    # планшет с чек-листом
    board = (84, y + 40, 620, 1012)
    c.shadow(board, r=24, alpha=110, blur=16, off=(6, 12))
    c.rect(board, fill=(142, 98, 60), r=24)
    pp = (board[0] + 28, board[1] + 44, board[2] - 28, board[3] - 28)
    c.rect(pp, fill=WH, r=8)
    mx = (board[0] + board[2]) / 2
    c.rect((mx - 84, board[1] - 18, mx + 84, board[1] + 40), fill=(170, 176, 188), r=12)
    c.rect((mx - 50, board[1] - 30, mx + 50, board[1] - 6), fill=(150, 156, 168), r=10)
    head = "FULL ADULT ADHD ASSESSMENT"
    c.text((pp[0] + 30, pp[1] + 34), head, "sb", c.fit(head, "sb", pp[2] - pp[0] - 60, 1, 25), TEAL2)
    c.line([(pp[0] + 30, pp[1] + 74), (pp[2] - 30, pp[1] + 74)], (222, 226, 232), 2)
    items = ["Detailed interview", "Childhood: signs before age 12", "Longer rating scales", "Checks for other explanations",
             "Written report"]
    iy = pp[1] + 98
    step = (pp[3] - 70 - iy) / len(items)
    for it in items:
        cbox(c, pp[0] + 30, iy + 4, 38, True, (40, 160, 100))
        c.block(it, "sb", 30, iy, pp[2] - pp[0] - 120, (36, 40, 52), align="left", x=pp[0] + 88, max_lines=2, gap=1.04)
        iy += step
    foot = "1–3 appointments · 2–4 hours in total"
    c.text(((pp[0] + pp[2]) / 2, pp[3] - 34), foot, "s", c.fit(foot, "s", pp[2] - pp[0] - 50, 1, 25), (100, 106, 120), anchor="mm")
    c.button(P["cta"], 840, 990, size=40, fill=CORAL2)
    return c, [t1, sub, f"на планшете: {head} ✓ " + " ✓ ".join(items) + f" · {foot}", "лист «SCHOOL REPORT»", P["cta"]]


PACKS[2] = dict(
    doc="NT-psy-adhd-en-2026-09-30", cta="Learn more",
    a=dict(fn=s2a, concept="сетка из 6 стикеров на пробковой доске: темы 6 вопросов скрининга",
           src="раздел 1 «The 6 screening questions and the answer scale» (6 пунктов пересказом: final details, getting things in order, appointments, getting started, fidgeting, «driven by a motor») + лид (about two minutes, ASRS)",
           note="визуал гипотезы — стикеры 1–6; заголовок = заголовок статьи; подпись «A screener, not a diagnosis»; без людей в «хаосе»"),
    b=dict(fn=s2b, concept="карточка-опросник в телефоне: вопрос 4 из 6 со шкалой never … very often",
           src="раздел 1 (вопрос 4: getting started delayed when a task requires a lot of thought; 5 ответов never / rarely / sometimes / often / very often; past six months) + раздел 2 (A screener is not a diagnosis)",
           note="бирюзовый фон; вопрос теста безлично, без «you/your»; если Meta прочтёт как вопрос о здоровье — первый подозреваемый"),
    c=dict(fn=s2c, concept="сравнение «public or private»: таблица сроков и цен по 4 странам",
           src="раздел «Waiting times and costs in 2026» (US insurance often covers part, testing about $1,000–$3,000; UK GP referral, months or years vs private £500–£1,500 in weeks; Canada provincial plan vs CA$1,500–$3,000; Australia rebate with GP referral vs psychologist paid privately; «Numbers vary widely»)",
           note="цифры только из статьи; NHS / Medicare на картинке не названы (UK — «GP referral», AU — «rebate»); без «free»"),
    d=dict(fn=s2d, concept="сцена-иллюстрация: стол — планшет с чек-листом полной оценки, школьный табель, кружка, ручка",
           src="раздел «ADHD evaluation for adults: what a full assessment includes» (interview, childhood before 12 + old school reports, rating scales, other explanations, written report; 1–3 appointments, 2–4 hours) + adPosts РК 3",
           note="заголовок-крючок РК 3 «A 2-minute screener is only the start»; без людей, лекарств и «diagnosed online»"),
)


# =====================================================================  3. P60 · здоровье 60+ · бессонница после 60 (IT)
INK3, TERRA3, NIGHT3, AMB3 = (36, 40, 78), (212, 86, 52), (20, 28, 62), (250, 200, 100)


def s3a(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (252, 246, 236), (242, 228, 206))
    t1, t2 = "Insonnia dopo i 60:", "le 7 cause più comuni"
    y = c.block(t1, "db", 64, 36, 980, INK3, max_lines=1)
    y = c.block(t2, "db", 58, y - 2, 980, TERRA3, max_lines=1)
    items = [("drop_moon", "Il bagno di notte"), ("joint", "I dolori"), ("snore", "Russamento e pause del respiro"),
             ("legs", "Le gambe senza riposo"), ("flame", "Reflusso e bruciore di stomaco"),
             ("storm", "Preoccupazioni e umore basso"), ("clock", "Giornate senza orari")]
    top = y + 24
    rh, g = 90, 11
    for k, (ic, lab) in enumerate(items):
        ry = top + k * (rh + g)
        c.card((60, ry, 1020, ry + rh), r=rh / 2, sh_alpha=45, blur=10, off=(0, 5))
        c.circle(60 + rh / 2 + 4, ry + rh / 2, 34, fill=(252, 234, 216))
        ico(c, ic, 60 + rh / 2 + 4, ry + rh / 2, 50, INK3, bg=(252, 234, 216))
        c.text((60 + rh + 24, ry + rh / 2), lab, "sb", 33, (36, 38, 52), anchor="lm")
        cx = 1020 - rh / 2
        c.circle(cx, ry + rh / 2, 25, fill=TERRA3)
        c.line([(cx - 5, ry + rh / 2 - 11), (cx + 6, ry + rh / 2), (cx - 5, ry + rh / 2 + 11)], WH, 5)
    c.button(P["cta"], W / 2, top + 7 * (rh + g) + 60, size=42, fill=TERRA3)
    return c, [t1 + " " + t2] + [f"{k + 1} {it[1]}" for k, it in enumerate(items)] + [P["cta"]]


def s3b(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (30, 42, 92), (16, 22, 54))
    stars(c, (0, 0, W, W), 46, 21)
    crescent(c, 972, 92, 44, (250, 222, 150), (30, 42, 92))
    t1, t2 = "Sonno dopo i 60:", "il bisogno cala meno\ndi quanto si creda"
    y = c.block(t1, "db", 62, 44, 880, WH, max_lines=1)
    y = c.block(t2, "db", 44, y + 2, 900, AMB3, max_lines=2, gap=1.08)
    box = (70, y + 30, 1010, 870)
    c.card(box, r=36, sh_alpha=130, blur=22)
    x0, x1 = box[0] + 50, box[2] - 50
    yy = box[1] + 40
    tag = "QUIZ SONNO"
    tw = c.tw(tag, c.font("sb", 24))[0]
    c.rect((x0, yy, x0 + tw + 30, yy + 40), fill=(234, 236, 250), r=20)
    c.text((x0 + 15, yy + 20), tag, "sb", 24, (70, 84, 180), anchor="lm")
    yy += 62
    q = "Di quante ore di sonno ha ancora bisogno la maggior parte degli adulti sopra i 60 anni?"
    yy = c.block(q, "db", 38, yy, x1 - x0, (32, 34, 46), align="left", x=x0, max_lines=3, gap=1.12)
    opts = ["Circa 5 ore", "Circa 7 ore", "Circa 9 ore", "Non lo so"]
    g = 20
    ow = (x1 - x0 - g) / 2
    oh = min(118, (box[3] - 40 - yy - 20 - g) / 2)
    for k, o in enumerate(opts):
        ox = x0 + (k % 2) * (ow + g)
        oy = yy + 20 + (k // 2) * (oh + g)
        c.rect((ox, oy, ox + ow, oy + oh), fill=(244, 246, 250), r=22, outline=(206, 212, 222), width=3)
        c.circle(ox + 46, oy + oh / 2, 25, fill=(70, 84, 180))
        c.text((ox + 46, oy + oh / 2), "ABCD"[k], "db", 25, WH, anchor="mm")
        c.text((ox + 88, oy + oh / 2), o, "sb", 32, (40, 44, 56), anchor="lm")
    c.button(P["cta"], W / 2, 968, size=44, fill=TERRA3)
    return c, [t1 + " " + t2.replace("\n", " "), f"{tag}: {q}", " / ".join(opts), P["cta"]]


def s3c(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (248, 250, 246), (234, 240, 234))
    t1, t2 = "Insonnia dopo i 60:", "cosa è normale e cosa no"
    y = c.block(t1, "db", 62, 36, 980, INK3, max_lines=1)
    y = c.block(t2, "db", 54, y - 2, 980, TERRA3, max_lines=1)
    GREEN, ORANGE = (40, 150, 96), (226, 116, 40)
    blocks = [("NORMALE DOPO I 60", GREEN, (232, 246, 238), "ok",
               ["Sonno più leggero e più spezzato", "Un risveglio di pochi minuti durante la notte",
                "Sonno verso le 21, risveglio alle 4 o alle 5"]),
              ("DA PARLARNE CON IL MEDICO", ORANGE, (254, 240, 226), "!",
               ["Restare svegli per ore, quasi tutte le notti", "Almeno 3 notti a settimana, da più di 3 mesi",
                "Russamento forte con pause del respiro", "Colpi di sonno durante il giorno"])]
    top = y + 24
    shown = [t1 + " " + t2]
    for head, col, fill, mark, its in blocks:
        h = 96 + len(its) * 62
        box = (60, top, 1020, top + h)
        c.card(box, fill=fill, r=28, sh_alpha=45, blur=12, off=(0, 6))
        hw = c.tw(head, c.font("db", 30))[0] + 96
        c.rect((box[0] + 28, top + 24, box[0] + 28 + hw, top + 76), fill=col, r=26)
        c.circle(box[0] + 58, top + 50, 17, fill=WH)
        if mark == "ok":
            c.check(box[0] + 49, top + 42, 18, col, 4)
        else:
            c.text((box[0] + 58, top + 50), "!", "db", 24, col, anchor="mm")
        c.text((box[0] + 86, top + 50), head, "db", 30, WH, anchor="lm")
        iy = top + 104
        for it in its:
            c.circle(box[0] + 50, iy + 20, 9, fill=col)
            c.text((box[0] + 74, iy + 20), it, "sb", 31, (36, 38, 50), anchor="lm")
            iy += 62
        shown.append(head + ": " + " · ".join(its))
        top += h + 24
    c.button(P["cta"], W / 2, max(top + 58, 972), size=42, fill=TERRA3)
    return c, shown + [P["cta"]]


def s3d(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (16, 24, 58), (44, 56, 108))
    stars(c, (0, 0, W, 34), 8, 33)
    stars(c, (0, 190, W, 290), 10, 37)
    stars(c, (0, 290, 150, 700), 6, 34)
    stars(c, (930, 230, W, 560), 5, 35)
    stars(c, (440, 320, 640, 560), 5, 36)
    t1 = "Sonno alle 21, sveglia alle 4"
    y = c.block(t1, "db", 66, 42, 980, WH, max_lines=1)
    sub = "Perché dopo i 60 l'orologio biologico si anticipa"
    y = c.block(sub, "s", 34, y + 8, 980, (206, 214, 244), max_lines=1)
    cyc = y + 262
    # дуга-переход между часами
    pts = [(300 + (780 - 300) * t / 40, cyc - 150 - math.sin(math.pi * t / 40) * 44) for t in range(41)]
    for k in range(0, 40, 3):
        c.line(pts[k:k + 2], (250, 214, 140), 5, alpha=200)
    crescent(c, 540, cyc - 196, 28, (250, 222, 150), (24, 32, 70))
    for cx, h, lab, word in ((300, 9, "21:00", "sonno"), (780, 4, "4:00", "sveglia")):
        c.glow((cx - 150, cyc - 150, cx + 150, cyc + 150), (250, 220, 150), alpha=60, blur=30)
        clock(c, cx, cyc, 128, h, 0, face=(250, 246, 232), rim=(92, 104, 170), hand=(30, 36, 70), accent=TERRA3)
        c.text((cx, cyc + 176), lab, "db", 50, AMB3, anchor="mm")
        c.text((cx, cyc + 226), word, "s", 32, (214, 220, 246), anchor="mm")
    # спальня внизу
    fy = 870
    c.rect((0, fy, W, W), fill=(28, 30, 60))
    c.rect((40, 720, 118, fy + 40), fill=(92, 72, 88), r=14)
    c.rect((60, 800, 800, 870), fill=(226, 228, 242), r=16)
    c.rect((136, 766, 300, 822), fill=(246, 246, 252), r=24)
    c.poly([(300, 790), (800, 782), (800, 890), (280, 890)], (78, 92, 176))
    c.poly([(280, 796), (340, 794), (330, 890), (280, 890)], (110, 124, 204))
    c.rect((60, 870, 800, 906), fill=(60, 50, 80))
    ns = (850, 800, 1030, W)
    c.rect(ns, fill=(92, 72, 88), r=8)
    c.rect((ns[0] + 20, ns[1] + 30, ns[2] - 20, ns[1] + 110), fill=(104, 84, 98), r=8)
    c.glow((820, 600, 1060, 820), (255, 210, 130), alpha=90, blur=30)
    c.poly([(890, 690), (990, 690), (1010, 760), (870, 760)], (250, 214, 150))
    c.rect((934, 760, 946, 800), fill=(200, 180, 150))
    c.button(P["cta"], W / 2, 990, size=44, fill=TERRA3)
    return c, [t1, sub, "часы: 21:00 sonno · 4:00 sveglia", P["cta"]]


PACKS[3] = dict(
    doc="P60-sleep-60-it-2026-09-30", cta="Scopri di più",
    a=dict(fn=s3a, concept="сетка-выбор списком (fake interactivity): 7 причин строками-кнопками со стрелкой",
           src="раздел «Le 7 cause più comuni delle notti in bianco dopo i 60» (bagno di notte, dolori, russamento e pause del respiro, gambe senza riposo, reflusso e bruciore di stomaco, preoccupazioni e umore basso, giornate senza orari)",
           note="каждая строка — как пункт меню с красной стрелкой; иконки без таблеток и лекарств; «60» — тема, не обращение"),
    b=dict(fn=s3b, concept="карточка-опросник 2×2 о правиле, не о зрителе: сколько сна нужно после 60",
           src="раздел «Cosa cambia nel sonno dopo i 60» («Il bisogno di sonno, invece, cala meno di quanto si creda: la maggior parte degli adulti sopra i 60 anni ha ancora bisogno di circa 7 ore»)",
           note="ночной фон, вопрос о факте (ответ «circa 7 ore» — в статье); без «Non riesci a dormire?» и «Il tuo sonno»"),
    c=dict(fn=s3c, concept="сравнение «normale / da parlarne con il medico» двумя карточками",
           src="раздел «Cosa cambia nel sonno dopo i 60» (sonno più leggero e frammentato, risveglio di pochi minuti — normale, sonno verso le 21 e risveglio alle 4–5; restare svegli per ore quasi tutte le notti — no) + раздел «Quando rivolgersi al medico: 6 segnali» (3 notti a settimana da più di 3 mesi, russamento forte con pause, colpi di sonno)",
           note="зелёная карточка ✓ и оранжевая «!»; пункт про мелатонин из статьи не вынесен (запрет)"),
    d=dict(fn=s3d, concept="сцена-иллюстрация: двое часов 21:00 и 4:00 над ночной спальней с пустой кроватью",
           src="раздел «Cosa cambia nel sonno dopo i 60» («l'orologio biologico tende ad anticiparsi: il sonno arriva già verso le 21 e il risveglio alle 4 o alle 5») + adPosts РК 2 «Sonno alle 21, sveglia alle 4»",
           note="заголовок-крючок РК 2; без людей, без до/после"),
)


# =====================================================================  4. NT · донорство спермы · FR
NAVY4, CORAL4, BLUE4 = (22, 42, 96), (222, 66, 72), (28, 96, 180)
NB = " "


def s4a(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (238, 245, 252), (220, 232, 248))
    t1, t2 = f"Don de sperme en France{NB}:", "les 3 principes du don"
    y = c.block(t1, "mx", 58, 42, 980, NAVY4, max_lines=1)
    y = c.block(t2, "mx", 52, y, 980, CORAL4, max_lines=1)
    tiles = [("heart_hands", "GRATUIT", "Le don ne coûte rien au donneur"),
             ("doc_sign", "VOLONTAIRE", "Consentement écrit, révocable tant que le don n'est pas utilisé"),
             ("anon", "ANONYME", "Le donneur ne connaît pas les familles")]
    top, bot = y + 30, 744
    g = 24
    tw = (960 - 2 * g) / 3
    ws = min(c.fit(t[1], "db", tw - 36, 1, 36) for t in tiles)
    ds = min(c.fit(t[2], "s", tw - 40, 4, 28) for t in tiles)
    for k, (ic, word, desc) in enumerate(tiles):
        x0 = 60 + k * (tw + g)
        box = (x0, top, x0 + tw, bot)
        c.card(box, r=28, sh_alpha=55, blur=14, off=(0, 8))
        cx = x0 + tw / 2
        c.circle(cx, top + 96, 70, fill=(226, 236, 250))
        ico(c, ic, cx, top + 96, 102, NAVY4, bg=(226, 236, 250))
        c.text((cx, top + 206), word, "db", ws, BLUE4, anchor="mm")
        c.block(desc, "s", ds, top + 244, tw - 40, (54, 60, 78), cx=cx, gap=1.1)
        c.pill(P["cta"], cx, bot - 40, size=21, fill=CORAL4, padx=18, pady=11)
    fb = (60, 774, 1020, 1010)
    c.card(fb, fill=NAVY4, r=28, sh_alpha=70, blur=14, off=(0, 8))
    c.text((fb[0] + 150, (fb[1] + fb[3]) / 2 + 4), "10", "mx", 150, (255, 120, 120), anchor="mm")
    l1, l2 = "naissances maximum", "par donneur"
    c.text((fb[0] + 290, fb[1] + 56), l1, "mb", 46, WH, anchor="lm")
    c.text((fb[0] + 290, fb[1] + 112), l2, "mb", 46, WH, anchor="lm")
    why = "pour limiter le nombre de demi-frères et demi-sœurs"
    c.block(why, "s", 26, fb[1] + 154, fb[2] - fb[0] - 320, (200, 212, 240), align="left", x=fb[0] + 290, max_lines=2, gap=1.08)
    return c, [t1 + " " + t2] + [f"{t[1]} – {t[2]}" for t in tiles] + [f"×3 «{P['cta']}»", f"10 {l1} {l2} – {why}"]


def s4b(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (255, 245, 236), (252, 224, 206))
    c.ellipse((780, -160, 1260, 320), fill=WH, alpha=30)
    t1, t2 = f"Don de sperme{NB}:", f"vrai ou faux{NB}?"
    y = c.block(t1, "mx", 62, 44, 980, NAVY4, max_lines=1)
    y = c.block(t2, "mx", 62, y - 4, 980, CORAL4, max_lines=1)
    sts = ["Il faut déjà avoir un enfant pour donner", "Le don est possible de 18 à 45 ans",
           "Le donneur connaît les familles", "À 18 ans, l'enfant peut demander l'identité du donneur"]
    top = y + 32
    rh, g = 140, 22
    ss = min(c.fit(s_, "sb", 560, 2, 32) for s_ in sts)
    for k, s_ in enumerate(sts):
        ry = top + k * (rh + g)
        c.card((60, ry, 1020, ry + rh), r=26, sh_alpha=50, blur=12, off=(0, 6))
        c.circle(112, ry + rh / 2, 26, fill=(236, 240, 250))
        c.text((112, ry + rh / 2), str(k + 1), "db", 26, NAVY4, anchor="mm")
        nl = len(c.wrap(s_, c.font("sb", ss), 560))
        lh = c.lh("sb", ss, 1.08)
        c.block(s_, "sb", ss, ry + rh / 2 - nl * lh / 2 + 2, 560, (34, 38, 54), align="left", x=156, gap=1.08)
        for lab, col, bx in (("VRAI", (34, 150, 90), 740), ("FAUX", CORAL4, 880)):
            b = (bx, ry + rh / 2 - 30, bx + 118, ry + rh / 2 + 30)
            c.rect(b, fill=WH, r=30, outline=col, width=4)
            c.text(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), lab, "db", 25, col, anchor="mm")
    c.button(P["cta"], W / 2, 976, size=42, fill=CORAL4)
    return c, [t1 + " " + t2] + [f"{k + 1} {s_} [VRAI] [FAUX]" for k, s_ in enumerate(sts)] + [P["cta"]]


def s4c(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (255, 255, 255), (232, 240, 250))
    t1, t2 = f"Don de sperme{NB}: anonyme,", "mais pas tout à fait"
    y = c.block(t1, "mx", 56, 40, 980, NAVY4, max_lines=1)
    y = c.block(t2, "mx", 56, y - 2, 980, CORAL4, max_lines=1)
    sub = "Ce qui a changé en septembre 2022"
    y = c.block(sub, "s", 32, y + 6, 980, (86, 94, 116), max_lines=1)
    top, bot = y + 28, 880
    GREY = (122, 128, 146)
    L, R = (60, top, 522, bot), (558, top, 1020, bot)
    cols = [("AVANT 2022", GREY, "padlock", ["anonyme", "anonymat total", "aucun"]),
            ("DEPUIS 2022", BLUE4, "key_plus", ["anonyme", "accès aux origines et à l'identité, sur demande", "aucun"])]
    labels = ["AU MOMENT DU DON", "À 18 ANS, POUR L'ENFANT NÉ DU DON", "LIEN DE FILIATION"]
    iw = 462 - 64
    ry0 = top + 236
    hs = []
    for i, lab in enumerate(labels):
        nl = max(len(c.wrap(cols[0][3][i], c.font("sb", 30), iw)), len(c.wrap(cols[1][3][i], c.font("sb", 30), iw)))
        hs.append(30 + nl * c.lh("sb", 30, 1.06))
    spare = (bot - 24 - ry0 - sum(hs)) / (len(hs) - 1)
    for box, (head, col, ic, vals) in zip((L, R), cols):
        c.card(box, fill=mix(col, WH, 0.9), r=30, sh_alpha=45, blur=12, off=(0, 6))
        c.rect((box[0], box[1], box[2], box[1] + 88), fill=col, r=30)
        c.rect((box[0], box[1] + 58, box[2], box[1] + 88), fill=col)
        c.text(((box[0] + box[2]) / 2, box[1] + 44), head, "mx", 34, WH, anchor="mm")
        c.circle((box[0] + box[2]) / 2, box[1] + 152, 50, fill=WH)
        ico(c, ic, (box[0] + box[2]) / 2, box[1] + 152, 74, col)
        ry = ry0
        for lab, v, h in zip(labels, vals, hs):
            c.block(lab, "sb", c.fit(lab, "sb", iw, 1, 21), ry, iw, col, align="left", x=box[0] + 32, max_lines=1)
            c.block(v, "sb", 30, ry + 32, iw, (32, 36, 52), align="left", x=box[0] + 32, gap=1.06)
            ry += h + spare
    c.circle(W / 2, top + 152, 34, fill=WH, outline=(200, 206, 216), width=3)
    c.text((W / 2, top + 152), "→", "sb", 34, (90, 96, 110), anchor="mm")
    c.button(P["cta"], W / 2, 972, size=42, fill=CORAL4)
    return c, [t1 + " " + t2, sub] + [f"{h}: " + " · ".join(f"{l_} – {v}" for l_, v in zip(labels, vs)) for h, _, _, vs in cols] + [P["cta"]]


def s4d(P):
    c = C(WH)
    c.vgrad((0, 0, W, 800), (242, 246, 250), (226, 234, 244))
    c.rect((0, 800, W, W), fill=(212, 204, 194))
    for k in range(6):
        c.line([(0, 820 + k * 46), (W, 820 + k * 46)], (200, 192, 182), 2)
    kick = "DON DE SPERME EN FRANCE"
    c.text((W / 2, 52), kick, "sb", 26, CORAL4, anchor="mm")
    t1 = "Pourquoi de plus en plus d'hommes s'y intéressent"
    y = c.block(t1, "mx", 50, 78, 960, NAVY4, max_lines=2, gap=1.08)
    sub = "Possible sans avoir eu d'enfant, en quelques rendez-vous"
    y = c.block(sub, "s", 31, y + 6, 980, (80, 88, 110), max_lines=1)
    steps = ["Premier rendez-vous", "Examens", "Recueils", "Contrôle final"]
    g = 30
    sw = (960 - 3 * g) / 4
    sy = y + 26
    sh = 104
    fs0 = min(c.fit(st, "sb", sw - 76, 2, 26) for st in steps)
    for k, st in enumerate(steps):
        x0 = 60 + k * (sw + g)
        c.card((x0, sy, x0 + sw, sy + sh), r=20, sh_alpha=50, blur=10, off=(0, 5))
        c.circle(x0 + 34, sy + sh / 2, 21, fill=BLUE4)
        c.text((x0 + 34, sy + sh / 2), str(k + 1), "db", 24, WH, anchor="mm")
        fs = fs0
        nl = len(c.wrap(st, c.font("sb", fs), sw - 76))
        lh = c.lh("sb", fs, 1.04)
        c.block(st, "sb", fs, sy + sh / 2 - nl * lh / 2 + 1, sw - 76, NAVY4, align="left", x=x0 + 64, gap=1.04)
        if k < 3:
            ax = x0 + sw + g / 2
            c.poly([(ax - 8, sy + sh / 2 - 12), (ax + 10, sy + sh / 2), (ax - 8, sy + sh / 2 + 12)], CORAL4)
    # сцена: кабинет центра
    top = sy + sh + 34
    WS.window(c, (96, top + 20, 330, top + 250), sky0=(170, 210, 240), sky1=(226, 240, 250))
    cb = (730, top + 8, 990, top + 262)
    c.shadow(cb, r=12, alpha=80, blur=14, off=(0, 10))
    c.rect(cb, fill=WH, r=12)
    c.rect((cb[0], cb[1], cb[2], cb[1] + 64), fill=BLUE4, r=12)
    c.rect((cb[0], cb[1] + 40, cb[2], cb[1] + 64), fill=BLUE4)
    for k in range(5):
        xx = cb[0] + 40 + k * (cb[2] - cb[0] - 80) / 4
        c.rect((xx - 4, cb[1] - 14, xx + 4, cb[1] + 14), fill=(150, 150, 160), r=3)
    c.text(((cb[0] + cb[2]) / 2, cb[1] + 34), "RENDEZ-VOUS", "sb", 26, WH, anchor="mm")
    cw = (cb[2] - cb[0] - 30) / 7
    chh = (cb[3] - cb[1] - 64 - 24) / 5
    marks = {(0, 2): 1, (1, 3): 2, (2, 1): 3, (4, 2): 4}
    for r_ in range(5):
        for q in range(7):
            x0_ = cb[0] + 15 + q * cw
            y0_ = cb[1] + 76 + r_ * chh
            box_ = (x0_ + 4, y0_ + 4, x0_ + cw - 4, y0_ + chh - 4)
            if (r_, q) in marks:
                c.rect(box_, fill=CORAL4, r=6)
                c.text(((box_[0] + box_[2]) / 2, (box_[1] + box_[3]) / 2), str(marks[(r_, q)]), "db", 20, WH, anchor="mm")
            else:
                c.rect(box_, fill=(234, 238, 246) if q < 5 else (246, 248, 252), r=6)
    # стол
    dt = 830
    c.rect((300, dt - 14, 960, dt + 8), fill=(170, 124, 84), r=6)
    c.rect((320, dt + 8, 340, 1010), fill=(150, 108, 72))
    c.rect((920, dt + 8, 940, 1010), fill=(150, 108, 72))
    c.rect((560, dt + 8, 940, dt + 120), fill=(160, 116, 78), r=4)
    S.plant(c, 880, dt - 14, 0.42, pot=(236, 236, 240), leaf=(70, 146, 96))
    S.paper(c, (440, dt - 100, 640, dt - 12), -3, col=WH, lines=3, head="CONSENTEMENT", head_col=NAVY4, head_size=18)
    S.pen(c, 660, dt - 26, 760, dt - 40, col=BLUE4, w=10)
    # два стула
    for x in (140, 1000):
        c.rect((x - 60, 760, x + 60, 800), fill=(76, 110, 170), r=10)
        c.rect((x - 60, 800, x + 60, 830), fill=(64, 96, 150), r=6)
        c.rect((x - 52, 830, x - 40, 950), fill=(60, 64, 76))
        c.rect((x + 40, 830, x + 52, 950), fill=(60, 64, 76))
    c.button(P["cta"], W / 2, 988, size=42, fill=CORAL4)
    return c, [kick, t1, sub] + [f"{k + 1} {s_}" for k, s_ in enumerate(steps)] + ["календарь «RENDEZ-VOUS» с 4 отмеченными днями 1–4", "лист «CONSENTEMENT»", P["cta"]]


PACKS[4] = dict(
    doc="NT-sperm-donation-fr-2026-09-30", cta="En savoir plus",
    a=dict(fn=s4a, concept="сетка-выбор из 3 плиток-принципов, у каждой «En savoir plus», и плашка «10 naissances maximum»",
           src="раздел «Gratuit, volontaire, anonyme : les trois principes du don» (le don ne coûte rien au donneur — из раздела о расходах; consentement écrit, retour possible tant que non utilisé; le donneur ne connaît pas les familles; pas plus de dix naissances)",
           note="без денег: ни «rémunéré», ни «€», ни «indemnité»; иконки — сердце в ладонях, подпись документа, силуэт с «?»; без эмблем центров"),
    b=dict(fn=s4b, concept="карточка-опросник «Vrai ou faux ?»: 4 утверждения с кнопками VRAI / FAUX (fake interactivity)",
           src="разделы «Conditions pour devenir donneur» (18–45 ans; plus nécessaire d'avoir eu un enfant), «Gratuit, volontaire, anonyme» (le donneur ne connaît pas les familles), «Anonymat et accès aux origines» (à 18 ans — identité sur demande)",
           note="ответы в статье (faux / vrai / faux / vrai); пункт «rémunéré» из брифа заменён на «connaît les familles» — запрет денег; утверждения о правилах, не о зрителе"),
    c=dict(fn=s4c, concept="сравнение «Avant 2022 / Depuis 2022» двумя колонками (замок → ключ)",
           src="раздел «Anonymat et accès aux origines : ce qui a changé en 2022» (anonymat au moment du don; à 18 ans accès aux données non identifiantes et à l'identité sur demande; aucun lien de filiation) + adPosts РК 3 «Anonyme, mais pas tout à fait»",
           note="заголовок-крючок РК 3; «anonymat total» до 2022 — формулировка брифа gaps"),
    d=dict(fn=s4d, concept="сцена-иллюстрация: кабинет центра (стол, лист «CONSENTEMENT», календарь с 4 датами, стулья, окно) + 4 шага пути",
           src="заголовок статьи («pourquoi de plus en plus d'hommes s'y intéressent») + раздел «Frais pris en charge et pourquoi l'intérêt augmente» (possible sans avoir eu d'enfant, en quelques rendez-vous) + раздел «Le parcours du don … étape par étape» (4 шага)",
           note="без людей, пробирок и откровенных образов; без названия CECOS и эмблем"),
)


# =====================================================================  5. NT · услуги · массаж на дому · GB
GREEN5, SAGE5, TERRA5, SAND5 = (28, 58, 48), (96, 146, 120), (204, 92, 60), (246, 238, 226)


def s5a(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (240, 246, 240), (224, 236, 226))
    t1, t2 = "Massage at home in 2026:", "6 types – pick one"
    y = c.block(t1, "mx", 56, 38, 980, GREEN5, max_lines=1)
    y = c.block(t2, "mx", 46, y - 2, 980, TERRA5, max_lines=1)
    tiles = [("leaf", "Relaxing (Swedish)", "Light to medium pressure"),
             ("press", "Deep tissue", "Slower, firmer pressure"),
             ("shoe", "Mobile sports", "Before an event or after training"),
             ("oil", "Aromatherapy", "A blend of essential oils"),
             ("pillow", "Pregnancy", "On the side, by trained therapists"),
             ("people2", "Couples & groups", "Two therapists at once")]
    pal = dict(tile=WH, iconbg=(226, 240, 230), icon=GREEN5, ink=GREEN5, sub=(96, 110, 104), btn=TERRA5)
    tiles_grid(c, tiles, y + 26, 1044, 3, P["cta"], pal, label_size=30, sub_size=24, icon_r=58, gap=22, pill_size=21)
    return c, [t1 + " " + t2] + [f"{t[1]} – {t[2]}" for t in tiles] + [f"×6 «{P['cta']}»"]


def s5b(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (248, 240, 228), (234, 218, 196))
    t1, t2 = "Before booking a mobile\nmassage therapist:", "6 checks"
    y = c.block(t1, "db", 50, 40, 960, GREEN5, max_lines=2, gap=1.08)
    y = c.block(t2, "db", 50, y, 960, TERRA5, max_lines=1)
    box = (90, y + 28, 990, 900)
    c.card(box, r=22, sh_alpha=80, blur=16, off=(0, 10))
    c.rect((box[0], box[1], box[2], box[1] + 18), fill=SAGE5, r=22)
    c.rect((box[0], box[1] + 10, box[2], box[1] + 22), fill=WH)
    items = ["Qualifications: Level 3 diploma or higher", "Professional and public liability insurance",
             "Membership of a professional association", "Recent reviews from other clients",
             "A health questionnaire before the session", "Clear prices, travel fees and cancellation terms"]
    iy = box[1] + 46
    step = (box[3] - 30 - iy) / len(items)
    fs = min(c.fit(it, "sb", box[2] - box[0] - 150, 1, 32) for it in items)
    for k, it in enumerate(items):
        cbox(c, box[0] + 40, iy + step / 2 - 22, 44, k < 2, SAGE5)
        c.text((box[0] + 108, iy + step / 2), it, "sb", fs, (36, 44, 42), anchor="lm")
        if k < len(items) - 1:
            c.line([(box[0] + 108, iy + step), (box[2] - 40, iy + step)], (232, 228, 220), 2)
        iy += step
    c.button(P["cta"], W / 2, 976, size=42, fill=TERRA5)
    return c, [t1.replace("\n", " ") + " " + t2] + [("☑ " if k < 2 else "☐ ") + it for k, it in enumerate(items)] + [P["cta"]]


def s5c(P):
    c = C(WH)
    c.vgrad((0, 0, W, W), (252, 250, 246), (238, 242, 236))
    t1, t2 = "At-home massage price 2026:", "what it depends on"
    y = c.block(t1, "db", 50, 52, 660, GREEN5, align="left", x=60, max_lines=2, gap=1.06)
    y = c.block(t2, "db", 46, y, 660, TERRA5, align="left", x=60, max_lines=1)
    # ценник «£?»
    tcx, tcy = 876, 150
    pts = [(tcx - 120, tcy - 72), (tcx + 70, tcy - 72), (tcx + 130, tcy), (tcx + 70, tcy + 72), (tcx - 120, tcy + 72)]
    pts = rotpts(pts, tcx, tcy, -8)
    c.shadow((tcx - 120, tcy - 60, tcx + 120, tcy + 90), r=20, alpha=70, blur=14, off=(0, 8))
    c.poly(pts, TERRA5)
    hx, hy = rotpts([(tcx + 76, tcy)], tcx, tcy, -8)[0]
    c.circle(hx, hy, 12, fill=WH)
    c.text((tcx - 30, tcy + 2), "£?", "db", 76, WH, anchor="mm")
    tiles = [("clock", "Session length", "60, 90 or 120 minutes"),
             ("press", "Type of massage", "Sports and deep tissue often cost a little more"),
             ("moon_cal", "Evenings & weekends", "Often a surcharge"),
             ("city", "City", "Central London typically the highest"),
             ("car", "Travel distance", "A fee outside the usual area"),
             ("stones", "Extras", "Second therapist, hot stones, last-minute")]
    top = max(y, 250) + 30
    bot = 858
    g = 20
    tw = (960 - 2 * g) / 3
    th = (bot - top - g) / 2
    ds = min(c.fit(t[2], "s", tw - 40, 2, 25) for t in tiles)
    for k, (ic, lab, d) in enumerate(tiles):
        x0 = 60 + (k % 3) * (tw + g)
        y0 = top + (k // 3) * (th + g)
        c.card((x0, y0, x0 + tw, y0 + th), r=24, sh_alpha=45, blur=12, off=(0, 6))
        cx = x0 + tw / 2
        c.circle(cx, y0 + 78, 54, fill=(226, 240, 230))
        ico(c, ic, cx, y0 + 78, 76, GREEN5, bg=(226, 240, 230))
        c.text((cx, y0 + 160), lab, "sb", c.fit(lab, "sb", tw - 30, 1, 29), GREEN5, anchor="mm")
        c.block(d, "s", ds, y0 + 190, tw - 40, (96, 106, 102), cx=cx, gap=1.08)
    foot = "Usually more than a salon: travel and setup are included"
    c.block(foot, "sb", 29, 884, 980, GREEN5, max_lines=1)
    c.button(P["cta"], W / 2, 984, size=42, fill=TERRA5)
    return c, [t1 + " " + t2, "ценник «£?» (без суммы)"] + [f"{t[1]} – {t[2]}" for t in tiles] + [foot, P["cta"]]


def massage_table(c, x0, x1, top, floor_y):
    pad = (126, 168, 146)
    # ножки (А-образные)
    for lx in (x0 + 60, x1 - 60):
        c.line([(lx - 36, top + 44), (lx + 26, floor_y)], (150, 116, 80), 13)
        c.line([(lx + 36, top + 44), (lx - 26, floor_y)], (170, 132, 92), 13)
    c.line([(x0 + 60, top + 150), (x1 - 60, top + 150)], (150, 116, 80), 8)
    c.rect((x0, top + 30, x1, top + 50), fill=(170, 132, 92), r=6)
    c.rect((x0 - 6, top - 6, x1 + 6, top + 38), fill=pad, r=18)
    c.rect((x0 + 10, top, x1 - 10, top + 10), fill=mix(pad, WH, 0.3), r=5)
    # подголовник
    c.rect((x1 + 8, top + 10, x1 + 30, top + 26), fill=(150, 116, 80), r=4)
    c.ellipse((x1 + 26, top - 4, x1 + 104, top + 34), fill=pad)
    c.ellipse((x1 + 48, top + 6, x1 + 82, top + 22), fill=mix(pad, (0, 0, 0), 0.25))


def s5d(P):
    c = C(WH)
    c.vgrad((0, 0, W, 800), (248, 240, 230), (238, 226, 210))
    S.wood(c, (0, 800, W, W), (206, 166, 124), (188, 146, 104), lines=8, seed=7)
    c.rect((0, 792, W, 806), fill=(226, 214, 198))
    kick = "NO TRIP TO THE SPA"
    c.text((W / 2, 50), kick, "sb", 26, TERRA5, anchor="mm")
    t1 = "At-home massage:\nwhat a session includes"
    y = c.block(t1, "mx", 56, 76, 980, GREEN5, max_lines=2, gap=1.08)
    # окно со шторами
    WS.window(c, (80, 330, 300, 600), sky0=(186, 220, 240), sky1=(234, 244, 250))
    c.rect((50, 308, 100, 640), fill=(214, 150, 120), r=10)
    c.rect((280, 308, 330, 640), fill=(214, 150, 120), r=10)
    # настенные часы + плашка сеанса
    clock(c, 920, 380, 62, 3, 0, face=WH, rim=(70, 90, 80), hand=GREEN5, accent=TERRA5)
    # коврик / место 2 × 3 м (пунктир)
    fl = (150, 850, 930, 960)
    k = fl[0]
    while k < fl[2]:
        c.line([(k, fl[1]), (min(k + 26, fl[2]), fl[1])], GREEN5, 4)
        c.line([(k, fl[3]), (min(k + 26, fl[2]), fl[3])], GREEN5, 4)
        k += 44
    k = fl[1]
    while k < fl[3]:
        c.line([(fl[0], k), (fl[0], min(k + 20, fl[3]))], GREEN5, 4)
        c.line([(fl[2], k), (fl[2], min(k + 20, fl[3]))], GREEN5, 4)
        k += 36
    # растение
    S.plant(c, 1000, 820, 0.85, pot=(236, 232, 224), leaf=(76, 140, 96))
    # табурет с маслами и колонкой
    st = (60, 700, 220, 730)
    c.rect(st, fill=(170, 132, 92), r=8)
    c.rect((80, 730, 94, 880), fill=(150, 116, 80))
    c.rect((186, 730, 200, 880), fill=(150, 116, 80))
    for bx, col in ((84, (190, 120, 60)), (120, (120, 150, 90)), (156, (170, 90, 110))):
        c.rect((bx - 14, 640, bx + 14, 700), fill=col, r=8)
        c.rect((bx - 6, 624, bx + 6, 642), fill=(60, 60, 64), r=3)
    c.rect((184, 650, 216, 700), fill=(60, 64, 72), r=8)
    c.circle(200, 676, 9, fill=(120, 124, 132))
    # массажный стол с полотенцами
    ttop = 680
    massage_table(c, 330, 790, ttop, 900)
    for i, col in enumerate(((250, 250, 248), (206, 178, 146), (250, 250, 248))):
        c.rect((356, ttop - 22 - i * 24, 500, ttop - i * 24), fill=col, r=8)
    c.ellipse((640, ttop - 44, 690, ttop - 4), fill=(236, 226, 206))
    c.rect((665, ttop - 44, 760, ttop - 4), fill=(250, 250, 246))
    c.ellipse((735, ttop - 44, 785, ttop - 4), fill=(236, 232, 224))
    c.ellipse((747, ttop - 34, 773, ttop - 14), fill=(222, 214, 196))
    # плашки-подписи
    chips = ["Set up in 10–15 minutes", "60 / 90 / 120 min", "About 2 × 3 m of space"]
    chip(c, chips[0], 560, ttop - 120, size=27, fill=WH, ink=GREEN5, dot=TERRA5)
    chip(c, chips[1], 720, 380, size=27, fill=WH, ink=GREEN5, dot=TERRA5)
    chip(c, chips[2], 540, 905, size=26, fill=WH, ink=GREEN5, dot=TERRA5)
    c.button(P["cta"], W / 2, 1006, size=40, fill=TERRA5, pady=18)
    return c, [kick, t1.replace("\n", " ")] + chips + [P["cta"]]


PACKS[5] = dict(
    doc="NT-athome-massage-gb-2026-09-30", cta="Learn more",
    a=dict(fn=s5a, concept="сетка выбора 3×2 (fake interactivity): 6 видов массажа на дому, у каждой плитки «Learn more»",
           src="раздел «Types of massage offered at home» (Swedish/relaxing — light to medium pressure; deep tissue — slower, firmer; mobile sports — before an event or after heavy training; aromatherapy — blend of essential oils; pregnancy — on the side, therapists trained in it; couples & groups — two therapists at once)",
           note="иконки без тел: лист, давление на слои, кроссовок, флакон с каплей, С-подушка с сердцем, два силуэта; без мед. обещаний и цен"),
    b=dict(fn=s5b, concept="карточка-чек-лист «6 checks» с галочками (2 отмечены — fake interactivity)",
           src="раздел «How to choose an at-home massage therapist» (Level 3 diploma, professional and public liability insurance, professional association, recent reviews, health questionnaire, clear prices incl. travel fees and cancellation terms) + adPosts РК 3",
           note="без логотипов ассоциаций и платформ, без «private / discreet / sensual»"),
    c=dict(fn=s5c, concept="«сколько стоит»: ценник «£?» и 6 факторов цены плитками",
           src="раздел «What affects the price» (length 60/90/120, type, evenings/weekends/bank holidays surcharge, city — central London highest, travel distance fee, extras: second therapist, hot stones, last-minute) + первая фраза раздела (costs more than a salon: travel and setup included)",
           note="сумм в £ нет — только «£?», статья раскрывает, от чего зависит цена; «City» — фактор, не обращение к локации"),
    d=dict(fn=s5d, concept="сцена-иллюстрация: гостиная — складной массажный стол с полотенцами, табурет с маслами и колонкой, пунктир «2 × 3 m» на полу, часы",
           src="раздел «What a session includes» (arrives 10–15 minutes before to set up; table, towels, oils, small speaker; clear space about two by three metres; sessions 60, 90 or 120 minutes) + лид (no trip to a spa)",
           note="без людей и тел; без «to your door / near me»"),
)


# =====================================================================  проверка запретов и сборка
BANNED = [r"\byou\b", r"\byour\b", r"\bfree\b", r"\bcure", r"\bfix", r"guarantee", r"\bpill", r"melaton", r"sleeping pill",
          r"rémunér", r"gagner", "€", r"\bargent", r"\bpayé", r"indemnit", r"discreet", r"sensual",
          r"near (me|you|home)", r"in your area", r"click", r"nhs", r"medicare", r"\bwho\b", r"cecos", r"\bssn\b", r"\basl\b",
          r"près de", r"vicino", r"cura\b", r"guarir", r"gratis", r"diagnosed online", r"to your door", r"pain relief",
          r"heals", r"reduces stress", r"nearby", r"\bmy\b"]


def check_texts(doc, letter, shown):
    import re
    bad = []
    for s_ in shown:
        low = s_.lower()
        for pat in BANNED:
            if re.search(pat, low):
                bad.append((pat, s_))
        if doc.startswith("NT-athome"):
            if "£" in s_ and "£?" not in s_:
                bad.append(("£-сумма", s_))
            if re.search(r"\bprivate\b", low):
                bad.append(("private", s_))
    for pat, s_ in bad:
        print(f"  !! {doc}/{letter}: «{pat}» в «{s_}»")
    return not bad


def build(n, letters="abcd", save=True):
    P = PACKS[n]
    doc = P["doc"]
    items = []
    for Lt in "abcd":
        t = P[Lt]
        c, shown = t["fn"](P)
        check_texts(doc, Lt, shown)
        if save and Lt in letters:
            c.save(f"{doc}/{Lt}.png")
        items.append(dict(letter=Lt, file=f"cr/packs/{doc}/{Lt}.png",
                          concept=t["concept"] + " — " + t["note"] + "; опора: " + t["src"],
                          text=" · ".join(shown), cta=P["cta"]))
    if save:
        os.makedirs(os.path.join(OUT6, doc), exist_ok=True)
        with open(os.path.join(OUT6, doc, "creatives.json"), "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if a == "icons":
            icon_sheet()
        elif a == "check":
            for k in PACKS:
                build(k, save=False)
        elif ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
