"""Новые плоские иконки для пакетов волны 2 (w2b, 30.09). Подписываются в p60_icons.ICONS при импорте
(в памяти, файл p60_icons не меняется). Каждая рисуется в квадрате со стороной s с центром (cx, cy).
Без логотипов, гербов, эмблем, флагов и знаков различия."""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p60_lib import mix, rotpts
import p60_icons as I

WH = (255, 255, 255)


def bulb(c, cx, cy, s, col, bg=WH, glow=(255, 206, 70)):
    c.circle(cx, cy - s * 0.1, s * 0.27, fill=glow)
    c.poly([(cx - s * 0.17, cy + s * 0.06), (cx + s * 0.17, cy + s * 0.06), (cx + s * 0.11, cy + s * 0.2), (cx - s * 0.11, cy + s * 0.2)], glow)
    c.rect((cx - s * 0.12, cy + s * 0.2, cx + s * 0.12, cy + s * 0.36), fill=col, r=s * 0.03)
    for k in range(2):
        c.line([(cx - s * 0.12, cy + s * 0.25 + k * s * 0.06), (cx + s * 0.12, cy + s * 0.25 + k * s * 0.06)], bg, s * 0.02)
    c.rect((cx - s * 0.05, cy + s * 0.36, cx + s * 0.05, cy + s * 0.42), fill=col, r=s * 0.02)
    c.arc((cx - s * 0.16, cy - s * 0.26, cx + s * 0.02, cy - s * 0.02), 180, 270, WH, s * 0.035)
    for a in (-150, -120, -90, -60, -30):
        r0, r1 = s * 0.34, s * 0.45
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        c.line([(cx + ca * r0, cy - s * 0.1 + sa * r0), (cx + ca * r1, cy - s * 0.1 + sa * r1)], glow, s * 0.04)


def bolt(c, cx, cy, s, col, bg=WH):
    pts = [(cx + s * 0.08, cy - s * 0.44), (cx - s * 0.26, cy + s * 0.06), (cx - s * 0.02, cy + s * 0.06),
           (cx - s * 0.1, cy + s * 0.44), (cx + s * 0.26, cy - s * 0.08), (cx + s * 0.02, cy - s * 0.08)]
    c.poly(pts, col)


def plug(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.1, cy - s * 0.42, cx - s * 0.04, cy - s * 0.2), fill=col, r=s * 0.02)
    c.rect((cx + s * 0.04, cy - s * 0.42, cx + s * 0.1, cy - s * 0.2), fill=col, r=s * 0.02)
    c.rect((cx - s * 0.22, cy - s * 0.22, cx + s * 0.22, cy + s * 0.04), fill=col, r=s * 0.06)
    c.poly([(cx - s * 0.16, cy + s * 0.02), (cx + s * 0.16, cy + s * 0.02), (cx + s * 0.06, cy + s * 0.16), (cx - s * 0.06, cy + s * 0.16)], col)
    c.line([(cx, cy + s * 0.14), (cx, cy + s * 0.26), (cx + s * 0.2, cy + s * 0.34), (cx + s * 0.36, cy + s * 0.3)], col, s * 0.06)


def meter(c, cx, cy, s, col, bg=WH):
    """Счётчик электроэнергии без марки."""
    c.rect((cx - s * 0.34, cy - s * 0.42, cx + s * 0.34, cy + s * 0.42), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.26, cy - s * 0.32, cx + s * 0.26, cy - s * 0.1), fill=bg, r=s * 0.03)
    for i in range(5):
        x = cx - s * 0.2 + i * s * 0.1
        c.rect((x - s * 0.035, cy - s * 0.27, x + s * 0.035, cy - s * 0.15), fill=mix(col, bg, 0.5), r=s * 0.01)
    c.circle(cx, cy + s * 0.14, s * 0.12, fill=bg)
    c.line([(cx, cy + s * 0.14), (cx + s * 0.07, cy + s * 0.07)], col, s * 0.03)
    bolt(c, cx - s * 0.2, cy + s * 0.3, s * 0.18, bg)


