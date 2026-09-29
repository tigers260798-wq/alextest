"""Волна 5 · NT (29.09, креативщик w5nt): 5 карточек «Готово к заливу» из article_drafts/NT-*-2026-09-30 × 4 статики 1:1, Pillow.
    python3 w5_nt.py            — все пакеты
    python3 w5_nt.py 3 5        — пакеты 3 и 5
    python3 w5_nt.py 3:a,c      — пакет 3, буквы a и c
Пишет /home/user/alextest/creatives/ready/2026-09-30_packs/<docId>/<a|b|c|d>.png и creatives.json рядом.
Движок — w3_packs / w4_ukde / w5_0929 (импорт, файлы не меняются): p60_templates (quiz / compare), w2b_layouts.scene_d,
w4 grid6, иконки p60/w2b/w3/w4/w5. Здесь — свои раскладки (лестница сертификатов, шкала сроков, чек, 3 карточки,
таблица на 2 колонки, 2 порта, квиз-посадочный), сцены (перрон и ангар, учебный класс медассистента, кухня вечером,
стол с документами, порт на закате) и иконки w5n_*.
Весь текст на картинках — только из статей карточек (раздел — в поле src). Без зарплат, обещаний работы, сумм, ставок и
сроков кредита, цен и скидок круизов, «free diploma», «instant / same day / guaranteed», «near me / près de chez vous»,
«click here», логотипов, эмблем, бортовых номеров и названий лайнеров, вопросов о зрителе."""
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w5_0929 as W5  # noqa: E402  (тянет w4_ukde, w3_packs и весь движок; переставляет p60_lib.OUT — вернём ниже)
import w4_ukde as W4  # noqa: E402
import w3_packs as W3  # noqa: E402
import p60_lib  # noqa: E402
from p60_lib import C, W, mix, rotpts  # noqa: E402
import p60_icons as I  # noqa: E402
import p60_scenes as S  # noqa: E402
import p60_templates as T  # noqa: E402
import p60w2_art as A  # noqa: E402
import w2b_scenes as WS  # noqa: E402
import w2b_layouts as L  # noqa: E402

