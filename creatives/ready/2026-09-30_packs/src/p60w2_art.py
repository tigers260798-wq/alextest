"""Волна 2 пакетов «Готово к заливу» 30.09 (10 пакетов US/UK/CA): новые иконки, «герои» для сеток,
сцены-иллюстрации и раскладка «merge» (несколько платежей → один) поверх общих шаблонов p60_*.
Иконки регистрируются в p60_icons.ICONS, сцены — атрибутами p60_scenes (чужие файлы не меняются).
Плоский стиль, люди без лиц, без логотипов, гербов, эмблем и красного креста."""
import math
import random
from PIL import Image, ImageDraw
from p60_lib import C, W, mix, rotpts
import p60_icons as I
import p60_scenes as S

WH = (255, 255, 255)
RED_BTN = (220, 56, 50)
GOLD = (236, 180, 50)


def _cap(c, pts, col, w):
    """Линия со скруглёнными концами."""
    c.line(pts, col, w)
    for (x, y) in (pts[0], pts[-1]):
        c.circle(x, y, w / 2, fill=col)


def _badge(c, x, y, r, fill, bg=WH):
    c.circle(x, y, r, fill=fill, outline=bg, width=r * 0.22)


# =====================================================================  иконки
def heart_plain(c, cx, cy, s, col, bg=WH):
    c.circle(cx - s * 0.17, cy - s * 0.1, s * 0.2, fill=col)
    c.circle(cx + s * 0.17, cy - s * 0.1, s * 0.2, fill=col)
    c.poly([(cx - s * 0.355, cy - s * 0.02), (cx + s * 0.355, cy - s * 0.02), (cx, cy + s * 0.38)], col)


def salt(c, cx, cy, s, col, bg=WH, acc=(220, 60, 50)):
    """Солонка с «минусом» — low-sodium."""
    c.rect((cx - s * 0.2, cy - s * 0.16, cx + s * 0.2, cy + s * 0.4), fill=col, r=s * 0.08)
    c.pie((cx - s * 0.2, cy - s * 0.38, cx + s * 0.2, cy + s * 0.02), 180, 360, mix(col, (0, 0, 0), 0.2))
    for dx in (-0.08, 0, 0.08):
        c.circle(cx + dx * s, cy - s * 0.25, s * 0.025, fill=bg)
    c.rect((cx - s * 0.12, cy + s * 0.02, cx + s * 0.12, cy + s * 0.2), fill=bg, r=s * 0.03)
    _badge(c, cx + s * 0.28, cy + s * 0.28, s * 0.15, acc, bg)
    c.rect((cx + s * 0.2, cy + s * 0.26, cx + s * 0.36, cy + s * 0.3), fill=bg)