def specs(c, cx, cy, s, col, bg=WH, lens=(214, 234, 248)):
    """Очки анфас."""
    r = s * 0.17
    for k in (-1, 1):
        x = cx + k * s * 0.22
        c.rect((x - r * 1.2, cy - r, x + r * 1.2, cy + r * 0.9), fill=lens, r=r * 0.7, outline=col, width=s * 0.05)
    c.arc((cx - s * 0.07, cy - s * 0.08, cx + s * 0.07, cy + s * 0.06), 200, 340, col, s * 0.045)
    c.line([(cx - s * 0.42, cy - s * 0.08), (cx - s * 0.48, cy - s * 0.14)], col, s * 0.045)
    c.line([(cx + s * 0.42, cy - s * 0.08), (cx + s * 0.48, cy - s * 0.14)], col, s * 0.045)


def specs_prog(c, cx, cy, s, col, bg=WH, lens=(214, 234, 248)):
    """Прогрессивные очки: линзы с тремя зонами (градиент полос)."""
    r = s * 0.17
    for k in (-1, 1):
        x = cx + k * s * 0.22
        c.rect((x - r * 1.2, cy - r, x + r * 1.2, cy + r * 0.9), fill=lens, r=r * 0.7)
        c.rect((x - r * 1.05, cy - r * 0.05, x + r * 1.05, cy + r * 0.3), fill=mix(lens, col, 0.18))
        c.rect((x - r * 0.9, cy + r * 0.3, x + r * 0.9, cy + r * 0.75), fill=mix(lens, col, 0.34), r=r * 0.4)
        c.rect((x - r * 1.2, cy - r, x + r * 1.2, cy + r * 0.9), r=r * 0.7, outline=col, width=s * 0.05)
    c.arc((cx - s * 0.07, cy - s * 0.08, cx + s * 0.07, cy + s * 0.06), 200, 340, col, s * 0.045)
    c.line([(cx - s * 0.42, cy - s * 0.08), (cx - s * 0.48, cy - s * 0.14)], col, s * 0.045)
    c.line([(cx + s * 0.42, cy - s * 0.08), (cx + s * 0.48, cy - s * 0.14)], col, s * 0.045)


def reading(c, cx, cy, s, col, bg=WH):
    """Очки для чтения на раскрытой книге."""
    c.poly([(cx - s * 0.46, cy + s * 0.02), (cx, cy + s * 0.1), (cx, cy + s * 0.42), (cx - s * 0.46, cy + s * 0.34)], mix(col, bg, 0.75))
    c.poly([(cx + s * 0.46, cy + s * 0.02), (cx, cy + s * 0.1), (cx, cy + s * 0.42), (cx + s * 0.46, cy + s * 0.34)], mix(col, bg, 0.6))
    for k in range(3):
        c.line([(cx - s * 0.38, cy + s * (0.1 + k * 0.08)), (cx - s * 0.08, cy + s * (0.15 + k * 0.08))], col, s * 0.02, alpha=140)
        c.line([(cx + s * 0.08, cy + s * (0.15 + k * 0.08)), (cx + s * 0.38, cy + s * (0.1 + k * 0.08))], col, s * 0.02, alpha=140)
    specs(c, cx, cy - s * 0.18, s * 0.8, col, bg)


def contact(c, cx, cy, s, col, bg=WH, lens=(150, 206, 240)):
    """Контактная линза на кончике пальца (палец — простая капля-форма)."""
    c.rect((cx - s * 0.16, cy - s * 0.02, cx + s * 0.16, cy + s * 0.5), fill=(236, 190, 160), r=s * 0.16)
    c.ellipse((cx - s * 0.1, cy + s * 0.02, cx + s * 0.1, cy + s * 0.16), fill=(246, 214, 196))
    c.pie((cx - s * 0.3, cy - s * 0.38, cx + s * 0.3, cy + s * 0.14), 180, 360, lens, alpha=220)
    c.arc((cx - s * 0.3, cy - s * 0.38, cx + s * 0.3, cy + s * 0.14), 180, 360, col, s * 0.04)
    c.line([(cx - s * 0.3, cy - s * 0.12), (cx + s * 0.3, cy - s * 0.12)], col, s * 0.04)
    c.arc((cx - s * 0.2, cy - s * 0.3, cx + s * 0.04, cy - s * 0.06), 200, 260, WH, s * 0.04)