OUTN = "/home/user/alextest/creatives/ready/2026-09-30_packs"
p60_lib.OUT = OUTN  # C.save пишет в p60_lib.OUT; w5_0929 при импорте ставит туда 2026-09-29_drafts
p60_lib.F.setdefault("mono", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
p60_lib.F.setdefault("monob", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf")
WH = (255, 255, 255)
SKIN = A.SKIN
CONCEPT = W3.CONCEPT
PACKS = {}


def icon(c, name, cx, cy, s, col, bg=WH):
    I.ICONS[name](c, cx, cy, s, col, bg=bg)


def _bg(c, p):
    if p.get("bg2"):
        c.vgrad((0, 0, W, W), p["bg"], p["bg2"])


def pill_w(c, label, size=22, padx=20):
    b = c.pill(label, 0, -500, size=size, padx=padx, pady=10)
    return b[2] - b[0]


# =====================================================================  иконки w5n (квадрат s, центр cx, cy)
def w5n_school(c, cx, cy, s, col, bg=WH, acc=(236, 170, 40)):
    """Здание школы: фронтон, колонны, флажок без символики."""
    c.poly([(cx - s * 0.46, cy - s * 0.12), (cx, cy - s * 0.4), (cx + s * 0.46, cy - s * 0.12)], col)
    c.rect((cx - s * 0.4, cy - s * 0.12, cx + s * 0.4, cy + s * 0.34), fill=col, r=s * 0.02)
    for k in range(4):
        x = cx - s * 0.3 + k * s * 0.2
        c.rect((x - s * 0.045, cy - s * 0.04, x + s * 0.045, cy + s * 0.26), fill=bg, r=s * 0.02)
    c.rect((cx - s * 0.46, cy + s * 0.3, cx + s * 0.46, cy + s * 0.38), fill=col, r=s * 0.02)
    c.circle(cx, cy - s * 0.2, s * 0.06, fill=acc)


def w5n_ged(c, cx, cy, s, col, bg=WH, acc=(236, 170, 40)):
    """Лист теста с 4 галочками-разделами (4 предмета)."""
    c.rect((cx - s * 0.3, cy - s * 0.4, cx + s * 0.3, cy + s * 0.4), fill=col, r=s * 0.06)
    c.rect((cx - s * 0.25, cy - s * 0.35, cx + s * 0.25, cy + s * 0.35), fill=bg, r=s * 0.04)
    for k in range(4):
        y = cy - s * 0.22 + k * s * 0.16
        c.rect((cx - s * 0.19, y - s * 0.05, cx - s * 0.09, y + s * 0.05), fill=acc, r=s * 0.02)
        c.rect((cx - s * 0.04, y - s * 0.022, cx + s * 0.19, y + s * 0.022), fill=col, r=s * 0.02)


def w5n_engine(c, cx, cy, s, col, bg=WH, acc=(236, 170, 40)):
    """Поршневой двигатель с винтом (силовая установка)."""
    c.rect((cx - s * 0.2, cy - s * 0.18, cx + s * 0.28, cy + s * 0.18), fill=col, r=s * 0.05)
    for k in range(3):
        x = cx - s * 0.12 + k * s * 0.14
        for j in range(3):
            c.rect((x - s * 0.05, cy - s * 0.28 - j * s * 0.0 + j * s * 0.035, x + s * 0.05, cy - s * 0.26 + j * s * 0.035),
                   fill=col, r=s * 0.01)
    c.rect((cx - s * 0.3, cy - s * 0.05, cx - s * 0.2, cy + s * 0.05), fill=col)
    c.circle(cx - s * 0.33, cy, s * 0.06, fill=acc)
    c.poly([(cx - s * 0.36, cy - s * 0.02), (cx - s * 0.3, cy - s * 0.02), (cx - s * 0.31, cy - s * 0.44), (cx - s * 0.35, cy - s * 0.44)], col)
    c.poly([(cx - s * 0.36, cy + s * 0.02), (cx - s * 0.3, cy + s * 0.02), (cx - s * 0.31, cy + s * 0.44), (cx - s * 0.35, cy + s * 0.44)], col)


def w5n_house_split(c, cx, cy, s, col, bg=WH, acc=(236, 170, 40)):
    """Дом, у которого закрашена доля (продажа доли будущей цены — home reversion)."""
    c.poly([(cx - s * 0.46, cy - s * 0.04), (cx, cy - s * 0.42), (cx + s * 0.46, cy - s * 0.04)], col)
    c.rect((cx - s * 0.36, cy - s * 0.06, cx + s * 0.36, cy + s * 0.38), fill=col, r=s * 0.02)
    c.poly([(cx, cy - s * 0.42), (cx + s * 0.46, cy - s * 0.04), (cx + s * 0.36, cy - s * 0.04), (cx + s * 0.36, cy + s * 0.38), (cx, cy + s * 0.38)], acc)
    c.rect((cx - s * 0.24, cy + s * 0.08, cx - s * 0.08, cy + s * 0.24), fill=bg, r=s * 0.02)
    c.line([(cx, cy - s * 0.44), (cx, cy + s * 0.42)], bg, s * 0.035)


def w5n_lighthouse(c, cx, cy, s, col, bg=WH, acc=(236, 170, 40)):
    """Маяк на волне."""
    c.poly([(cx - s * 0.16, cy + s * 0.3), (cx + s * 0.16, cy + s * 0.3), (cx + s * 0.1, cy - s * 0.2), (cx - s * 0.1, cy - s * 0.2)], col)
    for k in range(2):
        y = cy + s * (0.14 - k * 0.2)
        c.poly([(cx - s * (0.145 - k * 0.02), y), (cx + s * (0.145 - k * 0.02), y), (cx + s * (0.135 - k * 0.02), y - s * 0.07),
                (cx - s * (0.135 - k * 0.02), y - s * 0.07)], bg)
    c.rect((cx - s * 0.13, cy - s * 0.3, cx + s * 0.13, cy - s * 0.2), fill=acc, r=s * 0.02)
    c.poly([(cx - s * 0.15, cy - s * 0.3), (cx + s * 0.15, cy - s * 0.3), (cx, cy - s * 0.42)], col)
    c.poly([(cx + s * 0.13, cy - s * 0.28), (cx + s * 0.46, cy - s * 0.38), (cx + s * 0.46, cy - s * 0.14)], acc, alpha=150)
    pts = [(cx - s * 0.46 + k * s * 0.04, cy + s * 0.36 + math.sin(k * 0.9) * s * 0.03) for k in range(24)]
    c.line(pts, col, s * 0.04)


I.ICONS.update(dict(w5n_school=w5n_school, w5n_ged=w5n_ged, w5n_engine=w5n_engine, w5n_house_split=w5n_house_split,
                    w5n_lighthouse=w5n_lighthouse))


# =====================================================================  предметы
def trainer_plane(c, x0, base, L, body=WH, stripe=(30, 110, 200), stripe2=(240, 120, 30), glass=(120, 160, 200), prop=True):
    """Учебный одномоторный высокоплан сбоку, нос вправо. x0 — хвост, base — земля, L — длина. Без номеров и логотипов."""
    def P(u, v):
        return (x0 + u * L, base - v * L)
    dark = (60, 66, 78)
    # стабилизатор (за фюзеляжем)
    c.poly([P(0.0, 0.232), P(0.15, 0.228), P(0.15, 0.212), P(0.02, 0.214)], mix(body, dark, 0.12))
    # киль
    c.poly([P(0.03, 0.25), P(0.055, 0.42), P(0.115, 0.42), P(0.2, 0.262)], body)
    c.poly([P(0.047, 0.36), P(0.055, 0.42), P(0.115, 0.42), P(0.135, 0.36)], stripe)
    # подкос крыла (дальний)
    c.line([P(0.535, 0.315), P(0.6, 0.145)], mix(dark, WH, 0.35), L * 0.009)
    # стойки шасси
    c.line([P(0.56, 0.125), P(0.52, 0.045)], dark, L * 0.012)
    c.line([P(0.9, 0.125), P(0.9, 0.045)], dark, L * 0.01)
    # фюзеляж
    fus = [P(0.03, 0.205), P(0.03, 0.255), P(0.45, 0.305), P(0.66, 0.305), P(0.76, 0.24), P(0.93, 0.228), P(0.97, 0.195),
           P(0.97, 0.15), P(0.92, 0.12), P(0.62, 0.112), P(0.45, 0.128)]
    c.poly(fus, body)
    # полосы
    c.poly([P(0.05, 0.233), P(0.94, 0.176), P(0.955, 0.19), P(0.05, 0.245)], stripe)
    c.poly([P(0.05, 0.219), P(0.94, 0.162), P(0.945, 0.17), P(0.05, 0.227)], stripe2)
    # окна кабины
    c.poly([P(0.49, 0.292), P(0.645, 0.292), P(0.735, 0.238), P(0.49, 0.238)], glass)
    c.line([P(0.6, 0.292), P(0.6, 0.238)], body, L * 0.008)
    c.poly([P(0.5, 0.286), P(0.56, 0.286), P(0.53, 0.262)], mix(glass, WH, 0.5))
    # дверь
    c.line([P(0.5, 0.236), P(0.5, 0.13)], mix(body, dark, 0.3), L * 0.003)
    c.line([P(0.6, 0.236), P(0.605, 0.125)], mix(body, dark, 0.3), L * 0.003)
    # капот: швы и выхлоп
    c.line([P(0.8, 0.236), P(0.8, 0.118)], mix(body, dark, 0.25), L * 0.003)
    c.rect((P(0.86, 0.13)[0], P(0.86, 0.13)[1], P(0.9, 0.12)[0], P(0.9, 0.12)[1]), fill=dark, r=2)
    # кок винта
    c.poly([P(0.97, 0.196), P(0.99, 0.188), P(1.005, 0.172), P(0.99, 0.156), P(0.97, 0.149)], mix(stripe, WH, 0.1))
    # крыло (сбоку — профиль) + ближний подкос
    c.poly([P(0.44, 0.312), P(0.47, 0.33), P(0.7, 0.33), P(0.715, 0.318), P(0.7, 0.308), P(0.44, 0.306)], body)
    c.line([P(0.44, 0.309), P(0.715, 0.315)], mix(body, dark, 0.2), L * 0.003)
    c.line([P(0.52, 0.31), P(0.585, 0.14)], mix(dark, WH, 0.15), L * 0.01)
    # колёса с обтекателями
    for u, r in ((0.52, 0.045), (0.9, 0.036)):
        wx, wy = P(u, r)
        c.circle(wx, wy, r * L, fill=(40, 42, 48))
        c.circle(wx, wy, r * L * 0.45, fill=(150, 154, 162))
        c.ellipse((wx - r * L * 1.25, wy - r * L * 1.05, wx + r * L * 1.2, wy + r * L * 0.1), fill=body)
        c.line([(wx - r * L * 1.1, wy - r * L * 0.05), (wx + r * L * 1.05, wy - r * L * 0.05)], mix(body, dark, 0.2), L * 0.003)
    # хвостовое колесо не рисуем (трёхколёсное шасси)
    # винт (размытый диск)
    if prop:
        px = P(1.0, 0.17)[0]
        c.ellipse((px - L * 0.012, base - 0.34 * L, px + L * 0.012, base - 0.0 * L - L * 0.015), fill=(200, 206, 214), alpha=110)
        c.line([(px, base - 0.33 * L), (px, base - 0.03 * L)], (90, 96, 108), L * 0.006, alpha=140)


def chock(c, cx, by, s, col=(250, 196, 40)):
    c.poly([(cx - s, by), (cx + s, by), (cx + s * 0.35, by - s * 0.9), (cx - s * 0.35, by - s * 0.9)], col)


def windsock(c, x, by, h, col=(240, 110, 40)):
    c.line([(x, by), (x, by - h)], (120, 126, 136), 6)
    c.circle(x, by - h, 6, fill=(120, 126, 136))
    segs = 5
    for k in range(segs):
        x0 = x + k * h * 0.09
        x1 = x0 + h * 0.09
        r0 = h * (0.09 - k * 0.01)
        r1 = h * (0.09 - (k + 1) * 0.01)
        yc0, yc1 = by - h + r0 + k * 3, by - h + r1 + (k + 1) * 3
        c.poly([(x0, yc0 - r0), (x1, yc1 - r1), (x1, yc1 + r1), (x0, yc0 + r0)], col if k % 2 == 0 else WH)


def engine_stand(c, cx, by, s):
    """Поршневой двигатель на жёлтом стенде с колёсами (учебный ангар)."""
    yel, dark, metal = (244, 190, 40), (54, 58, 66), (170, 176, 186)
    # стенд
    c.rect((cx - 150 * s, by - 60 * s, cx + 150 * s, by - 44 * s), fill=yel, r=4 * s)
    for x in (cx - 120 * s, cx + 120 * s):
        c.rect((x - 8 * s, by - 150 * s, x + 8 * s, by - 44 * s), fill=yel, r=3 * s)
        c.circle(x, by - 14 * s, 16 * s, fill=dark)
        c.circle(x, by - 14 * s, 6 * s, fill=metal)
    c.line([(cx - 120 * s, by - 150 * s), (cx - 60 * s, by - 110 * s)], yel, 10 * s)
    c.line([(cx + 120 * s, by - 150 * s), (cx + 60 * s, by - 110 * s)], yel, 10 * s)
    # картер
    c.rect((cx - 90 * s, by - 190 * s, cx + 80 * s, by - 100 * s), fill=metal, r=14 * s)
    c.rect((cx - 90 * s, by - 150 * s, cx + 80 * s, by - 138 * s), fill=mix(metal, dark, 0.3))
    # цилиндры с рёбрами (сверху)
    for k in range(3):
        x = cx - 60 * s + k * 55 * s
        c.rect((x - 20 * s, by - 250 * s, x + 20 * s, by - 186 * s), fill=mix(metal, dark, 0.2), r=5 * s)
        for j in range(5):
            y = by - 244 * s + j * 11 * s
            c.rect((x - 26 * s, y, x + 26 * s, y + 5 * s), fill=mix(metal, dark, 0.45), r=2 * s)
    # фланец винта
    c.rect((cx + 80 * s, by - 160 * s, cx + 110 * s, by - 130 * s), fill=dark, r=4 * s)
    c.circle(cx + 118 * s, by - 145 * s, 22 * s, fill=mix(metal, WH, 0.2))
    c.circle(cx + 118 * s, by - 145 * s, 8 * s, fill=dark)
    # трубки
    c.line([(cx - 80 * s, by - 110 * s), (cx - 100 * s, by - 80 * s), (cx - 60 * s, by - 70 * s)], (200, 90, 50), 6 * s)


def tool_cart(c, x, by, s, col=(210, 50, 50)):
    c.rect((x - 60 * s, by - 170 * s, x + 60 * s, by - 30 * s), fill=col, r=8 * s)
    for k in range(4):
        y = by - 160 * s + k * 32 * s
        c.rect((x - 52 * s, y, x + 52 * s, y + 26 * s), fill=mix(col, (0, 0, 0), 0.12), r=4 * s)
        c.rect((x - 16 * s, y + 10 * s, x + 16 * s, y + 15 * s), fill=(220, 224, 230), r=2 * s)
    for xx in (x - 44 * s, x + 44 * s):
        c.circle(xx, by - 14 * s, 14 * s, fill=(40, 42, 48))


# =====================================================================  раскладки
def stairs6(P, t):
    """Лестница из 6 ступеней: снизу вверх, каждая — карточка с номером, подписью, строкой и кнопкой.
    В свободном левом верхнем углу — «герой» (самолёт в наборе высоты)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56), t2_col=p.get("acc"))
    steps = t["steps"]
    n = len(steps)
    g = 12
    rh = t.get("row_h", 108)
    wd = t.get("row_w", 640)
    dx = (1040 - 40 - wd) / (n - 1)
    if t.get("hero"):
        t["hero"](c, (40, y + 44, 40 + dx * (n - 2) - 20, 1040 - (n - 3) * rh - (n - 4) * g - 20))
    pw = pill_w(c, P["cta"], 21, 18)
    for k, (lab, sub) in enumerate(steps):
        y0 = 1040 - (k + 1) * rh - k * g
        x0 = 40 + k * dx
        box = (x0, y0, x0 + wd, y0 + rh)
        c.card(box, fill=p["tile"], r=20, sh_alpha=55, blur=10, off=(0, 5))
        col = mix(p["step0"], p["step1"], k / (n - 1))
        c.rect((x0, y0, x0 + 84, y0 + rh), fill=col, r=20)
        c.rect((x0 + 60, y0, x0 + 84, y0 + rh), fill=col)
        c.text((x0 + 42, y0 + rh / 2), str(k + 1), "db", 44, WH, anchor="mm")
        tx = x0 + 106
        tw_ = wd - 106 - pw - 34
        fs = min(c.fit(s_[0], "db", tw_, 1, 31) for s_ in steps)
        c.text((tx, y0 + rh * 0.36), lab, "db", fs, p["tile_ink"], anchor="lm")
        c.text((tx, y0 + rh * 0.7), sub, "s", c.fit(sub, "s", tw_, 1, 24), p["sub"], anchor="lm")
        c.pill(P["cta"], x0 + wd - 18 - pw / 2, y0 + rh / 2, size=21, fill=p["btn"], padx=18, pady=10)
    return c


def plane_rot(c, x, y, L, ang, **kw):
    """Высокоплан, повёрнутый на ang градусов (против часовой — нос вверх); x, y — левый верх вставки.
    Возвращает (ширина, высота, точка хвоста) в единицах 1080."""
    from PIL import Image
    tmp = C((0, 0, 0), K=c.K)
    tmp.im.putalpha(0)
    trainer_plane(tmp, 20, L * 0.5, L, **kw)
    cw, ch = L * 1.08, L * 0.5 + 6
    crop = tmp.im.crop(tmp.sb((0, 0, cw, ch)))
    rot = crop.rotate(ang, expand=True, resample=Image.BICUBIC)
    px, py = c.sp([(x, y)])[0]
    c.im.alpha_composite(rot, (px, py))
    rw, rh = rot.width / c.K, rot.height / c.K
    a = math.radians(ang)
    tx, ty = 20 + 0.04 * L - cw / 2, L * 0.5 - 0.23 * L - ch / 2
    return rw, rh, (x + tx * math.cos(a) + ty * math.sin(a) + rw / 2, y - tx * math.sin(a) + ty * math.cos(a) + rh / 2)


def hero_climb(c, box):
    """Самолёт в наборе высоты (нос — к верхней ступени), пунктир-траектория и облака; без номеров."""
    x0, y0, x1, y1 = box
    for cx, cy, s in ((x0 + 60, y0 + 30, 0.7), (x0 + 130, y1 - 60, 0.8)):
        for dx, dy, r in ((-40, 6, 30), (0, -8, 40), (42, 6, 30)):
            c.circle(cx + dx * s, cy + dy * s, r * s, fill=WH, alpha=235)
    w_, h_, tail = plane_rot(c, x0 + 14, y0 + 30, 250, 20)
    pts = []
    for k in range(31):
        tt = k / 30
        pts.append((x0 + 8 + (tail[0] + 6 - x0 - 8) * tt ** 1.5, y1 + 10 - (y1 + 10 - tail[1] - 8) * tt))
    for k in range(0, 30, 3):
        c.line([pts[k], pts[k + 1]], (120, 162, 210), 6)


def timeline5(P, t):
    """Шкала сроков: строки с подписью, сроком справа, полосой длины (sqrt-шкала) и кнопкой; метка «not a credential»."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56), t2_col=p.get("acc"))
    rows = t["rows"]
    n = len(rows)
    top = y + 26
    g = 14
    rh = (1044 - top - (n - 1) * g) / n
    pw = pill_w(c, P["cta"], 22, 20)
    dmax = max(r[2] for r in rows)
    for k, (lab, dur, days, chip) in enumerate(rows):
        y0 = top + k * (rh + g)
        box = (40, y0, 1040, y0 + rh)
        c.card(box, fill=p["tile"], r=22, sh_alpha=50, blur=10, off=(0, 5))
        short = chip is not None
        col = p["short"] if short else p["prog"]
        c.rect((40, y0, 54, y0 + rh), fill=col, r=7)
        c.text((80, y0 + rh * 0.3), lab, "db", 32, p["tile_ink"], anchor="lm")
        lw = c.tw(lab, c.font("db", 32))[0]
        if chip:
            cw_ = c.tw(chip, c.font("sb", 21))[0] + 28
            cb = (80 + lw + 18, y0 + rh * 0.3 - 18, 80 + lw + 18 + cw_, y0 + rh * 0.3 + 18)
            c.rect(cb, fill=mix(p["short"], WH, 0.82), r=18)
            c.text(((cb[0] + cb[2]) / 2, (cb[1] + cb[3]) / 2 + 1), chip, "sb", 21, mix(p["short"], (0, 0, 0), 0.25), anchor="mm")
        c.text((1040 - 30, y0 + rh * 0.3), dur, "db", 30, col, anchor="rm")
        bx0, bx1 = 80, 1040 - 30 - pw - 40
        by = y0 + rh * 0.7
        c.rect((bx0, by - 12, bx1, by + 12), fill=(232, 236, 240), r=12)
        f = max(0.035, math.sqrt(days / dmax))
        c.rect((bx0, by - 12, bx0 + (bx1 - bx0) * f, by + 12), fill=col, r=12)
        c.pill(P["cta"], 1040 - 30 - pw / 2, by, size=22, fill=p["btn"], padx=20, pady=10)
    return c


def receipt(P, t):
    """Чек «из чего складывается цена»: строки с отточием и «$?», одна цифра статьи, итог «$?», подпись и кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56), t2_col=p.get("acc"))
    top = y + 34
    bot = 846
    x0, x1 = 160, 920
    # бумага с зубчатым низом
    c.shadow((x0, top, x1, bot), r=6, alpha=70, blur=16, off=(0, 10))
    c.rect((x0, top, x1, bot - 14), fill=WH, r=6)
    k = 0
    xx = x0
    zz = []
    while xx < x1:
        zz += [(xx, bot - 14), (min(x1, xx + 14), bot + 2)]
        xx += 28
    zz += [(x1, bot - 14)]
    c.poly([(x0, bot - 20)] + zz + [(x1, bot - 20)], WH)
    cx = (x0 + x1) / 2
    yy = top + 34
    c.text((cx, yy + 18), t["bill"], "monob", 32, p["ink"], anchor="mm")
    yy += 50
    if t.get("bill_sub"):
        c.text((cx, yy + 14), t["bill_sub"], "mono", 24, p["sub"], anchor="mm")
        yy += 40
    for xx in range(int(x0 + 30), int(x1 - 30), 18):
        c.line([(xx, yy + 10), (xx + 9, yy + 10)], (180, 186, 196), 3)
    yy += 36
    rows = t["rows"]
    rh = (bot - 124 - yy) / len(rows)
    for lab, val, note in rows:
        c.text((x0 + 44, yy + 20), lab, "monob", 30, (40, 44, 54), anchor="lm")
        lw = c.tw(lab, c.font("monob", 30))[0]
        vw = c.tw(val, c.font("monob", 32))[0]
        for xx in range(int(x0 + 44 + lw + 14), int(x1 - 44 - vw - 14), 14):
            c.circle(xx, yy + 30, 2.4, fill=(170, 176, 186))
        c.text((x1 - 44, yy + 20), val, "monob", 32, p["acc"] if val.endswith("?") else p["ink"], anchor="rm")
        if note:
            c.text((x0 + 44, yy + 54), note, "mono", 22, p["sub"], anchor="lm")
        yy += rh
    for xx in range(int(x0 + 30), int(x1 - 30), 18):
        c.line([(xx, yy), (xx + 9, yy)], (180, 186, 196), 3)
    c.text((x0 + 44, yy + 44), t["total"][0], "monob", 36, p["ink"], anchor="lm")
    c.text((x1 - 44, yy + 44), t["total"][1], "monob", 40, p["acc"], anchor="rm")
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 872, 1000, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 984, size=42, fill=p["btn"])
    return c


def cards3(P, t):
    """3 высокие карточки-маршрута: иконка в круге, подпись, строка из статьи, кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 58), t2_col=p.get("acc"))
    top = y + 34
    g = 22
    tw = (1000 - 2 * g) / 3
    bot = 1044
    for i, (ic, lab, desc, col, res) in enumerate(t["cards"]):
        x0 = 40 + i * (tw + g)
        box = (x0, top, x0 + tw, bot)
        c.card(box, fill=p["tile"], r=28, sh_alpha=60, blur=14, off=(0, 8))
        c.rect((x0, top, x0 + tw, top + 20), fill=col, r=10)
        c.rect((x0, top + 10, x0 + tw, top + 28), fill=p["tile"])
        cx = x0 + tw / 2
        c.text((x0 + 30, top + 60), f"{i + 1}", "db", 40, col, anchor="lm")
        icy = top + (bot - top) * 0.26
        c.circle(cx, icy, 86, fill=mix(col, WH, 0.86))
        icon(c, ic, cx, icy, 120, col, bg=mix(col, WH, 0.86))
        ly = icy + 118
        fs = min(c.fit(x[1], "db", tw - 36, 2, 34) for x in t["cards"])
        ly = c.block(lab, "db", fs, ly, tw - 36, p["tile_ink"], cx=cx, max_lines=2, gap=1.04)
        c.block(desc, "s", 26, ly + 12, tw - 44, p["sub"], cx=cx, max_lines=3, gap=1.1)
        if res:
            rb = (x0 + 20, bot - 190, x0 + tw - 20, bot - 100)
            c.rect(rb, fill=mix(col, WH, 0.88), r=16)
            c.text((cx, rb[1] + 26), t.get("res_label", "Result"), "s", 22, mix(col, (0, 0, 0), 0.2), anchor="mm")
            c.text((cx, rb[1] + 60), res, "db", c.fit(res, "db", tw - 60, 1, 26), mix(col, (0, 0, 0), 0.25), anchor="mm")
        c.pill(P["cta"], cx, bot - 50, size=24, fill=p["btn"], padx=22, pady=11)
    return c