def drop_check(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    c.circle(cx - s * 0.04, cy + s * 0.1, s * 0.26, fill=col)
    c.poly([(cx - s * 0.285, cy + s * 0.02), (cx - s * 0.04, cy - s * 0.42), (cx + s * 0.205, cy + s * 0.02)], col)
    _badge(c, cx + s * 0.26, cy + s * 0.26, s * 0.16, acc, bg)
    c.check(cx + s * 0.19, cy + s * 0.19, s * 0.14, bg, s * 0.035)


def soup_bowl(c, cx, cy, s, col, bg=WH):
    for k in (-1, 0, 1):
        pts = [(cx + k * s * 0.14 + math.sin(t / 2.2) * s * 0.03, cy - s * 0.08 - t * s * 0.028) for t in range(0, 11)]
        c.line(pts, mix(col, bg, 0.45), s * 0.035)
    c.line([(cx + s * 0.08, cy + s * 0.12), (cx + s * 0.4, cy - s * 0.34)], mix(col, (0, 0, 0), 0.25), s * 0.05)
    c.ellipse((cx + s * 0.32, cy - s * 0.46, cx + s * 0.46, cy - s * 0.28), fill=mix(col, (0, 0, 0), 0.25))
    c.pie((cx - s * 0.44, cy - s * 0.2, cx + s * 0.44, cy + s * 0.44), 0, 180, col)
    c.rect((cx - s * 0.46, cy + s * 0.06, cx + s * 0.46, cy + s * 0.14), fill=mix(col, (0, 0, 0), 0.15), r=s * 0.04)
    c.rect((cx - s * 0.14, cy + s * 0.4, cx + s * 0.14, cy + s * 0.46), fill=col, r=s * 0.02)


def meal_plate(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.33, fill=WH, outline=col, width=s * 0.035)
    c.circle(cx, cy, s * 0.25, fill=(250, 248, 242))
    box = (cx - s * 0.22, cy - s * 0.22, cx + s * 0.22, cy + s * 0.22)
    c.pie(box, 200, 325, (96, 164, 84))
    c.pie(box, 330, 85, (196, 116, 72))
    c.pie(box, 90, 195, (238, 196, 90))
    _cap(c, [(cx - s * 0.44, cy - s * 0.3), (cx - s * 0.44, cy + s * 0.36)], col, s * 0.04)
    for k in (-1, 0, 1):
        c.line([(cx - s * 0.44 + k * s * 0.035, cy - s * 0.36), (cx - s * 0.44 + k * s * 0.035, cy - s * 0.2)], col, s * 0.022)
    c.poly([(cx + s * 0.42, cy - s * 0.36), (cx + s * 0.47, cy - s * 0.3), (cx + s * 0.47, cy + s * 0.04), (cx + s * 0.42, cy + s * 0.04)], col)
    _cap(c, [(cx + s * 0.445, cy + s * 0.04), (cx + s * 0.445, cy + s * 0.36)], col, s * 0.04)


def snowflake(c, cx, cy, s, col, bg=WH):
    for k in range(6):
        a = math.radians(k * 60 - 90)
        ex, ey = cx + math.cos(a) * s * 0.42, cy + math.sin(a) * s * 0.42
        _cap(c, [(cx, cy), (ex, ey)], col, s * 0.06)
        for side in (-1, 1):
            b = a + side * math.radians(40)
            mx, my = cx + math.cos(a) * s * 0.26, cy + math.sin(a) * s * 0.26
            _cap(c, [(mx, my), (mx + math.cos(b) * s * 0.12, my + math.sin(b) * s * 0.12)], col, s * 0.05)
    c.circle(cx, cy, s * 0.07, fill=col)


def pendant(c, cx, cy, s, col, bg=WH, btn=RED_BTN):
    c.line([(cx - s * 0.3, cy - s * 0.46), (cx, cy - s * 0.04)], mix(col, bg, 0.35), s * 0.035)
    c.line([(cx + s * 0.3, cy - s * 0.46), (cx, cy - s * 0.04)], mix(col, bg, 0.35), s * 0.035)
    c.circle(cx, cy + s * 0.17, s * 0.25, fill=col)
    c.circle(cx, cy + s * 0.17, s * 0.15, fill=btn)
    c.circle(cx - s * 0.05, cy + s * 0.12, s * 0.04, fill=WH, alpha=160)


def wristband(c, cx, cy, s, col, bg=WH, btn=RED_BTN):
    c.rect((cx - s * 0.15, cy - s * 0.46, cx + s * 0.15, cy + s * 0.46), fill=mix(col, bg, 0.35), r=s * 0.08)
    for k in range(3):
        c.circle(cx, cy + s * 0.3 + k * s * 0.05, s * 0.018, fill=mix(col, bg, 0.7))
    c.rect((cx - s * 0.26, cy - s * 0.26, cx + s * 0.26, cy + s * 0.22), fill=col, r=s * 0.1)
    c.circle(cx, cy - s * 0.02, s * 0.13, fill=btn)


def base_station(c, cx, cy, s, col, bg=WH, btn=RED_BTN):
    c.poly([(cx - s * 0.44, cy + s * 0.3), (cx - s * 0.38, cy - s * 0.12), (cx + s * 0.38, cy - s * 0.12), (cx + s * 0.44, cy + s * 0.3)], col)
    c.rect((cx - s * 0.46, cy + s * 0.26, cx + s * 0.46, cy + s * 0.34), fill=mix(col, (0, 0, 0), 0.25), r=s * 0.03)
    for k in range(4):
        c.rect((cx - s * 0.32, cy - s * 0.02 + k * s * 0.065, cx - s * 0.06, cy + s * 0.0 + k * s * 0.065), fill=mix(col, bg, 0.45), r=s * 0.01)
    c.circle(cx + s * 0.18, cy + s * 0.08, s * 0.15, fill=btn, outline=mix(col, bg, 0.6), width=s * 0.03)
    c.line([(cx + s * 0.3, cy - s * 0.12), (cx + s * 0.36, cy - s * 0.42)], col, s * 0.035)
    c.circle(cx + s * 0.36, cy - s * 0.43, s * 0.035, fill=col)


def gps_phone(c, cx, cy, s, col, bg=WH, pin=RED_BTN):
    c.rect((cx - s * 0.24, cy - s * 0.44, cx + s * 0.24, cy + s * 0.44), fill=col, r=s * 0.07)
    c.rect((cx - s * 0.19, cy - s * 0.36, cx + s * 0.19, cy + s * 0.34), fill=mix(col, bg, 0.85), r=s * 0.03)
    c.line([(cx - s * 0.19, cy + s * 0.1), (cx + s * 0.19, cy - s * 0.05)], mix(col, bg, 0.6), s * 0.03)
    c.line([(cx - s * 0.05, cy - s * 0.36), (cx + s * 0.02, cy + s * 0.34)], mix(col, bg, 0.6), s * 0.03)
    c.circle(cx, cy - s * 0.1, s * 0.12, fill=pin)
    c.poly([(cx - s * 0.1, cy - s * 0.04), (cx + s * 0.1, cy - s * 0.04), (cx, cy + s * 0.12)], pin)
    c.circle(cx, cy - s * 0.1, s * 0.045, fill=WH)


def eye(c, cx, cy, s, col, bg=WH):
    pts = []
    for k in range(0, 181, 10):
        a = math.radians(k)
        pts.append((cx - s * 0.44 * math.cos(a), cy - s * 0.26 * math.sin(a)))
    for k in range(0, 181, 10):
        a = math.radians(k)
        pts.append((cx + s * 0.44 * math.cos(a), cy + s * 0.26 * math.sin(a)))
    c.poly(pts, bg)
    c.line(pts + [pts[0]], col, s * 0.05)
    c.circle(cx, cy, s * 0.17, fill=col)
    c.circle(cx, cy, s * 0.075, fill=(20, 22, 30))
    c.circle(cx - s * 0.06, cy - s * 0.06, s * 0.04, fill=WH)


def glasses_icon(c, cx, cy, s, col, bg=WH, glass=(214, 234, 248)):
    r = s * 0.17
    for k in (-1, 1):
        c.circle(cx + k * s * 0.22, cy + s * 0.04, r, fill=glass, outline=col, width=s * 0.055)
    c.arc((cx - s * 0.08, cy - s * 0.04, cx + s * 0.08, cy + s * 0.08), 200, 340, col, s * 0.05)
    _cap(c, [(cx - s * 0.39, cy - s * 0.0), (cx - s * 0.47, cy - s * 0.1)], col, s * 0.05)
    _cap(c, [(cx + s * 0.39, cy - s * 0.0), (cx + s * 0.47, cy - s * 0.1)], col, s * 0.05)


def lens(c, cx, cy, s, col, bg=WH):
    """Интраокулярная линза: круг и две «гаптики»."""
    for off in (0, 180):
        pts = []
        for k in range(0, 23):
            t = k / 22
            a = math.radians(off - 60 + t * 150)
            rr = s * (0.2 + 0.24 * t)
            pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        c.line(pts, col, s * 0.04)
    c.circle(cx, cy, s * 0.24, fill=mix(col, bg, 0.8), outline=col, width=s * 0.045)
    c.arc((cx - s * 0.16, cy - s * 0.16, cx + s * 0.16, cy + s * 0.16), 200, 260, WH, s * 0.035)


def _tag(c, cx, cy, s, col, bg, sym):
    pts = [(cx - s * 0.4, cy - s * 0.1), (cx - s * 0.14, cy - s * 0.38), (cx + s * 0.42, cy - s * 0.38), (cx + s * 0.42, cy + s * 0.3),
           (cx - s * 0.14, cy + s * 0.3), (cx - s * 0.4, cy + s * 0.02)]
    c.poly(pts, col)
    c.circle(cx - s * 0.2, cy - s * 0.04, s * 0.05, fill=bg)
    c.text((cx + s * 0.13, cy - s * 0.04), sym, "db", s * 0.42, bg, anchor="mm")


def pound_tag(c, cx, cy, s, col, bg=WH):
    _tag(c, cx, cy, s, col, bg, "£")


def dollar_tag(c, cx, cy, s, col, bg=WH):
    _tag(c, cx, cy, s, col, bg, "$")


def stretch(c, cx, cy, s, col, bg=WH):
    """Упражнение (физиотерапия): фигура без лица на коврике."""
    c.rect((cx - s * 0.44, cy + s * 0.37, cx + s * 0.44, cy + s * 0.45), fill=mix(col, bg, 0.5), r=s * 0.04)
    c.circle(cx, cy - s * 0.3, s * 0.1, fill=col)
    w = s * 0.085
    _cap(c, [(cx, cy - s * 0.16), (cx, cy + s * 0.08)], col, w)
    _cap(c, [(cx, cy - s * 0.12), (cx - s * 0.2, cy - s * 0.26), (cx - s * 0.28, cy - s * 0.44)], col, w * 0.75)
    _cap(c, [(cx, cy - s * 0.12), (cx + s * 0.2, cy - s * 0.26), (cx + s * 0.28, cy - s * 0.44)], col, w * 0.75)
    _cap(c, [(cx, cy + s * 0.08), (cx - s * 0.2, cy + s * 0.2), (cx - s * 0.26, cy + s * 0.36)], col, w * 0.85)
    _cap(c, [(cx, cy + s * 0.08), (cx + s * 0.2, cy + s * 0.2), (cx + s * 0.26, cy + s * 0.36)], col, w * 0.85)


def syringe(c, cx, cy, s, col, bg=WH):
    def R(pts):
        return rotpts(pts, cx, cy, -45)
    c.poly(R([(cx - s * 0.28, cy - s * 0.11), (cx + s * 0.2, cy - s * 0.11), (cx + s * 0.2, cy + s * 0.11), (cx - s * 0.28, cy + s * 0.11)]), mix(col, bg, 0.8))
    c.poly(R([(cx - s * 0.02, cy - s * 0.11), (cx + s * 0.2, cy - s * 0.11), (cx + s * 0.2, cy + s * 0.11), (cx - s * 0.02, cy + s * 0.11)]), mix(col, bg, 0.35))
    c.poly(R([(cx - s * 0.28, cy - s * 0.11), (cx + s * 0.2, cy - s * 0.11), (cx + s * 0.2, cy + s * 0.11), (cx - s * 0.28, cy + s * 0.11)]), None, outline=col, width=s * 0.035)
    for k in range(4):
        x = cx - s * 0.2 + k * s * 0.1
        c.line(R([(x, cy - s * 0.11), (x, cy - s * 0.03)]), col, s * 0.022)
    c.poly(R([(cx - s * 0.46, cy - s * 0.035), (cx - s * 0.28, cy - s * 0.035), (cx - s * 0.28, cy + s * 0.035), (cx - s * 0.46, cy + s * 0.035)]), col)
    c.poly(R([(cx - s * 0.5, cy - s * 0.14), (cx - s * 0.45, cy - s * 0.14), (cx - s * 0.45, cy + s * 0.14), (cx - s * 0.5, cy + s * 0.14)]), col)
    c.poly(R([(cx + s * 0.2, cy - s * 0.06), (cx + s * 0.28, cy - s * 0.035), (cx + s * 0.28, cy + s * 0.035), (cx + s * 0.2, cy + s * 0.06)]), col)
    c.line(R([(cx + s * 0.28, cy), (cx + s * 0.5, cy)]), col, s * 0.022)


def hot_pack(c, cx, cy, s, col, bg=WH, heat=(236, 120, 60)):
    for k in (-1, 0, 1):
        pts = [(cx + k * s * 0.16 + math.sin(t / 1.8) * s * 0.035, cy - s * 0.14 - t * s * 0.028) for t in range(0, 10)]
        c.line(pts, heat, s * 0.04)
    c.rect((cx - s * 0.38, cy - s * 0.1, cx + s * 0.38, cy + s * 0.4), fill=col, r=s * 0.1)
    c.rect((cx - s * 0.3, cy - s * 0.02, cx + s * 0.3, cy + s * 0.32), outline=mix(col, bg, 0.45), width=s * 0.025, r=s * 0.06)
    for k in (-1, 1):
        c.line([(cx + k * s * 0.1, cy - s * 0.02), (cx + k * s * 0.1, cy + s * 0.32)], mix(col, bg, 0.45), s * 0.02)


def tens(c, cx, cy, s, col, bg=WH, wire=(60, 66, 80)):
    c.line([(cx - s * 0.06, cy - s * 0.04), (cx - s * 0.14, cy + s * 0.16), (cx - s * 0.28, cy + s * 0.22)], wire, s * 0.025)
    c.line([(cx + s * 0.06, cy - s * 0.04), (cx + s * 0.14, cy + s * 0.16), (cx + s * 0.28, cy + s * 0.22)], wire, s * 0.025)
    for k in (-1, 1):
        c.rect((cx + k * s * 0.3 - s * 0.14, cy + s * 0.18, cx + k * s * 0.3 + s * 0.14, cy + s * 0.44), fill=mix(col, bg, 0.55), r=s * 0.05)
        c.rect((cx + k * s * 0.3 - s * 0.08, cy + s * 0.24, cx + k * s * 0.3 + s * 0.08, cy + s * 0.38), fill=mix(col, bg, 0.8), r=s * 0.03)
    c.rect((cx - s * 0.18, cy - s * 0.46, cx + s * 0.18, cy + s * 0.0), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.12, cy - s * 0.4, cx + s * 0.12, cy - s * 0.24), fill=(200, 230, 214), r=s * 0.02)
    for k in (-1, 1):
        c.circle(cx + k * s * 0.07, cy - s * 0.12, s * 0.04, fill=mix(col, bg, 0.6))