def eye_lens(c, cx, cy, s, col, bg=WH, acc=(80, 170, 230)):
    """Схема глаза с интраокулярной линзой (условная, не медицинское фото)."""
    c.ellipse((cx - s * 0.46, cy - s * 0.26, cx + s * 0.46, cy + s * 0.26), fill=bg, outline=col, width=s * 0.05)
    c.circle(cx, cy, s * 0.2, fill=acc)
    c.circle(cx, cy, s * 0.09, fill=col)
    c.circle(cx - s * 0.06, cy - s * 0.06, s * 0.035, fill=WH)
    c.ellipse((cx - s * 0.16, cy - s * 0.05, cx + s * 0.16, cy + s * 0.05), outline=WH, width=s * 0.025)
    c.line([(cx - s * 0.28, cy), (cx - s * 0.16, cy)], WH, s * 0.025)
    c.line([(cx + s * 0.16, cy), (cx + s * 0.28, cy)], WH, s * 0.025)


def tooth(c, cx, cy, s, col, bg=WH, fill=WH, spark=None):
    """Зуб (контур). fill — цвет эмали."""
    pts = []
    for i in range(0, 181, 10):
        a = math.radians(180 + i)
        pts.append((cx + math.cos(a) * s * 0.34, cy - s * 0.12 + math.sin(a) * s * 0.26))
    pts += [(cx + s * 0.32, cy + s * 0.06), (cx + s * 0.22, cy + s * 0.42), (cx + s * 0.12, cy + s * 0.44), (cx + s * 0.04, cy + s * 0.16),
            (cx - s * 0.04, cy + s * 0.16), (cx - s * 0.12, cy + s * 0.44), (cx - s * 0.22, cy + s * 0.42), (cx - s * 0.32, cy + s * 0.06)]
    c.poly(pts, fill, outline=col, width=s * 0.05)
    c.circle(cx - s * 0.12, cy - s * 0.12, s * 0.07, fill=WH, alpha=200)
    if spark:
        for a in range(0, 360, 90):
            ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
            c.line([(cx + s * 0.38, cy - s * 0.36), (cx + s * 0.38 + ca * s * 0.1, cy - s * 0.36 + sa * s * 0.1)], spark, s * 0.035)


def tooth_fill(c, cx, cy, s, col, bg=WH, acc=(60, 150, 220)):
    tooth(c, cx, cy, s, col, bg)
    c.ellipse((cx - s * 0.1, cy - s * 0.28, cx + s * 0.14, cy - s * 0.12), fill=acc)


def implant(c, cx, cy, s, col, bg=WH, metal=(160, 170, 184)):
    tooth(c, cx, cy - s * 0.2, s * 0.62, col, bg)
    c.rect((cx - s * 0.1, cy + s * 0.08, cx + s * 0.1, cy + s * 0.14), fill=metal, r=s * 0.02)
    c.poly([(cx - s * 0.09, cy + s * 0.14), (cx + s * 0.09, cy + s * 0.14), (cx + s * 0.05, cy + s * 0.46), (cx - s * 0.05, cy + s * 0.46)], metal)
    for k in range(5):
        y = cy + s * (0.18 + k * 0.055)
        w = s * (0.12 - k * 0.012)
        c.line([(cx - w, y), (cx + w, y + s * 0.02)], mix(metal, (0, 0, 0), 0.3), s * 0.02)


def denture(c, cx, cy, s, col, bg=WH, gum=(236, 130, 140)):
    c.pie((cx - s * 0.44, cy - s * 0.36, cx + s * 0.44, cy + s * 0.3), 180, 360, gum)
    c.rect((cx - s * 0.44, cy - s * 0.04, cx + s * 0.44, cy + s * 0.02), fill=gum)
    for i in range(6):
        x = cx - s * 0.33 + i * s * 0.132
        c.rect((x - s * 0.058, cy - s * 0.06, x + s * 0.058, cy + s * 0.18), fill=WH, r=s * 0.04, outline=col, width=s * 0.02)
    c.pie((cx - s * 0.44, cy + s * 0.04, cx + s * 0.44, cy + s * 0.62), 180, 360, bg, alpha=0)