def table2(P, t):
    """Таблица на 2 колонки с широкой колонкой подписей (подпись до 2 строк)."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 54))
    top = y + 26
    bot = 862 if t.get("foot") else 900
    box = (40, top, 1040, bot)
    c.card(box, r=28, sh_alpha=60, blur=14, off=(0, 8))
    lw = t.get("label_w", 250)
    cw = (box[2] - box[0] - lw) / 2
    for k, (head, ic, col) in enumerate(t["cols"]):
        x0 = box[0] + lw + k * cw
        bgc = mix(col, WH, 0.9)
        if k == 1:
            c.rect((x0, box[1], x0 + cw, box[3]), fill=bgc, r=28)
            c.rect((x0, box[1], x0 + 30, box[3]), fill=bgc)
        cx = x0 + cw / 2
        icon(c, ic, cx, box[1] + 60, 80, col, bg=bgc if k == 1 else WH)
        c.block(head, "db", c.fit(head, "db", cw - 30, 2, 28), box[1] + 110, cw - 30, col, cx=cx, max_lines=2, gap=1.0)
    hh = 178
    rows = t["rows"]
    rh = (box[3] - box[1] - hh - 10) / len(rows)
    ry = box[1] + hh
    for lab, *vals in rows:
        c.line([(box[0] + 20, ry), (box[2] - 20, ry)], (224, 228, 234), 2)
        nl = len(c.wrap(lab, c.font("sb", 27), lw - 44))
        c.block(lab, "sb", 27, ry + rh / 2 - nl * c.lh("sb", 27, 1.04) / 2 + 2, lw - 44, (80, 86, 98), align="left", x=box[0] + 30,
                max_lines=2, gap=1.04)
        for k, v in enumerate(vals):
            x0 = box[0] + lw + k * cw
            sz = 29
            while sz > 21 and len(c.wrap(v, c.font("sb", sz), cw - 40)) > 2:
                sz -= 1
            nl = len(c.wrap(v, c.font("sb", sz), cw - 40))
            c.block(v, "sb", sz, ry + rh / 2 - nl * c.lh("sb", sz, 1.04) / 2 + 2, cw - 40, (36, 40, 50), cx=x0 + cw / 2, max_lines=2, gap=1.04)
        ry += rh
    if t.get("foot"):
        c.block(t["foot"], "sb", 32, 886, 1000, p["ink"], max_lines=1)
    c.button(P["cta"], W / 2, 986, size=42, fill=p["btn"])
    return c


def ports2(P, t):
    """2 порта колонками: шапка (иконка, порт, море) + 4 строки-кнопки со стоянками, у каждой кнопка."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 56), t2_col=p.get("acc"))
    top = y + 30
    g = 24
    cw = (1000 - g) / 2
    pw = pill_w(c, P["cta"], 20, 16)
    for i, (name, sea, cities, ic, col) in enumerate(t["ports"]):
        x0 = 40 + i * (cw + g)
        hb = (x0, top, x0 + cw, top + 150)
        c.card(hb, fill=col, r=26, sh_alpha=60, blur=12, off=(0, 6))
        c.circle(x0 + 76, top + 75, 52, fill=WH)
        icon(c, ic, x0 + 76, top + 75, 74, col)
        c.text((x0 + 150, top + 56), name, "db", c.fit(name, "db", cw - 170, 1, 42), WH, anchor="lm")
        c.text((x0 + 150, top + 106), sea, "sb", c.fit(sea, "sb", cw - 170, 1, 26), mix(col, WH, 0.75), anchor="lm")
        n = len(cities)
        rt = top + 150 + 18
        gg = 12
        rh = (1044 - rt - (n - 1) * gg) / n
        for k, city in enumerate(cities):
            ry = rt + k * (rh + gg)
            rb = (x0, ry, x0 + cw, ry + rh)
            c.card(rb, fill=p["tile"], r=20, sh_alpha=45, blur=8, off=(0, 4))
            c.rect((x0, ry, x0 + 12, ry + rh), fill=col, r=6)
            c.text((x0 + 34, ry + rh * 0.34), city, "db", c.fit(city, "db", cw - 60, 1, 32), p["tile_ink"], anchor="lm")
            c.pill(P["cta"], x0 + 34 + pw / 2, ry + rh * 0.72, size=20, fill=p["btn"], padx=16, pady=9)
    return c