def odometer(c, cx, cy, s, col, bg=WH, acc=(220, 60, 50)):
    box = (cx - s * 0.44, cy - s * 0.36, cx + s * 0.44, cy + s * 0.52)
    c.pie(box, 180, 360, mix(col, bg, 0.85))
    c.arc(box, 180, 360, col, s * 0.06)
    oy = cy + s * 0.08
    for k in range(7):
        a = math.radians(180 + k * 30)
        c.line([(cx + math.cos(a) * s * 0.34, oy + math.sin(a) * s * 0.34), (cx + math.cos(a) * s * 0.26, oy + math.sin(a) * s * 0.26)], col, s * 0.03)
    c.line([(cx, oy), (cx - s * 0.2, oy - s * 0.2)], acc, s * 0.045)
    c.circle(cx, oy, s * 0.06, fill=col)
    c.rect((cx - s * 0.46, oy + s * 0.02, cx + s * 0.46, oy + s * 0.06), fill=col, r=s * 0.02)
    c.rect((cx - s * 0.18, oy + s * 0.14, cx + s * 0.18, oy + s * 0.3), fill=col, r=s * 0.03)
    for k in range(4):
        c.rect((cx - s * 0.15 + k * s * 0.078, oy + s * 0.17, cx - s * 0.1 + k * s * 0.078, oy + s * 0.27), fill=bg, r=s * 0.01)


def black_box(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    for k, r in enumerate((0.16, 0.27, 0.38)):
        c.arc((cx + s * 0.2 - s * r, cy - s * 0.1 - s * r, cx + s * 0.2 + s * r, cy - s * 0.1 + s * r), 250, 340, col, s * 0.045)
    c.rect((cx - s * 0.36, cy - s * 0.06, cx + s * 0.28, cy + s * 0.36), fill=col, r=s * 0.07)
    c.circle(cx + s * 0.16, cy + s * 0.06, s * 0.045, fill=acc)
    for k in range(3):
        c.rect((cx - s * 0.26, cy + s * 0.02 + k * s * 0.08, cx - s * 0.02, cy + s * 0.05 + k * s * 0.08), fill=mix(col, bg, 0.5), r=s * 0.01)


def compare_docs(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40)):
    I.doc(c, cx - s * 0.2, cy - s * 0.06, s * 0.62, col, bg)
    I.doc(c, cx + s * 0.2, cy - s * 0.06, s * 0.62, mix(col, bg, 0.35), bg)
    y = cy + s * 0.38
    c.line([(cx - s * 0.24, y), (cx + s * 0.24, y)], acc, s * 0.05)
    c.poly([(cx + s * 0.34, y), (cx + s * 0.2, y - s * 0.08), (cx + s * 0.2, y + s * 0.08)], acc)
    c.poly([(cx - s * 0.34, y), (cx - s * 0.2, y - s * 0.08), (cx - s * 0.2, y + s * 0.08)], acc)


def steering(c, cx, cy, s, col, bg=WH):
    c.circle(cx, cy, s * 0.4, outline=col, width=s * 0.085)
    c.circle(cx, cy + s * 0.03, s * 0.12, fill=col)
    for a in (180, 0, 90):
        r = math.radians(a)
        c.line([(cx, cy + s * 0.03), (cx + math.cos(r) * s * 0.36, cy + s * 0.03 + math.sin(r) * s * 0.36)], col, s * 0.08)


def bus(c, cx, cy, s, col, bg=WH, glass=(200, 228, 244)):
    c.rect((cx - s * 0.34, cy - s * 0.42, cx + s * 0.34, cy + s * 0.34), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.26, cy - s * 0.36, cx + s * 0.26, cy - s * 0.26), fill=mix(col, (0, 0, 0), 0.3), r=s * 0.02)
    c.rect((cx - s * 0.28, cy - s * 0.2, cx + s * 0.28, cy + s * 0.08), fill=glass, r=s * 0.03)
    for k in (-1, 1):
        c.circle(cx + k * s * 0.2, cy + s * 0.2, s * 0.055, fill=(250, 236, 170))
        c.rect((cx + k * s * 0.22 - s * 0.07, cy + s * 0.32, cx + k * s * 0.22 + s * 0.07, cy + s * 0.46), fill=(40, 40, 46), r=s * 0.03)
    c.rect((cx - s * 0.08, cy + s * 0.18, cx + s * 0.08, cy + s * 0.22), fill=mix(col, bg, 0.5), r=s * 0.01)


def train(c, cx, cy, s, col, bg=WH, glass=(200, 228, 244)):
    c.line([(cx - s * 0.2, cy + s * 0.38), (cx - s * 0.36, cy + s * 0.48)], col, s * 0.04)
    c.line([(cx + s * 0.2, cy + s * 0.38), (cx + s * 0.36, cy + s * 0.48)], col, s * 0.04)
    c.rect((cx - s * 0.3, cy - s * 0.3, cx + s * 0.3, cy + s * 0.36), fill=col, r=s * 0.06)
    c.pie((cx - s * 0.3, cy - s * 0.46, cx + s * 0.3, cy - s * 0.14), 180, 360, col)
    c.rect((cx - s * 0.22, cy - s * 0.26, cx + s * 0.22, cy + s * 0.02), fill=glass, r=s * 0.04)
    for k in (-1, 1):
        c.circle(cx + k * s * 0.17, cy + s * 0.18, s * 0.05, fill=(250, 236, 170))
    c.rect((cx - s * 0.3, cy + s * 0.06, cx + s * 0.3, cy + s * 0.1), fill=mix(col, bg, 0.5))


def pill_bottle(c, cx, cy, s, col, bg=WH, cap=(60, 64, 76)):
    c.rect((cx - s * 0.26, cy - s * 0.44, cx + s * 0.26, cy - s * 0.26), fill=cap, r=s * 0.04)
    for k in range(5):
        c.line([(cx - s * 0.2 + k * s * 0.1, cy - s * 0.42), (cx - s * 0.2 + k * s * 0.1, cy - s * 0.28)], mix(cap, bg, 0.3), s * 0.02)
    c.rect((cx - s * 0.23, cy - s * 0.26, cx + s * 0.23, cy + s * 0.44), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.23, cy - s * 0.08, cx + s * 0.23, cy + s * 0.26), fill=bg)
    for k in range(3):
        c.rect((cx - s * 0.15, cy - s * 0.02 + k * s * 0.08, cx + s * (0.15 - 0.06 * (k % 2)), cy + s * 0.02 + k * s * 0.08), fill=mix(col, bg, 0.4), r=s * 0.01)


def basket(c, cx, cy, s, col, bg=WH):
    c.arc((cx - s * 0.28, cy - s * 0.48, cx + s * 0.28, cy + s * 0.08), 180, 360, col, s * 0.05)
    c.circle(cx - s * 0.16, cy - s * 0.1, s * 0.12, fill=(236, 110, 60))
    c.rect((cx - s * 0.02, cy - s * 0.3, cx + s * 0.1, cy - s * 0.02), fill=(240, 200, 120), r=s * 0.04)
    c.poly([(cx + s * 0.14, cy - s * 0.04), (cx + s * 0.22, cy - s * 0.3), (cx + s * 0.3, cy - s * 0.04)], (90, 160, 80))
    c.poly([(cx - s * 0.44, cy - s * 0.08), (cx + s * 0.44, cy - s * 0.08), (cx + s * 0.34, cy + s * 0.38), (cx - s * 0.34, cy + s * 0.38)], col)
    for k in range(1, 4):
        x0 = cx - s * 0.44 + k * s * 0.22
        c.line([(x0, cy - s * 0.04), (x0 - (x0 - cx) * 0.2, cy + s * 0.34)], mix(col, bg, 0.4), s * 0.025)
    c.line([(cx - s * 0.4, cy + s * 0.12), (cx + s * 0.4, cy + s * 0.12)], mix(col, bg, 0.4), s * 0.025)