def toothbrush(c, cx, cy, s, col, bg=WH):
    pts = rotpts([(cx - s * 0.44, cy - s * 0.04), (cx + s * 0.2, cy - s * 0.04), (cx + s * 0.2, cy + s * 0.04), (cx - s * 0.44, cy + s * 0.04)], cx, cy, -30)
    c.poly(pts, col)
    head = rotpts([(cx + s * 0.16, cy - s * 0.06), (cx + s * 0.44, cy - s * 0.06), (cx + s * 0.44, cy + s * 0.04), (cx + s * 0.16, cy + s * 0.04)], cx, cy, -30)
    c.poly(head, col)
    for k in range(6):
        x = cx + s * (0.18 + k * 0.045)
        p = rotpts([(x, cy - s * 0.06), (x, cy - s * 0.2)], cx, cy, -30)
        c.line(p, (120, 200, 240), s * 0.03)


def rings(c, cx, cy, s, col, bg=WH, gold=(226, 176, 60)):
    c.circle(cx - s * 0.12, cy + s * 0.04, s * 0.24, outline=gold, width=s * 0.07)
    c.circle(cx + s * 0.14, cy + s * 0.04, s * 0.24, outline=mix(gold, (255, 255, 255), 0.35), width=s * 0.07)
    c.poly([(cx - s * 0.2, cy - s * 0.28), (cx - s * 0.12, cy - s * 0.38), (cx - s * 0.04, cy - s * 0.28), (cx - s * 0.12, cy - s * 0.2)], (190, 226, 250))


def stroller(c, cx, cy, s, col, bg=WH):
    c.pie((cx - s * 0.4, cy - s * 0.36, cx + s * 0.2, cy + s * 0.24), 180, 270, mix(col, bg, 0.3))
    c.pie((cx - s * 0.4, cy - s * 0.36, cx + s * 0.2, cy + s * 0.24), 0, 180, col)
    c.rect((cx - s * 0.4, cy - s * 0.07, cx + s * 0.2, cy - s * 0.04), fill=col)
    c.line([(cx + s * 0.2, cy - s * 0.06), (cx + s * 0.3, cy - s * 0.3), (cx + s * 0.42, cy - s * 0.3)], col, s * 0.05)
    for x in (cx - s * 0.26, cx + s * 0.08):
        c.circle(x, cy + s * 0.34, s * 0.09, fill=bg, outline=col, width=s * 0.05)


def age75(c, cx, cy, s, col, bg=WH, acc=(236, 180, 50)):
    """Бейдж «75+» — возраст как тема (без людей)."""
    c.circle(cx, cy, s * 0.42, fill=col)
    c.circle(cx, cy, s * 0.35, outline=bg, width=s * 0.025)
    c.text((cx, cy + s * 0.02), "75+", "db", s * 0.3, bg, anchor="mm")


def num_badge(c, cx, cy, s, col, bg=WH, txt="13"):
    c.rect((cx - s * 0.36, cy - s * 0.36, cx + s * 0.36, cy + s * 0.4), fill=bg, outline=col, width=s * 0.05, r=s * 0.08)
    c.rect((cx - s * 0.36, cy - s * 0.36, cx + s * 0.36, cy - s * 0.16), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.36, cy - s * 0.24, cx + s * 0.36, cy - s * 0.16), fill=col)
    c.text((cx, cy + s * 0.12), txt, "db", s * 0.3, col, anchor="mm")


def badge_1314(c, cx, cy, s, col, bg=WH):
    num_badge(c, cx - s * 0.16, cy + s * 0.04, s * 0.7, mix(col, bg, 0.35), bg, "13")
    num_badge(c, cx + s * 0.16, cy - s * 0.04, s * 0.7, col, bg, "14")