def pass_quiz(P, t):
    """Квиз на «посадочном»: шапка-лента, маршрут, вопрос и 4 варианта; справа отрывной корешок со штрихкодом."""
    p = P["pal"]
    c = C(p["bg"])
    _bg(c, p)
    c.ellipse((780, -160, 1260, 320), fill=WH, alpha=22)
    c.ellipse((-200, 760, 260, 1220), fill=WH, alpha=16)
    y = T.header(c, t, col=p["ink"], sub_col=p["sub"], size=t.get("size", 54), t2_col=p.get("t2"))
    top = y + 34
    box = (50, top, 1030, 900)
    stub = 820
    c.shadow(box, r=26, alpha=110, blur=20, off=(0, 12))
    c.rect(box, fill=WH, r=26)
    # шапка
    c.rect((box[0], box[1], box[2], box[1] + 74), fill=p["band"], r=26)
    c.rect((box[0], box[1] + 40, box[2], box[1] + 74), fill=p["band"])
    icon(c, "w4_ship", box[0] + 58, box[1] + 38, 60, WH, bg=p["band"])
    c.text((box[0] + 104, box[1] + 38), t["pass_head"], "db", 28, WH, anchor="lm")
    c.text((box[2] - 34, box[1] + 38), t["step"], "sb", 24, mix(p["band"], WH, 0.7), anchor="rm")
    # перфорация и выемки
    for yy in range(int(box[1] + 90), int(box[3] - 20), 22):
        c.line([(stub, yy), (stub, yy + 11)], (200, 206, 214), 3)
    c.circle(stub, box[1] + 74, 16, fill=p["bg2"] if p.get("bg2") else p["bg"])
    c.circle(stub, box[3], 16, fill=p["bg2"] if p.get("bg2") else p["bg"])
    # маршрут
    x0, x1 = box[0] + 40, stub - 36
    ry = box[1] + 104
    a, b = t["pass_route"].split(" → ")
    c.text((x0, ry), t.get("from_lab", ""), "s", 22, (120, 126, 136))
    c.text((x1, ry), t.get("to_lab", ""), "s", 22, (120, 126, 136), anchor="ra")
    c.text((x0, ry + 30), a, "db", 40, p["ink"])
    c.text((x1, ry + 30), b, "db", 40, p["ink"], anchor="ra")
    aw = c.tw(a, c.font("db", 40))[0]
    bw = c.tw(b, c.font("db", 40))[0]
    mx0, mx1 = x0 + aw + 24, x1 - bw - 24
    for xx in range(int(mx0), int(mx1 - 30), 20):
        c.line([(xx, ry + 56), (xx + 10, ry + 56)], p["acc"], 4)
    c.poly([(mx1 - 26, ry + 44), (mx1, ry + 56), (mx1 - 26, ry + 68)], p["acc"])
    yy = ry + 110
    c.line([(x0, yy - 14), (x1, yy - 14)], (230, 234, 238), 2)
    yy = c.block(t["q"], "db", t.get("q_size", 34), yy, x1 - x0, (38, 38, 46), align="left", x=x0, max_lines=2, gap=1.1) + 14
    n = len(t["opts"])
    h = min(70, (box[3] - 30 - yy - (n - 1) * 12) / n)
    fs = min(c.fit(o, "sb", x1 - x0 - h - 30, 1, 30) for o in t["opts"])
    for o in t["opts"]:
        c.rect((x0, yy, x1, yy + h), fill=(246, 248, 249), r=h / 2, outline=(206, 214, 220), width=3)
        c.circle(x0 + h / 2 + 4, yy + h / 2, h * 0.22, fill=WH, outline=(150, 160, 170), width=3)
        c.text((x0 + h + 8, yy + h / 2), o, "sb", fs, (48, 52, 60), anchor="lm")
        yy += h + 12
    # корешок
    sx0, sx1 = stub + 24, box[2] - 24
    scx = (sx0 + sx1) / 2
    for k, (lab, val) in enumerate(t["stub"]):
        c.text((scx, box[1] + 120 + k * 110), lab, "s", 20, (120, 126, 136), anchor="mm")
        c.text((scx, box[1] + 154 + k * 110), val, "db", 30, p["ink"], anchor="mm")
    rnd = random.Random(3)
    bx = sx0 + 26
    while bx < sx1 - 26:
        w_ = rnd.choice((3, 3, 5, 7))
        c.rect((bx, box[3] - 190, bx + w_, box[3] - 50), fill=(40, 44, 54))
        bx += w_ + rnd.choice((3, 4, 6))
    c.button(P["cta"], W / 2, 978, size=42, fill=p["btn"])
    return c


FN = dict(W5.FN)
FN.update({"scene_card2": lambda P, t: scene_card2(P, t)})
FN.update({"ports2": ports2, "pass_quiz": pass_quiz})
FN.update({"stairs6": stairs6, "timeline5": timeline5, "receipt": receipt, "cards3": cards3, "table2": table2})


# =====================================================================  сцены
def sc_apron_hangar(c):
    """Перрон учебного аэродрома: высокоплан без номеров с колодками, конус ветра, открытый ангар с двигателем на стенде."""
    c.vgrad((0, 0, W, 700), (96, 164, 226), (206, 230, 248))
    for cx, cy, s in ((180, 470, 1.0), (860, 420, 0.8), (560, 560, 0.6)):
        for dx, dy, r in ((-50, 8, 36), (0, -10, 48), (52, 8, 36)):
            c.circle(cx + dx * s, cy + dy * s, r * s, fill=WH, alpha=220)
    # дальний лес
    rnd = random.Random(7)
    for k in range(30):
        x = k * 38 + rnd.uniform(-8, 8)
        r = rnd.uniform(28, 46)
        c.circle(x, 700 - r * 0.4, r, fill=(88, 134, 104))
    c.rect((0, 690, W, 720), fill=(118, 160, 110))
    # перрон
    c.vgrad((0, 716, W, W), (178, 182, 188), (150, 154, 160))
    for k in range(-2, 12):
        c.line([(k * 130, W), (k * 130 + 200, 716)], (164, 168, 174), 3)
    c.line([(0, 1010), (W, 960)], (246, 196, 40), 8)
    # ангар
    hx0, hx1, hy_top, hy_base = 590, 1120, 520, 900
    c.rect((hx0, 610, hx1, hy_base), fill=(214, 220, 228))
    c.pie((hx0 - 10, hy_top, hx1 + 10, 700), 180, 360, (170, 180, 192))
    c.rect((hx0, 600, hx1, 616), fill=(150, 160, 172))
    for k in range(9):
        x = hx0 + 20 + k * 60
        c.line([(x, 616), (x, hy_base)], (200, 206, 216), 3)
    dx0, dx1 = hx0 + 40, hx1 - 70
    c.vgrad((dx0, 640, dx1, hy_base), (58, 64, 76), (96, 102, 112))
    for x in (dx0 + 90, dx0 + 260, dx0 + 420):
        c.ellipse((x - 40, 652, x + 40, 668), fill=(255, 248, 210))
        c.glow((x - 70, 650, x + 70, 760), (255, 244, 200), alpha=50, blur=20)
    c.rect((dx0, hy_base - 16, dx1, hy_base), fill=(120, 124, 132))
    # сдвинутые створки
    c.rect((dx0 - 36, 640, dx0 + 6, hy_base), fill=(196, 204, 214))
    c.rect((dx1 - 6, 640, dx1 + 36, hy_base), fill=(196, 204, 214))
    engine_stand(c, dx0 + 190, hy_base - 4, 0.72)
    tool_cart(c, dx0 + 380, hy_base - 4, 0.72)
    # верстак и мануал
    c.rect((dx0 + 20, hy_base - 110, dx0 + 70, hy_base - 4), fill=(110, 90, 70))
    c.rect((dx0 + 10, hy_base - 120, dx0 + 80, hy_base - 106), fill=(140, 110, 80))
    # конус ветра
    windsock(c, 470, 716, 150)
    # самолёт
    trainer_plane(c, 30, 990, 540)
    chock(c, 30 + 0.52 * 540 - 34, 990, 14)
    chock(c, 30 + 0.52 * 540 + 34, 990, 14)


def bp_gauge(c, cx, cy, r, cuff=(40, 96, 170)):
    """Тонометр: манжета, трубка, круглый манометр, груша."""
    c.rect((cx - 190, cy + 20, cx - 40, cy + 74), fill=cuff, r=16)
    c.rect((cx - 180, cy + 30, cx - 50, cy + 40), fill=mix(cuff, WH, 0.3), r=4)
    c.line([(cx - 60, cy + 46), (cx - 20, cy + 70), (cx, cy + r)], (50, 54, 62), 5)
    c.line([(cx - 120, cy + 74), (cx - 110, cy + 110), (cx - 60, cy + 120)], (50, 54, 62), 5)
    c.ellipse((cx - 70, cy + 104, cx - 20, cy + 136), fill=(50, 54, 62))
    c.circle(cx, cy, r + 6, fill=(60, 64, 72))
    c.circle(cx, cy, r, fill=WH)
    for k in range(12):
        a = math.radians(135 + k * 270 / 11)
        c.line([(cx + math.cos(a) * r * 0.78, cy + math.sin(a) * r * 0.78), (cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92)],
               (60, 64, 72), 3)
    a = math.radians(200)
    c.line([(cx, cy), (cx + math.cos(a) * r * 0.75, cy + math.sin(a) * r * 0.75)], (210, 50, 50), 4)
    c.circle(cx, cy, 5, fill=(60, 64, 72))


def training_arm(c, x0, y, L, skin=(232, 190, 160), pad=(120, 170, 200)):
    """Учебная рука-манекен для инъекций на подложке (предплечье + кисть), без людей."""
    c.rect((x0 - 20, y - 10, x0 + L + 30, y + 60), fill=pad, r=18)
    c.rect((x0 - 20, y + 40, x0 + L + 30, y + 60), fill=mix(pad, (0, 0, 0), 0.15), r=10)
    c.poly([(x0, y - 36), (x0 + L * 0.72, y - 20), (x0 + L * 0.72, y + 22), (x0, y + 30)], skin)
    c.circle(x0, y - 3, 33, fill=skin)
    hx = x0 + L * 0.72
    c.rect((hx - 10, y - 30, hx + L * 0.16, y + 26), fill=skin, r=18)
    for k in range(4):
        fy = y - 24 + k * 13
        c.rect((hx + L * 0.12, fy, hx + L * 0.28 - k * 6, fy + 11), fill=skin, r=5)
    c.rect((hx + 10, y - 44, hx + L * 0.12, y - 30), fill=skin, r=7)
    c.line([(x0 + 30, y - 6), (x0 + L * 0.3, y - 2), (x0 + L * 0.6, y + 4)], (120, 150, 200), 5)
    c.line([(x0 + L * 0.3, y - 2), (x0 + L * 0.5, y - 14)], (120, 150, 200), 4)


def laptop_screen(c, x0, y0, w, h, head, lines, acc, body=(40, 44, 52), bars=0):
    c.rect((x0 - 12, y0 - 12, x0 + w + 12, y0 + h + 12), fill=body, r=12)
    c.rect((x0, y0, x0 + w, y0 + h), fill=WH, r=4)
    c.rect((x0, y0, x0 + w, y0 + 40), fill=acc, r=4)
    c.rect((x0, y0 + 24, x0 + w, y0 + 40), fill=acc)
    c.text((x0 + 16, y0 + 20), head, "sb", 20, WH, anchor="lm")
    yy = y0 + 60
    for ln in lines:
        c.text((x0 + 16, yy), ln, "sb", 21, (40, 44, 54), anchor="lm")
        yy += 34
    for k in range(bars):
        c.rect((x0 + 16, yy - 6, x0 + 16 + (w - 32) * (0.9 - 0.18 * (k % 3)), yy + 4), fill=(214, 220, 230), r=4)
        yy += 22
    c.rect((x0 + 16, y0 + h - 30, x0 + w - 16, y0 + h - 18), fill=(226, 230, 236), r=6)
    c.rect((x0 + 16, y0 + h - 30, x0 + 16 + (w - 32) * 0.4, y0 + h - 18), fill=acc, r=6)
    c.poly([(x0 - 40, y0 + h + 12), (x0 + w + 40, y0 + h + 12), (x0 + w + 64, y0 + h + 36), (x0 - 64, y0 + h + 36)], mix(body, WH, 0.35))
    c.rect((x0 + w / 2 - 40, y0 + h + 18, x0 + w / 2 + 40, y0 + h + 26), fill=mix(body, WH, 0.2), r=3)


def stethoscope(c, x, y, s=1.0, col=(50, 54, 62)):
    pts = [(x + math.cos(math.radians(a)) * 70 * s, y + math.sin(math.radians(a)) * 34 * s) for a in range(200, 520, 12)]
    c.line(pts, col, 7 * s)
    c.line([(x - 60 * s, y - 10 * s), (x - 84 * s, y - 40 * s)], (170, 176, 186), 5 * s)
    c.line([(x - 50 * s, y - 16 * s), (x - 60 * s, y - 50 * s)], (170, 176, 186), 5 * s)
    c.circle(pts[-1][0] + 14 * s, pts[-1][1] + 6 * s, 20 * s, fill=(170, 176, 186))
    c.circle(pts[-1][0] + 14 * s, pts[-1][1] + 6 * s, 12 * s, fill=(210, 214, 222))