def ticket(c, cx, cy, s, col, bg=WH):
    pts = rotpts([(cx - s * 0.44, cy - s * 0.24), (cx + s * 0.44, cy - s * 0.24), (cx + s * 0.44, cy + s * 0.24), (cx - s * 0.44, cy + s * 0.24)], cx, cy, -12)
    c.poly(pts, col)
    for k in (-1, 1):
        x, y = rotpts([(cx + k * s * 0.44, cy)], cx, cy, -12)[0]
        c.circle(x, y, s * 0.08, fill=bg)
    a, b = rotpts([(cx + s * 0.18, cy - s * 0.2), (cx + s * 0.18, cy + s * 0.2)], cx, cy, -12)
    for t in range(0, 8, 2):
        p0 = (a[0] + (b[0] - a[0]) * t / 8, a[1] + (b[1] - a[1]) * t / 8)
        p1 = (a[0] + (b[0] - a[0]) * (t + 1) / 8, a[1] + (b[1] - a[1]) * (t + 1) / 8)
        c.line([p0, p1], bg, s * 0.03)
    I.star(c, *rotpts([(cx - s * 0.12, cy)], cx, cy, -12)[0], s * 0.36, bg)


def merge_arrows(c, cx, cy, s, col, bg=WH):
    for dy in (-0.3, 0, 0.3):
        c.line([(cx - s * 0.44, cy + dy * s), (cx - s * 0.2, cy + dy * s), (cx + s * 0.04, cy)], mix(col, bg, 0.3 if dy else 0), s * 0.07)
    c.line([(cx + s * 0.02, cy), (cx + s * 0.28, cy)], col, s * 0.09)
    c.poly([(cx + s * 0.46, cy), (cx + s * 0.24, cy - s * 0.16), (cx + s * 0.24, cy + s * 0.16)], col)


def card_transfer(c, cx, cy, s, col, bg=WH, acc=(236, 150, 40)):
    I.card(c, cx - s * 0.08, cy + s * 0.12, s * 0.8, col, bg)
    pts = [(cx - s * 0.3, cy - s * 0.24)]
    for k in range(1, 11):
        a = math.radians(200 + k * 12)
        pts.append((cx + s * 0.02 + math.cos(a) * s * 0.34, cy - s * 0.02 + math.sin(a) * s * 0.26))
    c.line(pts, acc, s * 0.06)
    ex, ey = pts[-1]
    c.poly([(ex + s * 0.14, ey + s * 0.02), (ex - s * 0.04, ey - s * 0.1), (ex - s * 0.02, ey + s * 0.1)], acc)


def chat(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.46, cy - s * 0.4, cx + s * 0.14, cy - s * 0.02), fill=col, r=s * 0.1)
    c.poly([(cx - s * 0.34, cy - s * 0.04), (cx - s * 0.36, cy + s * 0.12), (cx - s * 0.2, cy - s * 0.04)], col)
    c2 = mix(col, bg, 0.45)
    c.rect((cx - s * 0.1, cy - s * 0.02, cx + s * 0.46, cy + s * 0.34), fill=c2, r=s * 0.1)
    c.poly([(cx + s * 0.28, cy + s * 0.32), (cx + s * 0.36, cy + s * 0.46), (cx + s * 0.18, cy + s * 0.32)], c2)
    for k in range(3):
        c.circle(cx - s * 0.28 + k * s * 0.12, cy - s * 0.21, s * 0.035, fill=bg)


def scales(c, cx, cy, s, col, bg=WH):
    c.rect((cx - s * 0.03, cy - s * 0.36, cx + s * 0.03, cy + s * 0.36), fill=col)
    c.poly([(cx - s * 0.22, cy + s * 0.44), (cx + s * 0.22, cy + s * 0.44), (cx + s * 0.12, cy + s * 0.34), (cx - s * 0.12, cy + s * 0.34)], col)
    c.rect((cx - s * 0.4, cy - s * 0.3, cx + s * 0.4, cy - s * 0.25), fill=col, r=s * 0.02)
    c.circle(cx, cy - s * 0.38, s * 0.05, fill=col)
    for k in (-1, 1):
        x = cx + k * s * 0.34
        c.line([(x, cy - s * 0.27), (x - s * 0.12, cy + s * 0.04)], col, s * 0.02)
        c.line([(x, cy - s * 0.27), (x + s * 0.12, cy + s * 0.04)], col, s * 0.02)
        c.pie((x - s * 0.16, cy - s * 0.1, x + s * 0.16, cy + s * 0.16), 0, 180, col)


def _doc_badge(c, cx, cy, s, col, bg, kind):
    I.doc(c, cx - s * 0.06, cy, s, col, bg)
    bx, by, br = cx + s * 0.24, cy + s * 0.26, s * 0.17
    if kind == "sign":
        pts = [(cx - s * 0.28 + k * s * 0.04, cy + s * 0.3 + math.sin(k * 1.3) * s * 0.04) for k in range(10)]
        c.line(pts, (30, 60, 150), s * 0.03)
        c.line([(cx + s * 0.34, cy - s * 0.1), (cx + s * 0.06, cy + s * 0.34)], (30, 60, 150), s * 0.05)
        c.poly([(cx + s * 0.06, cy + s * 0.34), (cx + s * 0.1, cy + s * 0.26), (cx + s * 0.02, cy + s * 0.3)], (30, 60, 150))
        return
    if kind == "coin":
        _badge(c, bx, by, br, GOLD, bg)
        c.text((bx, by), "$", "db", s * 0.2, WH, anchor="mm")
    elif kind == "heart":
        _badge(c, bx, by, br, (226, 80, 80), bg)
        heart_plain(c, bx, by + s * 0.01, s * 0.2, WH)


def doc_sign(c, cx, cy, s, col, bg=WH):
    _doc_badge(c, cx, cy, s, col, bg, "sign")


def doc_coin(c, cx, cy, s, col, bg=WH):
    _doc_badge(c, cx, cy, s, col, bg, "coin")


def doc_heart(c, cx, cy, s, col, bg=WH):
    _doc_badge(c, cx, cy, s, col, bg, "heart")


def otc_box(c, cx, cy, s, col, bg=WH):
    """Коробка из аптеки/магазина (без бренда) с надписью OTC."""
    c.rect((cx - s * 0.32, cy - s * 0.36, cx + s * 0.32, cy + s * 0.42), fill=col, r=s * 0.05)
    c.rect((cx - s * 0.1, cy - s * 0.46, cx + s * 0.1, cy - s * 0.34), fill=col, r=s * 0.04)
    c.circle(cx, cy - s * 0.4, s * 0.03, fill=bg)
    c.rect((cx - s * 0.24, cy - s * 0.24, cx + s * 0.24, cy + s * 0.12), fill=mix(col, bg, 0.85), r=s * 0.04)
    bte_aid(c, cx, cy - s * 0.06, s * 0.36, col, bg)
    c.text((cx, cy + s * 0.27), "OTC", "db", s * 0.17, bg, anchor="mm")