def talk(c, cx, cy, s, col, bg=WH, acc=None):
    acc = acc or mix(col, bg, 0.45)
    c.rect((cx - s * 0.44, cy - s * 0.36, cx + s * 0.1, cy + s * 0.02), fill=col, r=s * 0.12)
    c.poly([(cx - s * 0.32, cy), (cx - s * 0.18, cy), (cx - s * 0.36, cy + s * 0.16)], col)
    c.rect((cx - s * 0.06, cy - s * 0.1, cx + s * 0.44, cy + s * 0.26), fill=acc, r=s * 0.12)
    c.poly([(cx + s * 0.22, cy + s * 0.24), (cx + s * 0.34, cy + s * 0.24), (cx + s * 0.38, cy + s * 0.4)], acc)
    for k in range(3):
        c.circle(cx + s * (0.07 + k * 0.12), cy + s * 0.08, s * 0.035, fill=bg)


def compass(c, cx, cy, s, col, bg=WH, acc=(226, 84, 56)):
    c.circle(cx, cy, s * 0.42, fill=bg, outline=col, width=s * 0.06)
    c.poly([(cx, cy - s * 0.3), (cx + s * 0.08, cy), (cx - s * 0.08, cy)], acc)
    c.poly([(cx, cy + s * 0.3), (cx + s * 0.08, cy), (cx - s * 0.08, cy)], col)
    c.circle(cx, cy, s * 0.04, fill=bg)


def storm(c, cx, cy, s, col, bg=WH, acc=(255, 196, 40)):
    for (x, y, r) in ((-0.18, -0.08, 0.2), (0.06, -0.16, 0.24), (0.26, -0.04, 0.17)):
        c.circle(cx + x * s, cy + y * s, r * s, fill=col)
    c.rect((cx - s * 0.36, cy - s * 0.06, cx + s * 0.42, cy + s * 0.12), fill=col, r=s * 0.09)
    bolt(c, cx + s * 0.02, cy + s * 0.28, s * 0.4, acc)


def handshake(c, cx, cy, s, col, bg=WH, acc=None):
    acc = acc or mix(col, bg, 0.45)
    c.poly(rotpts([(cx - s * 0.46, cy - s * 0.06), (cx + s * 0.1, cy - s * 0.06), (cx + s * 0.1, cy + s * 0.12), (cx - s * 0.46, cy + s * 0.12)], cx, cy, 18), col)
    c.poly(rotpts([(cx - s * 0.1, cy - s * 0.1), (cx + s * 0.46, cy - s * 0.1), (cx + s * 0.46, cy + s * 0.08), (cx - s * 0.1, cy + s * 0.08)], cx, cy, -18), acc)
    c.circle(cx, cy, s * 0.14, fill=col)
    for k in range(3):
        c.rect((cx - s * 0.08 + k * s * 0.07, cy - s * 0.02, cx - s * 0.03 + k * s * 0.07, cy + s * 0.14), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.02)


def cap(c, cx, cy, s, col, bg=WH, tassel=(236, 180, 50)):
    """Академическая шапочка."""
    c.poly([(cx - s * 0.46, cy - s * 0.1), (cx, cy - s * 0.32), (cx + s * 0.46, cy - s * 0.1), (cx, cy + s * 0.12)], col)
    c.poly([(cx - s * 0.26, cy + s * 0.0), (cx + s * 0.26, cy + s * 0.0), (cx + s * 0.26, cy + s * 0.24), (cx, cy + s * 0.32), (cx - s * 0.26, cy + s * 0.24)], mix(col, (0, 0, 0), 0.2))
    c.line([(cx, cy - s * 0.1), (cx + s * 0.36, cy - s * 0.02), (cx + s * 0.36, cy + s * 0.26)], tassel, s * 0.03)
    c.rect((cx + s * 0.33, cy + s * 0.22, cx + s * 0.39, cy + s * 0.34), fill=tassel, r=s * 0.02)


def notebook(c, cx, cy, s, col, bg=WH, paper=WH):
    c.rect((cx - s * 0.3, cy - s * 0.42, cx + s * 0.32, cy + s * 0.42), fill=col, r=s * 0.04)
    c.rect((cx - s * 0.22, cy - s * 0.38, cx + s * 0.28, cy + s * 0.38), fill=paper, r=s * 0.02)
    for k in range(6):
        c.line([(cx - s * 0.14, cy - s * 0.24 + k * s * 0.11), (cx + s * 0.2, cy - s * 0.24 + k * s * 0.11)], mix(col, paper, 0.55), s * 0.02)
    for k in range(5):
        c.circle(cx - s * 0.3, cy - s * 0.3 + k * s * 0.15, s * 0.035, fill=mix(col, (0, 0, 0), 0.3))