def lab_coat_chair(c, x, y_top, h, coat=(250, 250, 250), chair=(150, 110, 76)):
    """Спинка деревянного стула (стойки видны) с наброшенным белым халатом."""
    w = h * 0.5
    for sx in (x - w / 2, x + w / 2):
        c.rect((sx - 12, y_top - 20, sx + 12, y_top + h), fill=chair, r=8)
        c.circle(sx, y_top - 22, 15, fill=mix(chair, (0, 0, 0), 0.1))
    c.rect((x - w / 2, y_top + 10, x + w / 2, y_top + 50), fill=chair, r=8)
    c.rect((x - w / 2, y_top + h * 0.62, x + w / 2, y_top + h * 0.62 + 30), fill=chair, r=8)
    cw = w * 0.86
    # халат переброшен через верхнюю перекладину
    c.rect((x - cw / 2, y_top + 6, x + cw / 2, y_top + h * 0.56), fill=coat, r=18)
    c.rect((x - cw / 2, y_top + 6, x + cw / 2, y_top + 40), fill=mix(coat, (0, 0, 0), 0.05), r=16)
    c.poly([(x - cw * 0.2, y_top + 40), (x, y_top + h * 0.26), (x + cw * 0.2, y_top + 40)], (226, 232, 238))
    c.line([(x - cw * 0.2, y_top + 40), (x, y_top + h * 0.26), (x + cw * 0.2, y_top + 40)], (196, 202, 212), 4)
    c.line([(x, y_top + h * 0.26), (x, y_top + h * 0.56)], (206, 210, 218), 3)
    c.rect((x - cw * 0.44, y_top + h * 0.34, x - cw * 0.12, y_top + h * 0.44), outline=(200, 206, 214), width=3, r=4)
    c.line([(x - cw * 0.3, y_top + h * 0.31), (x - cw * 0.3, y_top + h * 0.38)], (40, 96, 170), 5)
    # рукав свисает сбоку
    c.rect((x + cw / 2 - 30, y_top + 30, x + cw / 2 + 22, y_top + h * 0.84), fill=mix(coat, (0, 0, 0), 0.03), r=20)
    c.line([(x + cw / 2 - 26, y_top + h * 0.78), (x + cw / 2 + 18, y_top + h * 0.78)], (206, 210, 218), 3)


def sc_ma_classroom(c):
    """Учебный класс медассистента: доска «VITAL SIGNS», стол — ноутбук с модулем, тонометр, учебная рука-манекен,
    стетоскоп, халат на спинке стула. Людей и пациентов нет. Верх (до y≈460) закрывает карточка."""
    c.vgrad((0, 0, W, 800), (224, 240, 236), (206, 228, 222))
    c.dots((0, 0, W, 800), 46, 2.4, (170, 200, 192), alpha=60)
    # доска (по центру, над тонометром)
    bx0, by0, bx1, by1 = 400, 486, 790, 716
    c.rect((bx0, by0, bx1, by1), fill=(200, 206, 214), r=10)
    c.rect((bx0 + 12, by0 + 12, bx1 - 12, by1 - 12), fill=WH, r=6)
    c.text((bx0 + 34, by0 + 44), "VITAL SIGNS", "db", 30, (30, 90, 160), anchor="lm")
    zx = bx0 + 34
    zz = [(zx, 620), (zx + 50, 620), (zx + 70, 584), (zx + 90, 664), (zx + 110, 600), (zx + 126, 620), (zx + 190, 620), (zx + 208, 590),
          (zx + 226, 648), (zx + 244, 620), (bx1 - 34, 620)]
    c.line(zz, (210, 60, 60), 5)
    for k in range(2):
        c.rect((zx, 672 + k * 18, zx + 250 - k * 90, 681 + k * 18), fill=(200, 206, 216), r=4)
    # спинка стула с халатом
    lab_coat_chair(c, 930, 560, 300)
    # стол
    c.rect((0, 790, W, W), fill=(214, 186, 150))
    S.wood(c, (0, 804, W, W), (220, 192, 156), (204, 176, 140), lines=7, seed=12)
    c.rect((0, 790, W, 806), fill=(190, 160, 124))
    laptop_screen(c, 70, 594, 300, 206, "Module 2", ["Medical terminology", "Anatomy basics", "Infection control"], (0, 132, 126))
    bp_gauge(c, 620, 820, 46)
    training_arm(c, 520, 960, 460)
    stethoscope(c, 250, 960, 0.9)


def sc_hs_kitchen(c):
    """Вечер, кухня: человек со спины за ноутбуком (курс на экране), тетрадь, кружка, окно с ночным небом, лампа.
    Без надписей о возрасте или положении зрителя. Верх (до y≈320) — место под заголовок."""
    c.vgrad((0, 0, W, 770), (34, 42, 74), (58, 64, 98))
    # окно
    wx0, wy0, wx1, wy1 = 690, 350, 1010, 650
    c.rect((wx0 - 14, wy0 - 14, wx1 + 14, wy1 + 14), fill=(86, 90, 118), r=8)
    c.vgrad((wx0, wy0, wx1, wy1), (16, 22, 52), (44, 50, 96))
    rnd = random.Random(5)
    for k in range(18):
        c.circle(rnd.uniform(wx0 + 10, wx1 - 10), rnd.uniform(wy0 + 10, wy1 - 60), rnd.uniform(1.5, 3.2), fill=(240, 240, 220))
    c.circle(wx1 - 80, wy0 + 70, 34, fill=(250, 240, 200))
    c.circle(wx1 - 66, wy0 + 60, 30, fill=(24, 30, 62))
    for k in range(6):
        x = wx0 + k * 60
        c.rect((x, wy1 - 50 - (k % 3) * 20, x + 44, wy1), fill=(26, 30, 56))
        c.rect((x + 10, wy1 - 34 - (k % 3) * 20, x + 18, wy1 - 26 - (k % 3) * 20), fill=(250, 210, 120))
    c.rect((wx0 + (wx1 - wx0) / 2 - 6, wy0, wx0 + (wx1 - wx0) / 2 + 6, wy1), fill=(86, 90, 118))
    # верхние шкафы
    for k in range(3):
        x = 50 + k * 128
        c.rect((x, 350, x + 118, 520), fill=(78, 86, 120), r=6)
        c.rect((x + 50, 470, x + 68, 480), fill=(150, 156, 180), r=3)
    # лампа и тёплый свет
    c.line([(470, 300), (470, 360)], (20, 24, 40), 4)
    c.poly([(420, 400), (520, 400), (500, 360), (440, 360)], (236, 170, 60))
    c.glow((250, 380, 690, 900), (255, 200, 120), alpha=70, blur=60)
    # стол
    c.rect((0, 770, W, W), fill=(160, 112, 72))
    S.wood(c, (0, 784, W, W), (170, 122, 80), (150, 104, 66), lines=6, seed=21)
    c.rect((0, 770, W, 786), fill=(130, 90, 58))
    # ноутбук (экран к зрителю, человек смотрит в него)
    laptop_screen(c, 560, 530, 340, 214, "Online course", ["Mathematical reasoning", "Unit 3 · practice test"], (60, 100, 200),
                  body=(40, 44, 52), bars=3)
    c.glow((520, 500, 940, 780), (140, 180, 255), alpha=40, blur=30)
    # тетрадь и ручка, кружка
    c.poly([(610, 850), (840, 836), (852, 930), (618, 946)], (250, 248, 240))
    for k in range(5):
        c.line([(628, 866 + k * 15), (838, 853 + k * 15)], (180, 196, 220), 2)
    S.pen(c, 780, 920, 860, 872)
    WS.mug(c, 985, 860, 0.55, (220, 90, 60))
    # человек со спины
    WS.senior_back(c, 250, 1110, 1.85, (70, 120, 110), hair=(70, 50, 38))


def gum_tree(c, cx, by, s, trunk=(214, 206, 196), leaf=((110, 140, 110), (90, 124, 96), (130, 156, 120))):
    """Эвкалипт: светлый ствол, рыхлая крона."""
    rnd = random.Random(int(cx))
    c.poly([(cx - 14 * s, by), (cx + 14 * s, by), (cx + 6 * s, by - 190 * s), (cx - 6 * s, by - 190 * s)], trunk)
    c.line([(cx, by - 120 * s), (cx + 60 * s, by - 200 * s)], trunk, 9 * s)
    c.line([(cx, by - 140 * s), (cx - 50 * s, by - 210 * s)], trunk, 8 * s)
    for k in range(14):
        c.circle(cx + rnd.uniform(-90, 90) * s, by - rnd.uniform(170, 280) * s, rnd.uniform(34, 56) * s, fill=leaf[k % len(leaf)])


def sc_au_table(c):
    """Кухонный стол у окна: пара со спины, папка с документами, блокнот «5 QUESTIONS», калькулятор с пустым экраном, чашки;
    за окном сад, эвкалипт и соседний дом. Без сумм, логотипов и цветов ведомств. Верх (до y≈420) закрывает карточка."""
    c.vgrad((0, 0, W, 800), (246, 236, 222), (234, 220, 202))
    # окно
    wx0, wy0, wx1, wy1 = 250, 430, 850, 740
    c.rect((wx0 - 18, wy0 - 18, wx1 + 18, wy1 + 18), fill=(250, 248, 244), r=6)
    c.vgrad((wx0, wy0, wx1, wy1), (150, 200, 236), (214, 234, 246))
    c.rect((wx0, wy1 - 90, wx1, wy1), fill=(150, 184, 120))
    # соседний дом
    hx = wx0 + 340
    c.rect((hx, wy1 - 170, hx + 200, wy1 - 60), fill=(236, 226, 206))
    c.poly([(hx - 20, wy1 - 170), (hx + 100, wy1 - 240), (hx + 220, wy1 - 170)], (170, 90, 70))
    c.rect((hx + 30, wy1 - 140, hx + 80, wy1 - 100), fill=(160, 200, 230))
    c.rect((hx + 120, wy1 - 140, hx + 170, wy1 - 100), fill=(160, 200, 230))
    c.rect((hx + 88, wy1 - 120, hx + 112, wy1 - 60), fill=(120, 90, 70))
    gum_tree(c, wx0 + 140, wy1 - 70, 0.9)
    c.rect((wx0, wy1 - 70, wx1, wy1 - 58), fill=(236, 230, 214))
    for k in range(12):
        x = wx0 + 10 + k * 50
        c.rect((x, wy1 - 96, x + 12, wy1 - 58), fill=(240, 236, 224), r=3)
    c.rect(((wx0 + wx1) / 2 - 8, wy0, (wx0 + wx1) / 2 + 8, wy1), fill=(250, 248, 244))
    c.rect((wx0, (wy0 + wy1) / 2 - 6, wx1, (wy0 + wy1) / 2 + 6), fill=(250, 248, 244))
    S.plant(c, wx1 + 110, 790, 0.9)
    # стол
    c.rect((0, 790, W, W), fill=(196, 160, 118))
    S.wood(c, (0, 804, W, W), (206, 170, 128), (188, 152, 110), lines=6, seed=33)
    c.rect((0, 790, W, 806), fill=(176, 140, 100))
    # предметы на столе
    W3.calc_obj(c, 800, 830, 130, 150, shown="")
    S.paper(c, (430, 820, 640, 1000), -5, head="5 QUESTIONS", head_size=22, lines=5, head_col=(64, 36, 84))
    c.rect((150, 850, 380, 1010), fill=(90, 70, 110), r=10)
    c.rect((166, 836, 364, 994), fill=WH, r=4)
    for k in range(6):
        c.rect((186, 862 + k * 20, 330 - (k % 2) * 60, 870 + k * 20), fill=(200, 204, 214), r=3)
    S.pen(c, 610, 1010, 700, 960)
    S.teacup(c, 980, 880, 0.7, rim=(90, 70, 110))
    S.glasses(c, 700, 1040, 0.7)
    # пара со спины
    WS.senior_back(c, 300, 1150, 1.45, (110, 140, 170), hair=(214, 214, 220))
    WS.senior_back(c, 760, 1160, 1.4, (200, 120, 90), hair=(226, 226, 230), bun=True)