def bte_aid(c, cx, cy, s, col, bg=WH, tube=(150, 160, 174)):
    """Заушный слуховой аппарат: корпус-«полумесяц», прозрачная трубка, вкладыш."""
    bx, by, R = cx + s * 0.1, cy + s * 0.04, s * 0.36
    pts = [(bx + math.cos(math.radians(a)) * R, by + math.sin(math.radians(a)) * R) for a in range(128, 236, 9)]
    _cap(c, pts, col, s * 0.22)
    c.circle(pts[len(pts) // 2][0] + s * 0.02, pts[len(pts) // 2][1], s * 0.035, fill=mix(col, bg, 0.5))
    tx, ty, tr = cx + s * 0.1, cy - s * 0.2, s * 0.17
    tp = [pts[-1]] + [(tx + math.cos(math.radians(a)) * tr, ty + math.sin(math.radians(a)) * tr) for a in range(215, 425, 15)]
    tp.append((tp[-1][0] + s * 0.02, tp[-1][1] + s * 0.14))
    c.line(tp, tube, s * 0.04)
    ex, ey = tp[-1]
    c.ellipse((ex - s * 0.09, ey - s * 0.02, ex + s * 0.09, ey + s * 0.14), fill=mix(col, bg, 0.55))


def itc_aid(c, cx, cy, s, col, bg=WH):
    """Внутриканальный аппарат."""
    c.ellipse((cx - s * 0.3, cy - s * 0.3, cx + s * 0.24, cy + s * 0.22), fill=col)
    c.ellipse((cx + s * 0.02, cy + s * 0.0, cx + s * 0.4, cy + s * 0.34), fill=mix(col, (0, 0, 0), 0.12))
    c.circle(cx - s * 0.06, cy - s * 0.06, s * 0.13, fill=mix(col, bg, 0.35))
    c.circle(cx - s * 0.06, cy - s * 0.06, s * 0.035, fill=mix(col, (0, 0, 0), 0.4))
    c.line([(cx + s * 0.1, cy - s * 0.22), (cx + s * 0.22, cy - s * 0.36)], mix(col, (0, 0, 0), 0.3), s * 0.025)


def person_heart(c, cx, cy, s, col, bg=WH):
    I.person(c, cx - s * 0.08, cy, s * 0.9, col, bg)
    _badge(c, cx + s * 0.28, cy + s * 0.22, s * 0.17, (226, 80, 80), bg)
    heart_plain(c, cx + s * 0.28, cy + s * 0.23, s * 0.19, WH)


def med_bag(c, cx, cy, s, col, bg=WH):
    """Сумка патронажной сестры: белый «плюс» на цветном (не красный крест)."""
    c.rect((cx - s * 0.16, cy - s * 0.4, cx + s * 0.16, cy - s * 0.18), outline=col, width=s * 0.06, r=s * 0.06)
    c.rect((cx - s * 0.42, cy - s * 0.24, cx + s * 0.42, cy + s * 0.38), fill=col, r=s * 0.08)
    c.rect((cx - s * 0.05, cy - s * 0.1, cx + s * 0.05, cy + s * 0.24), fill=bg, r=s * 0.015)
    c.rect((cx - s * 0.17, cy + s * 0.02, cx + s * 0.17, cy + s * 0.12), fill=bg, r=s * 0.015)


def care_hands(c, cx, cy, s, col, bg=WH):
    """Личный уход: рука поддерживает руку."""
    I.heart_hands(c, cx, cy, s, col, bg)


def home_heart(c, cx, cy, s, col, bg=WH):
    I.house(c, cx, cy, s, col, bg, door=bg)
    heart_plain(c, cx, cy + s * 0.2, s * 0.22, (226, 80, 80))


def shield_check(c, cx, cy, s, col, bg=WH):
    pts = [(cx, cy - s * 0.44), (cx + s * 0.36, cy - s * 0.3), (cx + s * 0.32, cy + s * 0.1), (cx, cy + s * 0.44), (cx - s * 0.32, cy + s * 0.1), (cx - s * 0.36, cy - s * 0.3)]
    c.poly(pts, col)
    c.check(cx - s * 0.16, cy - s * 0.12, s * 0.32, bg, s * 0.07)


def car_shield(c, cx, cy, s, col, bg=WH, acc=(40, 170, 90)):
    I.car(c, cx - s * 0.06, cy + s * 0.08, s * 0.92, col, bg)
    c.circle(cx + s * 0.3, cy - s * 0.26, s * 0.2, fill=bg)
    shield_check(c, cx + s * 0.3, cy - s * 0.26, s * 0.34, acc, bg)


def piggy(c, cx, cy, s, col, bg=WH):
    c.ellipse((cx - s * 0.4, cy - s * 0.24, cx + s * 0.34, cy + s * 0.3), fill=col)
    c.ellipse((cx + s * 0.22, cy - s * 0.06, cx + s * 0.46, cy + s * 0.12), fill=mix(col, (0, 0, 0), 0.1))
    c.poly([(cx - s * 0.16, cy - s * 0.2), (cx - s * 0.06, cy - s * 0.4), (cx + s * 0.04, cy - s * 0.2)], col)
    for x in (-0.24, 0.12):
        c.rect((cx + x * s, cy + s * 0.22, cx + x * s + s * 0.1, cy + s * 0.4), fill=col, r=s * 0.03)
    c.rect((cx - s * 0.12, cy - s * 0.22, cx + s * 0.06, cy - s * 0.18), fill=mix(col, (0, 0, 0), 0.35), r=s * 0.02)
    c.circle(cx + s * 0.14, cy - s * 0.06, s * 0.03, fill=(40, 30, 30))
    c.circle(cx + s * 0.1, cy - s * 0.46, s * 0.1, fill=GOLD)


NEW_ICONS = dict(heart_plain=heart_plain, salt=salt, drop_check=drop_check, soup_bowl=soup_bowl, meal_plate=meal_plate,
                 snowflake=snowflake, pendant=pendant, wristband=wristband, base_station=base_station, gps_phone=gps_phone,
                 eye=eye, glasses_icon=glasses_icon, lens=lens, pound_tag=pound_tag, dollar_tag=dollar_tag, stretch=stretch,
                 syringe=syringe, hot_pack=hot_pack, tens=tens, odometer=odometer, black_box=black_box, compare_docs=compare_docs,
                 steering=steering, bus=bus, train=train, pill_bottle=pill_bottle, basket=basket, ticket=ticket,
                 merge_arrows=merge_arrows, card_transfer=card_transfer, chat=chat, scales=scales, doc_sign=doc_sign,
                 doc_coin=doc_coin, doc_heart=doc_heart, otc_box=otc_box, bte_aid=bte_aid, itc_aid=itc_aid,
                 person_heart=person_heart, med_bag=med_bag, care_hands=care_hands, home_heart=home_heart,
                 shield_check=shield_check, car_shield=car_shield, piggy=piggy)
I.ICONS.update(NEW_ICONS)


# =====================================================================  люди без лиц
SKIN = [(238, 198, 166), (196, 142, 104), (150, 98, 68), (244, 212, 186)]


def _head(c, x, y, r, skin, hair, kind):
    if kind == "long":
        c.rect((x - r * 1.1, y - r * 0.3, x + r * 1.1, y + r * 1.55), fill=hair, r=r * 0.55)
    c.circle(x, y, r, fill=skin)
    if kind in ("short", "long", "bun", "curly"):
        c.pie((x - r * 1.07, y - r * 1.14, x + r * 1.07, y + r * 0.86), 180, 360, hair)
        c.pie((x - r * 1.07, y - r * 0.9, x - r * 0.35, y + r * 0.5), 90, 270, hair)
    if kind == "bun":
        c.circle(x + r * 0.2, y - r * 1.05, r * 0.45, fill=hair)
    if kind == "curly":
        for a in range(190, 360, 34):
            c.circle(x + math.cos(math.radians(a)) * r * 0.95, y + math.sin(math.radians(a)) * r * 0.95, r * 0.3, fill=hair)
    if kind == "bald":
        c.pie((x - r * 1.05, y - r * 0.55, x - r * 0.35, y + r * 0.45), 90, 270, hair)
        c.pie((x + r * 0.35, y - r * 0.55, x + r * 1.05, y + r * 0.45), 270, 450, hair)


def standing(c, x, yb, h, skin, hair, kind, top, bottom, shoe=(58, 46, 40), arm_l=None, arm_r=None, skirt=False):
    """Стоящая фигура анфас. arm_l / arm_r — точки кистей (иначе руки опущены)."""
    r = h * 0.085
    hip = yb - h * 0.46
    sh = yb - h * 0.79
    tw = h * 0.14
    lw = h * 0.075
    if skirt:
        c.poly([(x - tw * 0.95, hip - h * 0.04), (x + tw * 0.95, hip - h * 0.04), (x + tw * 1.25, yb - h * 0.2), (x - tw * 1.25, yb - h * 0.2)], bottom)
        for k in (-1, 1):
            c.rect((x + k * lw * 0.75 - lw * 0.42, yb - h * 0.21, x + k * lw * 0.75 + lw * 0.42, yb - h * 0.03), fill=skin)
    else:
        for k in (-1, 1):
            c.rect((x + k * lw * 0.68 - lw * 0.55, hip - h * 0.02, x + k * lw * 0.68 + lw * 0.55, yb - h * 0.03), fill=bottom, r=lw * 0.3)
    for k in (-1, 1):
        c.rect((x + k * lw * 0.75 - lw * 0.75 + k * lw * 0.15, yb - h * 0.045, x + k * lw * 0.75 + lw * 0.75 + k * lw * 0.15, yb), fill=shoe, r=lw * 0.3)
    shoulder_l, shoulder_r = (x - tw * 0.82, sh + h * 0.05), (x + tw * 0.82, sh + h * 0.05)
    hl = arm_l or (x - tw * 1.05, hip + h * 0.02)
    hr = arm_r or (x + tw * 1.05, hip + h * 0.02)
    aw = h * 0.062
    for s_, hnd in ((shoulder_l, hl), (shoulder_r, hr)):
        if hnd is not None:
            mid = ((s_[0] + hnd[0]) / 2 + (x - s_[0]) * -0.1, (s_[1] + hnd[1]) / 2)
            _cap(c, [s_, mid, hnd], top, aw)
            c.circle(hnd[0], hnd[1], aw * 0.55, fill=skin)
    c.rect((x - tw, sh, x + tw, hip + h * 0.03), fill=top, r=tw * 0.55)
    c.rect((x - r * 0.35, sh - r * 0.6, x + r * 0.35, sh + r * 0.3), fill=skin)
    _head(c, x, sh - r * 1.25, r, skin, hair, kind)
    return dict(sh_l=shoulder_l, sh_r=shoulder_r, hip=hip, head=(x, sh - r * 1.25), r=r)


def seated(c, x, yseat, yfloor, h, skin, hair, kind, top, bottom, shoe=(58, 46, 40), arm_l=None, arm_r=None):
    """Сидящая фигура анфас (h — рост стоя)."""
    r = h * 0.085
    tw = h * 0.14
    lw = h * 0.078
    sh = yseat - h * 0.35
    for k in (-1, 1):
        c.rect((x + k * lw * 0.72 - lw * 0.55, yseat + h * 0.02, x + k * lw * 0.72 + lw * 0.55, yfloor - h * 0.03), fill=bottom, r=lw * 0.3)
        c.rect((x + k * lw * 0.9 - lw * 0.75, yfloor - h * 0.045, x + k * lw * 0.9 + lw * 0.75, yfloor), fill=shoe, r=lw * 0.3)
    c.rect((x - tw * 1.1, yseat - h * 0.04, x + tw * 1.1, yseat + h * 0.09), fill=bottom, r=h * 0.04)
    shoulder_l, shoulder_r = (x - tw * 0.82, sh + h * 0.05), (x + tw * 0.82, sh + h * 0.05)
    hl = arm_l or (x - tw * 0.55, yseat - h * 0.02)
    hr = arm_r or (x + tw * 0.55, yseat - h * 0.02)
    aw = h * 0.062
    c.rect((x - tw, sh, x + tw, yseat + h * 0.01), fill=top, r=tw * 0.55)
    for s_, hnd in ((shoulder_l, hl), (shoulder_r, hr)):
        mid = (s_[0] + (hnd[0] - s_[0]) * 0.3 + (s_[0] - x) * 0.25, (s_[1] + hnd[1]) / 2)
        _cap(c, [s_, mid, hnd], mix(top, (0, 0, 0), 0.08), aw)
        c.circle(hnd[0], hnd[1], aw * 0.55, fill=skin)
    c.rect((x - r * 0.35, sh - r * 0.6, x + r * 0.35, sh + r * 0.3), fill=skin)
    _head(c, x, sh - r * 1.25, r, skin, hair, kind)


def armchair(c, cx, yseat, yfloor, w, col):
    c.rect((cx - w * 0.42, yseat - w * 0.78, cx + w * 0.42, yseat + w * 0.05), fill=col, r=w * 0.16)
    c.rect((cx - w * 0.36, yseat - w * 0.7, cx + w * 0.36, yseat), fill=mix(col, WH, 0.12), r=w * 0.12)
    c.rect((cx - w * 0.5, yseat - w * 0.12, cx + w * 0.5, yseat + w * 0.2), fill=mix(col, (0, 0, 0), 0.06), r=w * 0.1)
    for k in (-1, 1):
        c.rect((cx + k * w * 0.5 - w * 0.13, yseat - w * 0.34, cx + k * w * 0.5 + w * 0.13, yseat + w * 0.26), fill=col, r=w * 0.1)
        c.rect((cx + k * w * 0.4 - w * 0.025, yseat + w * 0.24, cx + k * w * 0.4 + w * 0.025, yfloor), fill=(110, 76, 50), r=4)


def wall_clock(c, cx, cy, r, col=(60, 60, 70)):
    c.circle(cx, cy, r, fill=WH, outline=col, width=r * 0.12)
    for k in range(12):
        a = math.radians(k * 30)
        c.line([(cx + math.cos(a) * r * 0.72, cy + math.sin(a) * r * 0.72), (cx + math.cos(a) * r * 0.82, cy + math.sin(a) * r * 0.82)], col, r * 0.05)
    c.line([(cx, cy), (cx, cy - r * 0.6)], col, r * 0.08)
    c.line([(cx, cy), (cx + r * 0.42, cy + r * 0.1)], col, r * 0.08)
    c.circle(cx, cy, r * 0.08, fill=col)


# =====================================================================  сцены (концепция d)
def home_visit(c):
    """Уход на дому: гостиная, сиделка подаёт чашку пожилой женщине в кресле. Лиц нет."""
    c.vgrad((0, 0, W, 880), (252, 240, 228), (244, 224, 204))
    S.wood(c, (0, 880, W, W), (206, 160, 116), (184, 138, 96), lines=6, seed=21)
    c.rect((0, 870, W, 886), fill=(252, 246, 238))
    # окно слева
    wx0, wy0, wx1, wy1 = 60, 500, 330, 820
    c.rect((wx0 - 12, wy0 - 12, wx1 + 12, wy1 + 12), fill=WH, r=6)
    c.vgrad((wx0, wy0, wx1, wy1), (170, 214, 238), (226, 242, 248))
    for (x, y, r) in ((110, 790, 60), (200, 800, 70), (300, 780, 64)):
        c.circle(x, y, r, fill=(126, 180, 112))
    c.rect(((wx0 + wx1) / 2 - 6, wy0, (wx0 + wx1) / 2 + 6, wy1), fill=WH)
    c.rect((wx0, (wy0 + wy1) / 2 - 6, wx1, (wy0 + wy1) / 2 + 6), fill=WH)
    c.rect((wx0 - 30, wy1 + 8, wx1 + 30, wy1 + 24), fill=(240, 232, 220), r=4)
    # часы на стене
    wall_clock(c, 470, 560, 46)
    # ковёр
    c.ellipse((250, 960, 1000, 1070), fill=(226, 190, 150))
    c.ellipse((300, 976, 950, 1054), outline=(206, 164, 120), width=5)
    # столик с растением справа
    c.rect((905, 820, 1050, 836), fill=(150, 104, 70), r=4)
    c.rect((970, 836, 986, 1000), fill=(130, 90, 60))
    S.plant(c, 978, 820, 0.62, pot=(222, 120, 80))
    # кресло и пожилая женщина
    TEAL = (40, 120, 128)
    armchair(c, 720, 820, 1000, 330, TEAL)
    seated(c, 720, 820, 990, 420, SKIN[0], (214, 214, 220), "bun", (226, 120, 90), (70, 80, 110),
           arm_l=(640, 760), arm_r=(760, 812))
    c.rect((560, 820, 880, 900), fill=(236, 190, 90), r=24)  # плед на коленях
    for k in range(4):
        c.line([(585 + k * 80, 824), (575 + k * 80, 896)], (214, 164, 64), 4)
    # сиделка
    standing(c, 470, 1010, 470, SKIN[2], (40, 30, 28), "curly", (92, 150, 200), (48, 66, 110),
             arm_l=(405, 780), arm_r=(598, 748))
    # чашка в руках
    S.teacup(c, 622, 742, 0.42, rim=TEAL, steam=True)


def doorstep_meals(c):
    """Доставка готовых обедов: крыльцо, дверь, термосумка и контейнеры на скамейке."""
    c.vgrad((0, 0, W, 940), (250, 246, 238), (240, 232, 218))
    for y in range(420, 930, 34):
        c.line([(0, y), (W, y)], (228, 218, 200), 3)
    # дверь
    dx0, dx1, dy0, dy1 = 150, 420, 440, 910
    c.rect((dx0 - 22, dy0 - 22, dx1 + 22, dy1), fill=WH, r=6)
    c.rect((dx0, dy0, dx1, dy1), fill=(38, 96, 72), r=4)
    for (x0, y0, x1, y1) in ((dx0 + 30, dy0 + 40, dx1 - 30, dy0 + 200), (dx0 + 30, dy0 + 240, dx1 - 30, dy1 - 40)):
        c.rect((x0, y0, x1, y1), outline=(28, 76, 56), width=6, r=4)
    c.rect((dx0 + 70, dy0 + 70, dx1 - 70, dy0 + 170), fill=(200, 226, 236), r=4)
    c.circle(dx1 - 40, dy0 + 260, 12, fill=(236, 200, 110))
    c.rect(((dx0 + dx1) / 2 - 40, dy0 + 214, (dx0 + dx1) / 2 + 40, dy0 + 226), fill=(236, 200, 110), r=3)
    # светильник
    c.rect((470, 470, 510, 540), fill=(60, 60, 66), r=8)
    c.rect((476, 480, 504, 530), fill=(255, 236, 170), r=6)
    # ступень и дорожка
    c.rect((0, 910, W, W), fill=(210, 204, 196))
    c.rect((100, 900, 480, 940), fill=(190, 184, 176), r=4)
    for x in range(0, W, 110):
        c.line([(x, 940), (x - 30, W)], (192, 186, 178), 3)
    c.rect((170, 880, 400, 904), fill=(150, 110, 70), r=6)  # коврик
    # скамейка
    c.rect((560, 800, 1000, 826), fill=(170, 120, 80), r=6)
    for x in (590, 950):
        c.rect((x, 826, x + 22, 930), fill=(140, 96, 62), r=4)
    # термосумка
    c.shadow((600, 610, 800, 800), r=18, alpha=60, blur=8, off=(0, 6))
    c.rect((600, 640, 800, 800), fill=(228, 90, 56), r=18)
    c.rect((600, 640, 800, 690), fill=(206, 72, 44), r=18)
    c.arc((640, 570, 760, 680), 180, 360, (60, 60, 66), 10)
    c.rect((640, 716, 760, 770), fill=(250, 244, 236), r=8)
    I.ICONS["meal_plate"](c, 700, 743, 60, (206, 72, 44), bg=(250, 244, 236))
    # стопка контейнеров
    lids = [(96, 164, 84), (236, 180, 60), (80, 140, 200)]
    for k in range(3):
        y1 = 800 - k * 58
        c.rect((820, y1 - 52, 980, y1), fill=(250, 250, 246), r=10, outline=(210, 206, 196), width=2)
        c.rect((814, y1 - 60, 986, y1 - 44), fill=lids[k], r=6)
        c.rect((860, y1 - 34, 940, y1 - 16), fill=mix(lids[k], WH, 0.6), r=4)
    S.plant(c, 70, 910, 0.62, pot=(214, 110, 70))


def will_desk(c):
    """Завещание: стол сверху — лист LAST WILL AND TESTAMENT, перьевая ручка, очки, ключи, конверт."""
    S.wood(c, (0, 0, W, W), (122, 78, 52), (104, 64, 42), lines=18, seed=31, grain=(90, 54, 34))
    # кожаный бювар
    c.rect((20, 470, 1060, 1100), fill=(46, 58, 50), r=16)
    c.rect((36, 486, 1044, 1100), outline=(80, 96, 84), width=3, r=12)
    S.paper(c, (80, 540, 520, 1130), -4, head="LAST WILL AND TESTAMENT", head_size=22, lines=8)
    # линия подписи
    c.line([(150, 1000), (440, 980)], (60, 60, 70), 3)
    pts = [(170 + k * 14, 972 + math.sin(k * 0.9) * 12 - k * 0.8) for k in range(16)]
    c.line(pts, (30, 50, 140), 4)
    # перьевая ручка
    c.line([(560, 1030), (760, 760)], (20, 20, 26), 22)
    c.line([(700, 840), (760, 760)], (200, 170, 90), 22)
    c.poly([(560, 1030), (548, 1064), (574, 1044)], (200, 170, 90))
    c.circle(760, 760, 11, fill=(20, 20, 26))
    # очки
    S.glasses(c, 860, 620, 1.1)
    # ключи на кольце
    c.circle(840, 900, 34, outline=(190, 190, 196), width=6)
    for ang, col in ((-30, (210, 180, 90)), (20, (190, 190, 196))):
        pts = rotpts([(866, 890), (970, 890), (970, 912), (866, 912)], 866, 900, ang)
        c.poly(pts, col)
        hx, hy = rotpts([(880, 900)], 866, 900, ang)[0]
        c.circle(hx, hy, 24, fill=col)
        c.circle(hx, hy, 8, fill=(46, 58, 50))
    # конверт
    pts = rotpts([(620, 560), (840, 560), (840, 700), (620, 700)], 730, 630, 8)
    c.poly(pts, (244, 236, 220))
    a, b, cc, d = pts
    c.line([a, ((a[0] + b[0] + cc[0] + d[0]) / 4, (a[1] + b[1] + cc[1] + d[1]) / 4 + 10), b], (200, 190, 170), 3)


def hearing_table(c, table_y=690):
    """Слуховые аппараты на столе: коробка OTC с ценником $200 и футляр клиники с ценником $7,000+."""
    c.vgrad((0, 0, W, table_y), (240, 246, 250), (222, 232, 240))
    c.dots((0, 0, W, table_y), 44, 2.5, (180, 196, 210), alpha=60)
    c.rect((0, table_y, W, W), fill=(236, 228, 214))
    c.vgrad((0, table_y, W, W), (238, 230, 216), (222, 212, 196))
    c.rect((0, table_y - 8, W, table_y + 4), fill=(206, 196, 180))
    NAVY = (30, 60, 100)
    # слева: коробка OTC
    c.shadow((120, 700, 360, 980), r=18, alpha=70, blur=10, off=(8, 10))
    I.ICONS["otc_box"](c, 240, 840, 330, (60, 110, 170), bg=WH)
    # справа: открытый футляр с парой аппаратов
    c.shadow((520, 760, 900, 990), r=40, alpha=80, blur=12, off=(8, 12))
    c.rect((520, 620, 900, 760), fill=(36, 44, 56), r=40)
    c.rect((520, 740, 900, 990), fill=(36, 44, 56), r=40)
    c.rect((548, 766, 872, 966), fill=(70, 86, 120), r=28)
    I.ICONS["bte_aid"](c, 650, 862, 160, (200, 206, 214), bg=(70, 86, 120))
    I.ICONS["bte_aid"](c, 780, 862, 160, (200, 206, 214), bg=(70, 86, 120))
    # ценники
    for (x, y, lab, col) in ((330, 720, "$200", (40, 160, 90)), (880, 640, "$7,000+", (220, 70, 50))):
        c.line([(x - 30, y + 24), (x - 70, y + 70)], (120, 120, 120), 3)
        tw_ = c.tw(lab, c.font("db", 34))[0] + 50
        pts = [(x - 20, y), (x, y - 26), (x + tw_, y - 26), (x + tw_, y + 26), (x, y + 26)]
        c.poly(pts, col)
        c.circle(x - 2, y, 6, fill=WH)
        c.text((x + 16, y), lab, "db", 34, WH, anchor="lm")
    # чашка и растение
    S.teacup(c, 990, 990, 0.7, rim=NAVY)
    S.plant(c, 60, 700, 0.6, pot=(90, 140, 190))


def nightstand_alert(c):
    """Спальня: тумбочка с базовой станцией и кулоном тревожной кнопки, лампа, край кровати."""
    c.vgrad((0, 0, W, 860), (238, 244, 242), (222, 232, 230))
    S.wood(c, (0, 860, W, W), (196, 160, 122), (176, 140, 104), lines=5, seed=14)
    c.rect((0, 850, W, 866), fill=(250, 250, 246))
    # картина
    c.rect((760, 110, 1010, 320), fill=(160, 120, 80), r=6)
    c.rect((776, 126, 994, 304), fill=(200, 226, 236))
    c.poly([(776, 304), (850, 210), (920, 270), (960, 230), (994, 270), (994, 304)], (110, 168, 120))
    c.circle(950, 170, 22, fill=(250, 220, 120))
    # кровать слева внизу
    c.rect((-40, 780, 520, 1080), fill=(92, 130, 170), r=30)
    c.rect((-40, 740, 380, 830), fill=(250, 250, 250), r=40)
    c.rect((-40, 840, 520, 900), fill=(72, 108, 150), r=10)
    # тумбочка
    c.rect((640, 760, 1040, 790), fill=(170, 120, 80), r=8)
    c.rect((660, 790, 1020, 1020), fill=(186, 136, 94), r=6)
    c.rect((680, 820, 1000, 900), outline=(150, 106, 70), width=4, r=6)
    c.circle(840, 860, 8, fill=(120, 84, 56))
    c.rect((680, 1020, 700, 1060), fill=(150, 106, 70))
    c.rect((980, 1020, 1000, 1060), fill=(150, 106, 70))
    # лампа
    c.rect((952, 620, 964, 760), fill=(80, 80, 88))
    c.ellipse((920, 748, 996, 766), fill=(80, 80, 88))
    c.poly([(900, 540), (1016, 540), (1040, 630), (876, 630)], (250, 226, 170))
    c.glow((860, 560, 1060, 720), (255, 240, 190), alpha=90, blur=30)
    # базовая станция и кулон
    I.ICONS["base_station"](c, 790, 690, 230, (52, 60, 74), bg=WH)
    I.ICONS["pendant"](c, 920, 722, 90, (52, 60, 74), bg=WH)


def optician_wall(c):
    """Оптика: таблица для проверки зрения, полка с оправами, книга с очками на столе."""
    c.rect((0, 0, W, W), fill=(244, 242, 250))
    c.rect((0, 880, W, W), fill=(206, 176, 140))
    S.wood(c, (0, 880, W, W), (214, 180, 142), (196, 160, 122), lines=5, seed=41)
    c.rect((0, 872, W, 888), fill=(186, 150, 112))
    # таблица
    bx0, by0, bx1, by1 = 660, 400, 1000, 860
    c.shadow((bx0, by0, bx1, by1), r=8, alpha=50, blur=10, off=(0, 6))
    c.rect((bx0, by0, bx1, by1), fill=WH, r=8)
    rows = ["E", "F P", "T O Z", "L P E D", "P E C F D", "E D F C Z P"]
    y = by0 + 40
    for k, rw in enumerate(rows):
        sz = [110, 70, 52, 40, 32, 26][k]
        c.text(((bx0 + bx1) / 2, y), rw, "db", sz, (20, 20, 26), anchor="ma")
        y += sz * 1.25 + 6
    # полка с оправами
    c.rect((50, 640, 580, 660), fill=(150, 110, 80), r=4)
    for k, col in enumerate(((40, 36, 34), (150, 60, 50), (40, 80, 150))):
        S.glasses(c, 140 + k * 170, 600, 0.75, col=col)
    c.rect((50, 440, 580, 460), fill=(150, 110, 80), r=4)
    for k, col in enumerate(((120, 90, 60), (30, 120, 110))):
        S.glasses(c, 190 + k * 230, 400, 0.75, col=col)
    # раскрытая книга с очками
    c.poly([(200, 950), (520, 930), (530, 1050), (210, 1070)], (250, 248, 240))
    c.poly([(520, 930), (840, 950), (830, 1070), (530, 1050)], (244, 240, 230))
    for k in range(5):
        c.line([(240, 970 + k * 18), (490, 954 + k * 18)], (200, 200, 206), 4)
        c.line([(560, 956 + k * 18), (800, 972 + k * 18)], (200, 200, 206), 4)
    S.glasses(c, 520, 980, 1.05)
    S.plant(c, 990, 1000, 0.6, pot=(120, 100, 180))


def park_walk(c):
    """Парк: тропинка, скамейка, деревья, пожилая пара на прогулке (без лиц)."""
    c.vgrad((0, 0, W, 700), (196, 228, 246), (236, 246, 250))
    c.poly([(0, 640), (300, 560), (620, 620), (900, 540), (W, 580), (W, 760), (0, 760)], (150, 200, 130))
    c.rect((0, 700, W, W), fill=(128, 186, 110))
    c.poly([(420, W), (700, W), (600, 700), (540, 700)], (228, 212, 180))
    for (x, y, r, tr) in ((110, 560, 110, 40), (260, 600, 80, 30), (900, 520, 120, 44), (1010, 600, 80, 30)):
        c.rect((x - tr / 4, y, x + tr / 4, y + 200), fill=(120, 84, 56))
        c.circle(x, y, r, fill=(84, 150, 90))
        c.circle(x - r * 0.4, y + r * 0.3, r * 0.7, fill=(96, 164, 100))
    # скамейка
    c.rect((740, 840, 1020, 860), fill=(150, 100, 60), r=4)
    c.rect((740, 790, 1020, 808), fill=(150, 100, 60), r=4)
    for x in (760, 1000):
        c.rect((x - 6, 808, x + 6, 940), fill=(70, 70, 76))
    c.rect((880, 800, 912, 840), fill=(90, 150, 210), r=6)
    # пара на прогулке
    standing(c, 470, 990, 330, SKIN[3], (200, 200, 206), "short", (216, 104, 70), (60, 70, 96), arm_r=(530, 850))
    standing(c, 590, 1000, 350, SKIN[1], (170, 170, 176), "bald", (60, 110, 160), (80, 80, 86), arm_l=(535, 852))
    for (x, y) in ((180, 900), (320, 960), (860, 980), (980, 1040)):
        c.circle(x, y, 10, fill=(250, 220, 90))
        c.circle(x + 14, y + 6, 8, fill=(250, 250, 250))


def driveway(c):
    """Автостраховка: дом с гаражом, машина на подъездной дорожке, письмо о продлении полиса."""
    c.vgrad((0, 0, W, 900), (206, 230, 246), (240, 247, 251))
    for (x, y, r) in ((140, 180, 44), (200, 170, 60), (260, 186, 40), (880, 120, 40), (940, 110, 54)):
        c.circle(x, y, r, fill=WH, alpha=180)
    # дом
    c.poly([(470, 560), (770, 400), (1080, 560)], (70, 76, 92))
    c.rect((500, 560, 1080, 880), fill=(206, 170, 130))
    for r_ in range(570, 880, 28):
        c.line([(500, r_), (1080, r_)], (190, 154, 116), 2)
    c.rect((760, 660, 1040, 880), fill=(236, 236, 232))
    for y in range(680, 880, 36):
        c.line([(760, y), (1040, y)], (206, 206, 202), 4)
    c.rect((540, 620, 660, 720), fill=WH)
    c.rect((550, 630, 650, 710), fill=(160, 204, 228))
    c.rect((597, 630, 603, 710), fill=WH)
    # газон и дорожка
    c.rect((0, 870, W, W), fill=(130, 186, 110))
    c.poly([(700, 870), (1080, 870), (1080, W), (560, W)], (200, 200, 204))
    c.poly([(0, 900), (420, 900), (300, W), (0, W)], (118, 172, 100))
    # машина
    cx, cy = 790, 900
    s = 420
    c.ellipse((cx - s * 0.5, cy + s * 0.22, cx + s * 0.5, cy + s * 0.32), fill=(0, 0, 0), alpha=40)
    I.car(c, cx, cy, s, (30, 90, 170), bg=WH)
    # письмо
    S.paper(c, (60, 690, 360, 1040), -8, head="RENEWAL", head_size=30, lines=5)
    S.plant(c, 470, 880, 0.55)


def wallet_table(c):
    """Скидки 60+: стол сверху — проездные без логотипов, кошелёк, пакет из аптеки, чек, корзина."""
    c.rect((0, 0, W, W), fill=(252, 244, 232))
    c.dots((0, 0, W, W), 40, 2.5, (230, 200, 170), alpha=70)
    # кошелёк
    c.shadow((70, 520, 470, 780), r=24, alpha=70, blur=10, off=(6, 10))
    c.rect((70, 520, 470, 780), fill=(120, 60, 150), r=24)
    c.rect((70, 520, 470, 600), fill=(100, 48, 128), r=24)
    c.circle(430, 650, 18, fill=(236, 196, 90))
    # две карты-проездные (пиктограммы вместо логотипов)
    for (x, y, ang, col, ic) in ((250, 470, -8, (30, 110, 190), "bus"), (330, 500, 6, (230, 110, 40), "train")):
        pts = rotpts([(x - 150, y - 90), (x + 150, y - 90), (x + 150, y + 90), (x - 150, y + 90)], x, y, ang)
        c.shadow((x - 150, y - 80, x + 150, y + 96), r=16, alpha=50, blur=8, off=(0, 6))
        c.poly(pts, col)
        ix, iy = rotpts([(x - 80, y - 10)], x, y, ang)[0]
        c.circle(ix, iy, 50, fill=WH)
        I.ICONS[ic](c, ix, iy, 76, col, bg=WH)
        l0 = rotpts([(x + 10, y - 30), (x + 120, y - 30)], x, y, ang)
        l1 = rotpts([(x + 10, y + 10), (x + 90, y + 10)], x, y, ang)
        c.line(l0, WH, 12, alpha=200)
        c.line(l1, WH, 12, alpha=200)
    # пакет из аптеки с флаконом
    c.shadow((620, 420, 860, 700), r=10, alpha=60, blur=10, off=(6, 10))
    c.poly([(620, 440), (860, 440), (850, 700), (630, 700)], (250, 250, 246))
    c.poly([(620, 440), (860, 440), (850, 470), (630, 470)], (230, 230, 226))
    I.ICONS["pill_bottle"](c, 740, 590, 170, (40, 150, 110), bg=WH)
    # чек со знаком %
    S.paper(c, (880, 420, 1040, 720), 6, head="%", head_size=40, lines=6)
    # корзина
    I.ICONS["basket"](c, 780, 870, 300, (200, 110, 40), bg=(252, 244, 232))
    # билет в музей/кино
    I.ICONS["ticket"](c, 250, 880, 220, (40, 150, 110), bg=(252, 244, 232))


def bills_table(c, table_y=660):
    """Консолидация долгов: на столе несколько счетов и карт, стрелки сходятся в один конверт."""
    c.vgrad((0, 0, W, table_y), (240, 246, 247), (222, 234, 236))
    c.dots((0, 0, W, table_y), 44, 2.5, (170, 196, 200), alpha=60)
    S.wood(c, (0, table_y, W, W), (198, 156, 112), (178, 136, 94), lines=7, seed=51)
    c.rect((0, table_y - 6, W, table_y + 6), fill=(150, 110, 74))
    S.paper(c, (40, 700, 300, 960), -10, head="STATEMENT", head_size=22, lines=5)
    S.paper(c, (180, 760, 440, 1040), 6, head="BILL", head_size=24, lines=5)
    I.card(c, 140, 1000, 220, (30, 60, 120), ang=-14)
    I.card(c, 390, 700, 200, (190, 60, 60), ang=10)
    # стрелки
    TEAL = (0, 120, 130)
    for (x0, y0) in ((330, 740), (460, 880), (330, 1000)):
        pts = [(x0 + k * 30, y0 + (880 - y0) * (k / 8) ** 1.5) for k in range(9)]
        c.line(pts, TEAL, 12, alpha=220)
    c.poly([(640, 880), (600, 850), (600, 910)], TEAL)
    # один конверт
    c.shadow((670, 770, 1010, 990), r=10, alpha=70, blur=10, off=(6, 10))
    I.ICONS["envelope"] if False else None
    c.rect((670, 770, 1010, 990), fill=WH, r=8, outline=(200, 206, 210), width=3)
    c.line([(674, 774), (840, 890), (1006, 774)], (200, 206, 210), 4)
    c.circle(840, 930, 34, fill=TEAL)
    c.text((840, 930), "1", "db", 40, WH, anchor="mm")
    S.teacup(c, 980, 700, 0.6, rim=TEAL)


for _fn in (home_visit, doorstep_meals, will_desk, hearing_table, nightstand_alert, optician_wall, park_walk, driveway,
            wallet_table, bills_table):
    setattr(S, "w2_" + _fn.__name__, _fn)