def armchair(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.3, cy - s * 0.36, cx + s * 0.3, cy + s * 0.12), fill=col, r=s * 0.12)
    c.rect((cx - s * 0.44, cy - s * 0.08, cx - s * 0.24, cy + s * 0.3), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.08)
    c.rect((cx + s * 0.24, cy - s * 0.08, cx + s * 0.44, cy + s * 0.3), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.08)
    c.rect((cx - s * 0.26, cy + s * 0.06, cx + s * 0.26, cy + s * 0.28), fill=mix(col, WH, 0.2), r=s * 0.06)
    c.rect((cx - s * 0.36, cy + s * 0.3, cx - s * 0.3, cy + s * 0.42), fill=(110, 76, 50))
    c.rect((cx + s * 0.3, cy + s * 0.3, cx + s * 0.36, cy + s * 0.42), fill=(110, 76, 50))


def bed(c, cx, cy, s, col, bg=WH, n=1, sheet=WH):
    """Кровать сбоку: n=1 одна, n=2 две рядом (двухместная комната)."""
    def one(x, w):
        c.rect((x - w * 0.5, cy - s * 0.3, x - w * 0.42, cy + s * 0.3), fill=col, r=s * 0.02)
        c.rect((x + w * 0.42, cy - s * 0.06, x + w * 0.5, cy + s * 0.3), fill=col, r=s * 0.02)
        c.rect((x - w * 0.46, cy + s * 0.02, x + w * 0.46, cy + s * 0.18), fill=sheet, r=s * 0.04, outline=col, width=s * 0.02)
        c.rect((x - w * 0.42, cy - s * 0.08, x - w * 0.18, cy + s * 0.04), fill=mix(col, bg, 0.7), r=s * 0.04)
        c.rect((x - w * 0.14, cy - s * 0.02, x + w * 0.46, cy + s * 0.1), fill=mix(col, bg, 0.45), r=s * 0.04)
    if n == 1:
        one(cx, s * 0.9)
    else:
        one(cx - s * 0.24, s * 0.46)
        one(cx + s * 0.24, s * 0.46)


def bed2(c, cx, cy, s, col, bg=WH):
    bed(c, cx, cy, s, col, bg, n=2)


def sun_house(c, cx, cy, s, col, bg=WH, sun=(250, 190, 50)):
    c.circle(cx + s * 0.24, cy - s * 0.24, s * 0.16, fill=sun)
    I.house(c, cx - s * 0.06, cy + s * 0.1, s * 0.72, col)


def home_help(c, cx, cy, s, col, bg=WH, heart=(232, 88, 70)):
    I.house(c, cx - s * 0.08, cy + s * 0.04, s * 0.8, col)
    c.circle(cx + s * 0.26, cy + s * 0.22, s * 0.17, fill=bg)
    x, y, r = cx + s * 0.26, cy + s * 0.22, s * 0.11
    c.circle(x - r * 0.45, y - r * 0.2, r * 0.55, fill=heart)
    c.circle(x + r * 0.45, y - r * 0.2, r * 0.55, fill=heart)
    c.poly([(x - r * 0.95, y - r * 0.02), (x + r * 0.95, y - r * 0.02), (x, y + r * 0.9)], heart)


def phone(c, cx, cy, s, col, bg=WH, screen=(200, 226, 246)):
    c.rect((cx - s * 0.22, cy - s * 0.44, cx + s * 0.22, cy + s * 0.44), fill=col, r=s * 0.07)
    c.rect((cx - s * 0.18, cy - s * 0.36, cx + s * 0.18, cy + s * 0.32), fill=screen, r=s * 0.03)
    c.rect((cx - s * 0.13, cy - s * 0.26, cx + s * 0.08, cy - s * 0.16), fill=WH, r=s * 0.04)
    c.rect((cx - s * 0.08, cy - s * 0.1, cx + s * 0.13, cy), fill=mix(col, screen, 0.4), r=s * 0.04)
    c.rect((cx - s * 0.13, cy + s * 0.06, cx + s * 0.06, cy + s * 0.16), fill=WH, r=s * 0.04)
    c.circle(cx, cy + s * 0.38, s * 0.03, fill=screen)