def lighthouse_pier(c, x, base, h, body=WH, band=(214, 60, 50)):
    c.rect((x - 200, base - 12, x + 60, base + 10), fill=(120, 110, 104))
    c.poly([(x - 18, base - 12), (x + 18, base - 12), (x + 12, base - h), (x - 12, base - h)], body)
    c.rect((x - 16, base - h * 0.6, x + 16, base - h * 0.45), fill=band)
    c.rect((x - 14, base - h * 0.3, x + 14, base - h * 0.17), fill=band)
    c.rect((x - 16, base - h - 18, x + 16, base - h), fill=(60, 60, 70), r=3)
    c.poly([(x - 18, base - h - 18), (x + 18, base - h - 18), (x, base - h - 34)], band)
    c.glow((x - 40, base - h - 50, x + 40, base - h + 14), (255, 236, 170), alpha=150, blur=10)


def suitcase(c, x, by, s, col=(0, 132, 150)):
    w, h = 170 * s, 240 * s
    c.ellipse((x - w * 0.6, by - 12 * s, x + w * 0.6, by + 12 * s), fill=(0, 0, 0), alpha=50)
    c.rect((x - 30 * s, by - h - 70 * s, x - 20 * s, by - h), fill=(60, 64, 72))
    c.rect((x + 20 * s, by - h - 70 * s, x + 30 * s, by - h), fill=(60, 64, 72))
    c.rect((x - 40 * s, by - h - 80 * s, x + 40 * s, by - h - 62 * s), fill=(40, 44, 50), r=6 * s)
    c.rect((x - w / 2, by - h, x + w / 2, by - 14 * s), fill=col, r=22 * s)
    for k in (-1, 0, 1):
        c.rect((x + k * w * 0.26 - 6 * s, by - h + 14 * s, x + k * w * 0.26 + 6 * s, by - 28 * s), fill=mix(col, (0, 0, 0), 0.15), r=4 * s)
    c.rect((x - w / 2 + 12 * s, by - h + 10 * s, x - w / 2 + 26 * s, by - 40 * s), fill=WH, alpha=60, r=6 * s)
    for xx in (x - w * 0.36, x + w * 0.36):
        c.circle(xx, by - 8 * s, 10 * s, fill=(30, 32, 38))


