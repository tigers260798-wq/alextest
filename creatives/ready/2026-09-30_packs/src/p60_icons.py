"""Плоские иконки для сеток и сравнений. Каждая рисуется в квадрате со стороной s с центром (cx, cy).
Без логотипов, гербов, эмблем и знаков различия."""
import math
from p60_lib import mix, rotpts

WH = (255, 255, 255)


def person(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy - s * 0.2, s * 0.17, fill=col)
    c.rect((cx - s * 0.3, cy + s * 0.02, cx + s * 0.3, cy + s * 0.42), fill=col, r=s * 0.18)
    c.rect((cx - s * 0.3, cy + s * 0.3, cx + s * 0.3, cy + s * 0.42), fill=col)


def person_check(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    person(c, cx - s * 0.1, cy, s * 0.9, col)
    c.circle(cx + s * 0.28, cy + s * 0.24, s * 0.17, fill=acc, outline=bg, width=s * 0.04)
    c.check(cx + s * 0.19, cy + s * 0.16, s * 0.17, bg, s * 0.045)


def people2(c, cx, cy, s, col, bg=WH):
    person(c, cx + s * 0.16, cy - s * 0.02, s * 0.8, mix(col, bg, 0.45))
    person(c, cx - s * 0.14, cy + s * 0.04, s * 0.85, col)


def calendar(c, cx, cy, s, col, bg=WH, acc=None):
    acc = acc or col
    x0, y0, x1, y1 = cx - s * 0.4, cy - s * 0.34, cx + s * 0.4, cy + s * 0.42
    c.rect((x0, y0, x1, y1), fill=bg, r=s * 0.08, outline=col, width=s * 0.05)
    c.rect((x0, y0, x1, y0 + s * 0.2), fill=col, r=s * 0.08)
    c.rect((x0, y0 + s * 0.1, x1, y0 + s * 0.2), fill=col)
    for k in (-1, 1):
        c.rect((cx + k * s * 0.2 - s * 0.035, y0 - s * 0.1, cx + k * s * 0.2 + s * 0.035, y0 + s * 0.06), fill=col, r=s * 0.03)
    for i in range(3):
        for j in range(2):
            x = x0 + s * 0.14 + i * s * 0.26
            y = y0 + s * 0.34 + j * s * 0.2
            c.rect((x - s * 0.06, y - s * 0.05, x + s * 0.06, y + s * 0.05), fill=acc if (i, j) == (1, 1) else mix(col, bg, 0.7), r=s * 0.02)


def coins(c, cx, cy, s, col, bg=WH, gold=(236, 180, 50)):
    for k in range(4):
        y = cy + s * 0.3 - k * s * 0.13
        c.ellipse((cx - s * 0.36, y - s * 0.08, cx + s * 0.16, y + s * 0.08), fill=mix(gold, (150, 100, 20), 0.25), outline=None)
        c.ellipse((cx - s * 0.36, y - s * 0.12, cx + s * 0.16, y + s * 0.04), fill=gold)
    c.circle(cx + s * 0.2, cy - s * 0.1, s * 0.22, fill=gold, outline=mix(gold, (150, 100, 20), 0.35), width=s * 0.04)
    c.circle(cx + s * 0.2, cy - s * 0.1, s * 0.13, outline=mix(gold, (150, 100, 20), 0.35), width=s * 0.025)


def key_plus(c, cx, cy, s, col, bg=WH, acc=(236, 180, 50)):
    c.circle(cx - s * 0.2, cy - s * 0.05, s * 0.2, fill=col)
    c.circle(cx - s * 0.2, cy - s * 0.05, s * 0.08, fill=bg)
    c.rect((cx - s * 0.02, cy - s * 0.09, cx + s * 0.38, cy - s * 0.01), fill=col, r=s * 0.02)
    c.rect((cx + s * 0.22, cy - s * 0.02, cx + s * 0.28, cy + s * 0.1), fill=col)
    c.rect((cx + s * 0.32, cy - s * 0.02, cx + s * 0.38, cy + s * 0.14), fill=col)
    c.circle(cx + s * 0.22, cy + s * 0.3, s * 0.15, fill=acc)
    c.rect((cx + s * 0.22 - s * 0.09, cy + s * 0.3 - s * 0.025, cx + s * 0.22 + s * 0.09, cy + s * 0.3 + s * 0.025), fill=bg)
    c.rect((cx + s * 0.22 - s * 0.025, cy + s * 0.3 - s * 0.09, cx + s * 0.22 + s * 0.025, cy + s * 0.3 + s * 0.09), fill=bg)


def laptop(c, cx, cy, s, col, bg=WH, acc=None):
    acc = acc or mix(col, bg, 0.75)
    c.rect((cx - s * 0.36, cy - s * 0.32, cx + s * 0.36, cy + s * 0.16), fill=col, r=s * 0.05)
    c.rect((cx - s * 0.3, cy - s * 0.26, cx + s * 0.3, cy + s * 0.1), fill=acc)
    c.poly([(cx - s * 0.46, cy + s * 0.2), (cx + s * 0.46, cy + s * 0.2), (cx + s * 0.4, cy + s * 0.3), (cx - s * 0.4, cy + s * 0.3)], col)
    for k in range(3):
        c.rect((cx - s * 0.22, cy - s * 0.18 + k * s * 0.09, cx + s * (0.2 - k * 0.08), cy - s * 0.14 + k * s * 0.09), fill=col, r=s * 0.02)


def house(c, cx, cy, s, col, bg=WH, roof=None, door=None):
    roof = roof or col
    c.poly([(cx - s * 0.46, cy - s * 0.02), (cx, cy - s * 0.42), (cx + s * 0.46, cy - s * 0.02)], roof)
    c.rect((cx - s * 0.34, cy - s * 0.06, cx + s * 0.34, cy + s * 0.4), fill=col)
    c.rect((cx - s * 0.08, cy + s * 0.12, cx + s * 0.08, cy + s * 0.4), fill=door or bg, r=s * 0.02)
    c.rect((cx - s * 0.26, cy + s * 0.02, cx - s * 0.14, cy + s * 0.14), fill=bg)
    c.rect((cx + s * 0.14, cy + s * 0.02, cx + s * 0.26, cy + s * 0.14), fill=bg)


def house_ramp(c, cx, cy, s, col, bg=WH, acc=(236, 180, 50)):
    house(c, cx - s * 0.06, cy - s * 0.02, s * 0.86, col, bg, door=bg)
    c.poly([(cx - s * 0.08, cy + s * 0.33), (cx + s * 0.48, cy + s * 0.44), (cx - s * 0.08, cy + s * 0.44)], acc)


def percent_tag(c, cx, cy, s, col, bg=WH):
    pts = [(cx - s * 0.36, cy - s * 0.16), (cx + s * 0.2, cy - s * 0.4), (cx + s * 0.44, cy + s * 0.16), (cx - s * 0.12, cy + s * 0.4), (cx - s * 0.44, cy + s * 0.08)]
    c.poly(pts, col)
    c.circle(cx + s * 0.18, cy - s * 0.22, s * 0.05, fill=bg)
    c.text((cx - s * 0.02, cy + s * 0.04), "%", "db", s * 0.36, bg, anchor="mm")


def clock(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.4, fill=bg, outline=col, width=s * 0.07)
    c.line([(cx, cy), (cx, cy - s * 0.24)], col, s * 0.06)
    c.line([(cx, cy), (cx + s * 0.17, cy + s * 0.08)], col, s * 0.06)
    c.circle(cx, cy, s * 0.05, fill=col)


def envelope(c, cx, cy, s, col, bg=WH, paper=(255, 255, 255)):
    x0, y0, x1, y1 = cx - s * 0.44, cy - s * 0.28, cx + s * 0.44, cy + s * 0.3
    c.rect((x0, y0, x1, y1), fill=paper, outline=col, width=s * 0.05, r=s * 0.04)
    c.line([(x0 + s * 0.03, y0 + s * 0.03), (cx, cy + s * 0.04), (x1 - s * 0.03, y0 + s * 0.03)], col, s * 0.05)


def shower(c, cx, cy, s, col, bg=WH, water=(90, 180, 230)):
    c.line([(cx - s * 0.3, cy + s * 0.44), (cx - s * 0.3, cy - s * 0.34), (cx + s * 0.02, cy - s * 0.34), (cx + s * 0.02, cy - s * 0.24)], col, s * 0.06)
    c.pie((cx - s * 0.14, cy - s * 0.3, cx + s * 0.18, cy - s * 0.02), 180, 360, col)
    for i in range(4):
        x = cx - s * 0.08 + i * s * 0.07
        c.line([(x, cy - s * 0.1), (x - s * 0.03 + i * s * 0.02, cy + s * 0.22)], water, s * 0.03)
    c.rect((cx - s * 0.42, cy + s * 0.36, cx + s * 0.42, cy + s * 0.44), fill=col, r=s * 0.03)


def bath(c, cx, cy, s, col, bg=WH, water=(90, 180, 230)):
    c.rect((cx - s * 0.42, cy - s * 0.02, cx + s * 0.42, cy + s * 0.3), fill=col, r=s * 0.1)
    c.rect((cx - s * 0.42, cy - s * 0.06, cx + s * 0.42, cy + s * 0.04), fill=col, r=s * 0.03)
    # дверца
    c.rect((cx - s * 0.3, cy + s * 0.02, cx - s * 0.06, cy + s * 0.24), outline=bg, width=s * 0.03, r=s * 0.04)
    c.circle(cx - s * 0.1, cy + s * 0.13, s * 0.02, fill=bg)
    # сиденье
    c.rect((cx + s * 0.08, cy - s * 0.2, cx + s * 0.34, cy - s * 0.06), fill=mix(col, bg, 0.4), r=s * 0.03)
    c.rect((cx - s * 0.32, cy + s * 0.3, cx - s * 0.24, cy + s * 0.38), fill=col)
    c.rect((cx + s * 0.24, cy + s * 0.3, cx + s * 0.32, cy + s * 0.38), fill=col)
    c.line([(cx - s * 0.36, cy - s * 0.06), (cx - s * 0.36, cy - s * 0.3), (cx - s * 0.24, cy - s * 0.3)], col, s * 0.05)


def rail(c, cx, cy, s, col, bg=WH):
    """Поручень на кафельной стене (вид спереди)."""
    tile = mix(col, bg, 0.82)
    c.rect((cx - s * 0.46, cy - s * 0.4, cx + s * 0.46, cy + s * 0.4), fill=tile, r=s * 0.06)
    for k in (-1, 0, 1):
        c.line([(cx + k * s * 0.23 - s * 0.115 + s * 0.115, cy - s * 0.4), (cx + k * s * 0.23, cy + s * 0.4)], bg, s * 0.02)
    c.line([(cx - s * 0.46, cy), (cx + s * 0.46, cy)], bg, s * 0.02)
    for k in (-1, 1):
        c.circle(cx + k * s * 0.34, cy + s * 0.02, s * 0.09, fill=mix(col, (0, 0, 0), 0.15))
    c.rect((cx - s * 0.38, cy - s * 0.035, cx + s * 0.38, cy + s * 0.075), fill=col, r=s * 0.055)
    c.rect((cx - s * 0.3, cy - s * 0.02, cx + s * 0.3, cy + s * 0.0), fill=mix(col, bg, 0.5), r=s * 0.01)


def floor_tiles(c, cx, cy, s, col, bg=WH):
    pts = [(cx - s * 0.46, cy + s * 0.34), (cx + s * 0.46, cy + s * 0.34), (cx + s * 0.28, cy - s * 0.14), (cx - s * 0.28, cy - s * 0.14)]
    c.poly(pts, mix(col, bg, 0.55))
    for k in range(1, 4):
        t = k / 4
        xa = cx - s * 0.46 + (s * 0.18) * 0
        c.line([(cx - s * 0.46 + t * s * 0.92, cy + s * 0.34), (cx - s * 0.28 + t * s * 0.56, cy - s * 0.14)], bg, s * 0.02)
    for k in range(1, 3):
        t = k / 3
        y = cy - s * 0.14 + t * s * 0.48
        w_ = s * 0.28 + t * s * 0.18
        c.line([(cx - w_, y), (cx + w_, y)], bg, s * 0.02)
    # «нескользящие» точки
    for i in range(3):
        c.circle(cx - s * 0.18 + i * s * 0.18, cy - s * 0.3, s * 0.035, fill=col)


def card(c, cx, cy, s, col, bg=WH, stripe=None, chip=(236, 196, 90), ang=0):
    w_, h_ = s * 0.84, s * 0.54
    x0, y0 = cx - w_ / 2, cy - h_ / 2
    if ang:
        pts = rotpts([(x0, y0), (x0 + w_, y0), (x0 + w_, y0 + h_), (x0, y0 + h_)], cx, cy, ang)
        c.poly(pts, col)
        ch = rotpts([(x0 + s * 0.08, y0 + s * 0.16), (x0 + s * 0.22, y0 + s * 0.16), (x0 + s * 0.22, y0 + s * 0.26), (x0 + s * 0.08, y0 + s * 0.26)], cx, cy, ang)
        c.poly(ch, chip)
        return
    c.rect((x0, y0, x0 + w_, y0 + h_), fill=col, r=s * 0.06)
    c.rect((x0 + s * 0.08, y0 + s * 0.14, x0 + s * 0.22, y0 + s * 0.25), fill=chip, r=s * 0.02)
    for k in range(4):
        c.rect((x0 + s * 0.08 + k * s * 0.17, y0 + s * 0.34, x0 + s * 0.2 + k * s * 0.17, y0 + s * 0.38), fill=mix(col, bg, 0.55), r=s * 0.01)


def card_up(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    card(c, cx - s * 0.06, cy + s * 0.08, s * 0.9, col, bg)
    c.circle(cx + s * 0.3, cy - s * 0.26, s * 0.18, fill=acc, outline=bg, width=s * 0.04)
    c.line([(cx + s * 0.3, cy - s * 0.17), (cx + s * 0.3, cy - s * 0.35)], bg, s * 0.05)
    c.line([(cx + s * 0.22, cy - s * 0.27), (cx + s * 0.3, cy - s * 0.36), (cx + s * 0.38, cy - s * 0.27)], bg, s * 0.05)


def calc(c, cx, cy, s, col, bg=WH, screen=(200, 230, 210), txt=None):
    x0, y0, x1, y1 = cx - s * 0.3, cy - s * 0.42, cx + s * 0.3, cy + s * 0.42
    c.rect((x0, y0, x1, y1), fill=col, r=s * 0.06)
    c.rect((x0 + s * 0.06, y0 + s * 0.06, x1 - s * 0.06, y0 + s * 0.24), fill=screen, r=s * 0.02)
    if txt:
        c.text((x1 - s * 0.09, y0 + s * 0.15), txt, "sb", s * 0.12, (30, 40, 30), anchor="rm")
    for i in range(3):
        for j in range(4):
            x = x0 + s * 0.13 + i * s * 0.17
            y = y0 + s * 0.36 + j * s * 0.13
            c.rect((x - s * 0.06, y - s * 0.045, x + s * 0.06, y + s * 0.045), fill=mix(col, bg, 0.75 if (i, j) != (2, 3) else 0.2), r=s * 0.015)


def doc(c, cx, cy, s, col, bg=WH, paper=(255, 255, 255)):
    x0, y0, x1, y1 = cx - s * 0.3, cy - s * 0.42, cx + s * 0.3, cy + s * 0.42
    c.poly([(x0, y0), (x1 - s * 0.14, y0), (x1, y0 + s * 0.14), (x1, y1), (x0, y1)], paper)
    c.poly([(x0, y0), (x1 - s * 0.14, y0), (x1, y0 + s * 0.14), (x1, y1), (x0, y1)], None, outline=col, width=s * 0.04)
    for k in range(5):
        c.rect((x0 + s * 0.09, y0 + s * 0.2 + k * s * 0.12, x1 - s * (0.09 + (0.12 if k % 2 else 0)), y0 + s * 0.24 + k * s * 0.12), fill=mix(col, bg, 0.4), r=s * 0.01)


def briefcase(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.42, cy - s * 0.2, cx + s * 0.42, cy + s * 0.34), fill=col, r=s * 0.07)
    c.rect((cx - s * 0.16, cy - s * 0.36, cx + s * 0.16, cy - s * 0.18), outline=col, width=s * 0.06, r=s * 0.05)
    c.rect((cx - s * 0.42, cy + s * 0.02, cx + s * 0.42, cy + s * 0.06), fill=bg)
    c.rect((cx - s * 0.07, cy - s * 0.02, cx + s * 0.07, cy + s * 0.1), fill=bg, r=s * 0.02)


def padlock(c, cx, cy, s, col, bg=WH):
    c.arc((cx - s * 0.22, cy - s * 0.42, cx + s * 0.22, cy + s * 0.02), 180, 360, col, s * 0.08)
    c.line([(cx - s * 0.22 + s * 0.04, cy - s * 0.2), (cx - s * 0.22 + s * 0.04, cy - s * 0.04)], col, s * 0.08)
    c.line([(cx + s * 0.22 - s * 0.04, cy - s * 0.2), (cx + s * 0.22 - s * 0.04, cy - s * 0.04)], col, s * 0.08)
    c.rect((cx - s * 0.34, cy - s * 0.06, cx + s * 0.34, cy + s * 0.42), fill=col, r=s * 0.07)
    c.circle(cx, cy + s * 0.14, s * 0.07, fill=bg)
    c.rect((cx - s * 0.025, cy + s * 0.14, cx + s * 0.025, cy + s * 0.28), fill=bg)


def bank(c, cx, cy, s, col, bg=WH):
    """Условное здание банка (без логотипа)."""
    c.poly([(cx - s * 0.46, cy - s * 0.16), (cx, cy - s * 0.42), (cx + s * 0.46, cy - s * 0.16)], col)
    c.rect((cx - s * 0.42, cy - s * 0.16, cx + s * 0.42, cy - s * 0.1), fill=col)
    for i in range(4):
        x = cx - s * 0.3 + i * s * 0.2
        c.rect((x - s * 0.05, cy - s * 0.06, x + s * 0.05, cy + s * 0.28), fill=col)
    c.rect((cx - s * 0.46, cy + s * 0.3, cx + s * 0.46, cy + s * 0.4), fill=col)


def book_apple(c, cx, cy, s, col, bg=WH, apple=(220, 50, 40)):
    c.rect((cx - s * 0.42, cy + s * 0.06, cx + s * 0.34, cy + s * 0.2), fill=col, r=s * 0.02)
    c.rect((cx - s * 0.38, cy + s * 0.2, cx + s * 0.4, cy + s * 0.34), fill=mix(col, (0, 0, 0), 0.2), r=s * 0.02)
    c.rect((cx - s * 0.36, cy + s * 0.09, cx + s * 0.3, cy + s * 0.12), fill=bg)
    c.circle(cx - s * 0.02, cy - s * 0.14, s * 0.2, fill=apple)
    c.circle(cx + s * 0.1, cy - s * 0.14, s * 0.18, fill=apple)
    c.line([(cx + s * 0.04, cy - s * 0.3), (cx + s * 0.08, cy - s * 0.42)], (110, 70, 40), s * 0.04)
    c.poly([(cx + s * 0.08, cy - s * 0.36), (cx + s * 0.24, cy - s * 0.44), (cx + s * 0.18, cy - s * 0.32)], (80, 160, 70))


def car(c, cx, cy, s, col, bg=WH):
    c.poly([(cx - s * 0.26, cy - s * 0.06), (cx - s * 0.16, cy - s * 0.26), (cx + s * 0.18, cy - s * 0.26), (cx + s * 0.3, cy - s * 0.06)], col)
    c.rect((cx - s * 0.46, cy - s * 0.08, cx + s * 0.46, cy + s * 0.18), fill=col, r=s * 0.08)
    c.poly([(cx - s * 0.18, cy - s * 0.08), (cx - s * 0.11, cy - s * 0.2), (cx - s * 0.02, cy - s * 0.2), (cx - s * 0.02, cy - s * 0.08)], mix(col, bg, 0.7))
    c.poly([(cx + s * 0.03, cy - s * 0.08), (cx + s * 0.03, cy - s * 0.2), (cx + s * 0.15, cy - s * 0.2), (cx + s * 0.22, cy - s * 0.08)], mix(col, bg, 0.7))
    for k in (-1, 1):
        c.circle(cx + k * s * 0.26, cy + s * 0.2, s * 0.11, fill=(40, 40, 46))
        c.circle(cx + k * s * 0.26, cy + s * 0.2, s * 0.045, fill=(200, 200, 205))


def roller(c, cx, cy, s, col, bg=WH, paint=(236, 180, 50)):
    c.rect((cx - s * 0.4, cy - s * 0.4, cx + s * 0.24, cy - s * 0.18), fill=paint, r=s * 0.06)
    c.line([(cx + s * 0.24, cy - s * 0.29), (cx + s * 0.36, cy - s * 0.29), (cx + s * 0.36, cy - s * 0.06), (cx - s * 0.08, cy - s * 0.02), (cx - s * 0.08, cy + s * 0.12)], col, s * 0.05, joint="curve")
    c.rect((cx - s * 0.13, cy + s * 0.1, cx - s * 0.03, cy + s * 0.44), fill=col, r=s * 0.04)


def box(c, cx, cy, s, col, bg=WH, tape=(236, 206, 150)):
    c.rect((cx - s * 0.38, cy - s * 0.2, cx + s * 0.38, cy + s * 0.38), fill=col, r=s * 0.03)
    c.poly([(cx - s * 0.38, cy - s * 0.2), (cx - s * 0.46, cy - s * 0.34), (cx - s * 0.04, cy - s * 0.34), (cx, cy - s * 0.2)], mix(col, bg, 0.2))
    c.poly([(cx + s * 0.38, cy - s * 0.2), (cx + s * 0.46, cy - s * 0.34), (cx + s * 0.04, cy - s * 0.34), (cx, cy - s * 0.2)], mix(col, bg, 0.2))
    c.rect((cx - s * 0.06, cy - s * 0.2, cx + s * 0.06, cy + s * 0.1), fill=tape)
    c.line([(cx - s * 0.26, cy + s * 0.24), (cx - s * 0.1, cy + s * 0.24)], bg, s * 0.03)


def star(c, cx, cy, s, col, bg=WH):
    pts = []
    for i in range(10):
        r_ = s * (0.44 if i % 2 == 0 else 0.19)
        a = math.radians(-90 + i * 36)
        pts.append((cx + r_ * math.cos(a), cy + r_ * math.sin(a)))
    c.poly(pts, col)


def heart_hands(c, cx, cy, s, col, bg=WH, heart=(232, 88, 70)):
    # сердце
    c.circle(cx - s * 0.1, cy - s * 0.18, s * 0.13, fill=heart)
    c.circle(cx + s * 0.1, cy - s * 0.18, s * 0.13, fill=heart)
    c.poly([(cx - s * 0.225, cy - s * 0.13), (cx + s * 0.225, cy - s * 0.13), (cx, cy + s * 0.12)], heart)
    # ладони-чаша
    c.pie((cx - s * 0.44, cy - s * 0.14, cx + s * 0.44, cy + s * 0.44), 0, 180, col)
    c.pie((cx - s * 0.3, cy - s * 0.02, cx + s * 0.3, cy + s * 0.3), 0, 180, bg)
    c.rect((cx - s * 0.44, cy + s * 0.13, cx - s * 0.3, cy + s * 0.2), fill=col)
    c.rect((cx + s * 0.3, cy + s * 0.13, cx + s * 0.44, cy + s * 0.2), fill=col)


def field_cap(c, cx, cy, s, col, bg=WH):
    """Полевая кепка без кокарды."""
    c.poly([(cx - s * 0.34, cy + s * 0.06), (cx - s * 0.3, cy - s * 0.26), (cx + s * 0.3, cy - s * 0.3), (cx + s * 0.36, cy + s * 0.06)], col)
    c.rect((cx - s * 0.36, cy + s * 0.02, cx + s * 0.36, cy + s * 0.12), fill=mix(col, (0, 0, 0), 0.2), r=s * 0.02)
    c.poly([(cx - s * 0.36, cy + s * 0.1), (cx + s * 0.36, cy + s * 0.1), (cx + s * 0.46, cy + s * 0.26), (cx - s * 0.2, cy + s * 0.24)], mix(col, (0, 0, 0), 0.3))
    for (x, y) in ((-0.14, -0.14), (0.1, -0.06), (-0.02, -0.22), (0.2, -0.2)):
        c.circle(cx + x * s, cy + y * s, s * 0.05, fill=mix(col, bg, 0.3))


def peaked_cap(c, cx, cy, s, col, bg=WH, band=None):
    """Фуражка без кокарды и знаков."""
    band = band or mix(col, (0, 0, 0), 0.35)
    c.ellipse((cx - s * 0.46, cy - s * 0.34, cx + s * 0.46, cy - s * 0.02), fill=col)
    c.poly([(cx - s * 0.3, cy - s * 0.12), (cx + s * 0.3, cy - s * 0.12), (cx + s * 0.28, cy + s * 0.12), (cx - s * 0.28, cy + s * 0.12)], col)
    c.rect((cx - s * 0.29, cy + s * 0.0, cx + s * 0.29, cy + s * 0.12), fill=band)
    c.ellipse((cx - s * 0.36, cy + s * 0.06, cx + s * 0.36, cy + s * 0.24), fill=(30, 30, 34))
    c.rect((cx - s * 0.29, cy + s * 0.0, cx + s * 0.29, cy + s * 0.12), fill=band)


def boots(c, cx, cy, s, col, bg=WH, sole=(30, 30, 34)):
    """Пара армейских ботинок сбоку (без знаков)."""
    for k, dx in ((0, s * 0.12), (1, -s * 0.12)):
        x = cx + dx
        cc = col if k == 0 else mix(col, (0, 0, 0), 0.25)
        c.poly([(x - s * 0.22, cy - s * 0.4), (x + s * 0.02, cy - s * 0.4), (x + s * 0.04, cy + s * 0.04), (x + s * 0.3, cy + s * 0.14),
                (x + s * 0.32, cy + s * 0.3), (x - s * 0.24, cy + s * 0.3)], cc)
        c.rect((x - s * 0.26, cy + s * 0.28, x + s * 0.34, cy + s * 0.38), fill=sole, r=s * 0.03)
        for j in range(4):
            yy = cy - s * 0.32 + j * s * 0.09
            c.line([(x - s * 0.06, yy), (x + s * 0.02, yy + s * 0.03)], mix(cc, bg, 0.5), s * 0.02)


def helmet(c, cx, cy, s, col, bg=WH):
    """Каска пожарного без эмблем."""
    c.pie((cx - s * 0.34, cy - s * 0.36, cx + s * 0.34, cy + s * 0.3), 180, 360, col)
    c.rect((cx - s * 0.04, cy - s * 0.36, cx + s * 0.04, cy - s * 0.03), fill=mix(col, (255, 255, 255), 0.35))
    c.ellipse((cx - s * 0.48, cy - s * 0.08, cx + s * 0.48, cy + s * 0.14), fill=mix(col, (0, 0, 0), 0.2))
    c.rect((cx - s * 0.3, cy + s * 0.12, cx + s * 0.3, cy + s * 0.2), fill=(250, 210, 60), r=s * 0.02)


def binoculars(c, cx, cy, s, col, bg=WH):
    for k in (-1, 1):
        c.rect((cx + k * s * 0.22 - s * 0.14, cy - s * 0.3, cx + k * s * 0.22 + s * 0.14, cy + s * 0.06), fill=col, r=s * 0.05)
        c.circle(cx + k * s * 0.22, cy + s * 0.18, s * 0.19, fill=col)
        c.circle(cx + k * s * 0.22, cy + s * 0.18, s * 0.11, fill=mix(col, bg, 0.6))
    c.rect((cx - s * 0.08, cy - s * 0.16, cx + s * 0.08, cy + s * 0.02), fill=mix(col, (0, 0, 0), 0.25))


def robot(c, cx, cy, s, col, bg=WH, acc=(80, 170, 230)):
    """Робот-мойщик окон без логотипа."""
    c.rect((cx - s * 0.36, cy - s * 0.36, cx + s * 0.36, cy + s * 0.36), fill=col, r=s * 0.1)
    c.rect((cx - s * 0.26, cy - s * 0.26, cx + s * 0.26, cy + s * 0.26), fill=mix(col, bg, 0.25), r=s * 0.07)
    c.circle(cx, cy, s * 0.1, fill=acc)
    c.circle(cx + s * 0.18, cy - s * 0.18, s * 0.03, fill=(80, 210, 120))
    c.line([(cx + s * 0.36, cy - s * 0.24), (cx + s * 0.46, cy - s * 0.3), (cx + s * 0.48, cy - s * 0.46)], mix(col, bg, 0.3), s * 0.025)


def squeegee(c, cx, cy, s, col, bg=WH, rubber=(40, 40, 46)):
    pts = rotpts([(cx - s * 0.36, cy - s * 0.2), (cx + s * 0.36, cy - s * 0.2), (cx + s * 0.36, cy - s * 0.1), (cx - s * 0.36, cy - s * 0.1)], cx, cy, -20)
    c.poly(pts, mix(col, bg, 0.2))
    pts2 = rotpts([(cx - s * 0.38, cy - s * 0.1), (cx + s * 0.38, cy - s * 0.1), (cx + s * 0.38, cy - s * 0.05), (cx - s * 0.38, cy - s * 0.05)], cx, cy, -20)
    c.poly(pts2, rubber)
    hp = rotpts([(cx - s * 0.04, cy - s * 0.05), (cx + s * 0.04, cy - s * 0.05), (cx + s * 0.04, cy + s * 0.44), (cx - s * 0.04, cy + s * 0.44)], cx, cy, -20)
    c.poly(hp, col)
    for k in range(3):
        x, y = cx - s * 0.3 + k * s * 0.12, cy - s * 0.34 - k * s * 0.03
        c.circle(x, y, s * 0.035, fill=(90, 180, 230))


def window(c, cx, cy, s, col, bg=WH, glass=(190, 225, 245)):
    c.rect((cx - s * 0.4, cy - s * 0.42, cx + s * 0.4, cy + s * 0.42), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.33, cy - s * 0.35, cx - s * 0.03, cy + s * 0.35), fill=glass)
    c.rect((cx + s * 0.03, cy - s * 0.35, cx + s * 0.33, cy + s * 0.35), fill=glass)
    c.line([(cx - s * 0.26, cy - s * 0.2), (cx - s * 0.12, cy - s * 0.3)], bg, s * 0.03)


ICONS = {k: v for k, v in dict(globals()).items() if callable(v) and not k.startswith("_") and k not in ("mix", "rotpts")}