def shield(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    pts = [(cx, cy - s * 0.44), (cx + s * 0.36, cy - s * 0.3), (cx + s * 0.32, cy + s * 0.1), (cx, cy + s * 0.44), (cx - s * 0.32, cy + s * 0.1), (cx - s * 0.36, cy - s * 0.3)]
    c.poly(pts, col)
    c.check(cx - s * 0.16, cy - s * 0.14, s * 0.32, bg, s * 0.06)


def videocam(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.44, cy - s * 0.24, cx + s * 0.16, cy + s * 0.24), fill=col, r=s * 0.08)
    c.poly([(cx + s * 0.18, cy - s * 0.04), (cx + s * 0.44, cy - s * 0.2), (cx + s * 0.44, cy + s * 0.2), (cx + s * 0.18, cy + s * 0.04)], col)
    c.circle(cx - s * 0.14, cy - s * 0.02, s * 0.08, fill=bg)
    c.rect((cx - s * 0.3, cy + s * 0.1, cx + s * 0.02, cy + s * 0.16), fill=bg, r=s * 0.02)


def laptop_doc(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    I.laptop(c, cx, cy, s, col, bg)
    c.circle(cx + s * 0.3, cy - s * 0.26, s * 0.14, fill=acc, outline=bg, width=s * 0.03)
    c.check(cx + s * 0.23, cy - s * 0.32, s * 0.14, bg, s * 0.035)


def hourglass(c, cx, cy, s, col, bg=WH, sand=(236, 180, 50)):
    c.rect((cx - s * 0.28, cy - s * 0.44, cx + s * 0.28, cy - s * 0.36), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.28, cy + s * 0.36, cx + s * 0.28, cy + s * 0.44), fill=col, r=s * 0.03)
    c.poly([(cx - s * 0.22, cy - s * 0.36), (cx + s * 0.22, cy - s * 0.36), (cx + s * 0.03, cy), (cx + s * 0.22, cy + s * 0.36), (cx - s * 0.22, cy + s * 0.36), (cx - s * 0.03, cy)], mix(col, bg, 0.8))
    c.poly([(cx - s * 0.13, cy - s * 0.2), (cx + s * 0.13, cy - s * 0.2), (cx, cy - s * 0.03)], sand)
    c.poly([(cx - s * 0.18, cy + s * 0.36), (cx + s * 0.18, cy + s * 0.36), (cx, cy + s * 0.18)], sand)


def euro_q(c, cx, cy, s, col, bg=WH):
    """Монета с «?» — сумма неизвестна."""
    c.circle(cx, cy, s * 0.4, fill=col)
    c.circle(cx, cy, s * 0.32, outline=bg, width=s * 0.03)
    c.text((cx, cy + s * 0.02), "?", "db", s * 0.44, bg, anchor="mm")


def sofa(c, cx, cy, s, col, bg=WH, leg=(90, 64, 44)):
    c.rect((cx - s * 0.42, cy - s * 0.22, cx + s * 0.42, cy + s * 0.08), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.48, cy - s * 0.04, cx - s * 0.32, cy + s * 0.24), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.06)
    c.rect((cx + s * 0.32, cy - s * 0.04, cx + s * 0.48, cy + s * 0.24), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.06)
    c.rect((cx - s * 0.34, cy + s * 0.04, cx + s * 0.34, cy + s * 0.22), fill=mix(col, WH, 0.15), r=s * 0.05)
    c.line([(cx, cy + s * 0.05), (cx, cy + s * 0.21)], mix(col, (0, 0, 0), 0.2), s * 0.015)
    for x in (cx - s * 0.4, cx + s * 0.4):
        c.rect((x - s * 0.02, cy + s * 0.24, x + s * 0.02, cy + s * 0.32), fill=leg)


NEW = {k: v for k, v in dict(globals()).items() if callable(v) and not k.startswith("_") and k not in ("mix", "rotpts")}
for _k, _v in NEW.items():
    I.ICONS.setdefault(_k, _v)