def boarding_card(c, box, ang, lines, head="CARTE D'EMBARQUEMENT", band=(18, 48, 100)):
    """Бумажный посадочный без названия компании (повёрнут)."""
    from PIL import Image, ImageDraw
    x0, y0, x1, y1 = box
    K = c.K
    w_, h_ = c.s(x1 - x0), c.s(y1 - y0)
    img = Image.new("RGBA", (w_, h_), (252, 250, 244, 255))
    dd = ImageDraw.Draw(img)
    dd.rectangle((0, 0, w_, 34 * K), fill=band + (255,))
    dd.text((14 * K, 17 * K), head, font=c.font("sb", 17), fill=(255, 255, 255, 255), anchor="lm")
    y = 50
    for txt, fn, sz in lines:
        dd.text((14 * K, y * K), txt, font=c.font(fn, sz), fill=(30, 34, 44, 255))
        y += sz + 12
    st = (x1 - x0) * 0.74
    for yy in range(40, int(y1 - y0), 12):
        dd.line((st * K, yy * K, st * K, (yy + 6) * K), fill=(180, 186, 196, 255), width=2 * K)
    rnd = random.Random(8)
    bx = st + 12
    while bx < (x1 - x0) - 12:
        ww = rnd.choice((2, 2, 4))
        dd.rectangle((bx * K, 50 * K, (bx + ww) * K, (y1 - y0 - 16) * K), fill=(40, 44, 54, 255))
        bx += ww + rnd.choice((2, 3, 5))
    rot = img.rotate(-ang, expand=True, resample=Image.BICUBIC)
    cx, cy = c.s((x0 + x1) / 2), c.s((y0 + y1) / 2)
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    sh.putalpha(rot.getchannel("A").point(lambda v: v * 60 // 255))
    c.im.alpha_composite(sh, (cx - rot.width // 2 + 6 * K, cy - rot.height // 2 + 10 * K))
    c.im.alpha_composite(rot, (cx - rot.width // 2, cy - rot.height // 2))


def sc_fr_port_sunset(c):
    """Порт на закате: безымянный лайнер без логотипов выходит из гавани мимо маяка на молу; на причале — чемодан и
    посадочный без названия компании. Верх (до y≈400) — место под заголовок."""
    c.vgrad((0, 0, W, 640), (252, 226, 186), (246, 150, 96))
    c.glow((380, 470, 700, 700), (255, 230, 150), alpha=200, blur=40)
    c.circle(540, 612, 62, fill=(255, 226, 140))
    for cx, cy, s_ in ((200, 470, 1.0), (880, 430, 0.8)):
        c.ellipse((cx - 110 * s_, cy - 14 * s_, cx + 110 * s_, cy + 14 * s_), fill=(250, 190, 150), alpha=200)
    # холмы берега (силуэт)
    c.poly([(0, 640), (0, 590), (140, 560), (260, 590), (380, 600), (460, 640)], (170, 104, 110))
    c.poly([(640, 640), (760, 604), (880, 580), (1000, 596), (1080, 586), (1080, 640)], (180, 110, 114))
    # море
    c.vgrad((0, 640, W, 900), (236, 140, 110), (60, 80, 140))
    for k in range(14):
        y = 660 + k * 17
        w_ = 150 - k * 6
        c.rect((540 - w_, y, 540 + w_, y + 5), fill=(255, 220, 150), alpha=max(40, 190 - k * 12), r=3)
    for k in range(20):
        x = (k * 97) % W
        y = 700 + (k * 53) % 180
        c.line([(x, y), (x + 40, y)], (255, 200, 170), 3, alpha=110)
    # лайнер (без названия и логотипа), чуть в тени заката
    W4.liner(c, 110, 700, 560, hull=(250, 240, 234), band=(40, 50, 90), deck=(252, 244, 238), win=(120, 110, 140),
             funnel=(40, 50, 90), stripe=(236, 120, 70), boats=(236, 140, 60))
    c.poly([(110 + 560 * 0.05, 700), (110 + 560 * 0.9, 700), (110 + 560 * 0.86, 712), (110 + 560 * 0.08, 712)], (60, 70, 120), alpha=120)
    for k in range(4):
        c.line([(110 + 12, 706 + k * 6), (60 - k * 30, 706 + k * 8)], (255, 236, 220), 3, alpha=140)
    # мол с маяком
    lighthouse_pier(c, 930, 700, 150)
    # причал (передний план)
    c.rect((0, 900, W, W), fill=(176, 160, 146))
    for k in range(9):
        c.line([(k * 130, 900), (k * 130 - 40, W)], (156, 140, 126), 3)
    c.rect((0, 894, W, 912), fill=(150, 134, 120))
    for x in (90, 1000):
        c.rect((x - 24, 850, x + 24, 904), fill=(60, 60, 68), r=10)
        c.rect((x - 34, 846, x + 34, 862), fill=(70, 70, 78), r=6)
    suitcase(c, 340, 1040, 0.62)
    boarding_card(c, (560, 930, 900, 1060), -6, [("MARSEILLE → BARCELONE", "db", 22), ("3 NUITS · CABINE ---", "sb", 18)])


def scene_card2(P, t):
    """Сцена + карточка сверху: kicker, заголовок, 2 строки-пояснения с иконками, кнопка."""
    p = P["pal"]
    c = C(WH)
    getattr(WS, t["scene"])(c)
    box = t["card_box"]
    c.shadow(box, r=26, alpha=110, blur=18, off=(0, 10))
    c.rect(box, fill=WH, r=26, alpha=250)
    if t.get("frame"):
        c.rect((box[0] + 14, box[1] + 14, box[2] - 14, box[3] - 14), outline=p["frame"], width=3, r=18)
    cx = (box[0] + box[2]) / 2
    y = box[1] + t.get("pad", 40)
    if t.get("kicker"):
        y = c.block(t["kicker"], "sb", 26, y, box[2] - box[0] - 100, p["acc"], cx=cx, max_lines=1) + 6
    y = c.block(t["title"], t.get("font", "db"), t.get("size", 60), y, box[2] - box[0] - 90, p["ink"], cx=cx, max_lines=2, gap=1.06)
    y += 10
    lx = box[0] + 56
    fsz = min(c.fit(txt, "sb", box[2] - 56 - (lx + 66 + c.tw(lab + " ", c.font("db", 29))[0]), 1, 29) for _, lab, txt in t["legend"])
    for ic, lab, txt in t["legend"]:
        col = p["leg"][0] if ic == t["legend"][0][0] else p["leg"][1]
        c.circle(lx + 26, y + 26, 26, fill=mix(col, WH, 0.84))
        icon(c, ic, lx + 26, y + 26, 36, col, bg=mix(col, WH, 0.84))
        lw = c.tw(lab + " ", c.font("db", 29))[0]
        c.text((lx + 66, y + 26), lab, "db", 29, col, anchor="lm")
        c.text((lx + 66 + lw, y + 26), txt, "sb", fsz, (50, 54, 64), anchor="lm")
        y += 62
    c.button(P["cta"], cx, box[3] - t.get("btn_off", 62), size=t.get("btn_size", 40), fill=p["btn"])
    return c


SCENES = dict(w5n_apron_hangar=sc_apron_hangar, w5n_ma_classroom=sc_ma_classroom, w5n_hs_kitchen=sc_hs_kitchen,
              w5n_au_table=sc_au_table, w5n_fr_port_sunset=sc_fr_port_sunset)
for _k, _v in SCENES.items():
    setattr(WS, _k, _v)


# =====================================================================  ПАКЕТЫ
# ---------------------------------------------------------------- 1. US · обучение · авиация: пилот или авиатехник (без зарплат и обещаний работы)
NAVY1, SKY1, ORG1 = (18, 38, 74), (30, 120, 200), (236, 112, 30)
PACKS[1] = dict(
    doc="NT-aviation-training-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(236, 244, 252), bg2=(214, 232, 248), ink=NAVY1, sub=(84, 98, 118), acc=SKY1, btn=ORG1, tile=WH, tile_ink=NAVY1,
             icon=NAVY1, iconbg=(222, 236, 250), step0=(120, 176, 226), step1=NAVY1),
    a=dict(fn="stairs6", title="Pilot training programs:", title2="the certificate ladder", size=58, hero=hero_climb,
           sub="6 steps – pick one to see how it works",
           steps=[("Student pilot", "First solo flight from age 16"), ("Private pilot", "Personal trips, from age 17"),
                  ("Instrument rating", "Flying in cloud and low visibility"), ("Commercial pilot", "Minimum age 18"),
                  ("Flight instructor", "Teaching other pilots"), ("Airline transport pilot", "The top level, from age 23")],
           src="раздел 1 «Pilot training programs: the certificate ladder» (6 ступеней, минимальный возраст 16 / 17 / 18 / 23)",
           note="лестница из 6 карточек-ступеней снизу вверх (номер, ступень, строка из статьи, у каждой «Learn more») + самолёт в наборе высоты без номеров; налёт и сроки не вынесены"),
    b=dict(fn="quiz", layout="card2x2", title="Pilot training quiz:", title2="the first solo flight", size=58,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="From what age can a student pilot fly solo?", opts=["Age 14", "Age 16", "Age 18", "Age 21"],
           pal=dict(bg=(18, 38, 74), bg2=(30, 72, 130), ink=WH, sub=(200, 214, 236), acc=SKY1, t2=(250, 190, 80), btn=ORG1, deco=True),
           src="раздел 1: «Student pilot certificate… Solo flying is allowed from age 16» (верный ответ — 16)",
           note="тёмно-синее «небо», тест 2×2; вопрос о правиле, не о зрителе"),
    c=dict(fn="table2", title="Flight school or aircraft mechanic school?", sub="How the two aviation training paths compare", size=52,
           cols=[("FLIGHT SCHOOL", "w3_plane", SKY1), ("AIRCRAFT MECHANIC SCHOOL", "w3_wrench", ORG1)],
           rows=[("Length", "a few months (private) to 1–2 years (commercial)", "usually 18–24 months"),
                 ("How it's paid", "by the hour", "tuition per term"),
                 ("Training day", "in the air and in simulators", "in hangars and workshops"),
                 ("Medical certificate", "needed", "not needed")],
           foot="Plus: 5 questions to ask before enrolling",
           src="раздел 4 «Aircraft mechanic school or flight school: how the paths compare» (Length / How it is paid for / Training day / Medical requirements) + раздел 5 (вопросы перед записью)",
           note="таблица на 2 колонки: лётная школа vs школа авиамехаников; сроки — ровно как в статье, цен нет"),
    d=dict(fn="scene_d", scene="w5n_apron_hangar", style="bars", y=40,
           bars=[("COCKPIT OR HANGAR?", WH, NAVY1), ("PILOT TRAINING OR AIRCRAFT", NAVY1, (250, 200, 60)),
                 ("MAINTENANCE SCHOOL, STEP BY STEP", NAVY1, (250, 200, 60))],
           bar_size=74, cond=0.8, btn_size=40, max_w=960, pal=dict(btn=ORG1),
           src="заголовок и финал статьи («the cockpit or the hangar») + разделы 3–4 (hangars and workshops, air and simulators)",
           note="плашки (формула рабочих крео владельца) + перрон: учебный высокоплан без номеров и логотипов с колодками, конус ветра, открытый ангар с двигателем на стенде и тележкой с инструментом"),
)


# ---------------------------------------------------------------- 2. US · обучение · медассистент: сколько длится (без «3 days» как обещания, без работы/зарплат)
NAVY2, TEAL2, CORAL2 = (20, 48, 72), (0, 128, 122), (228, 86, 62)
PACKS[2] = dict(
    doc="NT-medical-assistant-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(238, 248, 245), bg2=(220, 240, 234), ink=NAVY2, sub=(80, 98, 108), acc=TEAL2, btn=CORAL2, tile=WH, tile_ink=NAVY2,
             icon=NAVY2, iconbg=(214, 238, 232), short=(150, 120, 60), prog=TEAL2),
    a=dict(fn="timeline5", title="Medical assistant certification:", title2="how long does it really take?", size=54,
           sub="From a 1-day CPR class to a 2-year degree",
           rows=[("CPR class", "1 day", 1, "not a credential"), ("Exam review course", "days to weeks", 10, "not a credential"),
                 ("Accelerated program", "4–6 months", 150, None), ("Certificate or diploma", "9–12 months", 315, None),
                 ("Associate degree", "about 2 years", 730, None)],
           src="раздел 3 «How long it really takes» (5 пунктов: CPR — 1 день, не credential; review — от нескольких дней до недель, не заменяет обучение; ускоренная 4–6 мес.; сертификат/диплом 9–12 мес.; associate ~2 года) + РК 1 («From a 1-day CPR class to a 2-year degree»)",
           note="шкала сроков: 5 строк-кнопок с полосой длины (sqrt-шкала), у коротких курсов метка «not a credential», у каждой «Learn more»; «3 days» не вынесено"),
    b=dict(fn="quiz", layout="card", title="Medical assistant training:", title2="what can be learned online?", size=56,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="Which of these can be studied from home?", opts=["Medical terminology", "Billing and coding", "Drawing blood", "Giving injections"],
           pal=dict(bg=(208, 238, 230), bg2=(170, 220, 208), ink=NAVY2, sub=(70, 96, 100), acc=TEAL2, t2=CORAL2, deco=True),
           src="раздел 4 «Medical assistant certification online: what works from home» (онлайн — терминология, кодирование и биллинг; кровь и уколы — лаборатория и практика в клинике)",
           note="мятный фон, карточка-тест; вопрос о программе, не о зрителе"),
    c=dict(fn="receipt", title="Medical assistant certification:", title2="what makes up the cost?", size=54,
           bill="CERTIFICATION COST", bill_sub="4 parts of the total",
           rows=[("Tuition", "$?", "depends on the school"), ("Books, scrubs, kit", "$?", "sometimes a background check too"),
                 ("Exam fee", "$100–250", "depends on the credential"), ("Renewal, later", "$?", "every few years")],
           total=("TOTAL", "$?"), foot="…and what a “free course with certificate” really is",
           pal=dict(bg=(246, 244, 238), bg2=(232, 228, 218)),
           src="раздел 5 «Medical assistant certification cost, and what free usually means» (обучение, книги/форма/набор, экзаменационный сбор ~$100–250, продление) + раздел 2 (renew every few years)",
           note="чек-«квитанция» из 4 статей расходов, все «$?», кроме единственной цифры статьи — сбор за экзамен $100–250; «free» — только в кавычках, как в статье"),
    d=dict(fn="scene_card2", scene="w5n_ma_classroom", card_box=(60, 34, 1020, 452), frame=True, pad=44,
           kicker="MEDICAL ASSISTANT CERTIFICATION", title="3 days or 12 months?", size=66,
           legend=[("hourglass", "3-day course:", "one skill or exam review, not the credential"),
                   ("calendar", "Certificate program:", "9–12 months, externship, then the exam")],
           pal=dict(frame=TEAL2, ink=NAVY2, acc=TEAL2, btn=CORAL2, leg=((150, 120, 60), TEAL2)),
           src="раздел 3 «How long it really takes» («a course that lasts three days can be a useful first step, but the path to a national credential is measured in months»; сертификат 9–12 мес.) + раздел 4 (externship в клинике) + РК 1 (хук «3 days or 12 months?»)",
           note="учебный класс без людей: доска «VITAL SIGNS», ноутбук с модулем «Medical terminology», тонометр, учебная рука-манекен, стетоскоп, халат на стуле; карточка с хуком и двумя строками-пояснениями — сразу видно, что 3 дня — это отдельный короткий курс, а не сертификация"),
)


# ---------------------------------------------------------------- 3. US · обучение · онлайн-школа для взрослых (без вопросов о зрителе, без «free diploma»)
INDIGO3, YEL3, RED3, TEAL3 = (36, 40, 100), (240, 176, 30), (220, 70, 50), (0, 128, 128)
PACKS[3] = dict(
    doc="NT-online-high-school-us-2026-09-30", cta="Learn more",
    pal=dict(bg=(248, 246, 240), bg2=(238, 234, 222), ink=INDIGO3, sub=(90, 92, 110), acc=(70, 90, 200), btn=RED3, tile=WH,
             tile_ink=INDIGO3, icon=INDIGO3, iconbg=(230, 232, 248)),
    a=dict(fn="cards3", title="Online high school for adults:", title2="3 ways to finish", size=56,
           sub="Pick a route to see how it works",
           cards=[("w5n_school", "Adult diploma program", "Public program, often free or low-cost", (60, 90, 200), "a diploma"),
                  ("laptop", "Accredited online school", "Self-paced courses, flexible schedule", TEAL3, "a diploma"),
                  ("w5n_ged", "GED test", "4 subject tests, no credits needed", (214, 120, 20), "an equivalency credential")],
           res_label="Leads to",
           src="раздел 1 «Three routes at a glance» (публичная программа — often free or low-cost; аккредитованная онлайн-школа — self-paced, very flexible; тест GED — subject tests, no credits needed) + раздел 4 (4 предмета)",
           note="3 высокие карточки-маршрута с иконкой, строкой из статьи и «Learn more»; без вопросов о зрителе, без «free diploma»"),
    b=dict(fn="quiz", layout="phone", title="Real diploma or diploma mill?", title2="Spot the warning sign", size=56,
           sub="6 signs of a fake online high school", tag="QUIZ", step="Question 1 of 3", prog=0.33, left_y=270,
           q="Which is a warning sign of a diploma mill?", opts=["A diploma in a week", "Credit for life experience", "No proctored exams", "All three"],
           pal=dict(bg=(252, 240, 214), bg2=(248, 222, 176), ink=INDIGO3, sub=(96, 86, 70), acc=RED3, btn=RED3),
           src="раздел 5 «Accredited online high schools for adults: how to spot a diploma mill» (6 признаков; верный ответ — все три) + заголовок статьи",
           note="слева заголовок и кнопка, справа телефон с тестом; «a diploma in a week» — вариант-признак фабрики дипломов, не обещание"),
    c=dict(fn="compare", layout="twocol", title="High school diploma or GED?", sub="How the two routes compare", size=58,
           cols=[("DIPLOMA", "w5_cert", (60, 90, 200)), ("GED", "w5n_ged", (214, 120, 20))],
           rows=[("WHAT IT TAKES", "completing the missing courses", "passing 4 subject tests"),
                 ("TIME", "a few months to 2 years", "prep: a few weeks to several months"),
                 ("COST", "public programs often free", "fee per subject, varies by state"),
                 ("RESULT", "a regular high school diploma", "a state-issued equivalency credential")],
           foot="Most colleges accept either – worth checking in advance",
           src="раздел 4 «Online GED programs or a diploma: how they compare» (What it takes / Time / Cost / Recognition) + раздел 2 (a few months … one or two years; regular diploma) + раздел 1 (state-issued equivalency credential)",
           note="две колонки аттестат vs GED; сроки и цена — словами статьи, без сумм"),
    d=dict(fn="scene_d", scene="w5n_hs_kitchen", style="top", y=40, size=56, lines=2,
           title="Online high school for adults: which options are free?",
           sub="Public programs, library scholarships, free test prep – and what usually costs money", sub_size=30,
           btn_y=990, pal=dict(ink=WH, sub=(214, 220, 240), acc=YEL3, btn=RED3),
           scene_text="на экране ноутбука: Online course / Mathematical reasoning / Unit 3 · practice test",
           src="раздел 3 «Online high school for adults free: where no-cost options exist» (публичные программы, стипендии библиотек, бесплатная подготовка к тесту; что обычно платно) + раздел 4 (Mathematical reasoning)",
           note="вечерняя кухня: взрослый со спины за ноутбуком с курсом, тетрадь, кружка, лампа, ночное окно; «free» — только вопросом «which options are free?», как в статье"),
)


# ---------------------------------------------------------------- 4. AU · кредиты · кредит под пенсию (Meta Financial: без сумм, ставок, сроков, без вопросов о зрителе,
#                                                                   не от имени Services Australia / Centrelink, без их цветов и логотипов)
PLUM4, ORG4, SAGE4 = (64, 36, 84), (222, 104, 40), (96, 128, 96)
PACKS[4] = dict(
    doc="NT-pension-loans-au-2026-09-30", cta="Learn more",
    pal=dict(bg=(250, 246, 240), bg2=(240, 232, 222), ink=PLUM4, sub=(96, 86, 100), acc=(150, 84, 160), btn=ORG4, tile=WH, tile_ink=PLUM4,
             icon=PLUM4, iconbg=(238, 228, 242)),
    a=dict(fn="grid6", title="Pension loans in Australia 2026:", title2="6 options explained", size=54,
           sub="Pick one to see how it works",
           tiles=[("house", "Home Equity Access Scheme"), ("calendar", "Pension advance payment"), ("bank", "Bank & credit union loans"),
                  ("heart_hands", "No-interest community loans"), ("key_plus", "Reverse mortgage"), ("w5n_house_split", "Home reversion")],
           src="разделы 1–4: Home Equity Access Scheme (бывш. Pension Loans Scheme), аванс пенсии, банки и кредитные союзы, беспроцентные займы некоммерческих организаций, частный reverse mortgage, home reversion",
           note="6 плиток 3×2 = варианты из статьи, у каждой «Learn more»; без ставок, сумм и сроков; сливово-оранжевая палитра, не цвета ведомств"),
    b=dict(fn="quiz", layout="card2x2", title="Pension loans quiz:", title2="the interest question", size=58,
           tag="QUIZ", step="Question 1 of 3", prog=0.33,
           q="Which of these options charge no interest?",
           opts=["Pension advance payment", "Community no-interest loan", "Private reverse mortgage", "Credit card balance"],
           pal=dict(bg=(64, 36, 84), bg2=(100, 60, 120), ink=WH, sub=(226, 214, 236), acc=(150, 84, 160), t2=(250, 190, 110), btn=ORG4, deco=True),
           src="раздел 2 («A Centrelink advance payment is not a loan with interest») + раздел 3 (community no-interest loan programs; credit cards can become expensive) + раздел 4 (reverse mortgages — rates usually higher); верно — первые два",
           note="тёмно-сливовый фон, тест 2×2 о продуктах, не о зрителе; продуктов вне статьи нет"),
    c=dict(fn="table2", title="Home Equity Access Scheme or private reverse mortgage?", sub="Two home-secured options, side by side", size=50,
           cols=[("GOVERNMENT SCHEME", "house", PLUM4), ("PRIVATE REVERSE MORTGAGE", "key_plus", ORG4)],
           rows=[("Offered by", "the federal government", "private lenders"),
                 ("Interest rate", "set by the government", "usually noticeably higher"),
                 ("Paid as", "fortnightly payments, lump sums possible", "lump sum or line of credit"),
                 ("Negative equity protection", "yes, if the conditions are met", "yes, by law")],
           foot="Both reduce the equity left for the family",
           src="раздел 1 (HEAS: offered by the federal government, rate set by the government, fortnightly payments + lump-sum advances, negative equity protection при условиях) + раздел 4 (private reverse mortgages: rates usually noticeably higher, lump sum or line of credit, negative equity protection by law) + раздел 5 (every home-secured option reduces the equity left for the family)",
           note="таблица на 2 колонки: госпрограмма vs частный reverse mortgage; ставки словами, без процентов, сумм и сроков; «government scheme» — описание, не от имени ведомства"),
    d=dict(fn="scene_d", scene="w5n_au_table", style="card", card_box=(60, 34, 1020, 410), frame=True, font="lserb",
           kicker="PENSION LOANS 2026", title="5 questions worth asking before signing anything",
           sub="Total cost, early repayment, what happens with aged care", size=52, lines=2, btn_size=38, btn_off=58, pad=40,
           pal=dict(frame=PLUM4, ink=PLUM4, sub=(96, 86, 100), acc=(150, 84, 160), btn=ORG4),
           scene_text="на блокноте: 5 QUESTIONS; экран калькулятора пустой",
           src="раздел 6 «Questions to ask before signing» (полная стоимость, досрочное погашение, aged care) + РК 3 (хук «5 questions before signing»)",
           note="кухонный стол у окна: пара со спины, папка с листами, блокнот «5 QUESTIONS», калькулятор с пустым экраном, чашка, очки; за окном сад, эвкалипт, соседний дом; без эмоций тревоги, без сумм и логотипов"),
)

# ---------------------------------------------------------------- 5. FR · путешествия · мини-круиз из Марселя или Гавра (без цен, скидок, брендов, «tout compris», «retraités»;
#                                                                   не повторяет квиз «что не входит в цену» и сравнение «круиз или курорт» из P60-senior-cruise-uk)
BLEU5, TURQ5, ORANGE5 = (18, 48, 100), (0, 146, 166), (236, 112, 40)
PACKS[5] = dict(
    doc="NT-mini-cruises-fr-2026-09-30", cta="En savoir plus",
    pal=dict(bg=(246, 250, 252), bg2=(222, 238, 246), ink=BLEU5, sub=(80, 96, 116), acc=TURQ5, btn=ORANGE5, tile=WH, tile_ink=BLEU5,
             icon=BLEU5, iconbg=(220, 238, 246)),
    a=dict(fn="ports2", title="Mini croisière 2026 :", title2="quel port de départ ?", size=58,
           sub="Les escales habituelles au départ de Marseille et du Havre",
           ports=[("MARSEILLE", "Méditerranée", ["Barcelone", "Gênes ou Savone", "Palma de Majorque", "Un port de Corse"], "w3_sun", TURQ5),
                  ("LE HAVRE", "Manche et mer du Nord", ["Southampton", "Zeebrugge (Bruges)", "Rotterdam ou Amsterdam", "Hambourg"],
                   "w5n_lighthouse", BLEU5)],
           src="раздел 2 «Mini croisière départ Marseille : les itinéraires habituels» (Barcelone, Gênes ou Savone, Palma aux Baléares, un port de Corse) + раздел 3 «Croisière au départ du Havre 2026» (Southampton, Zeebrugge pour Bruges, Rotterdam ou Amsterdam, Hambourg)",
           note="2 колонки-порта (Марсель — бирюзовая с солнцем, Гавр — синяя с маяком), по 4 стоянки-кнопки из статьи, у каждой «En savoir plus»; без цен, брендов и «3 nuits» над Балеарами (в статье — маршруты подлиннее)"),
    b=dict(fn="pass_quiz", title="Croisière au départ du Havre :", title2="escale en Angleterre, quel document ?", size=52,
           pass_head="CARTE D'EMBARQUEMENT", step="Quiz · question 1 sur 3", pass_route="LE HAVRE → SOUTHAMPTON",
           from_lab="Départ", to_lab="Escale", q="Pour cette escale, que faut-il présenter ?",
           opts=["Carte d'identité", "Passeport", "Passeport + autorisation électronique", "Aucun document"],
           stub=[("NUITS", "3"), ("ESCALES", "2 ou 3")],
           pal=dict(bg=(214, 236, 246), bg2=(170, 212, 232), ink=BLEU5, sub=(70, 90, 110), acc=TURQ5, t2=ORANGE5, band=BLEU5, btn=ORANGE5),
           src="раздел 3 (escale au Royaume-Uni : depuis 2021 la carte d'identité ne suffit plus, passeport + autorisation de voyage électronique depuis 2025; верный ответ — третий) + лид («trois ou quatre nuits, deux ou trois escales»)",
           note="квиз на бумажном посадочном без названия компании: маршрут Le Havre → Southampton, 4 варианта, корешок «3 nuits / 2 ou 3 escales» и штрихкод; вопрос о правиле, не о зрителе; не повторяет UK-квиз о цене"),
    c=dict(fn="compare", layout="twocol", title="Marseille ou Le Havre ?", sub="Mini croisière : mer, escales, saison et papiers", size=60,
           cols=[("MARSEILLE", "w3_sun", TURQ5), ("LE HAVRE", "w5n_lighthouse", BLEU5)],
           rows=[("MER", "Méditerranée", "Manche et mer du Nord"),
                 ("ESCALES", "Barcelone, Gênes, Baléares", "Southampton, Bruges, Rotterdam, Hambourg"),
                 ("SAISON", "presque toute l'année", "surtout du printemps à l'automne"),
                 ("PAPIERS", "carte d'identité ou passeport, selon les escales", "passeport + autorisation si escale au Royaume-Uni")],
           src="разделы 2–3 (моря, стоянки, «départs presque toute l'année» / «la saison va surtout du printemps à l'automne», паспорт и электронное разрешение для Royaume-Uni) + чек-лист («carte d'identité ou passeport suivant les escales»)",
           note="две колонки Марсель vs Гавр — порт против порта, не «круиз или курорт»; без цен"),
    d=dict(fn="scene_d", scene="w5n_fr_port_sunset", style="top", y=34, size=52, lines=2, kicker="3 NUITS À BORD, 2 OU 3 ESCALES",
           title="Mini croisière au départ de Marseille ou du Havre",
           sub="Itinéraires 2026, papiers, saison : ce qu'il faut savoir avant de réserver", sub_size=30,
           btn_y=470, pal=dict(ink=BLEU5, sub=(90, 60, 60), acc=(190, 70, 30), btn=ORANGE5),
           scene_text="на посадочном: CARTE D'EMBARQUEMENT / MARSEILLE → BARCELONE / 3 NUITS · CABINE ---",
           src="заголовок статьи и лид («Trois ou quatre nuits à bord, deux ou trois escales»; Marseille / Le Havre) + раздел 2 (Barcelone) + раздел 5 (réserver)",
           note="порт на закате: безымянный лайнер без логотипа и названия выходит из гавани мимо маяка на молу; на причале чемодан и посадочный без названия компании"),
)


# =====================================================================  сборка
def texts(t, cta):
    skip = ("rows",) if t["fn"] in ("timeline5", "receipt") else ()
    s = W4.texts({k: v for k, v in t.items() if k not in skip}, cta)
    extra = []
    if t.get("steps") and t["fn"] == "stairs6":
        extra.append(" / ".join(f"{k + 1}. {a} – {b}" for k, (a, b) in enumerate(t["steps"])) + f" (у каждой «{cta}»)")
    if t.get("fn") == "timeline5":
        extra.append(" / ".join(f"{a}: {b}" + (f" [{ch}]" if ch else "") for a, b, _, ch in t["rows"]) + f" (у каждой «{cta}»)")
    if t.get("fn") == "receipt":
        extra.append(t["bill"] + (" · " + t["bill_sub"] if t.get("bill_sub") else "") + " · " +
                     " · ".join(f"{a} … {b}" + (f" ({n_})" if n_ else "") for a, b, n_ in t["rows"]) + f" · {t['total'][0]} {t['total'][1]}")
    if t.get("cards"):
        extra.append(" / ".join(f"{k + 1}. {a} – {b}" + (f" – {t.get('res_label', 'Result')}: {r}" if r else "")
                                for k, (_, a, b, _, r) in enumerate(t["cards"])) + f" (у каждой «{cta}»)")
    if t.get("ports"):
        for name, sea, cities, _, _ in t["ports"]:
            extra.append(f"{name} ({sea}): " + " / ".join(cities))
        extra[-1] += f" (у каждой «{cta}»)"
    if t.get("legend"):
        extra.append(" / ".join(f"{a} {b}" for _, a, b in t["legend"]))
    if t.get("pass_route"):
        extra.append("посадочный: " + t["pass_head"] + " · " + t.get("from_lab", "") + " " + t["pass_route"].split(" → ")[0] + " → "
                     + t.get("to_lab", "") + " " + t["pass_route"].split(" → ")[1] + " · корешок: " + " · ".join(f"{a} {b}" for a, b in t["stub"])
                     + " · штрихкод")
    if extra:
        s = s.replace(f" / кнопка «{cta} →»", "")
        s = s + " / " + " / ".join(extra)
        if t["fn"] not in ("stairs6", "timeline5", "cards3", "ports2", "grid6"):
            s += f" / кнопка «{cta} →»"
    return s


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
    os.makedirs(os.path.join(OUTN, doc), exist_ok=True)
    with open(os.path.join(OUTN, doc, "creatives.json"), "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = sys.argv[1:] or [str(k) for k in PACKS]
    for a in args:
        if ":" in a:
            n, ls = a.split(":")
            build(int(n), ls.replace(",", ""))
        else:
            build(int(a))
